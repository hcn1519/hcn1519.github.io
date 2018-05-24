---
layout: post
title: "Concurrency programming과 GCD"
date: "2018-05-24 23:04:09 +0900"
---

> 이 글은 애플의 [Concurrency and Application Design](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/ConcurrencyandApplicationDesign/ConcurrencyandApplicationDesign.html#//apple_ref/doc/uid/TP40008091-CH100-SW1) 문서를 정리한 내용을 담고 있습니다.

## 과거 이야기(싱글 코어 시절)

어떤 컴퓨터의 속도가 빠르다는 것은 일반적으로 컴퓨터의 연산속도가 빠르다는 것을 의미합니다. 그리고 이 연산속도는 CPU의 연산속도를 의미합니다. 그래서 컴퓨터에 코어 개수가 1개이던 시절에는 컴퓨터의 연산속도를 높이기 위해 CPU의 클럭 수를 높이는 노력이 많이 이뤄졌습니다. 그런데 이렇게 클럭 수를 높이는 것은 하드웨어의 발열과 기타 물리적 한계로 인해 더이상 높일 수 없는 시기가 왔습니다. 그렇지만 컴퓨터의 속도는 계속 빨라져야 했기 때문에 하드웨어 업체들은 다른 방식으로 컴퓨터의 성능을 높이는 방식을 채택하였습니다. 바로 CPU 코어의 개수를 늘려서 여러 개의 코어가 동시에 일을 처리하는 방식을 사용하는 것입니다.

## 멀티 코어 프로세서의 시대

이제 컴퓨터 성능은 얼마나 코어들이 일을 잘 배분하여 수행하는 지에 달려 있습니다. 그런데 이것이 쉬운 일이 아닙니다. 자칫 잘못하면 하나의 코어만 일하고 나머지는 노는(그러다가 시스템이 죽는) 현상이 발생합니다. 이러한 한계를 극복하기 위해 개발자들은 많은 노력을 기울였습니다.

### 1. 전통적인 접근 방식

<div class="message">
  코어 개수를 늘렸으니 쓰레드 개수를 늘리자
</div>

전통적인 접근 방식은 코어의 개수를 늘렸으니 그에 상응하여 쓰레드의 개수도 늘리는 것입니다. 쉽고 명쾌한 해결방안 같지만, 이는 다음과 같은 문제가 있습니다.

1. 쓰레드 기반의 코드는 임의의 코어 개수에 대해 항상 최적의 성능을 보장하지 않는다

컴퓨터의 성능은 코어의 개수에 따라 매우 제각각입니다. 그래서 코어 개수에 따라서 적절한 양의 쓰레드를 사용할 필요가 있는데 쓰레드 기반의 개수는 코어 개수에 따른 스케일링을 제대로 해주지 못 했습니다.

2. 위의 문제로 인해 개발자가 처리해야 하는 것이 너무 많아졌다.

개발자는 우선 쓰레드와 코어의 개수간의 상관관계를 파악해야 합니다. 그리고 이를 설령 알아냈다고 하더라도 쓰레드의 효율적인 동작을 처리하는 것도 해주어야 했습니다. 즉, 쓰레드를 적절히 활용하기 위해서는 개발자가 **직접** 시스템 상태에 따른 쓰레드의 생성과 소멸도 조절하고 효율적 동작도 처리해야 했습니다. 😭

## Move away from threads

이처럼 쓰레드를 직접 사용하는 것은 앱의 성능 최적화에 어려움이 많습니다. 그래서 애플은 현재 OSX와 iOS에서 사용되고 있는 비동기적으로 컴퓨터의 자원을 사용하는 디자인을 내놓았습니다.

### Asynchronous design approach

이 방식은 쓰레드를 사용하는 대신 비동기 함수를 활용합니다. 비동기 함수는 개발자가 작성한 작업을 실행하고 바로 함수를 리턴합니다. 이 때 작업은 계속 진행중이지만 다른 쓰레드의 작업을 방해하지 않습니다. 그리고 해당 작업이 완료되면 `completion handler`를 호출하여 `notification`을 전달합니다.

OSX와 iOS에서는 이러한 작업들의 비동기 호출을 GCD(Grand Central Dispatch)를 통해 지원합니다.

## Grand Central Dispatch(GCD)

GCD는 개발자가 작성한 어떤 코드든 쓰레드 관리를 해주면서 해당 코드를 시스템 레벨에서 동작하도록 해줍니다.(메모리 관리는 별개입니다.) 사용방법도 매우 간단합니다. 개발자는 그저 수행할 tasks를 `Dispatch Queue`에 등록만 하면 됩니다. GCD가 쓰레드 생성이나 스케줄링과 관련된 일을 모두 담당합니다.

앞서서 tasks를 큐에 등록하면 된다고 하였는데, 이 때 큐가 `Dispatch Queue`만 있는 것은 아닙니다. 크게 `Dispatch Queue`, `Dispatch Sources`, `Operation Queue`가 있습니다. 이들에 대해 간단하게 살펴보겠습니다.

#### Dispatch Queue

<div class="message">
  Dispatch queues are a C-based mechanism for executing custom tasks.
</div>

`Dispatch Queue`의 종류에는 Serial, Concurrent Queue가 있습니다. 둘 모두 `FIFO(First-In-First-Out)` 형태로 작동하는데 Serial Queue는 한 순간에 하나의 task만 수행하는 반면 Concurrent queue는 등록된 task를 가능한 만큼 최대로 실행합니다.

애플은 이러한 Dispatch Queue의 장점을 다음과 같이 말합니다.

* (이전의 스레드를 직접 관리하는 것보다)쉽고,
* 어셈블리 수준의 속도를 유지하여 빠르고,
* 메모리 관리나 커널과 관련하여, deadlock 위험 없이 효율적이며
* 작업 규모에 따른 스케일링에 좋다.

DispatchQueue에 등록하는 작업들은 `block(closure)` 형태로 작성되어야 하며, 작업 실행시 함수의 본래 스코프를 벗어나서 heap에 해당 작업들을 복사하여 작업을 수행합니다. 그래서 다양한 방식으로 코드를 작성할 수 있고, 기존에 비해 코드 작성이 쉽습니다.

#### Dispatch Sources

<div class="message">
  Dispatch sources are a C-based mechanism for processing specific types of system events asynchronously.
</div>

`Dispatch Sources`는 시스템의 특정 이벤트가 발생하였을 때 특정 코드를 실행하도록 도와주는 것입니다.

#### Operation Queue

<div class="message">
  An operation queue is the Cocoa equivalent of a concurrent dispatch queue and is implemented by the  [NSOperationQueue](https://developer.apple.com/documentation/foundation/nsoperationqueue)  class.
</div>

`Operation Queue`는 Concurrent Dispatch Queue와 동일하지만, Priority Queue의 기능을 가지고 있어서 작업의 우선순위를 정할 수 있는 큐입니다. `Operation Queue`의 작업들은 `NSOperation` 인스턴스 형태이어야 합니다. `NSOperation` KVO 기반으로 notification을 전달하고 수행과정을 모니터링할 수 있도록 해줍니다.


## Asynchronous Design Techniques

---

## 참고자료
* [Concurrency and Application Design](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/ConcurrencyandApplicationDesign/ConcurrencyandApplicationDesign.html#//apple_ref/doc/uid/TP40008091-CH100-SW1)
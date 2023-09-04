---
layout: post
title: "Concurrent programming과 GCD"
date: "2018-05-24 23:04:09 +0900"
excerpt: "Concurreny에 대한 기본적인 개념을 살펴봅니다."
categories: Concurrent GCD iOS Thread
tags: [Concurrency, GCD, iOS, Thread]
table-of-contents: |
  ### Table of Contents  
  1. [과거 이야기(싱글 코어 시절)](./concurrent_programming#과거-이야기(싱글-코어-시절))
  1. [멀티 코어 프로세서의 시대](./concurrent_programming#멀티-코어-프로세서의-시대)
  1. [전통적인 접근 방식](./concurrent_programming#1-전통적인-접근-방식)
  1. [Move away from threads](./concurrent_programming#move-away-from-threads)
  1. [Grand Central Dispatch(GCD)](./concurrent_programming#grand-central-dispatch(gcd))
      1. [Dispatch Queue](./concurrent_programming#dispatch-queue)
      1. [Dispatch Sources](./concurrent_programming#dispatch-sources)
      1. [Operation Queue](./concurrent_programming#operation-queue)
  1. [Asynchronous Design Techniques](./concurrent_programming#asynchronous-design-techniques)
  1. [Tips for improving efficiency](./concurrent_programming#tips-for-improving-efficiency)

---

> 이 글은 애플의 [Concurrency and Application Design](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/ConcurrencyandApplicationDesign/ConcurrencyandApplicationDesign.html#//apple_ref/doc/uid/TP40008091-CH100-SW1) 문서를 정리한 내용을 담고 있습니다.

## 과거 이야기(싱글 코어 시절)

어떤 컴퓨터의 속도가 빠르다는 것은 일반적으로 컴퓨터의 연산속도가 빠르다는 것을 의미합니다. 그리고 이 연산속도는 CPU의 연산속도를 의미합니다. 그래서 컴퓨터에 코어 개수가 1개이던 시절에는 컴퓨터의 연산속도를 높이기 위해 CPU의 클럭 수를 높이는 노력이 많이 이뤄졌습니다.

그런데 이렇게 클럭 수를 높이는 것은 하드웨어의 발열과 기타 물리적 한계로 인해 무한정 높일 수 없습니다. 그렇지만 컴퓨터의 속도는 계속 빨라져야 했기 때문에 하드웨어 업체들은 다른 방식으로 컴퓨터의 성능을 높이는 방식을 선택하였습니다. 바로 CPU 코어의 개수를 늘려서 여러 개의 코어가 동시에 일을 처리하도록 하는 것입니다.

## 멀티 코어 프로세서의 시대

이제 컴퓨터 성능은 얼마나 코어들이 일을 잘 배분하여 수행하는 지에 달려 있습니다. 그런데 이것이 쉬운 일이 아닙니다. 자칫 잘못하면 하나의 코어만 일하고 나머지는 노는(그러다가 시스템이 죽는) 현상이 발생합니다. 이러한 한계를 극복하기 위해 개발자들은 많은 노력을 기울였습니다.

## 전통적인 접근 방식

<div class="message">
  코어 개수를 늘렸으니 쓰레드 개수를 늘리자
</div>

전통적인 접근 방식은 코어의 개수를 늘렸으니 그에 상응하여 쓰레드의 개수도 늘리는 것입니다. 쉽고 명쾌한 해결방안 같지만, 이는 다음과 같은 문제가 있습니다.

- 쓰레드 기반의 코드는 임의의 코어 개수에 대해 항상 최적의 성능을 보장하지 않는다.

컴퓨터의 성능은 코어의 개수에 따라 매우 제각각입니다. 그래서 코어 개수에 따라서 적절한 양의 쓰레드를 사용할 필요가 있는데 쓰레드 기반의 코드는 코어 개수에 따라 최적화된 성능을 보여주지 못 했습니다. 즉, 코어 개수에 따라 쓰레드의 개수가 적절히 늘어나거나 줄어들어야 하는데 그렇게 만들 수가 없었습니다.

- 위의 문제로 인해 개발자가 처리해야 하는 것이 너무 많아졌다.

위의 문제 때문에 개발자는 할 일이 너무 많아졌습니다. 먼저 개발자는 쓰레드와 코어의 개수간의 상관관계를 파악해야 합니다. 그리고 이를 설령 알아냈다고 하더라도 쓰레드의 효율적인 동작을 처리하는 것도 해주어야 했습니다. 즉, 쓰레드를 적절히 활용하기 위해서는 개발자가 **직접** 시스템 상태에 따른 쓰레드의 생성과 소멸을 조절하고 효율적 동작도 처리해야 했습니다. 😭

## Move away from threads

이처럼 쓰레드를 직접 사용하는 것은 앱의 성능 최적화에 어려움이 많습니다. 그래서 애플은 현재 OSX와 iOS에서 사용되고 있는 비동기적으로 컴퓨터의 자원을 사용하는 디자인을 내놓았습니다.

### Asynchronous design approach

이 방식은 쓰레드를 사용하는 대신 비동기 함수를 활용합니다. 비동기 함수는 일반적으로 수행 시간이 매우 긴 작업들을 처리하는 데 쓰이는 함수입니다. 비동기 함수는 할당 받은 작업을 메인 쓰레드를 방해하지 않으면서(주로 background thread에서) 작업을 수행하고
해당 작업이 완료되면 `completion handler`를 호출하여 `notification`을 전달합니다.

OSX와 iOS에서는 이러한 작업들의 비동기 호출을 `GCD(Grand Central Dispatch)`를 통해 지원합니다.

## Grand Central Dispatch(GCD)

GCD는 개발자가 작성한 어떤 코드든 쓰레드 관리를 해주면서 해당 코드를 시스템 레벨에서 동작하도록 해줍니다.(메모리 관리는 별개입니다.) 사용방법도 매우 간단합니다. 개발자는 그저 수행할 tasks를 `Dispatch Queue`에 등록만 하면 됩니다. GCD가 쓰레드 생성이나 스케줄링과 관련된 일을 모두 담당합니다.

앞서서 tasks를 큐에 등록하면 된다고 하였는데, 이 때 큐가 `Dispatch Queue`만 있는 것은 아닙니다. 크게 `Dispatch Queue`, `Dispatch Sources`, `Operation Queue`가 있습니다. 이들에 대해 간단하게 살펴보겠습니다.

### Dispatch Queue

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

### Dispatch Sources

<div class="message">
  Dispatch sources are a C-based mechanism for processing specific types of system events asynchronously.
</div>

`Dispatch Sources`는 시스템의 특정 이벤트가 발생하였을 때 특정 코드를 실행하도록 도와주는 것입니다.

#### Operation Queue

<div class="message">
  An operation queue is the Cocoa equivalent of a concurrent dispatch queue and is implemented by the  NSOperationQueue class.
</div>

`Operation Queue`는 Concurrent Dispatch Queue와 동일하지만, Priority Queue의 기능을 가지고 있어서 작업의 우선순위를 정할 수 있는 큐입니다. `Operation Queue`의 작업들은 `NSOperation` 인스턴스 형태이어야 합니다. `NSOperation` KVO 기반으로 notification을 전달하고 수행과정을 모니터링할 수 있도록 해줍니다.

## Asynchronous Design Techniques

앱에서 Concorrency를 지원하는 것은 동일한 시간에 많은 작업을 하는데 도움을 주는 것은 맞지만, 오버헤드가 생길 가능성이 있고, 코드가 복잡해지는 문제가 있습니다. 또한 코드를 잘못 짜면 오히려 속도가 느려질 수도 있습니다. 그렇기 때문에 코드 작성 전에 달성하고자 하는 목표를 명확히 하고, 그 과정에서 어느 부분에서 Concurrency를 지원할 것인지에 대해 생각해보아야 합니다.

여기서는 이러한 과정에서 어떻게 코드를 적절히 작성할 것인지에 대한 가이드라인을 단계별로 제시합니다.

* Define Your Application’s Expected Behavior

먼저 High level 수준의 앱의 task를 작성합니다. 이 task는 코드로 작성하는 것이 아니라, 추상적인 형태로 작성합니다. 그리고 각각의 task를 세분화하여 task가 성공적으로 동작하기 위한 단계를 구분합니다. 이 때 task에서 필요한 적절한 자료구조들에 대해 생각해보고 적용할 필요가 있습니다.

이와 같은 작업을 하게 되면 concurrency를 통해 효과를 얻을 수 있는 지점에 대해 파악할 수 있게 됩니다.

* Factor Out Executable Units of Work

이렇게 task를 명확히 구분한 뒤, 해당 작업들을 `block(closure)`, `NSOperation` 단위로 코드를 작성합니다.

* Identify the Queues You Need

다음은 작성된 task를 어떤 큐에서 작업할지 결정합니다. 이 때, 작업의 순서를 변경하면 결과가 바뀔 수 있는 task는 순차적으로 수행하고(`serial`), 그렇지 않으면 `concurrent`하게 수행하도록 합니다.

## Tips for improving efficiency

1. **Consider computing values directly within your task if memory usage is a factor.**
2. **Identify serial tasks early and do what you can to make them more concurrent.**
3. **Avoid using locks.**
4. **Rely on the system frameworks whenever possible.**


---

## 참고자료
* [Concurrency and Application Design](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/ConcurrencyandApplicationDesign/ConcurrencyandApplicationDesign.html#//apple_ref/doc/uid/TP40008091-CH100-SW1)

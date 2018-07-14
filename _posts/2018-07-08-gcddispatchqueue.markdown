---
layout: post
title: "GCD - Dispatch Queue"
excerpt: "Dispatch Queue에 대한 정리"
date: "2018-07-08 20:04:49 +0900"
categories: Concurrent GCD DispatchQueue
tags: [Concurrent, GCD, DispatchQueue]
---

> 이 글을 읽기 전 [Concurrenct programming과 GCD](https://hcn1519.github.io/articles/2018-05/concurrent_programming)을 먼저 읽으면 이해가 쉽습니다.

<div class="message">
  Dispatch queues are a C-based mechanism for executing custom tasks.
</div>


Dispatch Queue는 임의의 tasks를 sync/async하게 작동하도록 도와주는 object-like structure로 tasks의 제출과 실행을 통해 동작하는 API입니다.

Dispatch Queue는 3가지 종류가 있습니다.

### 1. Serial Queue(private dispatch queue)
* `Serial Queue`는 Queue에 추가된 작업을 순서대로 *한 번에 하나만* 수행합니다.
* `Serial Queue`는 일반적으로 리소스의 동기화를 위해 사용됩니다.
* `Serial Queue`는 생성 개수에 제한이 없습니다. 여러 개의 `Serial Queue`를 동시에 실행하면 각각의 `Serial Queue`는 한 번에 하나의 작업을 수행합니다. 하지만 각각의 Queue는 Concurrent하게 동작합니다.

예시를 통해 자세히 알아보겠습니다.

{% highlight swift %}
let queue = DispatchQueue(label: "serial")

let task: (String, String) -> Void = { task, item in
    (1...3).forEach { index in
        print("\(task)", item, "Index: \(index)")
    }
}

queue.async {
    print("register 1")
    print("Serial 1", Thread.current)
    task("task 1", "🍕")
    task("task 1", "⚽️")
}
print(":---:")

queue.async {
    print("register 2")
    print("Serial 3", Thread.current)
    task("task 2", "🍕")
    task("task 2", "⚽️")
}
print(":---:")

queue.async {
    print("register 3")
    print("Serial 5", Thread.current)
    task("task 3", "🍕")
    task("task 3", "⚽️")
}

/* 결과
register 1
:---:
Serial 1 <NSThread: 0x6040000706c0>{number = 3, name = (null)}
:---:
task 1 🍕 Index: 1
task 1 🍕 Index: 2
task 1 🍕 Index: 3
task 1 ⚽️ Index: 1
task 1 ⚽️ Index: 2
task 1 ⚽️ Index: 3
register 2
Serial 3 <NSThread: 0x6040000706c0>{number = 3, name = (null)}
task 2 🍕 Index: 1
task 2 🍕 Index: 2
task 2 🍕 Index: 3
task 2 ⚽️ Index: 1
task 2 ⚽️ Index: 2
task 2 ⚽️ Index: 3
register 3
Serial 5 <NSThread: 0x6040000706c0>{number = 3, name = (null)}
task 3 🍕 Index: 1
task 3 🍕 Index: 2
task 3 🍕 Index: 3
task 3 ⚽️ Index: 1
task 3 ⚽️ Index: 2
task 3 ⚽️ Index: 3
*/
{% endhighlight %}

Dispatch Queue 객체를 생성시 기본적으로 생성되는 것은 `Serial Queue`입니다. 위의 예제에서는 1개의 queue를 가지고 3번의 작업을 비동기로 수행합니다. 그런데, queue에서 수행하는 tasks들은 순서대로 동작합니다. 이것은 현재 생성한 Queue가 `Serial Queue`이기 때문입니다. `Serial Queue`는 한 번에 하나의 작업만 수행하고, 그래서 위의 tasks들은 순차적으로 등록되어 실행됩니다.

> 시스템이 비동기적으로 동작한다는 것의 기준은 "하나의 작업이 끝나기 전에 다른 작업이 수행될 수 있는가?"입니다. 여기서 queue의 첫 번 째 블럭이 완려되기 전에 queue 바깥의 코드(":---:")가 실행되었기 때문에 이는 비동기로 동작하였다고 할 수 있습니다.(만약 이를 동기적으로 수행하면 ":---:" 부분이 각각 register 2, 3 앞에서 수행됩니다.)

위의 예시에서 유의할 부분은 위에서는 모든 queue의 task가 같은 쓰레드에서 동작하였지만, 실제로 GCD는 이를 보장하지 않는다는 점입니다. `Serial Queue` 중 같은 쓰레드에서 작업이 이뤄지도록 보장된 것은 Main Queue밖에 없습니다.


### 2. Concurrent queue(global dispatch queue)

* `Concurrent Queue`는 Queue에 추가된 작업을 concurrent하게 수행합니다.
* 이 때, 동시에 수행되는 작업의 정확한 개수는 시스템의 상황에 따라 달라집니다.
* 시스템은 Global `Concurrent Queue`를 미리 정의하였습니다.
* 이 정의된 Queue는 우선순위가 서로 다른 Queue이며, `DispatchQueue`를 생성할 때 QoS(Quality of Service)를 통해 결정됩니다.

> The system provides each application with four concurrent dispatch queues. These queues are global to the application and are differentiated only by their priority level. Because they are global, you do not create them explicitly.

#### Qos(Priority)

사전에 정의된 Global `Concurrent Queue`의 종류는 아래와 같습니다.

1. user interactive - 📕 highest 우선순위,  ui를 업데이트하거나 즉시 실행되어야 하는 코드들을 넣는다. Main 쓰레드에서 동작한다.
2. user initiated - 📙 high 우선순위, user에 의해 실행되지만, 메인 쓰레드에서 동작할 필요가 없는 블럭을 실행한다. 즉각적인 결과를 필요로 할 때 사용한다.
3. utility - 📗 low 우선순위, 다운로드와 같은 오래 걸리는 작업을 처리하기에 적합하다.
4. Background - 📘 background 우선순위, 사용자의 눈에 보이지 않는 작업을 수행하기에 적합하다.

![img](https://dl.dropbox.com/s/ghb8lnx1yn4x1qx/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202018-07-13%20%EC%98%A4%EC%A0%84%2012.50.12.png)

이제 `Concurrent Queue`의 예제를 살펴보겠습니다. `Serial Queue`의 에제와 동일하지만, 동작하는 Queue의 종류만 변경한 것입니다.

{% highlight swift %}
let queue2 = DispatchQueue(label: "concurrent", qos: .default, attributes: .concurrent)

queue2.async {
    // Block A
    print("register 1")
    print("Concurrent 1", Thread.current)
    task("task 1", "🍕")
    task("task 1", "⚽️")
}
print(":---:")

queue2.async {
    // Block B
    print("register 2")
    print("Concurrent 3", Thread.current)
    task("task 2", "🍕")
    task("task 2", "⚽️")
}
print(":---:")

queue2.async {
    // Block C
    print("register 3")
    print("Concurrent 5", Thread.current)
    task("task 3", "🍕")
    task("task 3", "⚽️")
}

/* 결과
register 1
:---:
register 2
Concurrent 1 <NSThread: 0x60c000079100>{number = 3, name = (null)}
Concurrent 3 <NSThread: 0x604000071dc0>{number = 5, name = (null)}
:---:
register 3
Concurrent 5 <NSThread: 0x60c000079140>{number = 7, name = (null)}
task 2 🍕 Index: 1
task 1 🍕 Index: 1
task 3 🍕 Index: 1
task 2 🍕 Index: 2
task 1 🍕 Index: 2
task 3 🍕 Index: 2
task 1 🍕 Index: 3
task 2 🍕 Index: 3
task 3 🍕 Index: 3
task 2 ⚽️ Index: 1
task 1 ⚽️ Index: 1
task 3 ⚽️ Index: 1
task 1 ⚽️ Index: 2
task 3 ⚽️ Index: 2
task 2 ⚽️ Index: 2
task 1 ⚽️ Index: 3
task 3 ⚽️ Index: 3
task 2 ⚽️ Index: 3

*/
{% endhighlight %}

위의 예제에서는 `Serial Queue`의 결과와는 다르게 Block A, B, C의 작업들이 무작위로 수행됩니다. 즉, Queue의 작업이 Concurrent하게 실행되었습니다. 다만, Index 결과는 오름차순으로 나오는 것을 확인할 수 있는데, 이는 Concurrent Queue라고 하더라도 모든 작업이 똑같은 물리시간에 실행되는 것이 아니고, 추가된 순서대로 실행되기 때문입니다.

Concurrent Queue도 `Serial Queue`와 마찬가치로 동일한 쓰레드에서 수행되는 것을 보장하지 않습니다. 위에서 NSThread의 주소값이 서로 다른 것으로 보아 해당 작업은 모두 다른 쓰레드에서 수행된 것을 확인할 수 있습니다.(같은 쓰레드에서 수행될 수도 있습니다.)


### 3. Main Dispatch Queue
* 메인 쓰레드에서 작업을 수행하는 `Serial queue`
* 일반적으로 Main Queue는 작업의 동기화를 수행하는 공간(대표적으로 UI 업데이트)으로 활용됩니다.

`Main Dispatch Queue`는 앱의 `Main Thread`에서 작업을 수행하는 Queue입니다. `Main Thread`는 앱 실행시 바로 실행되는 쓰레드로 앱의 Run Loop를 담당([Application Life Cycle](https://hcn1519.github.io/articles/2017-09/ios_app_lifeCycle))합니다. 즉, `Main Thread`는 UIApplication 객체 생성하는 것과 같은 앱의 실행에 필요한 기반 작업들을 수행합니다. 그렇기 때문에 `Main Dispatch Queue`에서 모든 작업을 수행하는 것은 컴퓨터의 자원을 온전히 사용하지 못하도록 합니다.

`Main Dispatch Queue`는 `Serial Queue`이고, 그 특성에 따라 작업의 동기화를 수행하는 장소로 활용됩니다. 이 작업의 가장 대표적인 것이 UI 업데이트입니다. 모든 UI 업데이트는 `Main Dispatch Queue`에서 수행해야 하고 그렇지 않으면, 앱이 제대로 동작하지 않습니다.

## Serial Queue와 Concurrent Queue의 공통점과 차이점

위에서 Dispatch Queue의 각각에 대해 쭉 살펴보았는데, 관련해서 가장 이해가 되지 않았던 부분이 `Serial Queue`와 `Concurrent Queue`의 차이였습니다. 여기서는 이들의 공통점과 차이점을 구분하여 살펴보도록 하겠습니다.

#### 공통점

1. `Serial Queue`와 `Concurrent Queue` 모두 Concurrent하게 돌아간다.

* `Concurrent Queue`가 Concurrent(병렬적)하게 돌아간다는 것은 쉽게 이해할 수 있지만, `Serial Queue`가 Concurrent하게 돌아간다는 것은 다소 이해가 어려울 수 있습니다.  Queue 앞의 접두어로 들어가는 `Serial`과 `Concurrent`는  Queue가 tasks를 수행하는 방식을 의미하는 것이지,  Queue가 어떻게 돌아가는지를 의미하는 것이 아닙니다. Dispatch Queue는 코드가 모두 Concurrent하게 돌아가도록 하고, tasks가 sync/async하게 동작할지 여만 선택할 수 있습니다.

2. `Serial Queue`와 `Concurrent Queue` 모두 sync/async 코드 동작을 지원하고, sync로 수행할 경우 Main Thread가 작업 수행을 기다린다.

3. `Serial Queue`와 `Concurrent Queue` 모두 동일한 쓰레드에서 동작하는 것을 보장하지 않는다.

* Dispatch Queue에서 동일한 쓰레드에서 동작하도록 고안된 것은 `Main Queue`밖에 없습니다.

4. `Serial Queue`와 `Concurrent Queue` 모두 하드웨어적인 parallel을 보장하지 않는다.

* 하드웨어적으로 코드가 병렬적으로 돌아간다는 것은 하나의 프로세스 내에서 여러 개의 쓰레드가 돌아가는 것을 의미합니다. 하지만, GCD에 할당된 tasks가 몇 개의 쓰레드에서 돌아갈 것인지는 시스템의 환경이 결정합니다. 즉, 시스템의 환경에 따라 여러 개의 쓰레드에서 코드가 동작할 수도 있지만, 그렇지 않은 경우도 발생할 수 있다는 것입니다.


#### 차이점

1. `Serial Queue`는 한 번에 하나의 task만 하지만, `Concurrent Queue`는 동시에 여러 tasks를 수행한다.

* 앞선 예제에서 확인한 것처럼 `Serial Queue`는 항상 한 가지 task를 하고 있다는 것이 보장됩니다. 여기서 task의 단위는 하나의 코드 블럭(closure) 혹은 `DispatchWorkItem`를 의미합니다. 하지만 `Concurrent Queue`는 동시에 여러 개의 tasks를 수행합니다.

2. `Serial Queue`는 작업의 동기화에 주로 사용되고, `Concurrent Queue`는 작업의 수행에 주로 사용된다.


---

## 참고자료
* [Concurrency and Application Design](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/ConcurrencyandApplicationDesign/ConcurrencyandApplicationDesign.html#//apple_ref/doc/uid/TP40008091-CH100-SW1)

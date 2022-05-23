---
layout: post
title: "GCD - Dispatch Queue"
excerpt: "Dispatch Queue에 대한 정리"
date: "2018-07-08 20:04:49 +0900"
categories: Concurrent GCD DispatchQueue iOS OS Thread
tags: [Concurrency, GCD, DispatchQueue, iOS, OS, Thread]
image:
  feature: iOS.png
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
    // task1
    print("register 1")
    print("Serial 1", Thread.current)
    task("task 1", "🍕")
    task("task 1", "⚽️")
}
print(":---:")

queue.async {
    // task2
    print("register 2")
    print("Serial 3", Thread.current)
    task("task 2", "🍕")
    task("task 2", "⚽️")
}
print(":---:")

queue.async {
    // task3
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

Dispatch Queue 객체를 생성시 기본적으로 생성되는 것은 `Serial Queue`입니다. 위의 예제에서는 1개의 queue를 가지고 3번의 작업을 비동기로 수행합니다. 이 때, 생성한 Queue가 `Serial Queue`이기 때문에 queue에서 수행하는 tasks들은 순서대로 동작합니다. `Serial Queue`는 한 번에 하나의 작업만 수행합니다. 그래서 위의 tasks들은 순차적으로 등록되어 실행됩니다.

위의 예시에서 유의할 부분은 위에서는 모든 queue의 task가 같은 쓰레드에서 동작하였지만, 실제로 GCD는 이를 보장하지 않는다는 점입니다. `Serial Queue` 중 같은 쓰레드에서 작업이 이뤄지도록 보장된 것은 Main Queue밖에 없습니다.

#### 동기/비동기

시스템이 비동기적으로 동작한다는 것의 기준은 "하나의 작업이 끝나기 전에 다른 작업이 수행될 수 있는가?"입니다. 이 대답이 yes면 비동기, no면 동기입니다. 동기적으로 작성된 코드는 반드시 리턴이 되어야만 다음 작업이 진행됩니다. 그래서 먼저 작성된 코드가 뒤의 코드보다 우선적으로 실행될 수 없습니다. 만약 위의 예시를 동기적으로 수행하면 ":---:" 부분이 각각 register 2, 3보다 먼저 출력됩니다. 그런데 위의 예시는 queue의 첫 번째 블럭이 완료되기 전에 queue 바깥의 코드(":---:")가 실행되었기 때문에 이는 비동기로 동작하였다고 할 수 있습니다.

동기의 개념과 serial의 개념을 혼동하면 안 됩니다. 위의 예시에서 동기/비동기로 동작하는가를 판단하는 기준은 **queue의 작업이 다른 작업을 수행할 수 없게 만드는가?**에 대한 것입니다. 위의 예시는 그렇지 않기 때문에 비동기로 동작한다고 말할 수 있습니다. 한편, `Serial Queue`를 사용한다는 것은 queue의 작업이 추가한 순서대로(task 1 -> task 2 -> task 3) 수행되도록 하는 것을 의미합니다. 이는 **수행의 순서만을 지칭하는 것이지 task1이 task2의 수행을 완전히 막을 수는 없습니다.** 즉, task 1이 수행된 이후에 task 2가 수행된다고 말하는 것은 task 2의 수행이 task 1에 의해 불가능해진다.를 의미하지는 않습니다.

```swift
let queue = DispatchQueue(label: "serial")
let queue2 = DispatchQueue(label: "serial2")

let task: (String, String) -> Void = { task, item in
    (1...3).forEach { index in
        print("\(task)", item, "Index: \(index)")
    }
}

// queue.sync로 변경하면, queue2의 동작도 수행되지 않습니다.
// Block B는 queue가 아니라 queue2를 이용하면, Block A를 기다리지 않고 바로 수행될 수 있습니다.
queue.async {
    // Block A
    print("register 1")
    print("Concurrent 1", Thread.current)
    task("task 1", "🍕")
    task("task 1", "⚽️")
    sleep(5)
}
queue.async {
    // Block B
    print("register 2")
    print("Concurrent 3", Thread.current)
    task("task 2", "🍕")
    task("task 2", "⚽️")
}
queue2.async {
    // Block B
    print("register 2")
    print("Concurrent 3", Thread.current)
    task("task 2", "🍕")
    task("task 2", "⚽️")
}
```

### 2. Concurrent Queue(global dispatch queue)

* `Concurrent Queue`는 Queue에 추가된 작업을 concurrent하게 수행합니다.
* 이 때, 동시에 수행되는 작업의 정확한 개수는 시스템의 상황에 따라 달라집니다.
* 시스템은 Global `Concurrent Queue`를 미리 정의하였습니다.
* 이 정의된 Queue는 우선순위가 서로 다른 Queue이며, `DispatchQueue`를 생성할 때 QoS(Quality of Service)를 통해 결정됩니다.

> The system provides each application with four concurrent dispatch queues. These queues are global to the application and are differentiated only by their priority level. Because they are global, you do not create them explicitly.

#### QoS(Priority)

사전에 정의된 Global `Concurrent Queue`의 종류는 아래와 같습니다.

1. user interactive - 📕 highest 우선순위, ui를 업데이트하거나 즉시 실행되어야 하는 코드들을 넣는다. Main 쓰레드에서 동작한다.
2. user initiated - 📙 high 우선순위, user에 의해 실행되지만, 메인 쓰레드에서 동작할 필요가 없는 블럭을 실행한다. 즉각적인 결과를 필요로 할 때 사용한다.
3. utility - 📗 low 우선순위, 다운로드와 같은 오래 걸리는 작업을 처리하기에 적합하다.
4. Background - 📘 background 우선순위, 사용자의 눈에 보이지 않는 작업을 수행하기에 적합하다.

<img src="{{ site.imageUrl}}/2018-07/gcddispatchqueue/qos.png">

이제 `Concurrent Queue`의 예제를 살펴보겠습니다. `Serial Queue`의 에제와 동일하지만, 동작하는 Queue의 종류만 변경한 것입니다.

{% highlight swift %}
let queue2 = DispatchQueue(label: "concurrent", qos: .default, attributes: .concurrent)

let task: (String, String) -> Void = { task, item in
    (1...3).forEach { index in
        print("\(task)", item, "Index: \(index)")
    }
}

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

위의 예제에서는 `Serial Queue`의 결과와는 다르게 Block A, B, C의 작업들이 무작위로 수행됩니다. 즉, Queue의 작업이 Concurrent하게 실행되었습니다. 다만, Index 결과는 오름차순으로 나오는 것을 확인할 수 있는데, 이는 task closure의 반복문이 순차적으로 실행되기 때문입니다.

Concurrent Queue도 `Serial Queue`와 마찬가치로 동일한 쓰레드에서 수행되는 것을 보장하지 않습니다. 위에서 NSThread의 주소값이 서로 다른 것으로 보아 해당 작업은 모두 다른 쓰레드에서 수행된 것을 확인할 수 있습니다.(같은 쓰레드에서 수행될 수도 있습니다.)

### 3. Main Dispatch Queue

* 메인 쓰레드에서 작업을 수행하는 `Serial queue`
* 일반적으로 Main Queue는 작업의 동기화를 수행하는 공간(대표적으로 UI 업데이트)으로 활용됩니다.

`Main Dispatch Queue`는 앱의 `Main Thread`에서 작업을 수행하는 Queue입니다. `Main Thread`는 앱 실행시 바로 실행되는 쓰레드로 앱의 Run Loop를 담당([Application Life Cycle](https://hcn1519.github.io/articles/2017-09/ios_app_lifeCycle))합니다. 즉, `Main Thread`는 UIApplication 객체 생성하는 것과 같은 앱의 실행에 필요한 기반 작업들을 수행합니다. 그래서 `Main Thread`는 일반적으로 많이 바쁩니다. 그래서 `Main Thread`에서 반드시 수행될 필요가 없는 작업들은 다른 쓰레드에서 수행하는 것이 컴퓨터의 자원을 좀 더 적극적으로 사용할 수 있도록 합니다.

`Main Dispatch Queue`는 `Serial Queue`이고, 그 특성에 따라 작업의 동기화를 수행하는 장소로 활용됩니다. 이 작업의 가장 대표적인 것이 UI 업데이트입니다. 모든 UI 업데이트는 `Main Dispatch Queue`에서 수행해야 하고 그렇지 않으면, 화면이 제대로 업데이트 되지 않습니다.

## Serial Queue와 Concurrent Queue의 공통점과 차이점

위에서 Dispatch Queue의 각각에 대해 쭉 살펴보았는데, 관련해서 가장 이해가 되지 않았던 부분이 `Serial Queue`와 `Concurrent Queue`의 차이였습니다. 여기서는 이들의 공통점과 차이점을 구분하여 살펴보도록 하겠습니다.

#### 공통점

a. `Serial Queue`와 `Concurrent Queue` 모두 sync/async 코드 동작을 지원합니다. 하지만, sync는 일반적인 상황에서 쓸일이 거의 없습니다.

* sync로 작업을 수행하면 블럭의 작업이 끝날 때까지 쓰레드가 이를 기다립니다. 그리고 이 기다리는 쓰레드가 `Main Thread`라면 화면은 블럭의 작업이 끝날 때까지 아무 반응도 할 수 없습니다. 멀티 쓰레드 프로그래밍 환경에서는 **일반적으로 블럭의 작업이 끝날 때까지 기다리는 형태로 코드를 작성하지 않습니다.** 멀티 쓰레드 프로그래밍 환경에서 시스템은 블럭을 돌아다니면서 계속 작업을 수행합니다. 이 때 블럭에서는 작업을 마무리한 후에 작업이 끝났음을 알리는 completion Handler만 시스템에 전달합니다. 그래서 시스템은 다른 작업을 하고 있다가 completion Handler를 통해 기존에 수행하던 작업이 끝났음을 인지하고, 다음 작업을 이어갑니다.

b. `Serial Queue`와 `Concurrent Queue` 모두 동일한 쓰레드에서 동작하는 것을 보장하지 않는다.

* Dispatch Queue에서 동일한 쓰레드에서 동작하도록 고안된 것은 `Main Queue`밖에 없습니다.

c. `Serial Queue`와 `Concurrent Queue` 모두 하드웨어적인 parallel을 보장하지 않는다.

* 하드웨어적으로 코드가 병렬적으로 돌아간다는 것은 하나의 프로세스 내에서 여러 개의 쓰레드가 돌아가는 것을 의미합니다. 하지만, GCD에 할당된 tasks가 몇 개의 쓰레드에서 돌아갈 것인지는 시스템의 환경이 결정합니다. 즉, 시스템의 환경에 따라 여러 개의 쓰레드에서 코드가 동작할 수도 있지만, 그렇지 않은 경우도 발생할 수 있다는 것입니다.(이를 제한하기 위해서는 Operation Queue를 사용해야 합니다.)

#### 차이점

a. `Serial Queue`는 한 번에 하나의 task만 하지만, `Concurrent Queue`는 동시에 여러 tasks를 수행한다.

* 앞선 예제에서 확인한 것처럼 `Serial Queue`는 항상 한 가지 task를 하고 있다는 것이 보장됩니다. 여기서 task의 단위는 하나의 코드 블럭(closure) 혹은 `DispatchWorkItem`를 의미합니다. 하지만 `Concurrent Queue`는 동시에 여러 개의 tasks를 수행합니다.

b. `Serial Queue`는 작업의 동기화에 주로 사용되고, `Concurrent Queue`는 작업의 수행에 주로 사용된다.

* `Serial Queue`가 하나의 task만 수행하는 것은 작업의 수행 순서가 보장된 것이기 때문에, 여러 작업들의 동기화를 수행할 때 사용할 수 있습니다. `Concurrent Queue`는 자원을 병렬적으로 사용할 수 있도록 돕기 때문에 주로 일반적인 작업의 수행에 활용됩니다. 다만, `Concurrent Queue`에서 제한 없이 과도한 작업을 수행하게 되면 메모리 사용량이 제한 없이 늘어나기 때문에 주의가 필요합니다.


---

## 참고자료
* [Concurrency and Application Design](https://developer.apple.com/library/content/documentation/General/Conceptual/ConcurrencyProgrammingGuide/ConcurrencyandApplicationDesign/ConcurrencyandApplicationDesign.html#//apple_ref/doc/uid/TP40008091-CH100-SW1)

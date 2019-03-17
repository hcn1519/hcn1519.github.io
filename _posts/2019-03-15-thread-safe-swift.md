---
layout: post
title: "Thread Safe"
date: "2019-03-15 00:10:45 +0900"
excerpt: "Thread Safe에 대해서 알아봅니다."
categories: Swift Thread-Safe Language
tags: [Swift, Thread-Safe, Language]
image:
  feature: swiftLogo.jpg
---

## Thread Safe 개념

**어떤 것이 Thread Safe하다라고 하는 것은 (프로퍼티, 함수 등) 다중 쓰레드 환경에서 동시에 접근해도 괜찮다**는 것을 의미합니다. 여기서 괜찮다라는 것은 A 쓰레드에서 어떤 작업(프로퍼티, 함수 등)이 호출되어 동작하고 있는 도중에 B 쓰레드에서 해당 작업에 접근하여도 결과값이 올바르게 나오는 것을 의미합니다.

다만, 이는 Thread Safe한 작업을 판단할 때 있어서, 다소 모호하게 이해될 수 있는 부분이 있습니다.* 이를 좀 더 구체적으로 정리하면 다음과 같습니다.

1. Mutable한 자료구조가 Thread Safe하다는 것은 **공유 데이터에 대한 작업이 항상 최신의 데이터 상태에 대해 이뤄지는 것**을 의미합니다. 이는 때때로 논리적으로 일관적이지 않을 수 있습니다.
2. ImMutable한 자료구조가 Thread Safe하다는 것은 최신의 데이터가 아니더라도 모든 데이터에 대한 작업이 항상 논리적으로 일관적인 것을 의미합니다.

> *[What is this thing you call "thread safe"?](https://blogs.msdn.microsoft.com/ericlippert/2009/10/19/what-is-this-thing-you-call-thread-safe/)에서 이에 대해서 조금 더 자세하게 서술되어 있습니다.

## Thread Safe 판단 예시

### 1. Swift Class - Crash

 Swift class 인스턴스의 `reference count` 값은 `atomic`하게 업데이트 되어, `racing condition`*에 빠지지 않습니다. 하지만, `atomic`한 데이터라도 `reference type` 인스턴스의 alloc/dealloc 정보는 쓰레드 단위로 공유되지 않기 때문에 다중 쓰레드 환경에서 새로운 `reference type` 인스턴스에 동시에 접근하는 것은 여러 가지 문제를 일으킬 수 있습니다. 즉, `reference type` 인스턴스는 Thread Safe하지 않습니다.

> racing condition - 공유 자원에 대해 여러 개의 프로세스가 동시에 접근을 시도할 때 접근의 타이밍이나 순서 등이 결과값에 영향을 줄 수 있는 상태

* 출처: [위키 피디아 - 경쟁 상태](https://ko.wikipedia.org/wiki/경쟁_상태)

```swift
class Bird {}
var single = Bird()

DispatchQueue.global().async {
    while true { single = Bird() }
}

while true { single = Bird() }
// error - malloc: Double free of object 0x102887200
```

출처: [swift doc - Concurrency.rst](https://github.com/apple/swift/blob/master/docs/proposals/Concurrency.rst)

위의 예시는 에러 메시지에서 확인할 수 있듯이 이미 해제된 인스턴스를 다시 dealloc하는 시도가 이뤄졌기 때문에 crash가 발생합니다. 즉, 서로 다른 쓰레드에서 dealloc된 인스턴스 정보를 공유하지 않기 때문에 위의 문제가 발생합니다.

### 2. 최신 데이터에 대한 접근

파일에 데이터를 읽고 쓰는 작업을 서로 다른 쓰레드에서 수행할 경우 데이터는 항상 최신의 상태에서 접근될 수 없습니다. 즉, File I/O 작업도 Thread Safe하지 않습니다.

```swift
func writeContent(txtFileUrl: URL, savedContent: String, newContent: String) {
    let text = savedContent + newContent
    try? text.write(to: txtFileUrl, atomically: true, encoding: .utf8)
}

let documentsDirectoryURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
let txtFileUrl = documentsDirectoryURL.appendingPathComponent("sample.txt")

let task: (String) -> Void = { suffix in
    (1...100).forEach { content in
        let str = "\(content)" + suffix
        if let savedContent = try? String(contentsOf: txtFileUrl, encoding: .utf8) {
            writeContent(txtFileUrl: txtFileUrl, savedContent: savedContent, newContent: str)
        }
    }
}

DispatchQueue.global().async {
    task("a ")
}

DispatchQueue.global().async {
    task("b ")
}

sleep(2)
print("result", readFile(txtFileUrl: txtFileUrl)!)
// 원하는 결과 1a 2a 3a ... 100a 1b 2b 3b ... 100b
/* 예시 결과 -  결과는 조금씩 다릅니다.
result 1a 2a 3a 4a 5a 6a 7a 8a 9a 10a 11a 12a 13a 14a 15a 16a 15b 16b 17b 18b 19b 20b
21b 22b 23b 24b 25b 26b 27b 28b 29b 30b 31b 32b 33b 34b 36a 37a 38a 39a 40a
41a 42a 43a 44a 45a 46a 47a 48a 49a 48b 49b 50b 51b 52b 54a 55a 56a 57a 58a 59a 60a
61a 62a 63a 64a 65a 65b 66b 67b 68b 69b 70a 71a 72a 73a 73b 74b 75b 76b 77a 78a 79a 80a
81a 82a 83a 84a 85a 86a 87a 88a 89a 89b 90b 91b 92a 93a 94a 95a 96a 97a 98a 99a 100a 100b
*/
```

위의 예시는 File I/O 작업이 항상 최신의 데이터에 항상 접근될 수 없기 때문에 Thread Safe하지 않다는 것을 보여주는 예시입니다. 여기서 눈여겨 볼 부분은 File에 내용을 write하는 작업이 `atomic`하게 수행되었음에도 위와 같은 결과가 나왔다는 점입니다. 여기서 Thread Safe가 달성되지 못 하는 근본적인 원인은 공유 자원(여기서는 sample.txt라는 파일)에 동시에 접근하려고 시도하여 작업 순서에 관계 없이 권한을 획득한 task가 자신의 작업을 수행하기 때문입니다.

## Thread Safe 달성하기

Thread Safe를 달성하기 위해서 제안되는 것들이 몇 가지 있습니다. 아래의 내용은 일반적으로 Thread Safe를 달성하기 위해 제안되는 방법들입니다.

1. Mutual Exclusion - 쓰레드에 락이나 세마포어를 걸어서 공유자원에 하나의 쓰레드만 접근하도록 한다.
2. Thread Local Storage - 특정 쓰레드에서만 접근 가능한 저장소를 만든다.
3. ReEntrancy - 쓰레드에서 동작하는 코드가 동일 쓰레드에서 재수행되거나, 다른 쓰레드에서 해당 코드를 동시에 수행해도 동일한 결과값을 얻을 수 있도록 코드를 작성한다. 이는 쓰레드 진입시 local state를 저장하고 이를 atomic하게 사용하여 구현될 수 있습니다.
4. Atomic Opertaion - 데이터 변경시 atomic하게 데이터에 접근되도록 만든다.(참고 - [atomic/non-atomic](https://hcn1519.github.io/articles/2019-03/atomic))
5. ImMutable Object - 객체 생성 이후에 값을 변경할 수 없도록 만든다.

출처: [위키 피디아 - Thread Safety](https://en.wikipedia.org/wiki/Thread_safety)

## Swift와 Thread Safe

> 이하의 내용은 [swift doc - Concurrency.rst](https://github.com/apple/swift/blob/master/docs/proposals/Concurrency.rst)에 있는 내용을 기반으로 작성하였습니다. 그런데 본 문서의 서두에 not accepted proposal이라는 언급이 있습니다. 이는 async-await에 대한 feature가 거절된 것일뿐, Swift 언어 자체에 대한 분석 내용이 문제가 있는 것이 아닙니다. 여기서는 async-await에 대한 것을 다루는 것이 아니라, Swift의 Thread Safe 구현에 대한 것만 다룹니다.

일반적으로 Thread Safe는 공유된 mutable한 자원(shared mutable memory)이 존재할 때 발생합니다. 그렇기 때문에 Swift는 Thread Safe를 달성하기 위해 쓰레드간의 메모리를 공유하는 것을 방지하는 장치가 몇 가지 존재합니다.

### 1. Copyable Protocol

`Copyable Protocol`은 **해당 타입들이 쓰레드 context 단위로 안전한 복사가 가능한 것**을 명시합니다. 흔히 다른 언어에서 primitive type으로 알려져 있는 `Int`, `Float`, `Double` 등 타입 안에 reference를 포함하고 있지 않은 것들이 `Copyable Protocol`을 따르고 있습니다. 또한, `String`, `Array`(Copyable 타입을 담은 Array이어야 합니다.)처럼 실제로 reference는 가지고 있지만, value type으로 만들어진 것들도 쓰레드 단위로 복사가 허용됩니다.

### 2. ReEntrant code

`ReEntrant code`란, 주어진 arguments를 통해서만 접근할 수 있는 코드로, `ReEntrant code`는 전역 변수, 공유 자원에 접근할 수 없습니다. Swift는 코드 작성시에는 하나의 쓰레드에서는 다른 쓰레드의 논리적 복사 데이터에만 접근할 수 있도록 허용합니다. 전역변수에 접근할 때나 unsafe한 데이터에 접근할 때, Swift 컴파일러는 이를 반드시 확인합니다.(DispatchQueue를 사용할 때, queue 변경시 self를 명시적으로 작성해야 하는 것을 생각하면 됩니다.)

### 3. Gateway Annotation

Swift 항상 새로운 쓰레드를 만들어서 함수가 동작하도록 하는 annotation을 지원합니다. 바꿔말하면 Swift에는 Thread verifier가 존재하여 `Copyable Protocol` 조건과 `ReEntrant code` 조건이 충족되는지를 컴파일 단계에서 확인합니다.

```swift
@_semantics("swift.concurrent.launch")
public func createTask<ArgsTy>(args : ArgsTy, callback : (ArgsTy) -> Void) {
  ...
}
```

---

## 참고자료

* [What is this thing you call "thread safe"?](https://blogs.msdn.microsoft.com/ericlippert/2009/10/19/what-is-this-thing-you-call-thread-safe/)
* [swift doc - Concurrency.rst](https://github.com/apple/swift/blob/master/docs/proposals/Concurrency.rst)
* [위키 피디아 - 경쟁 상태](https://ko.wikipedia.org/wiki/경쟁_상태)
* [위키 피디아 - Thread Safety](https://en.wikipedia.org/wiki/Thread_safety)
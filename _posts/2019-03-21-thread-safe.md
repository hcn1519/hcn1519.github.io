---
layout: post
title: "Thread Safe"
date: "2019-03-21 00:10:45 +0900"
excerpt: "Thread Safe에 대해 알아 봅니다."
categories: Swift ThreadSafe atomic OS Thread Language
tags: [Swift, ThreadSafe, atomic, OS, Thread, Language]
image:
  feature: blogThumb.png
---

## 목차

1. [Thread Safe 개념](https://hcn1519.github.io/articles/2019-03/thread-safe#thread-safe-개념)
2. [Thread Safe 판단 예시](https://hcn1519.github.io/articles/2019-03/thread-safe#thread-safe-판단-예시)
3. [Thread Safe 달성하기](https://hcn1519.github.io/articles/2019-03/thread-safe#thread-safe-달성하기)
4. [Swift와 Thread Safe](https://hcn1519.github.io/articles/2019-03/thread-safe#swift와-thread-safe)

Thread Safe 여부를 판단하는 것은 다중 쓰레드 환경에서 코드를 작성할 때, 반드시 이해해야 하는 부분 중 하나입니다.이번 포스팅에서는 Thread Safe가 무엇이고, 어떻게 Thread Safe를 판단하는지에 대해 살펴보고자 합니다.

## Thread Safe 개념

Thread Safe에 대해서는 다음 글([Thread Safety - MIT](http://web.mit.edu/6.005/www/fa15/classes/20-thread-safety)에서 자세히 서술되어 있습니다. 아래의 내용은 이 글의 일부를 발췌하여 정리하였습니다. 원글에서는 Thread Safe에 대한 정의를 아래와 같이 서술하고 있습니다.

> A data type or static method is threadsafe if it behaves correctly when used from multiple threads, regardless of how those threads are executed, and without demanding additional coordination from the calling code.

이를 정리하면 다음과 같습니다. 데이터 타입이나 static 메소드가 Thread Safe하다라고 하는 것은 다음의 조건을 만족할 때 성립합니다.

1. 다중 쓰레드의 동작에 관계 없이 항상 올바르게 동작한다.
2. 호출에 있어서 추가적인 조건이 없다.

이에 대해 원글에서는 다음과 같은 설명을 덧붙입니다.

* **올바르게 동작 한다는 것**은 명세를 만족시키고 객체의 표현 불변성을 유지하는 것을 의미합니다.(`representation invariant`)
* 호출에 있어서 **추가적인 조건이 없다**는 것은 데이터 타입이 타이밍과 관련하여 호출자에 전제 조건을 지정할 수 없음을 의미합니다.

위 내용만으로는 제 스스로 Thread Safe에 대한 정의를 완전히 이해하기 어려워서 😭 관련하여 좀 더 내용을 알아보고, 이에 대해 정리하였습니다.

* `representation invariant`(표현 불변성)이라는 말은 어떤 클래스에서 항상 변하지 않는 것을 지칭합니다. 주사위를 굴리는 것을 예로 생각해보겠습니다. 주사위를 굴릴 때 눈금은 항상 1 에서 6 사이입니다. 한 개의 주사위를 굴리는 행위로는 1에서 6 사이의 자연수 이외의 숫자를 결과로 내놓을 수 없습니다. 바꿔 말하면, `Dice🎲` 클래스에서 `throwDice()`라는 메소드는 `Dice🎲` 클래스의 `representation invariant`을 유지한다고 할 수 있습니다.

* 타이밍과 관련하여 호출자에 전제 조건이 있는 것은 다음과 같은 경우입니다. `UITableView`는 특정 cell만 reload하기 위해 다음과 같이 코드를 작성합니다.

```swift
func updateCell() {
    tableView.beginUpdates()
    // cell update
    tableView.endUpdates()
}
```

이 경우에 `endUpdates()`은 반드시 `beginUpdates()` 이후에 호출되어야 하는 전제 조건이 있습니다. 이런 조건이 없는 것이 호출자에 전제 조건이 없는 것입니다.

## Thread Safe 판단 예시

### 1. Swift Class Instance

reference type의 인스턴스를 새로 만드는 것은 메모리 delloc 후에 alloc이 이루어져야 합니다. 하지만, 다중 쓰레드 환경에서 `reference type` 인스턴스의 alloc/dealloc 정보는 쓰레드 단위로 공유되지 않습니다.

```swift
class Bird {}
var single = Bird()

DispatchQueue.global().async {
    while true { single = Bird() }
}

while true { single = Bird() }
// error - malloc: Double free of object 0x102887200
```

위의 코드는 실행시 매우 빠르게 크래시가 발생합니다. 이 크래시는 다중 쓰레드 환경에서 A 쓰레드가 B 쓰레드의 인스턴스 해제 정보를 알지 못 하기 때문에 발생합니다.

Swift의 Class 인스턴스의 `reference count` 값은 `atomic`하게 업데이트 되어, `racing condition`에 빠지지 않습니다. 하지만, `atomic`하게 데이터를 업데이트 하는 것이 보장하는 것은 `reference type` 인스턴스의 생성(해제) 도중에 다른 쓰레드가 인스턴스에 접근하지 못 하도록 하는 것입니다. 이 경우 여전히 인스턴스 생성 이후, 생성 이전에는 다른 쓰레드에서 인스턴스에 접근이 가능합니다. 이 때, 다른 쓰레드는 alloc/dealloc 정보를 모르기 때문에 `reference type` 인스턴스의 생성과 해제는 Thread Safe하지 않습니다.

> racing condition - 공유 자원에 대해 여러 개의 프로세스가 동시에 접근을 시도할 때 접근의 타이밍이나 순서 등이 결과값에 영향을 줄 수 있는 상태

### 2. File read/write

파일에 데이터를 읽고 쓰는 작업이 Thread Safe한가에 대해서는 고려할 때, 타이밍 이슈를 생각해 볼 수 있습니다. 파일의 내용은 `read()`, `write()`의 순서에 따라 그 결과가 항상 변합니다. 즉, 

* `read()` 이후에 `write()`
* `write()` 이후에 `read()`
* `read()` 도중에 `write()`
* `write()` 도중에 `read()`

의 경우에서 결과가 같음이 보장되지 않습니다. 그렇기 때문에 File read/write는 Thread Safe하지 않습니다. 여기서 Thread Safe를 달성하지 못 하도록 만드는 주요한 요인은 File의 내용이 `Mutable`하다는 것입니다. 만약, File의 데이터가 `ImMutable`하다면(`write()`가 불가능하다면) 타이밍 이슈는 해결됩니다.

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
/* 예시 결과 -  결과는 코드 실행마다 다릅니다.
result 1a 2a 3a 4a 5a 6a 7a 8a 9a 10a 11a 12a 13a 14a 15a 16a 15b 16b 17b 18b 19b 20b
21b 22b 23b 24b 25b 26b 27b 28b 29b 30b 31b 32b 33b 34b 36a 37a 38a 39a 40a
41a 42a 43a 44a 45a 46a 47a 48a 49a 48b 49b 50b 51b 52b 54a 55a 56a 57a 58a 59a 60a
61a 62a 63a 64a 65a 65b 66b 67b 68b 69b 70a 71a 72a 73a 73b 74b 75b 76b 77a 78a 79a 80a
81a 82a 83a 84a 85a 86a 87a 88a 89a 89b 90b 91b 92a 93a 94a 95a 96a 97a 98a 99a 100a 100b
*/
```

## Thread Safe 달성하기

Thread Safe를 달성하기 위해서 제안되는 것들이 몇 가지 있습니다. 아래의 내용은 일반적으로 Thread Safe를 달성하기 위해 제안되는 방법들입니다.

1. Mutual Exclusion - 쓰레드에 락이나 세마포어를 걸어서 공유자원에 하나의 쓰레드만 접근하도록 한다.
2. Thread Local Storage - 특정 쓰레드에서만 접근 가능한 저장소를 만든다.
3. ReEntrancy - 쓰레드에서 동작하는 코드가 동일 쓰레드에서 재수행되거나, 다른 쓰레드에서 해당 코드를 동시에 수행해도 동일한 결과값을 얻을 수 있도록 코드를 작성한다. 이는 쓰레드 진입시 local state를 저장하고 이를 atomic하게 사용하여 구현될 수 있습니다.
4. Atomic Opertaion - 데이터 변경시 atomic하게 데이터에 접근되도록 만든다.(참고 - [atomic/non-atomic](https://hcn1519.github.io/articles/2019-03/atomic))
5. ImMutable Object - 객체 생성 이후에 값을 변경할 수 없도록 만든다.

출처: [위키 피디아 - Thread Safety](https://en.wikipedia.org/wiki/Thread_safety)

## Swift와 Thread Safe

> 이하의 내용은 [swift doc - Concurrency.rst](https://github.com/apple/swift/blob/master/docs/proposals/Concurrency.rst)에 있는 내용을 기반으로 작성하였습니다. 그런데 본 문서의 서두에 not accepted proposal이라는 언급이 있습니다. 이는 async-await에 대한 feature가 거절된 것일뿐, Swift의 Thread Safe에 대해 분석한 내용이 문제가 있는 것이 아닙니다.

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
* [what does the term rep-invariant and rep ok means?](https://stackoverflow.com/questions/7578086/what-does-the-term-rep-invariant-and-rep-ok-means)
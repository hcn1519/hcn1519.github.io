---
layout: post
comments: true
title:  "Swift Async Await"
excerpt: "Swift의 Async Await에 대해 알아봅니다."
categories: Swift Language Async Await Concurrency
date:   2022-04-08 00:30:00
tags: [Swift, Language, Async, Await, Concurrency, Thread]
image:
  feature: swiftLogo.jpg
---

이 글에서는 Swift 5.5에 소개된 Async/Await에 대해 살펴보고자 합니다.

## Table of Contents

1. [기존 Asynchronous 작업 처리 방식](./swift_async_await#1-기존-asynchronous-작업-처리-방식)
1. [Asynchronous Functions의 정의와 호출](./swift_async_await#2-asynchronous-functions의-정의와-호출)
1. [Asynchronous Sequences](./swift_async_await#3-asynchronous-sequences)
1. [Calling Asynchronous Functions in Parallel](./swift_async_await#4-calling-asynchronous-functions-in-parallel)
1. [Task and Task Groups](./swift_async_await#5-task-and-task-groups)

> 해당 내용은 [The Swift Programming Languages(5.5) - Concurrency](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html#)에 기반하여 작성된 내용입니다. 

- `Asynchronous code`를 사용하면 프로그램 여러가지 작업을 동시에 수행하는 것을 쉽게 만듭니다.
- `Asynchronous code`를 사용하면 코드 복잡도를 줄일 수 있습니다.

## 1. 기존 Asynchronous 작업 처리 방식

기존의 completion handler 기반의 async 코드를 사용하면 단순한 코드에도 nested closure를 사용해야 하므로 코드 복잡도가 올라갑니다.

```swift
listPhotos(inGallery: "Summer Vacation") { photoNames in
    let sortedNames = photoNames.sorted()
    let name = sortedNames[0]
    downloadPhoto(named: name) { photo in
        show(photo)
    }
}
```
- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

##  2. Asynchronous Functions의 정의와 호출

`asynchronous function`(method)이라는 새로운 형태의 함수는 실행 도중에 일시정지가 가능합니다. 기존의 `synchronous function`은 completion을 수행하거나, 에러를 던지거나, 리턴되지 않는 형태로만 동작합니다. 하지만 `asynchronous function`은 동작 도중에 멈추었다가 결과가 도착하면 다시 실행이 가능합니다. `asynchronous function`은 `async` keyword를 함수 선언부 마지막(리턴 화살표 전 `->`, `throws`를 같이 쓴다면 그 앞에 추가)에 추가하여 사용할 수 있습니다.

```swift
func listPhotos(inGallery name: String) async -> [String] {
    let result = // ... some asynchronous networking code ...
    return result
}
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

`asynchronous function` 호출시 함수의 실행은 함수가 리턴되기 전까지 진행되지 않습니다. 그리고 `asynchronous function` 내에서 `await` keyword를 사용하여 가능한 suspension point(중단 포인트)를 표기할 수 있습니다. `asynchronous function` 내에서 함수의 실행은 함수 내부에 추가적인 `asynchronous function`이 존재(`await` keyword가 있을 때)할 때만 일시정지 됩니다. 모든 suspension point에는 명시적으로 `await` keyword가 존재해야 합니다.

```swift
let photoNames = await listPhotos(inGallery: "Summer Vacation")
let sortedNames = photoNames.sorted()
let name = sortedNames[0]
let photo = await downloadPhoto(named: name)
show(photo)
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

위 코드 수행 순서는 다음과 같습니다.

1. 일반적인 코드 수행 호출 순서에 맞춰서 await keyword 전까지 수행됩니다. `listPhotos(inGallery:)`을 호출하고, 해당 함수가 리턴되기까지 기다립니다.
2. 코드의 수행이 멈춘 상태에서 프로그램은 다른 concurrent code를 수행합니다.
3. `listPhotos(inGallery:)`이 리턴되고나면, 리턴 위치부터 다음 코드를 수행합니다. 여기서는 photoNames에 리턴 값을 할당하는 작업이 진행됩니다.
4. `sortedNames`, `name`이 포함된 라인은 `await` keyword가 없으므로 일반적인 `synchronous code`처럼 동작합니다.
5. 이후에 await이 명시된 `downloadPhoto(named:)`이 호출되고 `listPhotos(inGallery:)`와 동일한 방식으로 코드가 수행됩니다.

`await`이 의미하는 것은 지정된 코드가 실행을 일시중지할 수도 있다는 것을 의미합니다. 그리고 이 코드는 `asynchronous function`이 리턴되기까지 기다립니다. Swift 내부적으로 이 과정에서 현재 쓰레드의 작업을 일시중지하고, 다른 쓰레드의 작업을 진행하기 때문에 이는 [yielding the thread](https://en.wikipedia.org/wiki/Yield_(multithreading))를 의미하기도 합니다. 이러한 이유 때문에 `await` keyword는 특정 상황에서만 사용이 가능합니다.

- asynchronous function, method, property body 내부
- static `main()` 함수 내부(`@main`로 명시된 struct, class, enum 안)
- detached child task 코드 내부

> Note: [Task.sleep(_:)](https://developer.apple.com/documentation/swift/task/3814836-sleep)을 활용하면 asynchronous function를 쉽게 테스트할 수 있습니다.

## 3. Asynchronous Sequences

기존의 [Sequence](https://developer.apple.com/documentation/swift/sequence) Protocol을 따르면 사용할 수 있는 `for-in` 루프처럼 [AsyncSequence](https://developer.apple.com/documentation/swift/asyncsequence) Protocol을 따를 경우 `for-await-in` 루프를 사용할 수 있습니다.

```swift
import Foundation

let handle = FileHandle.standardInput
for try await line in handle.bytes.lines {
    print(line)
}
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

`for-await-in` 루프는 각각의 반복문 수행마다 `await`이 수행되고, 이는 suspension point가 되기 때문에 각 반복문의 동작은 이전 동작이 완료된 이후에 수행됩니다.

## 4. Calling Asynchronous Functions in Parallel

여러 개의 독립적인 비동기 작업은 작업의 리턴값을 받는 상수 앞에 `async` 키워드를 추가(`async let` 형태)하여 작업이 parallel하게 수행될 수 있도록 합니다. `async let` 형태로 정의된 상수는 `await`을 통해 사용할 수 있습니다.

```swift
async let firstPhoto = downloadPhoto(named: photoNames[0])
async let secondPhoto = downloadPhoto(named: photoNames[1])
async let thirdPhoto = downloadPhoto(named: photoNames[2])

let photos = await [firstPhoto, secondPhoto, thirdPhoto]
show(photos)
```
- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

위 코드에서 작업은 `photos`가 정의된 라인까지 일반적인 형태로 진행됩니다. 이 지점에서 `firstPhoto`, `secondPhoto`, `thirdPhoto`은 `await`을 만나 코드는 중단되고(다른 비동기 작업을 수행하고), `downloadPhoto(named:)`은 parallel하게 수행됩니다.

## 5. Task and Task Groups

> A task is a unit of work that can be run asynchronously as part of your program.

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

모든 비동기 코드는 항상 어떤 Task의 일부분으로서 동작합니다. 예를 들어, 앞서서 나온 `async-let`은 시스템이 사용자를 위해 Child Task를 생성하고, 이를 수행합니다. Swift는 사용자가 직접 Task Group을 만들고, 그 안에 Child Task를 추가하여 사용할 수 있도록 지원합니다.

모든 Task는 특정 Task Group 안에 포함되고, 하나의 Task Group 안 Task들은 모두 같은 Parent Task를 가지게 됩니다. 또한, Task는 Child Task를 가질 수 있습니다. 이처럼 Task와 Task Group 사이의 관계가 계층구조를 이루는 접근을 [Structured Concurrency](https://en.wikipedia.org/wiki/Structured_concurrency)이라고 부릅니다.

TaskGroup을 만들기 위해서는 [withTaskGroup(of:returning:body:)](https://developer.apple.com/documentation/swift/taskgroup) API를 사용합니다.

```swift
await withTaskGroup(of: Data.self) { taskGroup in
    let photoNames = await listPhotos(inGallery: "Summer Vacation")
    for name in photoNames {
        taskGroup.addTask { await downloadPhoto(named: name) }
    }
}
```
- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

### Unstructured Concurrency

Swift는 Task Group에 포함되지 않은 Task를 생성하는 것을 지원합니다. 이 경우, [Task.init(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856790-init)와 [Task.detached(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856786-detached)을 사용하면 새로운 Task를 top-level Task로 생성할 수 있습니다.

- Task는 동기 함수에서 비동기 함수를 호출하고자 할 때 사용합니다. 
- Task caller의 priority와 현재 actor의 context를 유지하면서 Task를 생성하고 싶은 경우에는 [Task.init(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856790-init)을 사용합니다.
- 현재 actor와 별개의 Task를 생성하고자 할 경우 [Task.detached(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856786-detached)를 사용합니다.

### Task Cancellation

Swift에서 각각의 Task는 동작 과정에서 적절한 시점에 스스로가 취소되었는지를 확인하는 작업을 수행합니다. 이 때, Task는 error를 throwing하거나 빈 collection 혹은 nil을 리턴하거나, 부분적으로 완료된 task를 리턴합니다. Task는 [Task.checkCancellation()](https://developer.apple.com/documentation/swift/task/3814826-checkcancellation)나 [Task.isCancelled](https://developer.apple.com/documentation/swift/task/3814832-iscancelled)를 통해 취소 여부를 확인할 수 있습니다.

# 참고자료

- [The Swift Programming Language (5.5) - Concurrency](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html)
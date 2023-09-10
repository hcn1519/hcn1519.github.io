---
layout: post
comments: true
title: "Swift Async Await"
excerpt: "Exploring Swift's Async/Await"
categories: Swift Language Async Await Concurrency
date: 2022-04-08 00:30:00
tags: [Swift, Language, Async, Await, Concurrency, Thread]
image:
  feature: swiftLogo.jpg
table-of-contents: |
  ### Table of Contents
  1. [Handling Asynchronous Tasks in the Past](./swift_async_await#1-handling-asynchronous-tasks-in-the-past)
  2. [Defining and Calling Asynchronous Functions](./swift_async_await#2-defining-and-calling-asynchronous-functions)
  3. [Asynchronous Sequences](./swift_async_await#3-asynchronous-sequences)
  4. [Calling Asynchronous Functions in Parallel](./swift_async_await#4-calling-asynchronous-functions-in-parallel)
  5. [Task and Task Groups](./swift_async_await#5-task-and-task-groups)
translate: true
---

In this article, we will explore Async/Await introduced in Swift 5.5.

> This content is based on [The Swift Programming Language (5.5) - Concurrency](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html).

- Using asynchronous code makes it easy to perform multiple tasks concurrently in a program.
- Asynchronous code helps reduce code complexity.

## 1. Handling Asynchronous Tasks in the Past

Using the traditional completion handler-based asynchronous code, even simple code can become complex due to the need for nested closures.

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

## 2. Defining and Calling Asynchronous Functions

A new form of function called an "asynchronous function" allows pausing during execution. While traditional "synchronous functions" either perform a completion, throw an error, or do not return, asynchronous functions can pause during execution and resume when results arrive. You can declare an asynchronous function by adding the `async` keyword at the end of the function declaration (before `->`, or before `throws` if both are used).

```swift
func listPhotos(inGallery name: String) async -> [String] {
    let result = // ... some asynchronous networking code ...
    return result
}
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

When calling an asynchronous function, the function's execution doesn't proceed beyond the function call until it returns. Inside an asynchronous function, you can use the `await` keyword to mark suspension points. The execution of an asynchronous function pauses only when there are additional asynchronous functions (with `await`) within it. All suspension points must explicitly include the `await` keyword.

```swift
let photoNames = await listPhotos(inGallery: "Summer Vacation")
let sortedNames = photoNames.sorted()
let name = sortedNames[0]
let photo = await downloadPhoto(named: name)
show(photo)
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

The execution order of the above code is as follows:

1. The code executes in the usual order until the `await` keyword is reached. It calls `listPhotos(inGallery:)`, and the program waits until that function returns.
2. While the code is paused, the program can perform other concurrent tasks.
3. After `listPhotos(inGallery:)` returns, the code resumes from the point it was paused. In this case, it assigns the return value to `photoNames`.
4. The lines containing `sortedNames` and `name` do not have `await`, so they behave like regular synchronous code.
5. Later, `downloadPhoto(named:)` is called with `await`, and the code pauses in a similar fashion to the first asynchronous call.

The `await` keyword signifies that the code can potentially pause and wait for the asynchronous function to complete. Internally, Swift suspends the current thread, allowing other threads to execute, making it similar to [yielding the thread](https://en.wikipedia.org/wiki/Yield_(multithreading)). Because of this, the `await` keyword can only be used in specific contexts:

- Inside an asynchronous function, method, or property body.
- Inside the `main()` function of a type annotated with `@main`.
- Inside detached child task code.

> Note: You can use [Task.sleep(_:)](https://developer.apple.com/documentation/swift/task/3814836-sleep) for easier testing of asynchronous functions.

## 3. Asynchronous Sequences

Similar to the traditional [Sequence](https://developer.apple.com/documentation/swift/sequence) protocol for `for-in` loops, Swift introduces the [AsyncSequence](https://developer.apple.com/documentation/swift/asyncsequence) protocol. This allows you to use a `for-await-in` loop with asynchronous sequences.

```swift
import Foundation

let handle = FileHandle.standardInput
for try await line in handle.bytes.lines {
    print(line)
}
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

In a `for-await-in` loop, `await` is executed at each iteration, and each iteration's execution waits for the previous one to complete due to the suspension point.

## 4. Calling Asynchronous Functions in Parallel

Multiple independent asynchronous tasks can run concurrently by adding the `async` keyword before a constant that will hold the task's return value (`async let` form). Constants defined in this manner can be used with `await`.

```swift
async let firstPhoto = downloadPhoto(named: photoNames[0])
async let secondPhoto = downloadPhoto(named: photoNames[1])
async let thirdPhoto = downloadPhoto(named: photoNames[2])

let photos = await [firstPhoto, secondPhoto, thirdPhoto]
show(photos)
```

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

In the above code, execution proceeds normally until the line where `photos` is defined. At this point, the `await` keyword is encountered, and the code pauses. Meanwhile, the `downloadPhoto(named:)` calls are performed in parallel.

## 5. Task and Task Groups

> A task is a unit of work that can be run asynchronously as part of your program.

- [The Swift Programming Language (Swift 5.5) Apple Inc.](https://books.apple.com/kr/book/the-swift-programming-language-swift-5-5/id881256329)

All asynchronous code always runs as part of a Task. For example, the

 `async-let` constructs create child tasks for user convenience. Swift allows users to create their own Task Groups, add child tasks to them, and use them to manage concurrency effectively.

All tasks are part of a Task Group, and all tasks within a Task Group share the same parent task. Tasks can also have child tasks. This hierarchical relationship between tasks and Task Groups is referred to as [Structured Concurrency](https://en.wikipedia.org/wiki/Structured_concurrency).

To create a Task Group, you can use the [withTaskGroup(of:returning:body:)](https://developer.apple.com/documentation/swift/taskgroup) API.

```swift
await withTaskGroup(of: Data.self) { taskGroup in
    let photoNames = await listPhotos(inGallery: "Summer Vacation")
    for name in photoNames {
        taskGroup.addTask { await downloadPhoto(named: name) }
    }
}
```

### Unstructured Concurrency

Swift also supports creating tasks that are not part of a Task Group. In this case, you can use [Task.init(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856790-init) and [Task.detached(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856786-detached) to create a new Task as a top-level Task.

- Tasks are used when you want to call asynchronous functions from synchronous code.
- When you want to create a Task with the caller's priority and the current actor's context, use [Task.init(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856790-init).
- When you want to create a Task that is separate from the current actor, use [Task.detached(priority:operation:)](https://developer.apple.com/documentation/swift/task/3856786-detached).

### Task Cancellation

Each Task in Swift checks whether it has been canceled at appropriate points during its execution. A canceled Task can either throw an error, return an empty collection or nil, or return a partially completed task. You can check for cancellation using [Task.checkCancellation()](https://developer.apple.com/documentation/swift/task/3814826-checkcancellation) or [Task.isCancelled](https://developer.apple.com/documentation/swift/task/3814832-iscancelled).


## References

- [The Swift Programming Language (5.5) - Concurrency](https://docs.swift.org/swift-book/LanguageGuide/Concurrency.html)
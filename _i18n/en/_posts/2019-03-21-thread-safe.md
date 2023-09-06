---
layout: post
title: "Thread Safe"
date: "2019-03-21 00:10:45 +0900"
excerpt: "Exploring Thread Safety."
categories: Swift ThreadSafe atomic OS Thread Language
tags: [Swift, ThreadSafe, atomic, OS, Thread]
image:
  feature: blogThumb-noRadius.png
table-of-contents: |
  ### Table of Contents
  1. [Thread Safe Concept](./thread-safe#thread-safe-concept)
  2. [Examples of Thread Safety](./thread-safe#examples-of-thread-safety)
  3. [Achieving Thread Safety](./thread-safe#achieving-thread-safety)
  4. [Swift and Thread Safety](./thread-safe#swift-and-thread-safety)
---

Determining whether something is Thread Safe is one of the essential aspects to understand when writing code in a multi-threaded environment. In this post, we will explore what Thread Safety is and how to assess it.

## Thread Safe Concept

Thread Safety is elaborated in detail in the following article: [Thread Safety - MIT](http://web.mit.edu/6.005/www/fa15/classes/20-thread-safety). The content below is an excerpt and summary of that article. The original article defines Thread Safety as follows:

> A data type or static method is threadsafe if it behaves correctly when used from multiple threads, regardless of how those threads are executed, and without demanding additional coordination from the calling code.

In summary, for a data type or static method to be considered Thread Safe, it must satisfy the following conditions:

1. It must function correctly regardless of the actions of multiple threads.
2. It does not require additional conditions during its invocation.

The article also adds the following explanations:

* "Behaving correctly" means satisfying the specifications and maintaining the object's representation invariance.
* "Without demanding additional coordination" means that the data type does not impose additional conditions on the caller related to timing.

"Representation invariance" refers to something that remains constant in a class. For example, when rolling a die, the result is always a number between 1 and 6. Rolling a single die cannot produce a result outside this range. In this context, the `Dice🎲` class's `throwDice()` method can be considered to maintain the `Dice🎲` class's representation invariance. The absence of additional conditions related to timing during invocation means that the data type cannot specify preconditions for the caller regarding timing.

## Examples of Thread Safety

### 1. Swift Class Instance

Creating instances of reference types involves memory allocation after deallocation (`alloc`). However, in a multi-threaded environment, the `alloc`/`dealloc` information of reference type instances is not shared across threads.

```swift
class Bird {}
var single = Bird()

DispatchQueue.global().async {
    while true { single = Bird() }
}

while true { single = Bird() }
// error - malloc: Double free of object 0x102887200
```

The above code quickly crashes when executed. This crash occurs because in a multi-threaded environment, Thread A does not have knowledge of Thread B's instance deallocation information.

Although Swift's class instance's reference count is updated atomically, ensuring that other threads do not access the instance during its creation or destruction, it does not guarantee Thread Safety during instance creation. In other words, before and after the instance creation, other threads can still access the instance. In this case, other threads do not have knowledge of `alloc`/`dealloc` information, making instance creation and destruction not Thread Safe.

### 2. File Read/Write

Considering the Thread Safety of reading and writing data to a file involves thinking about timing issues. The content of a file changes based on the order of `read()` and `write()` operations. Specifically:

* `read()` followed by `write()`
* `write()` followed by `read()`
* `read()` during `write()`
* `write()` during `read()`

In these cases, the result is not guaranteed to be the same. Therefore, file read/write operations are not Thread Safe. The key factor making it not Thread Safe is that the file's content is mutable. If the file's data were immutable (i.e., if `write()` were not possible), timing issues would be resolved.

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
// The desired result is "1a 2a 3a ... 100a 1b 2b 3b ... 100b"
/* Example result - The result may vary with each code execution.
result 1a 2a 3a 4a 5a 6a 7a 8a 9a 10a 11a 12a 13a 14a 15a 16a 15b 16b 17b 18b 19b 20b
21b 22b 23b 24b 25b 26b 27b 28b 29b 30b 31b 32b 33b 34b 36a 37a 38a 39a 40a
41a 42a 43a 44a 45a 46a 47a 48a 49a 48b 49b 50b 51b 52b 54a 55a 56a 57a 58a 59a 60a
61a 62a 63a 64a 65a 65b 66b 67b 68b 69b 70a 71a 72a 73a 73b 74b 75b 76b 77a 78a 79a 80a
81a 82a 83a 84a 85a 86a 87a 88a 89a 89b

 90b 91b 92a 93a 94a 95a 96a 97a 98a 99a 100a 100b
*/
```

## Achieving Thread Safety

To achieve Thread Safety, several proposed methods are commonly used. Below are some of the methods proposed to achieve Thread Safety:

1. Mutual Exclusion - Use locks or semaphores to ensure that only one thread accesses shared resources.
2. Thread Local Storage - Create storage accessible only to specific threads.
3. Reentrancy - Write code in such a way that it can be executed in the same thread or concurrently in different threads, providing consistent results. This can be achieved by storing local state when a thread enters and using it atomically.
4. Atomic Operation - Ensure that data changes occur atomically when multiple threads access it. (See [atomic/non-atomic](https://hcn1519.github.io/en/articles/2019-03/atomic) for reference.)
5. Immutable Object - Make objects immutable after creation to prevent changes.

Source: [Wikipedia - Thread Safety](https://en.wikipedia.org/wiki/Thread_safety)

## Swift and Thread Safety

The following information is based on [swift doc - Concurrency.rst](https://github.com/apple/swift/blob/master/docs/proposals/Concurrency.rst). Please note that the document mentions that this is a not accepted proposal, referring to the rejection of the async-await feature, not the analysis of Swift's Thread Safety.

In general, Thread Safety arises when shared mutable memory exists. Therefore, Swift has mechanisms in place to prevent sharing memory between threads.

### 1. Copyable Protocol

The "Copyable Protocol" specifies that certain types can be safely copied on a per-thread basis. Types like `Int`, `Float`, and `Double`, which do not contain references, follow the Copyable Protocol. Even types like `String` and `Array`, which do contain references but are constructed as value types, allow copying on a per-thread basis.

### 2. Reentrant Code

"Reentrant code" refers to code that can only be accessed through given arguments, making it inaccessible to global variables and shared resources. Swift allows code to be written in such a way that it can only access logically copied data in a single thread. When accessing global variables or unsafe data, the Swift compiler enforces these restrictions. (Consider using `self` explicitly when using DispatchQueue to change queues.)

### 3. Gateway Annotation

Swift always creates new threads to execute functions, thanks to annotations that specify thread creation. In other words, Swift has a Thread Verifier that checks whether Copyable Protocol and Reentrant code conditions are met during the compilation process.

```swift
@_semantics("swift.concurrent.launch")
public func createTask<ArgsTy>(args : ArgsTy, callback : (ArgsTy) -> Void) {
  ...
}
```

## References

* [What is this thing you call "thread safe"?](https://blogs.msdn.microsoft.com/ericlippert/2009/10/19/what-is-this-thing-you-call-thread-safe/)
* [swift doc - Concurrency.rst](https://github.com/apple/swift/blob/master/docs/proposals/Concurrency.rst)
* [Wikipedia - Race Condition](https://ko.wikipedia.org/wiki/경쟁_상태)
* [Wikipedia - Thread Safety](https://en.wikipedia.org/wiki/Thread_safety)
* [What does the term rep-invariant and rep ok means?](https://stackoverflow.com/questions/7578086/what-does-the-term-rep-invariant-and-rep-ok-means)
---
layout: post
comments: true
title: "Understanding Escaping Closures in Swift"
excerpt: "Exploring the concept of escaping closures in Swift."
categories: Swift Closure, Escaping Closure Language Networking
date: 2017-09-12 00:30:00
tags: [Swift, Closure, EscapingClosure, Language, Networking]
image:
  feature: swiftLogo.jpg
table-of-contents: |
  ### Table of Contents
  1. [Concept of Escaping Closures](./swift_escaping_closure#1-concept-of-escaping-closures)
  1. [Storing Closures Outside Functions](./swift_escaping_closure#2-storing-closures-outside-functions)
  1. [Async Inside Async](./swift_escaping_closure#3-async-inside-async)

---

## 1. Concept of Escaping Closures

This article assumes a basic understanding of closures. If you are not familiar with closures, please read the [Swift Closure](https://hcn1519.github.io/en/articles/2017-05/swift_closure) article first before continuing.

<div class="message">
  A closure is said to escape a function when the closure is passed as an argument to the function, but is called after the function returns.
</div>

When a closure is said to "escape" a function, it means that the closure is passed as an argument to the function but is executed after the function has returned. This concept of closures escaping the scope of a function challenges the traditional understanding of variable scope. It allows a closure to persist beyond the lifetime of the enclosing function, which is different from the usual scope rules for local variables. In other words, escaping closures can be executed outside the function that originally defined them.

While the idea of a local variable (typically values like `Int`, `String`, etc.) surviving outside a function might seem similar to using global variables within a function, escaping closures offer more control over the execution order of functions.

> Escaping closures are useful for defining the execution order between functions, even allowing one function to run only after another has completed.

Ensuring the order of execution of functions is crucial, especially when dealing with asynchronous operations. Consider an app that retrieves JSON data from a server to display it on the screen. In this scenario, a networking library like `Alamofire` is often used in the following manner:

{% highlight swift %}
Alamofire.request(urlRequest).responseJSON { response in
  // Handle the response
}
{% endhighlight %}

The `Alamofire.request(urlRequest)` method sends a request to the server, typically to retrieve JSON data using the GET method. The result is obtained through a `Response` object. Usually, functions that send requests to a server and receive responses work asynchronously, returning immediately after sending the request. How is it possible to ensure that the response is received and processed in a way that guarantees proper sequencing? The answer lies in the concept of escaping closures. The `completionHandler` parameter in the `responseJSON` method is implemented as an escaping closure, indicated by the `{ response in }` part.

<div class="message">
  Using escaping closures, closure arguments can outlive the function that they were passed to. Starting from Swift 3, by default, closures passed as function arguments are not allowed to escape the function’s scope. This means that by default, you cannot store closures in external storage or execute them on other threads using GCD. However, escaping closures make these use cases possible, and you can mark a closure type with the `@escaping` keyword to indicate that it's an escaping closure.
</div>

Now, let's explore some code examples to understand how escaping closures work.

## 2. Storing Closures Outside Functions

{% highlight swift %}
// Example of storing a closure outside a function
// An array to store closures
var completionHandlers: [() -> Void] = []

func withEscaping(completion: @escaping () -> Void) {
    // Store the closure outside the function in the completionHandlers array
    completionHandlers.append(completion)
}

func withoutEscaping(completion: () -> Void) {
    completion()
}

class MyClass {
    var x = 10
    func callFunc() {
        withEscaping { self.x = 100 }
        withoutEscaping { x = 200 }
    }
}
let mc = MyClass()
mc.callFunc()
print(mc.x)
completionHandlers.first?()
print(mc.x)

// Output
// 200
// 100
{% endhighlight %}

In this example, the `MyClass` function `callFunc()` calls two functions, `withEscaping(completion:)` and `withoutEscaping(completion:)`. The `withEscaping(completion:)` function takes a closure parameter marked as an escaping closure using the `@escaping` keyword. In this function, we store the closure in the `completionHandlers` array outside the function's scope. This means that the closure escapes the function and can be executed at a later time.

<div class="message">
  Note: In this context, escaping does not mean that the closure interrupts and escapes the function's execution midway. Instead, it means that the closure can be passed outside the function and executed later.
</div>

## 3. Async Inside Async

As mentioned earlier, escaping closures are commonly used in asynchronous operations, especially in networking code with `completionHandlers`. To demonstrate this, let's consider a scenario where you need to retrieve data from a server using a `Server` class and update the UI once the data is received. To manage this, you might want to create a class with static methods for handling server requests.

{% highlight swift %}
class Server {
  static var persons: [Person] = []

  static getPerson(completion: @escaping (Bool, [Person]) -> Void) {
      // Step 2
      Alamofire.request(urlRequest).responseJSON { response in
          persons.append(data) // Replace 'data' with actual data
          DispatchQueue.main.async {
              // Step 3
              completion(true, persons)
          }
      }
  }
}
// Usage, e.g., in ViewController.swift
// Step 1
Server.getPerson { (isSuccess, persons) in
  // Step 4
  if isSuccess {
      // Update the UI
  }
}
{% endhighlight %}

Here's the sequence of how the code works:

1. In `ViewController`, you call the `Server` class's `getPerson(completion:)` function to request the necessary data.
2. Inside the `getPerson(completion:)` function, `Alamofire` sends a request to the server, and the `{ response in }` part of `responseJSON` is executed only after the request has completed. This part uses an escaping closure.
3. The `completion` closure, which is also an escaping closure, is called in order to send the data (persons) back to the original ViewController. It's important to perform UI updates on the main thread, so we use `DispatchQueue.main.async` to ensure this.
4. Finally, the `completion` closure in `ViewController` is executed. Here, you can check if the data retrieval was successful and update the UI accordingly.

## References

* Apple Inc. The Swift Programming Language (Swift 3.1) - Escaping Closure
* [escaping closure swift3](https://learnappmaking.com/escaping-closures-swift-3/)
* [What do

 mean @escaping and @nonescaping closures in Swift?](https://medium.com/@kumarpramod017/what-do-mean-escaping-and-nonescaping-closures-in-swift-d404d721f39d)
* [Completion handlers in Swift 3.0](https://stackoverflow.com/questions/41745328/completion-handlers-in-swift-3-0)

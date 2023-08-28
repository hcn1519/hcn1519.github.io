---
layout: post
comments: true
title: "Swift Closure"
excerpt: "Exploring Swift closures, known as anonymous functions."
categories: Swift Closure Language
date: 2017-05-08 00:30:00
tags: [Swift, Language, Closure]
image:
  feature: swiftLogo.jpg
---

Closures in Swift, also known as anonymous functions, differ from regular functions. Instead of being declared with the `func` keyword, they take the form of declaring functions as variables. Closures are a powerful feature that aids in writing concise and intuitive code. Let's explore closures by highlighting the differences in how they are used compared to regular functions.

#### Using Regular Functions

```swift
var counter = 0

func addCounter() {
  counter += 1
}

addCounter()
addCounter()

print(counter) // Result: 2
```

Regular functions are declared with a function name (`addCounter` in this case), and you call the function by using that name.

#### Using Closures

```swift
var counter = 0

let addCounter = {
    counter += 1
}

addCounter()
addCounter()

print(counter) // Result: 2
```

Closures, on the other hand, declare functions as variables. In this case, the `addCounter` variable is assigned a function, and you can call it like a function (`addCounter()`).

## Basic Structure of a Closure

Closures in Swift have a basic structure consisting of a **header** and a **body**:

```swift
var closure = { header in body }
```

In the header, you specify the arguments and return type, and in the body, you write the code that gets executed when the closure is called. The `in` keyword separates the header from the body.

![Closure Expression](<URL TO IMAGE>)

The official Swift documentation by Apple explains closures using the `sorted(by:)` method. The `sorted(by:)` method is a built-in Swift method used to sort an array based on a specified criterion. It relies on the comparison of elements in the array to determine their order. In other words, it repeatedly compares two values in the array, returning `true` if the first value should come before the second (ascending order) or `false` otherwise.

```swift
let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
let numbers = [4, 3, 2, 6, 1]

// The required argument depends on the data type within the array.
names.sorted(by: (String, String) -> Bool)
numbers.sorted(by: (Int, Int) -> Bool)
```

In this context, the `by` parameter of `sorted(by:)` expects a function or closure that returns a `Bool`. This means you can pass either a regular function or a closure as an argument. Here are examples of both:

```swift
let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]

// A function that returns true if s1 should come before s2.
func backward(_ s1: String, _ s2: String) -> Bool {
    return s1 > s2
}

var reversedNames = names.sorted(by: backward)

var reverse2 = names.sorted(by: { (s1: String, s2: String) -> Bool in return s1 < s2 })
```

In the above examples, `reversedNames` is sorted using a regular function (`backward`), while `reverse2` is sorted using a closure.

## Closure Shortening

One of the significant advantages of closures is their ability to write concise and intuitive code. However, understanding when and how to shorten closures is essential. Here, we'll explore scenarios where you can shorten closure expressions.

#### 1. Type Inference

Closures can infer the types of their parameters and the return type if that information is already known. This allows you to omit explicit type declarations.

```swift
names.sorted(by: { (s1: String, s2: String) -> Bool in return s1 < s2 })

// Omitting data types
names.sorted(by: { (s1, s2) in return s1 < s2 })
```

For instance, in the `sorted(by:)` method, the closure is always expected to take two arguments of the same type as the elements in the array and return a `Bool`. Since this information is known, you can omit the data type declarations.

#### 2. Omitting the "return" Keyword in Single Expression Closures

Single expression closures can omit the `return` keyword.

```swift
// Omitting the "return" keyword
names.sorted(by: { (s1, s2) in s1 < s2 })
var multiply: (Int, Int) -> Int = { (a, b) a * b }
```

In single expression closures, where the body contains only one expression, you can omit the `return` keyword.

#### 3. Short-hand Argument Names

Closures provide short-hand argument names that can be used instead of explicit parameter names.

```swift
// Using short-hand argument names
names.sorted(by: { $0 < $1 })
var multiply: (Int, Int) -> Int = { $0 * $1 }
```

You can use `$0`, `$1`, and so on to refer to the closure's arguments in the order they appear.

#### 4. Operator Methods for Shortening

Operator methods can further shorten closures, especially when they involve simple operations.

```swift
names.sorted(by: <)
var multiply: (Int, Int) -> Int = (*)
```

In the case of `sorted(by:)`, it always expects a closure that compares two values and returns a `Bool`. Similarly, the `multiply` closure, which multiplies two values, can be expressed concisely using the `*` operator.

## Passing Closures as Function Arguments

Just as you can pass variables as arguments to functions, you can also pass closures to functions. The syntax is similar to passing variables, following the `func functionName(label variableName: variableType)` pattern.

```swift
var hello: () -> Void = { print("Hello~") }

func runClosure(name aClosure: () -> Void) {
    aClosure()
}

runClosure(name: hello) // Hello~
```

#### Utilizing Trailing Closures for Syntax Sugar

Trailing closures are a syntax sugar that allows you to separate a closure from the function call when it becomes excessively long. You can use the trailing closure syntax to make your code more readable.

```swift
// Passing arguments
runClosure(name: hello) // Hello~
runClosure(name: { print("another closure") })

runClosure() {
  // Executes when aClosure() is called
  print("trailing1")
}

// If there are no other arguments, you can omit the parentheses.
runClosure {
  print("trailing2")
}
```

Trailing closures can be especially useful when you have multiple arguments in a function call.

```swift
func runClosure2(index: Int, name aClosure: () -> Void) {
  aClosure()
}
runClosure2(index: 2) {
    // Passes index as 2 and executes when aClosure() is called


    print("hi")
}
```

Trailing closures are commonly used in libraries like Alamofire for completion handlers.

```swift
// Passing arguments
Alamofire.request(URL).responseJSON(completionHandler: { response in
  // Handle the response
  completed()
})

// Utilizing trailing closures
Alamofire.request(URL).responseJSON { response in
  // Handle the response
  completed()
})
```

#### Using the Map Method

One of the most common uses of trailing closures is with the `map(_:)` method. The `map(_:)` method is used to modify all or some of the elements in a collection. It's like a loop, but with a strong focus on mapping values to new values.

```swift
var numbers = [4, 3, 2, 6, 1]

numbers = numbers.map { (value) -> Int in
  let newValue = value + 1
  return newValue
}
```

In the example above, the `numbers` array is modified by mapping each value to a new value (the original value plus one). The return type remains the same as the original. However, you can have a different return type if needed. You can also map collections to dictionaries or vice versa.

```swift
let digitNames = [
    0: "Zero", 1: "One", 2: "Two",   3: "Three", 4: "Four",
    5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"
]

let oddOrEvenArr = digitNames.map { (key, value) -> String in
    var str = ""
    if key % 2 == 0 {
      str = "Even"
    } else {
      str = "Odd"
    }
    return str
}
// oddOrEvenArr = ["Even", "Odd", ...] (Order may vary.)

let oddOrEvenDict = digitNames.map { (key, value) -> [Int: String] in
    var str = ""
    if key % 2 == 0 {
      str = "Even"
    } else {
      str = "Odd"
    }
    return [key: str]
}
// oddOrEvenDict = [0: "Even", 1: "Odd", ...] (Order may vary.)
```

In the above examples, `oddOrEvenArr` and `oddOrEvenDict` are created by mapping the `digitNames` dictionary into arrays and dictionaries, respectively.

---

## References
- Apple Inc. The Swift Programming Language (Swift 3.1)
- Raywenderlich - Closure
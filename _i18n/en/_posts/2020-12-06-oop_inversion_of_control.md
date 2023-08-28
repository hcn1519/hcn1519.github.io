---
layout: post
title: "Inversion Of Control"
date: "2020-12-06 00:53:17 +0900"
excerpt: "Exploring Inversion of Control."
categories: IoC, OOP, ControlFlow, Dependency
tags: [IoC, OOP, ControlFlow, Dependency]
image:
  feature: OOP.png
---

`Inversion of Control` (IoC) refers to a phenomenon where the flow of control is **inverted**, as the name suggests. To understand what it means for control flow to be inverted, it's necessary to first understand what control flow without inversion is. Therefore, in this article, we will first examine what non-inverted control flow is and then explore `Inversion of Control`.

## Table of Contents

1. [Control Flow](./oop_inversion_of_control#1-control-flow)
2. [Inversion of Control](./oop_inversion_of_control#2-inversion-of-control)
3. [Module Extension Through IoC](./oop_inversion_of_control#3-module-extension-through-ioc)
4. [Libraries and Frameworks from a Control Perspective](./oop_inversion_of_control#4-libraries-and-frameworks-from-a-control-perspective)

### 1. Control Flow

[Control flow](https://en.wikipedia.org/wiki/Control_flow) refers to the sequence or flow in which code is executed by a system. Typically, source code executes with code at the top running first and code at the bottom running later. Conditional and loop statements are often used to control the behavior in various situations. Let's look at a simple example:

> The example used here is a slightly modified version of the one from [InversionOfControl - Martin Fowler](https://martinfowler.com/bliki/InversionOfControl.html).

```swift
class ScreenPresenter {
    var name: String = ""
    var quest: String = ""

    func displayName() {
        print("Display User Input:", name)
    }

    func displayQuest() {
        print("Display User Input:", name)
    }
}

class User {
    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.name = "Hong"
        presenter.displayName()
        presenter.quest = "Do Something"
        presenter.displayQuest()
    }
}
```

The execution order of the above code is as follows:

1. Create `ScreenPresenter`.
2. Set the `name` property of `ScreenPresenter`.
3. Call `displayName()` to print the `name`.
4. Set the `quest` property of `ScreenPresenter`.
5. Call `displayQuest()` to print the `quest`.

While the sequence is described somewhat verbosely, the flow is intuitively understandable. In this flow, the developer controls when `displayName()` and `displayQuest()` are called, and the system executes the commands accordingly.

The key feature of control flow is that the developer-written code has control over the system's behavior. In other words, in the example above, the developer decides when to call `displayName()` and `displayQuest()`, and the system follows these commands.

### 2. Inversion of Control

Inversion of Control (`IoC`) refers to a phenomenon where the entity in control is inverted. As mentioned earlier, in control flow, the control over system behavior lies with the developer. IoC is the opposite; it means that control is shifted towards the system's side.

Let's look at an alternative implementation of the code we discussed earlier:

```swift
class ScreenPresenter {
    var name: String = "" {
        didSet {
            didFinishWritingName?(name)
        }
    }

    var quest: String = "" {
        didSet {
            didFinishWritingQuest?(quest)
        }
    }

    var didFinishWritingName: ((String) -> Void)?
    var didFinishWritingQuest: ((String) -> Void)?
}

class User {
    func display(value: String) {
        print("Display User Input:", value)
    }

    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.didFinishWritingName = { nameInput in
            display(value: nameInput)
        }
        presenter.didFinishWritingQuest = { questInput in
            display(value: questInput)
        }
        presenter.name = "Hong"
        presenter.quest = "Do Something"
    }
}
```

The execution order of the above code is as follows:

1. Create `ScreenPresenter`.
2. Configure `displayName()` to be called when `name` is set.
3. Configure `displayQuest()` to be called when `quest` is set.
4. Set the `name` property of `ScreenPresenter`.
5. Set the `quest` property of `ScreenPresenter`.

The key difference between this code and the previous examples is who calls the `display()` function. In the earlier examples, the developer directly called it, while in this example, the system calls it. In other words, there's an inversion (a reversal) of control.

> IoC is sometimes also referred to as the Hollywood Principle: "Don't call us; we'll call you."

### 3. Module Extension Through IoC

Even by examining just these two examples, it's evident that code with inverted control flow is relatively more complex than non-inverted code. This complexity arises because to invert control flow, mechanisms for delegating control have been introduced. These mechanisms are often referred to as delegates, and in the example above, closures/callbacks were used. Despite the added complexity, IoC is intentionally employed because it allows modules to be extended flexibly.

By using IoC, you can extend the functionality of a module without changing the module itself. Let's consider adding a feature that reloads the screen after calling `display(value:)` following user input. In the first example, you can add the following code:

```swift
class ScreenPresenter {
    var name: String = ""

    func displayName() {
        print("Display User Input:", name)
    }
    
    func reloadScreenForName() {
        print("Reload Screen")
    }
}

class User {
    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.name = "Hong"
        presenter.displayName()
        presenter.reloadScreenForName()
    }
}
```

In the second example, you can handle it like this:

```swift
class ScreenPresenter {
    var name: String = "" {
        didSet {
            didFinishWritingName?(name)
        }
    }
    var didFinishWritingName: ((String) -> Void)?
}

class User {
    func display(value: String) {
        print("Display User Input:", value)
    }

    func reload(value: String) {
        print("Reload Screen")
    }

    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.didFinishWritingName = { nameInput in
            display(value: nameInput)
            reload(value: nameInput)
        }
        presenter.name = "Hong"
    }
}
```

The significant difference between the two examples lies in **where you made changes in the source code**. In the first example, you added functionality to `ScreenPresenter`, which would require recompilation of that module. In the second example, you modified the code of the user of `ScreenPresenter`, and there was no need to recompile the `ScreenPresenter` module. 

This feature of preventing recompilation of a module through IoC allows the module to remain

 unconcerned with the user's code and allows users to extend the module's functionality as needed. The module only needs to provide the appropriate interfaces for the user.

### 4. Libraries and Frameworks from a Control Perspective

In terms of binary perspective, libraries and frameworks are often used interchangeably, with little difference. However, from a control perspective, these two terms are clearly distinguished:

- Library - In an application using a library, the application calls functions or creates classes from the library. The control resides with the application.
- Framework - In an application using a framework, the application must call methods according to the interfaces provided by the framework or perform sub-classing, among other requirements. The control resides with the framework.

When using `UIKit`'s `UIViewController`, for instance, users write code in line with the lifecycle of `UIViewController`. In this case, users don't directly call the lifecycle methods of `UIViewController`. Instead, upon creating an instance, the system directly calls these methods. From a control perspective, `UIKit` can be seen as a framework.

> In Apple's development ecosystem, libraries and frameworks are sometimes distinguished based on resource inclusion. For more details, you can refer to [Understanding Frameworks](https://hcn1519.github.io/articles/2019-11/framework_basic).

# References

- [InversionOfControl - Martin Fowler](https://martinfowler.com/bliki/InversionOfControl.html)
- [InversionOfControl - Just hack'em](https://justhackem.wordpress.com/2016/05/14/inversion-of-control/)
- [PlugIn - David Rice and Matt Foemmel](https://martinfowler.com/eaaCatalog/plugin.html)
- [ControlFlow - Wikipedia](https://en.wikipedia.org/wiki/Control_flow)
- [Inversion Of Control - Wikipedia](https://en.wikipedia.org/wiki/Inversion_of_control)
- [Clean Architecture - Robert C. Martin](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
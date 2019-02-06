---
layout: post
title: "Swift init 기본"
date: "2019-02-05 23:10:45 +0900"
excerpt: "Swift의 객체 초기화 방식에 대해 알아 봅니다."
categories: Swift init Language
tags: [Swift, init, Language]
image:
  feature: swiftLogo.jpg
---

## Basic

생성자(initializer, constructor)는 객체를 생성하는 메소드를 지칭합니다. 객체는 일반적으로 클래스를 통해 추상화된 형태로 description을 작성합니다. 그리고 클래스를 실제로 사용하기 위해서는 실제 메모리에 올라가는 객체의 인스턴스를 만들어야 합니다. 이 때, 객체의 인스턴스를 만드는 메소드가 생성자입니다. 다만, Swift에서는 클래스뿐만 아니라, struct에 대해서도 생성자를 지원합니다.

Swift에서 생성자는 `init()` 형태로 작성되며, 필요하면 argument를 추가해서 작성할 수도 있습니다.

```swift
class Car {
    let brand: String

    init(brand: String) {
        self.brand = brand
    }
}
```

생성자 메소드는 작성할 때 몇 가지 조건이 있습니다. 그 조건을 살펴보면 다음 같은 것들이 있습니다.

1. 생성자가 메소드가 끝나는 시점에서 객체의 모든 `stored properties`에는 값이 존재해야 합니다.
    * 옵셔널 값은 특별히 값을 지정하지 않아도 nil이 기본으로 들어갑니다.
    * property에 default value가 지정되어 있으면 `stored property`에 특별한 값을 지정하지 않아도 됩니다.

2. Constant property(let으로 선언된 property)는 생성자에서만 그 값을 설정할 수 있습니다.

3. struct는 생성자를 특별히 작성하지 않아도, `memberwise initializer`를 제공합니다. 다만, init 메소드를 별도로 작성하게 되면 `memberwise initializer`는 사용할 수 없게 됩니다.(extension 안에 생성자를 쓰면 memberwise initializer를 그대로 사용할 수 있습니다.)

```swift
struct Car {
    let brand: String
    let price: Int
}

// 별도로 작성하지 않아도 memberwise initializer가 제공됩니다.
let car = Car(brand: "BMW", price: 10000)
```

## Initializer Delegation

`Initializer Delegation`의 개념은 `Initializer`가 다른 `Initializer`를 호출하여 인스턴스 생성을 완료하는 것을 의미합니다. `Initializer Delegation`은 struct와 class인지 여부에 따라 적용되는 부분이 다르고, struct가 class에 비해 상대적으로 더 간단합니다.

### Struct

struct가 class에 비해 `Initializer Delegation`이 간단한 이유는 struct는 상속이 되지 않기 때문입니다. struct는 delegation용으로 `self.init()` 형태의 initializer만 호출합니다. 아래는 이에 대한 예시입니다.

```swift
struct Car {
    let brand: String
    let price: Int

    init() {
        // initializer delegation
        self.init(brand: "BMW", price: 10000)
    }

    init(brand: String, price: Int) {
        self.brand = brand
        self.price = price
    }
}

// brand: BMW, price :10000
let car = Car()
```

앞서서 생성자는 반드시 모든 `stored properties`들에 대한 값을 설정해주어야 한다고 서술하였습니다. 그런데 위의 예시에서는 `init()` 메소드는 `stored properties`의 값을 `self.init(brand: "BMW", price: 10000)` 호출을 통해 설정합니다. 즉, 이는 **초기화의 과정을 자신이 직접하는 것이 아니라, 일부(여기서는 전부) 다른 메소드가 수행하도록 위임한다(delegate)**고 할 수 있습니다.

### Class

#### designated initializer, convenience initializer

class의 initialize delegation을 얘기하기 위해서는 우선적으로 `designated initializer`와 `convenience initializer`에 대한 이해가 필요합니다. `designated initializer`와 `convenience initializer`를 구분하는 가장 쉬운 방법은 `convenience` 키워드의 유무입니다. `designated initializer`는 반드시 1개는 있어야 하고,(default initalizer가 이를 대신할 수 있습니다.) `convenience initializer`는 말 그대로 `designated initializer`보다 좀 더 작성 조건이 유연하여 편리하게 쓰려고 만드는 메소드입니다.

> Designated initializers are the primary initializers for a class. A designated initializer fully initializes all properties introduced by that class and calls an appropriate superclass initializer to continue the initialization process up the superclass chain.

> Convenience initializers are secondary, supporting initializers for a class. You can define a convenience initializer to call a designated initializer from the same class as the convenience initializer with some of the designated initializer’s parameters set to default values. You can also define a convenience initializer to create an instance of that class for a specific use case or input value type

#### Class initialize delegation

class의 initialize delegation은 상속을 고려해야 하기 때문에 struct에 비해 복잡합니다. 기본 rule에 대해 살펴보면 다음과 같습니다.

* Rule 1 - `designated initializer`는 `superClass`의 `designated initialzer`를 반드시 호출해야 한다.
* Rule 2 - `convenience initializer`는 동일 클래스의 initializer를 호출해야 한다.
* Rule 3 - `convenience initializer`는 반드시 `designated initialzer`를 호출해야 한다.

다음의 Rule에 대해 설명하는 예시를 살펴보겠습니다.

```swift
class Device {
    var icon: String

    init() {
        self.icon = "no icon"
    }
}

class Watch: Device {

    var price: Int

    override init() {
        // delegate up
        self.price = 0
        // Rule 1
        super.init()
    }

    convenience init(price: Int) {
        // delegate across
        // Rule 2, 3
        self.init()
        self.price = price
    }

    convenience init(foo: String, bar: Int) {
        // Rule 2, 3
        self.init(price: 100)
    }
}
```

* `Watch`는 `Device`를 상속하고 있습니다. 그래서 `Watch`의 `designated initializer`인 `init()`은 `super.init()`을 호출하고 있습니다.(Rule 1)
* `Watch`의 `convenience initializer` 중 `convenience init(price: Int)`은 `Watch`의 `designated initializer`인 `init()`을 호출하고 있습니다.(Rule 2, 3)
* `Watch`의 `convenience initializer` 중 `convenience init(foo: String, bar: Int)`은 동일 클래스의 initializer를 호출하고 있습니다.(Rule 2) 다만, 직접적으로 `designated initializer`을 호출하고 있지는 않습니다. 하지만, `convenience init(price: Int)`을 호출하여 결론적으로는 `designated initializer`도 호출합니다.(Rule 3)

---

# 참고자료

* [The Swift Programming Language (Swift 4.2)](https://itunes.apple.com/kr/book/the-swift-programming-language-swift-4-2/id881256329?mt=11)
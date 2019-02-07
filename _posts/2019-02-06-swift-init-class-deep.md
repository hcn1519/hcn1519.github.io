---
layout: post
title: "Swift init 2부"
date: "2019-02-06 23:10:45 +0900"
excerpt: "Swift의 Class 초기화 과정에서 일어나는 일에 대해 살펴 봅니다."
categories: Swift init Language
tags: [Swift, init, Language]
image:
  feature: swiftLogo.jpg
---

Swift의 객체 초기화 과정은 앞서서 언급한 것처럼 class의 경우에서 복잡해집니다. 여기서는 Swift의 class init의 과정에 대해 좀 더 살펴보겠습니다. 이전 글인 [Swift init 1부](https://hcn1519.github.io/articles/2019-02/swift-init-basic)를 미리 살펴보면 더 좋습니다.

* [1. Two Phase Initialization](https://hcn1519.github.io/articles/2019-02/swift-init-class-deep#1.-two-phase-initialization)

* [2. Two Phase Initialization - Code Example](https://hcn1519.github.io/articles/2019-02/swift-init-class-deep#1.-two-phase-initialization---code-example)

* [3. Two Phase init 과정에서의 Safety Check](https://hcn1519.github.io/articles/2019-02/swift-init-class-deep#3.-two-phase-init-과정에서의-safety-check)


## 1. Two Phase Initialization

Swift class의 초기화 과정은 공식 문서에서 **Two Phase Initialization**을 거친다고 말합니다. 그래서 다음의 2가지의 과정을 거쳐 class 객체가 초기화 됩니다.

### Phase 1
 
* `designated initializer` 혹은, `convenience initializer` 호출합니다.
* 객체 인스턴스에 대한 Memory allocation을 수행합니다. 다만 이 때는 `stored properties`에 들어가는 데이터의 크기를 모르기 때문에 정확한 메모리 크기가 설정되어 있지 않습니다.
* `designated initializer`가 모든 `stored properties`가 설정되었는지 체크 후, property들에 대한 메모리 init을 수행합니다.
* 이제 `subClass`의 작업을 마치고 `superClass`에서 위의 과정과 동일한 작업을 수행합니다.
* 계층 구조 최상단 `superClass`가 모든 properties가 값이 있는지 확인 후, init 작업이 완료됩니다.

### Phase 2

* Phase 1을 마치면 self에 접근할 수 있게 되고, 최상단 `superClass`는 property 값을 변경할 기회를 얻게 됩니다.
* 값 변경의 기회는 계층 구조 최상단 `superClass`부터 마지막 `subClass`의 순서로 주어집니다.
* 현재 클래스에서 init을 호출한 것이 `convenience initializer`라면, `designated initializer`부터 우선적으로 self의 값을 변경할 기회를 얻게 됩니다. 이 작업을 마치면 최종적으로 `convenience initializer`가 값을 변경할 기회를 얻게 됩니다.

위의 과정을 간단하게 하나의 그림으로 요약하면 아래와 같습니다. Phase 1 단계는 initializer가 isa 포인터를 타고 최상단 `superClass`로 올라가는 단계를 지칭합니다. Phase 2단계는 최상단에서 내려오면서 최종 `subClass`에 도착한 후 최종 메소드가 끝나서 인스턴스가 완전히 준비되기 직전까지를 의미합니다.

<img src="{{ site.imageUrl}}/2019-02/swift_init_class_deep/phase1-2.png">

> Note: Two Phase Initialization에서 Phase의 구분을 self 접근을 기준으로 나누는 설명도 존재합니다. 즉, self 접근이 가능한 Phase -> Phase 1 단계, 그렇지 않은 경우 -> Phase 2 단계로 나누는 것입니다. 이러한 구분은 초깃값을 설정하는 것과 혼동(designated initializer에서 모든 stored property에 값이 설정되기 전에 사용되는 self는  초깃값 설정용입니다.)이 될 수 있기 때문에 위의 방식으로 이해하는 것이 좋아 보입니다.

## 2. Two Phase Initialization - Code Example

이제는 **Two Phase Initialization**의 과정을 코드에서 살펴보겠습니다. 과정을 자세히 살펴보기 위해 breakpoint를 찍어서 각각을 살펴보겠습니다.

```swift
class SoftDrink {
    var size: String

    init() {
        // Step 3
        self.printHello() // 'self' used in method call 'printHello' before all stored properties are initialized
        self.size = "Regular"
        self.printHello() // 정상 동작
        print("Phase 2")
        print("self 접근 가능")
    }

    func printHello() {
        print("hello")
    }
}
class Coke: SoftDrink {
    var price: Int

    override init() {
        // Step 2
        self.price = 1300
        super.init()
    }

    convenience init(size: String, price: Int) {
        // Step 1
        print("Phase 1")
        print("self 접근 불가능")
        self.init()
        self.size = size
        self.price = price
    }
}

let coke = Coke(size: "large", price: 2000)
```

### Step 1

<img src="{{ site.imageUrl}}/2019-02/swift_init_class_deep/p1-self.png">

생성자를 호출하게 되면 객체에 대한 Memory allocation이 일어납니다. 그래서 생성자 호출 직후 `self`를 출력하게 되면 아래와 같은 메모리 주소값이 설정되어 있습니다.

```
(lldb) po self
<Coke: 0x101c05000>
```

다만, 이 단계에서는 `stored properties`가 설정되어 있지 않은 상황입니다. 그래서 동일한 단계에서 `stored properties`를 출력할 경우 해당 데이터 타입에 맞는 쓰레기 값이 출력됩니다.

```
(lldb) po self.price
140736069925464 // 이 숫자는 일정하지 않습니다.
```

### Step 2

<img src="{{ site.imageUrl}}/2019-02/swift_init_class_deep/p2-self.png">

`designated initializer`에서는 현재 `subClass`의 모든 `stored properties`에 값이 부여되어 있는지 체크합니다. 만약 값이 타입에 맞게 적절히 설정되어 있지 않다면 컴파일 에러가 발생합니다. 모든 조건을 만족한다면, 이제 인스턴스는 `subClass`의 `stored properties`의 값을 설정합니다.(init을 수행합니다.) 이 과정이 완료되면 `subClass`에 대한 작업은 모두 완료되고, `superClass`에 대한 작업이 진행됩니다.

### Step 3

`subClass`와 마찬가지로 `superClass`에서도 `stored properties`를 설정합니다. 그리고 `SoftDrink`는 계층 구조 최상단의 클래스입니다. 그래서 초기화 과정중 Phase 1 단계는 이 클래스에서 종료되는데, 그 시점은 **`stored properties`에 모든 값이 들어간 직후** 입니다. 만약 `stored properties`에 초깃값이 설정되어 있지 않은 경우에는 Phase 2 단계로 넘어갈 수 없고, self를 통한 메소드 호출 및 값 변경 등은 불가능합니다.

### Step 4(Phase 2)

이후에는 계층구조를 타고 내려오면서 객체에게 값 변경이나 메소드 호출의 기회가 주어집니다.

## 3. Two Phase init 과정에서의 Safety Check

Swift는 init의 과정에서 개발자가 생성자를 좀 더 안전하게 사용할 수 있도록 Safety Check 규칙을 제공합니다. 즉, 이 룰을 지키지 않으면 Swift 컴파일러는 컴파일 에러를 일으키고, 코드를 수정하도록 가이드합니다.

### Rule 1

* `designated initializer`에서는 현재 클래스에서 정의한 `stored properties`의 값이 delegate up되기 이전에 모두 초깃값을 가지고 있어야 한다.

```swift
import Foundation

class TestObject: NSObject {

    let tmpValue: Int

    override init() {
        self.tmpValue = 0 // super.init() 호출 이전에 값이 결정되어야 합니다.
        super.init()
    }
}
```

이 룰은 위의 경우에서 `tmpValue`가 `super.init()`의 호출보다 먼저 설정되는 것을 통해 적용됩니다.

객체의 메모리 크기는 모든 `stored properties`의 크기를 통해서 크기가 결정됩니다. Initialization 작업은 `subClass`에서 `superClass`방향으로 이뤄지고, 마지막 작업은 상속의 가장 위에 있는 class에서 끝나게 됩니다.(Phase 1 종료) 그러므로 `subClass`의 메모리 크기는 `superClass`로 가기 전에 알고 있어야 합니다. 

### Rule 2

* `designated initializer`는 상속받은 property의 값을 넣기 전에 `superClass`의 initializer를 호출해야 한다.(delegate up)

```swift
class SuperObject: NSObject {
    var superTmpValue: Int

    override init() {
        self.superTmpValue = -1
        super.init()
    }
}

class TestObject: SuperObject {

    let tmpValue: Int

    override init() {
        self.tmpValue = 0
        super.init()
        super.superTmpValue = -5 // 반드시 super.init() 뒤에 와야 한다.
    }
}
```

일반적으로 `subClass`에서 `superClass`의 property 값을 바꾸는 것은 `superClass`의 property 값을 그대로 사용하지 않는 경우입니다. 이런 경우가 아니라면 값을 바꿀 필요 없이 그대로 `superClass`의 값을 사용하면 됩니다. 그런데 `superClass`의 initializer는 `superClass`의 `stored properties`를 반드시 설정합니다. 그래서 `super.init()` 호출 이전에 `subClass`에서 `superClass`의 값을 변경하는 것은 반영이 되지 않을 수 있습니다.  이런 상황을 방지하기 위해 Swift 컴파일러는 상속받은 property의 값을 넣기 전에 `superClass`의 initializer를 호출하도록 합니다.

### Rule 3

* `convenience initializer`에서 property에 값을 설정하기 전에 `initializer delegation`을 수행해야합니다.

Rule 2와 비슷한 것이지만, `super.init()`이 `self.init()`으로 바뀐 것으로 이해하면 쉽습니다. 즉, 값 변경을 Phase 1 단계가 아니라 Phase 2 단계에서 수행하도록 강제하는 규칙입니다.

### Rule 4

* Phase 1 단계가 끝나기 전에 어떤 메소드를 호출하거나 프로퍼티에 접근하여 값을 사용하는 것이 불가능합니다.

Phase 1 단계가 완료되면 인스턴스가 초깃값으로 init이 완료됩니다. 반대로 얘기하면 Phase 1 단계에서는 인스턴스가 완전히 init이 되지 않은 상태입니다. 그렇기 때문에 Swift 컴파일러는 Phase 1 단계 이전에 self를 통한 메소드를 호출하거나 프로퍼티에 접근하여 값을 사용하는 것을 제한합니다.

---

# 참고자료

* [The Swift Programming Language (Swift 4.2)](https://itunes.apple.com/kr/book/the-swift-programming-language-swift-4-2/id881256329?mt=11)
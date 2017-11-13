---
layout: post
comments: true
title:  "Swift Protocol - Part1"
excerpt: "Swift의 Protocol의 기본 개념 및 사용법과 delegation 패턴에 대해 알아봅니다."
categories: Swift Protocol Delegation
date:   2017-11-11 00:30:00
tags: [Swift, Protocol, Delegation]
image:
  feature: swiftLogo.jpg
---

이번 포스팅에서는 Swift의 `Protocol` 기본 개념 및 사용법과 이에 기반한 delegation 패턴에 대해 알아 보고자 합니다. 먼저 Protocol의 정의부터 살펴보겠습니다.

<div class="message">
A protocol defines a blueprint of methods, properties, and other requirements that suit a particular task or piece of functionality.
</div>

Protocol은 자신을 따르는 어떤 객체가 구현해야 하는 **필요 요건** 을 서술한 것입니다.   
1. 여기서 객체가 의미하는 것은 `class` 뿐만 아니라, `struct`, `enum`을 포함합니다.
2. 객체들이 Protocol을 따르게 되면 컴파일시 이 필요 요건을 충족하는 지 확인합니다.

이 때, 객체들이 Protocol을 `따른다`는 표현을 썼는데, 이는 애플의 스위프트 공식 가이드 문서에서 `conform`이라는 단어로 표현됩니다. 또한 이와 같이 나오는 단어로 `adopt`가 있는데 이는 `채택하다`라는 의미로 사용됩니다. 예를 들면, 어떤 프로토콜을 따르는 객체는 해당 프로토콜을 채택하였다고 표현됩니다.

자동차라는 프로토콜을 만든다고 생각해보겠습니다. 자동차는 자동차이기 위해 필수적으로 가지고 있는 것이 있습니다. 자동차면 엔진이 필요하고, 연비 수치가 있을 것이고, 바퀴가 있을 것입니다. 이러한 것들을 프로토콜에 담아서 자동차라면 모름지기 가져야 하는 요소를 하나의 프로토콜로 작성할 수 있습니다. 그리고 미니쿠퍼라는 구조체를 만들 때, 그 구조체가 자동차 프로토콜을 따르게 만들 수 있습니다.

## 1. Protocol Syntax
Protocol은 다음과 같은 문법으로 사용됩니다.

{% highlight swift %}
protocol 프로토콜1 {
	 // 프로토콜1의 필수 구현 내용
}
protocol 프로토콜2 {
	 // 프로토콜2의 필수 구현 내용
}
struct 구조체1: 프로토콜1 {
	 // 프로토콜1의 필수 구현 내용을 충족해야 합니다.
}

class 어떤_클래스: 부모클래스, 프로토콜1, 프로토콜2 {
	 // 프로토콜1과 프로토콜2의 구현 내용 충족
	 // 부모클래스 상속
}
{% endhighlight %}

Protocol은 `class` 상속과 유사한 형태로 사용됩니다. 다만 Swift에서 하나의 `class`만 상속할 수 있는 것을 달리 객체는 복수의 Protocol을 따를 수 있습니다. 또한, 특정 `class`는 부모클래스를 상속하면서 Protocol도 따르는 형태로 구현될 수도 있습니다.

## 2. Requirements
Protocol을 따르는 객체가 충족시켜야하는 요건이라는 것은 일반적으로 **특정 프로퍼티 혹은 메소드를 필수로 구현해야 하는 것** 과 그 의미가 거의 같습니다. 그렇기 때문에 Protocol에는 이를 따르는 객체들이 구현해야 할 프로퍼티와 메소드의 **조건** 이 쓰여져야 합니다.

### Property Requirements
먼저 Property가 Protocol에서 어떻게 쓰여야하는지 살펴 보겠습니다.

* `Car` 프로토콜은 어떤 객체가 자동차이기 위해 필요한 프로퍼티들을 필수적으로 서술할 것을 요구합니다.

{% highlight swift %}
enum Fuel {
    case oil
    case electronic
}

protocol Car {
    var mileage: Int { get set }
    var maxSpeed: Int { get }
    var engineType: Fuel { get }
    var navigation: String? { get }
    var stateOfCar: CarState { get set }
}
{% endhighlight %}

1. Protocol에서 Property는 모두 `var`로 선언됩니다.(어떤 프로퍼티를 immutable하게 선언하고 싶다면 get-only 프로퍼티로 선언하고 사용하면 됩니다.)
2. Protocol은 어떤 **조건** 이기 때문에, 변수의 이름과 타입만 쓰고 변수의 값은 쓰지 않습니다.
3. Protocol은 변수가 `gettable`(`{ get }`) 여부, `settable`(`{ get set }`, set-only는 존재하지 않습니다.) 여부를 위의 예시처럼 표현합니다.
4. Protocol끼리도 서로 conform할 수 있습니다. 이 때, 따르는 프로토콜을 참조하는 객체는 모든 프로퍼티를 구현해주어야 합니다.

위의 Protocol을 따르는 객체를 생성하면 다음과 같이 될 수 있습니다.

* 여기서 `FeatureOfCar` 구조체는 `Car` 프로토콜을 따르고, 이에 따라 `Car` 프로토콜이 요구하는 프로퍼티들을 구현해야 합니다.

{% highlight swift %}
struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    var engineType: Fuel
    var navigation: String?
    var stateOfCar: CarState {
        didSet {
            print("자동차의 상태가 변경됩니다.", self.stateOfCar)
        }
    }
}
{% endhighlight %}

### Method Requirements

메소드 같은 경우에도 Protocol에서는 메소드의 body를 작성하지 않고, 함수명, 파라미터, 리턴 타입만을 명시합니다.

{% highlight swift %}
enum Fuel {
    case oil
    case electronic
}

protocol Car {
    var mileage: Int { get set }
    var maxSpeed: Int { get }
    var engineType: Fuel { get }
    var navigation: String? { get }
    var stateOfCar: CarState { get set }

    mutating func isRunning()
}

struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    var engineType: Fuel
    var navigation: String?

    var stateOfCar: CarState {
        didSet {
            print("자동차의 상태가 변경됩니다.", self.stateOfCar)
        }
    }

    mutating func isRunning() {
        self.mileage += 2
    }
}
{% endhighlight %}

위의 예시에서 `isRunning`이라는 메소드를 `Car` 프로토콜에 추가하였습니다. 이 때 `isRunning`은 객체의 프로퍼티를 변경하기 때문에 mutating 키워드를 써주어야 합니다.

## 3. Protocol Type

프로토콜은 데이터 타입으로도 사용될 수 있습니다. 이 말은 프로토콜이 우리가 사용하는 `Int`, `String` 같은 자리에 올 수 있다는 것을 의미합니다.

{% highlight swift %}
// 위의 예시의 Car Protocol을 사용합니다.
let feature: Car
{% endhighlight %}

여기서 생기는 의문이 있습니다. 그럼 프로토콜 타입의 변수에는 무엇이 와야하는 것인가요? 단순하게 생각하면 `Car` 인스턴스가 올 수 있지만, 프로토콜로는 인스턴스를 생성할 수 없습니다. 프로토콜 타입의 변수에는 그 프로토콜을 따르는 인스턴스가 올 수 있습니다.

코드에서 이 개념을 알아보겠습니다.

* 여기서는 `Car` 프로토콜 타입을 프로퍼티로 가지고 있는(따르는 것이 아닙니다.) `MiniCooper` 구조체를 생성하였습니다.

{% highlight swift %}
enum Fuel {
    case oil
    case electronic
}

protocol Car {
    var mileage: Int { get set }
    var maxSpeed: Int { get }
    var engineType: Fuel { get }
    var navigation: String? { get }
    var stateOfCar: CarState { get set }

    mutating func isRunning()
}

struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    var engineType: Fuel
    var navigation: String?

    var stateOfCar: CarState {
        didSet {
            print("자동차의 상태가 변경됩니다.", self.stateOfCar)
        }
    }

    mutating func isRunning() {
        self.mileage += 2
    }
}

struct MiniCooper {
    var feature: Car
}
{% endhighlight %}

위의 예시에서 `MiniCooper` struct는 `Car` 프로토콜 타입의 변수 `feature`를 갖습니다. 이 `feature`의 자리에는 `Car`을 따르는 객체 중 무엇이든 올 수 있습니다. 그래서 여기서는 `FeatureOfCar` 구조체가 `Car` 프로토콜을 따르기 때문에, `FeatureOfCar`의 인스턴스인 `miniCooperFeature`가 `feature`의 자리에 올 수 있습니다.

> 이와 같은 사실에서 알 수 있는 것은 객체가 어떤 프로토콜을 사용하는 것은 해당 프로토콜을 따르는 방법과 프로토콜을 프로퍼티로 가지고 있는 방법이 있다는 것입니다. 즉, 객체 스스로가 해당 프로토콜을 요구조건을 만족하도록 모든 프로퍼티, 메소드들을 구현할 수도 있고(따르는 방법), 자신은 프로토콜이 무엇을 하는지 모른채로 프로퍼티로만 가질 수도 있는 것(가지는 방법)입니다.

## 4. 프로토콜의 다형성과 Value Type의 확장

앞선 예제에서 프로토콜 타입의 데이터에는 프로토콜을 따르는 어떤 객체든 올 수 있다는 것을 파악하였습니다. 이 속성은 value type의 확장에 있어서 상당히 중요한 속성입니다. 아래 코드를 살펴보겠습니다.

{% highlight swift %}
struct FeatureOfCar {
    var mileage: Int
}
struct MiniCooper1 {
    var feature: FeatureOfCar
}

protocol Car {
    var mileage: Int { get }
}
struct MiniCooper2 {
    var feature: Car
}
{% endhighlight %}

위의 코드에서 `MiniCooper1`는 `FeatureOfCar`의 구조체를 프로퍼티로 가집니다. `MiniCooper2`는 `Car` 타입의 프로토콜을 가집니다. 필요한 속성이 같은 두 개의 차이는 무엇일까요? 바로 `확장성`입니다. `FeatureOfCar`에는 `FeatureOfCar` 구조체 타입만 올 수 있습니다. 반면, `Car`에는 `Car`를 따르는 어떠한 객체든 올 수 있습니다.

{% highlight swift %}
protocol Car {
    var mileage: Int { get }
}

class A: Car {
  var mileage: Int
  init() {
        self.mileage = 0
    }
}

struct B: Car {
  var mileage: Int
}
struct MiniCooper2 {
    var feature: Car
}

let a = A()
let b = B(mileage: 5)

let car1 = MiniCooper2(feature: a)
let car2 = MiniCooper2(feature: b)
{% endhighlight %}

위의 코드를 살펴보면 `feature`의 자리에는 클래스가 오든 구조체가 오든 `Car`를 따르는 무엇이든 올 수 있습니다. 이것이 프로토콜의 다형성 개념입니다.

<div class="message">
  프로토콜의 다형성이란 해당 프로토콜 타입에 그 프로토콜을 따르는 타입의 객체는 무엇이든 올 수 있는 개념입니다.
</div>

이 개념은 앞서 잠깐 언급한 것처럼, value type의 확장에 있어서 상당히 중요합니다. value type은 reference type과 다르게 상속이라는 개념이 없습니다. 그래서 value type 객체들이 동일한 특징을 갖게 만들려면 동일한 프로퍼티나 메소드를 모두 갖추고 있어야 했습니다. 하지만, 이제 프로토콜을 통해 value type은 자신이 모든 기능을 구현하지 않고도 확장이 가능해졌습니다. 요약하면, struct와 protocol로 class의 역할을 모두 대체할 수 있는 가능성이 생긴 것입니다.

> value type의 확장은 애플에서 제시한 Protocol Oriented Programming의 근간이 됩니다. 이 주제는 다음 글에서 다룰 예정입니다.

## 5. Delegation

프로토콜이 데이터 타입으로 쓰이는 특징은 iOS에서 많이 사용되는 `Delegate` 패턴의 기반이 됩니다. `Delegation`이라는 영어 단어는 자신이 해야하는 무언가를 다른 사람에게 위임하는 것을 의미합니다. 가이드북에 서술된 정의는 아래와 같습니다.

<div class="message">
Delegation is a design pattern that enables a class or structure to hand off(or delegate) some of its responsibilities to an instance of another type.
</div>

Delegate 패턴에서 하나의 객체가 자신의 책임을 위임한다는 것은 책임을 전가 받은 객체로 자신이 구현해야 하는 것들(프로퍼티, 메소드)을 위임하는 것을 의미합니다. 예를 들어 VC라는 `ViewController`가 있고, VC가 `CLLocationDelegate`(B)의 기능을 사용하고 싶다고 생각해보겠습니다. 이 때, VC는 B를 자신이 직접 구현하지 않고 다른 객체에 위임할 수 있습니다.(이와 관련된 자주 쓰는 `tableView.delegate=self`와 같은 표현은 뒤에서 다룹니다.) 즉, B를 구현해놓은 `LocationManager: CLLocationDelegate`(C)같은 형태의 객체를 만들면 VC가 이것을 가져다 쓸 수 있는 것입니다. 심지어, VC는 C가 무엇을 하는 객체인지 몰라도 됩니다. 그저 C가 B의 요구사항을 만족하기 위해 필요한 모든 프로퍼티나 메소드를 구현하기만 했으면 됩니다. 이처럼 delegate 프로토콜을 통해 기능 구현의 책임을 다른 객체로 위임하는 것을 객체의 책임이 캡슐화되었다고 표현합니다.

앞서서 사용했던 자동차 예제를 다시 가져와 보겠습니다.

{% highlight swift %}
// 중복되는 코드는 일부 생략하였습니다.
enum CarState {
    case running
    case stop
}
struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    var engineType: Fuel
    var navigation: String?

    var stateOfCar: CarState {
        didSet {
            print("자동차의 상태가 변경됩니다.", self.stateOfCar)
        }
    }

    mutating func isRunning() {
        self.mileage += 2
    }
}

struct MiniCooper {
    var feature: Car
    var delegate: CarDelegate?
}

protocol CarDelegate {
    func carDidStarted(car: Car)
    func carDidStopped(car: Car)
}

struct StateOfCar: CarDelegate {
    func carDidStopped(car: Car) {
        var car = car
        car.stateOfCar = .stop
        print("자동차가 멈춤니다.\n")
    }

    func carDidStarted(car: Car) {
        var car = car
        car.stateOfCar = .running
        print("자동차에 시동이 걸렸습니다.\n")
    }
}
{% endhighlight %}

위의 미니쿠퍼 예제에서 자동차의 주행 여부와 현재 주행 상태에 대해서 알 수 있는 `CarDelegate`를 추가하였습니다. `CarDelegate`의 역할은 자동차에 시동이 걸린 시점, 시동이 꺼진 시점을 반환하는 메소드를 가지고 있습니다. `MiniCooper` 구조체에는 새로운 프로퍼티인 `delegate`만 추가되었고, 자동차의 시동이 걸린(꺼진) 시점을 알 수 있는 메소드를 위한 코드는 하나도 작성되어 있지 않습니다. 그렇지만 `delegate` 프로퍼티가 `CarDelegate` 타입이기 때문에 적절한 인스턴스만 해당 프로퍼티에 넣어주면 자동차의 시동이 걸린(꺼진) 시점을 `miniCooper` 인스턴스로부터 알 수 있게 됩니다.

앞서서 Protocol의 타입에서 설명한 것을 다시 떠올려보면, 이 `delegate` 프로퍼티에는 `CarDelegate`을 따르는 어떤 인스턴스이든 전부 올 수 있습니다. 이제 `MiniCooper`에게 필요한 것은 자신의 `delegate` 변수를 채워줄 인스턴스입니다. 여기서는 그 인스턴스를 위해 만든 객체가 `StateOfCar`입니다. `StateOfCar`는 `CarDelegate`를 따르기 때문에 `MiniCooper`의 `delegate` 변수 자리에 올 수 있는 자격을 지니고 있습니다. `StateOfCar`에 적절한 `CarDelegate`의 필수 요건을 채웠기 때문에 컴파일 에러는 나지 않습니다.

이제 이 코드의 사용에 대해 알아보겠습니다.

{% highlight swift %}
let miniCooperFeature = FeatureOfCar(mileage: 20, maxSpeed: 150, engineType: Fuel.oil, navigation: "카카오 네비", stateOfCar: .stop)

// 1
var miniCooper = MiniCooper(feature: miniCooperFeature, delegate: nil)
// 2
var state = StateOfCar()

// 3
miniCooper.delegate = state

// 4
miniCooper.delegate?.carDidStarted(car: miniCooper.feature)
miniCooper.delegate?.carDidStopped(car: miniCooper.feature)

// print
// 자동차의 상태가 변경됩니다. running
// 자동차에 시동이 걸렸습니다.
//
// 자동차의 상태가 변경됩니다. stop
// 자동차가 멈춤니다.
{% endhighlight %}

1. 앞선 경우에서처럼 `miniCooper` 인스턴스를 생성하였습니다. 이 때는 `delegate`를 없는 상태로 인스턴스를 생성하였습니다.
2. `CarDelegate`를 따르는 `StateOfCar` 구조체 인스턴스를 `state`로 생성하였습니다.
3. `state`는 `CarDelegate`를 따르기 때문에 `miniCooper`의 `delegate` 프로퍼티에 할당될 수 있습니다.
4. 이제 `miniCooper`는 자신이 직접 `CarDelegate`를 구현하지 않고, `StateOfCar`를 통해 `CarDelegate`의 프로퍼티나 메소드를 사용할 수 있게 되었습니다. 심지어, delegate 안에 구현된 값으로 `miniCooper` 인스턴스의 값도 변경할 수 있습니다.

> miniCooper는 CarState의 변화에 대한 코드를 직접 작성하지 않고, delegate 프로퍼티를 가지는 것만으로 그 기능을 확장하였습니다. 반대로 state는 자신이 구현하도록 위임 받은 기능을 CarDelegate를 따르며 구현하였습니다. 이와 같은 delegation(위임)을 통해 책임을 전가하는 프로토콜을 작성하는 것이 delegate 디자인 패턴입니다.

##### Delegate 재사용하기

Delegate 패턴의 가장 큰 장점 중 하나는 기능을 재사용할 수 있는 단위로 분할하여 코드를 작성할 수 있다는 점입니다. 앞의 자동차 예제를 다시 들고 와보겠습니다.

{% highlight swift %}
var miniCooper = MiniCooper(feature: miniCooperFeature, delegate: nil)
var state = StateOfCar()
miniCooper.delegate = state


struct A8 {
    var feature: Car
    var delegate: CarDelegate?
    var color: String
}

let a8Feature = FeatureOfCar(mileage: 30, maxSpeed: 120, engineType: Fuel.oil, navigation: "네이버 지도", stateOfCar: .running)
var a8 = A8(feature: a8Feature, delegate: state, color: "Silver")
{% endhighlight %}

위의 코드에서는 `MiniCooper` 구조체와 `A8` 구조체 모두 `StateOfCar`를 `delegate`로 사용할 수 있습니다. 즉, `MiniCooper`, `A8` 구조체 각각에 `CarDelegate` 메소드를 작성하는 것이 아니라, `StateOfCar`를 재사용한 것입니다.

#### UITableViewDataSource의 delegate 패턴

이제 위의 개념을 통해 UITableView를 사용할 때, 소위 말해서 `tableView.dataSource = self`라는 코드가 어떤 의미를 담고 있는지 파악할 수 있습니다. 먼저 `UITableView`에는 어떤 변수들이 선언되어 있는지 살펴보면 다음과 같습니다.

{% highlight swift %}
// 일부만 가져왔습니다.
@available(iOS 2.0, *)
open class UITableView : UIScrollView, NSCoding, UIDataSourceTranslating {
    weak open var dataSource: UITableViewDataSource?

    weak open var delegate: UITableViewDelegate?

    @available(iOS 10.0, *)
    weak open var prefetchDataSource: UITableViewDataSourcePrefetching?

    @available(iOS 11.0, *)
    weak open var dragDelegate: UITableViewDragDelegate?

    @available(iOS 11.0, *)
    weak open var dropDelegate: UITableViewDropDelegate?
}
{% endhighlight %}

`dataSource` 변수는 `UITableView` 클래스 안에 들어 있는 변수입니다.(`dataSource`뿐만 아니라 다른 `delegate`, `prefetchDataSource` 등도 같은 형태를 취하고 있는 것을 확인할 수 있습니다.) `dataSource`는 `UITableViewDataSource` 타입으로 `UITableViewDataSource`를 따르는 객체는 무엇이든 올 수 있습니다.

이제 ViewController를 살펴보겠습니다.

{% highlight swift %}
// 1
class VC: UIViewController, UITableViewDataSource {

    @IBOutlet weak var tableView: UITableView!

    override func viewDidLoad() {
        super.viewDidLoad()

        // 2
        tableView.dataSource = self
    }

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return 1
    }

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        return UITableViewCell()
    }
}
{% endhighlight %}

1. `VC` 클래스는 흔히 사용되는 `UIViewController`로 `UITableViewDataSource`를 따릅니다. 그렇기 떄문에 `numberOfRowsInSection`과 `cellForRowAt`을 필수적으로 구현해주어야 합니다.
2. 앞서 살펴보았듯이, `UITableView` 안에는 `dataSource`라는 변수가 `UITableViewDataSource` 타입으로 선언되어 있었습니다. 여기서 `self`는 `VC`를 지칭하는 것으로 `VC`가 `UITableViewDataSource`를 따르고 있기 때문에, 해당 `dataSource`는 `VC`(self)에 구현된 dataSource 메소드(`numberOfRowsInSection`과 `cellForRowAt`)들과 연결됩니다.

> 참고로 UITableViewController는 UITableViewController dataSource와 delegate이 Interface Builder에서 설정되어 있기 때문에 따로 dataSource를 설정하지 않아도 됩니다.

---

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 4) - Protocol
* [Introducing Protocol-Oriented Programming in Swift 3 - raywenderlich](https://www.raywenderlich.com/148448/introducing-protocol-oriented-programming)

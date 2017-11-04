---
layout: post
comments: true
title:  "Swift Protocol - Part1"
excerpt: "Swift의 Protocol의 기본에 대해 알아봅니다."
categories: Swift Protocol Delegation
date:   2017-11-03 00:30:00
tags: [Swift, Protocol, Delegation]
image:
  feature: swiftLogo.jpg
---

이번 포스팅에서는 Swift의  `Protocol`에 대해 알아보고자 합니다.

<div class="message">
A protocol defines a blueprint of methods, properties, and other requirements that suit a particular task or piece of functionality.
</div>

Protocol은 자신을 따르는 어떤 객체가 구현해야 하는 필요 요건을 서술한 것입니다.   
1. 여기서 객체가 의미하는 것은 `class` 뿐만 아니라, `struct`, `enum`을 포함합니다.
2. 객체들이 Protocol을 따르게 되면 컴파일시 이 필요 요건을 충족하는 지 확인합니다.

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

Protocol은 `class` 상속과 유사한 형태로 사용됩니다. 다만 Swift에서 하나의 `class`만 상속할 수 있는 것을 달리 객체는 복수의 Protocol을  따를 수 있습니다. 또한, 특정 `class`는 부모클래스를 상속하면서 Protocol도 따르는 형태로 구현될 수도 있습니다.

## 2. Requirements
Protocol을 따르는 객체가 충족시켜야하는 요건이라는 것은 일반적으로 **특정 프로퍼티를 필수로 구현해야 하는 것**, 혹은 **특정 메소드를 필수로 구현해아 하는 것** 과 그 의미가 거의 같습니다. 그렇기 때문에 Protocol에는 이를 따르는 객체들의 구현해야 할 프로퍼티와 메소드의 조건이 쓰여져야 합니다.

### Property Requirements
먼저 Property가 Protocol에서 어떻게 쓰여야하는지 살펴 보겠습니다.

{% highlight swift %}
enum Fuel {
    case oil
    case electronic
}
protocol Transportation {
    var mileage: Int { get set }
    var maxSpeed: Int { get }
    var engineType: Fuel { get }
}
protocol Car: Transportation {
    var navigation: String? { get }
}
{% endhighlight %}

1. Protocol에서 Property는 모두 `var`로 선언됩니다.(어떤 프로퍼티를 immutable하게 선언하고 싶다면 get-only 프로퍼티로 선언하고 사용하면 됩니다.)
2. Protocol은 어떤 **조건** 이기 때문에, 변수의 이름과 타입만 쓰고 변수의 값은 쓰지 않습니다.
3. Protocol은 변수가 `gettable` 여부, `settable` 여부를 위의 예시처럼 표현합니다.
4. Protocol끼리도 서로 conform할 수 있습니다. 이 때, 따르는 프로토콜을 참조하는 객체는 모든 프로퍼티를 구현해주어야 합니다.

위의 Protocol을 따르는 객체를 생성하면 다음과 같이 될 수 있습니다.

{% highlight swift %}
struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    let engineType: Fuel
    var navigation: String?
}
{% endhighlight %}

### Method Requirements

메소드 같은 경우에도 Protocol에서는 메소드의 body를 작성하지 않고, 함수명, 파라미터, 리턴 타입만을 명시합니다.

{% highlight swift %}
enum Fuel {
    case oil
    case electronic
}
protocol Transportation {
    var mileage: Int { get set }
    let maxSpeed: Int { get }
    let engineType: Fuel { get }

    // 값을 변경 시키는 메소드는 mutating 키워드를 사용해야 합니다.
    mutating func isRunning()
}
protocol Car: Transportation {
    var navigation: String? { get }
}
struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    let engineType: Fuel
    var navigation: String?

    mutating func isRunning() {
        self.mileage += 2
    }
}
{% endhighlight %}

위의 예시에서 `isRunning`이라는 메소드를 `Transportation` 프로토콜에 추가하였습니다. 이 때 `isRunning`은 객체의 프로퍼티를 변경하기 때문에 mutating 키워드를 써주어야 합니다.

## 3. Protocol Type

프로토콜은 데이터 타입으로도 사용될 수 있습니다. 이 말은 프로토콜이 우리가 사용하는 `Int`, `String` 같은 자리에 올 수 있다는 것을 의미합니다.

{% highlight swift %}
// 위의 예시의 Car Protocol을 사용합니다.
let feature: Car
{% endhighlight %}

여기서 생기는 의문이 있습니다. 그 변수의 자리에는 무엇이 와야하는 것인가요? 단순하게 생각하면 `Car` 인스턴스가 와야합니다. 그런데 프로토콜로는 인스턴스를 생성할 수 없습니다.

> 프로토콜 데이터 타입에는 어떤 값이 들어갈 수 있는건가요? 바로 해당 프로토콜을 따르는(conform) 객체입니다.

코드에서 이 개념을 알아보겠습니다.

{% highlight swift %}
enum Fuel {
    case oil
    case electronic
}

protocol Transportation {
    var mileage: Int { get set }
    let maxSpeed: Int { get }
    let engineType: Fuel { get }

    mutating func isRunning()
}
protocol Car: Transportation {
    var navigation: String? { get }
}

struct FeatureOfCar: Car {
    var mileage: Int
    let maxSpeed: Int
    let engineType: Fuel
    var navigation: String?

    mutating func isRunning() {
        self.mileage += 2
    }
}

struct MiniCooper {
    let feature: Car
}

let miniCooperFeature = FeatureOfCar(mileage: 20, maxSpeed: 150, engineType: Fuel.oil, navigation: "카카오 네비")
var miniCooper = MiniCooper(feature: miniCooperFeature)

{% endhighlight %}

위의 예시에서 `MiniCooper` struct는 `Car` 프로토콜 타입의 변수 `feature`를 갖습니다. 이 `feature`의 자리에는 `Car`을 따르는 객체 중 무엇이든 올 수 있습니다. 그래서 여기서는 `FeatureOfCar` 구조체가 `Car` 프로토콜을 따르기 때문에, `FeatureOfCar`의 인스턴스인 `miniCooperFeature`가 `feature`의 자리에 올 수 있습니다.

## 4. Delegation

프로토콜이 데이터 타입으로 쓰이는 특징은 iOS에서 많이 사용되는 `Delegate` 패턴의 기반이 됩니다. `Delegation`의 이해를 위해 그 단어의 뜻을 찾아보면 다음과 같습니다.

> Delegation이라는 영어 단어는 위임이라는 뜻을 가지고 있습니다. 무언가를 다른 사람에게 위임한다는 것은 원래는 자기가 해야되는 일인데, 이를 다른 사람이 하도록 만드는 것입니다.

위의 뜻에서 사람을 객체로 치환하여, 아래 `Delegate` 패턴의 정의를 읽어보면 의미가 더 쉽게 와닿을 수 있습니다.

<div class="message">
Delegateion is a design pattern that enables a class or structure to hand off(or delegate) some of its responsibilities to an instance of another type.
</div>

Delegate 패턴에서 하나의 객체가 자신의 책임을 위임한다는 것은 책임을 전가 받은 객체로 자신이 구현해야 하는 것들(프로퍼티, 메소드)을 위임하는 것을 의미합니다. 즉, A라는 객체가 어떤 기능을 쓰기 위해 구현해야 하는 프로퍼티나 메소드들을 A가 직접 구현하지 않고, B라는 객체에 구현된 것을 A에서 가져다가 쓸 수 있도록 하는 것이 Delegate 패턴의 핵심입니다.

앞서서 사용했던 자동차 예제를 다시 가져와 보겠습니다.

{% highlight swift %}
// 중복되는 코드는 일부 생략하였습니다.
enum CarState {
    case running
    case stop
}
protocol CarDelegate {
    var stateOfCar: CarState { get set }
    func carDidStarted(car: Car)
    func carDidStopped(car: Car)
}

struct MiniCooper {
    let feature: Car
    var delegate: CarDelegate?
}

struct StateOfCar: CarDelegate {
    var stateOfCar: CarState {
        didSet {
            print("차의 상태가 변경되었습니다. 상태: \(self.stateOfCar)")
        }
    }

    func carDidStopped(car: Car) {
        print("자동차가 멈춤니다")
    }
    func carDidStarted(car: Car) {
        print("자동차에 시동이 걸렸습니다.")
    }
}
{% endhighlight %}

위의 미니쿠퍼 예제에서 자동차의 주행 여부와 현재 주행 상태에 대해서 알 수 있는 `CarDelegate`를 추가하였습니다. `MiniCooper` 구조체에는 새로운 변수인 `delegate`가 추가되었고, 이는 `CarDelegate` 타입입니다. 앞서서 Protocol의 타입에서 설명한 것을 다시 떠올려보면, 이 `delegate` 변수에는 `CarDelegate`을 따르는 어떤 것이든 올 수 있습니다. 이제 `MiniCooper`에게 필요한 것은 자신의 `delegate` 변수를 채워줄 객체입니다. 여기서는 그 객체가 `StateOfCar`입니다. `StateOfCar`는 `CarDelegate`를 따르기 때문에 `MiniCooper`의 `delegate` 변수 자리에 올 수 있는 자격을 지니고 있습니다. `StateOfCar`에 적절한 `CarDelegate`의 필수 요건을 채웠기 때문에 컴파일 에러는 나지 않습니다.

이제 이 코드의 사용에 대해 알아보겠습니다.

{% highlight swift %}
let miniCooperFeature = FeatureOfCar(mileage: 20, maxSpeed: 150, engineType: Fuel.oil, navigation: "카카오 네비")

// 1
var miniCooper = MiniCooper(feature: miniCooperFeature, delegate: nil)
// 2
var state = StateOfCar(stateOfCar: .stop)

// 3
miniCooper.delegate = state

// 4
miniCooper.delegate?.carDidStarted(car: miniCooper.feature) // 자동차에 시동이 걸렸습니다.
state.stateOfCar = .running // 차의 상태가 변경되었습니다. 상태: running
state.stateOfCar = .stop // 차의 상태가 변경되었습니다. 상태: stop
miniCooper.delegate?.carDidStopped(car: miniCooper.feature) // 자동차가 멈춤니다.
{% endhighlight %}

1. 앞선 경우에서처럼 `miniCooper` 인스턴스를 생성하였습니다. 이 때는 `delegate`를 없는 상태로 인스턴스를 생성하였습니다.
2. `CarDelegate`를 따르는 `StateOfCar` 구조체 인스턴스를 `state`로 생성하였습니다.
3. `state`는 `CarDelegate`를 따르기 때문에 `miniCooper`의 `delegate`에 할당될 수 있습니다.
4. 이제 `miniCooper`는 자신이 직접 `CarDelegate`를 구현하지 않고, `StateOfCar`를 통해 `CarDelegate`의 프로퍼티나 메소드를 사용할 수 있게 되었습니다.

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
2. 앞서 살펴보았듯이, `UITableView` 안에는 `dataSource`라는 변수가 `UITableViewDataSource` 타입으로 선언되어 있었습니다. 여기서 `self`는 `VC`를 지칭하는 것으로 `VC`가 `UITableViewDataSource`를 따르고 있기 때문에, 해당 `dataSource`는 `VC`에 구현된 dataSource 메소드(`numberOfRowsInSection`과 `cellForRowAt`)들과 연결됩니다.

> 참고로 UITableViewController는 UITableViewController dataSource와 delegate이 Interface Builder에서 설정되어 있기 때문에 따로 dataSource를 설정하지 않아도 됩니다.


---

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 4) - Protocol

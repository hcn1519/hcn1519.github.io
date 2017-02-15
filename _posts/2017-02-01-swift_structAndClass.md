---
layout: post
comments: true
title:  "Swift의 Struct와 Class"
excerpt: "Swift의 Struct와 Class의 차이에 대해 알아봅니다."
categories: Swift Language OOP Class
date:   2017-02-14 00:30:00
tags: [Swift, Language, OOP, Class]
image:
  feature: swiftLogo.jpg
---

## Class와 Struct 기본 구조

Class와 Struct는 매우 유사한 데이터 타입입니다. 형태도 유사하고, 쓰임새도 비슷합니다. Swift에서도 이러한 유사성은 유지되는데요. 그렇다면 구체적으로 어떤 부분에서 차이가 있을까요? 다음의 예제를 가지고 살펴보겠습니다.

{% highlight swift %}
class SportsCar {
    var brand: String
    var model: String
}
struct Truck {
    var weight: Int
    var mileage: Double
}
{% endhighlight %}

여기서는 <code>SportsCar</code>라는 Class와 <code>Truck</code> 이라는 구조체를 선언하였습니다. 정확히 class라는 단어와 struct라는 단어만 제외하면 그 형태가 동일합니다. 하지만, 여기서 class 부분은 컴파일 에러를 호출합니다. **Swift에서는 기본적으로 class에 생성자(init)를 포함해야 하기 때문입니다.**(Struct는 생성자가 없어도 됩니다.) 즉 다음과 같은 코드가 두 코드의 기본 형태입니다.

{% highlight swift %}
class SportsCar {
    var brand: String
    var model: String

    init(brand: String, model: String) {
        self.brand = brand
        self.model = model
    }
}
struct Truck {
    var weight: Int
    var mileage: Double
}
{% endhighlight %}

위와 같이 구성하면, 두 데이터 타입 모두 인스턴스(객체)를 생성할 수 있습니다.

{% highlight swift %}
var sportCar1 = SportsCar(brand: "포르쉐", model: "911")
var truck1 = Truck(weight: 2000, mileage: 16)
{% endhighlight %}

<br/>

## Class와 Struct의 차이

그렇다면 가장 근본적인 두 데이터 타입의 차이는 무엇일까요?

답은 바로, class는 <code>reference type</code>이고, struct는 <code>value type</code>이라는 점입니다.

#### Reference type
<div class="message">
  Reference type은 생성자를 통해 초기화 되고 나면, 변수에 값을 할당 하거나, 함수에서 호출할 때, 동일한 인스턴스의 reference(주소)를 반환하는 데이터 type을 말합니다. ex) Object
</div>


#### Value type
<div class="message">
  Value type은 변수에 값을 할당 하거나, 함수에서 호출할 때, 새로운 인스턴스를 만드는(copy) 데이터 type을 말합니다. ex) primitive data type - Int, Double, Char ...
</div>
출처 : [Reference and Value Types in Swift - Andrea Prearo](https://medium.com/@andrea.prearo/reference-and-value-types-in-swift-dad40ea76226#.lnwbky1s3)

Swift 언어를 만든 Apple에서 제공하는 공식 블로그에서는 두 타입의 차이를 mutation(변하기 쉬움)의 측면에서 설명하고 있습니다. [Apple blog - Value and Reference Types](https://developer.apple.com/swift/blog/?id=10)

위의 예제의 경우를 mutable 측면에서 살펴 보면,

{% highlight swift %}
var sportCar1 = SportsCar(brand: "포르쉐", model: "911")
var sportCar2 = sportCar1
sportCar2.brand = "람보르기니"

print(sportCar1.brand) // "람보르기니" 출력

var truck1 = Truck(weight: 2000, mileage: 16)
var truck2 = truck1
truck2.weight = 4000

print(truck1.weight) // 2000 출력
{% endhighlight %}

다음과 같이 차이가 생깁니다. 위의 경우를 살펴보면, <code>sportCar2.brand</code> 부분을 바꿨는데, <code>sportCar1.brand</code>의 값이 변했습니다. 반면, <code>truck2.weight</code> 부분을 바꾼 것은 <code>truck1.weight</code>에 영향을 끼치지 않았습니다. 이러한 현상이 왜 일어나는 것일까요? 그것은 <code>reference type</code>과 <code>value type</code>의 근본적인 메모리 모델이 다르기 때문입니다.

<img src="https://dl.dropbox.com/s/dbqmfztgx16ht1u/sportcar.png">

먼저 class의 경우, <code>sportCar1</code>과 같은 변수가 SportsCar 객체의 값을 직접 저장하지 않습니다. 대신 <code>sportCar1</code> 변수는 <code>sportCar1</code> 객체의 데이터들이 저장된 장소의 **주소** 를 저장합니다. 그렇기 때문에, <code>sportCar2 = sportCar1</code>의 결과는 <code>sportCar2</code>에 <code>sportCar1</code>의 **주소** 를 복사합니다. 반면, struct는 <code>truck1</code> 변수가 저장한 값을 통채로 복사하여 새로운 인스턴스를 생성하고 이를 <code>truck1</code>에 할당합니다.

<img src="https://dl.dropbox.com/s/bbz6bcc7n21g67a/truck.png">

즉, <code>truck2 = truck1</code>의 결과는 <code>truck2</code>에 <code>truck1</code>의 **값** 전체를 복사합니다. 그렇기 때문에, <code>truck2</code>와 <code>truck1</code>은 전혀 **별개의 데이터** 가 되고 둘은 서로에게 영향을 미치지 않습니다.

<div class="message">
  정리하자면, class는 변수 자신이 자신의 속성을 바꾸는 것 이외에도 외부에서 속성을 변경할 수 있습니다.(sportCar2.brand를 바꾼 것이 sportCar1.brand를 변화시킨 것) 반면 struct는 자신의 속성은 자신이 바꾸어야 합니다. 그렇기 때문에 value type인 struct가 class보다 좀 더 mutation에 대해 안전하다고 할 수 있습니다.
</div>

## 그렇다면 어떤 데이터를 사용해야 되나요?

많은 Swift의 API들은 class에 기반하고 있기 때문에 custom 데이터 타입을 만들 때 class를 무조건 사용해야 하는 경우가 빈번합니다. 하지만, 그 이외의 상황, 특히 multi threads 환경과 같은 곳에서는 mutable한 속성이 잘못된 결과를 쉽게 야기할 수 있기 때문에 struct를 사용할 것을 권장합니다.(기본 데이터 타입인 Array, String, Dictionary 등도 모두 value type에 속합니다.) Struct를 통해 동일한 값을 **복사** 하는 것은 constant time 수준만을 필요로 하고, 안전하게 데이터를 전달할 수 있습니다.

<br/>

##### 더 볼만한 추가 자료
- [Apple blog - Value and Reference Types](https://developer.apple.com/swift/blog/?id=10)
- [Reference and Value Types in Swift - Andrea Prearo](https://medium.com/@andrea.prearo/reference-and-value-types-in-swift-dad40ea76226#.lnwbky1s3)
- [Stackoverflow - Why Choose Struct Over Class?](http://stackoverflow.com/a/24232845/5130783)

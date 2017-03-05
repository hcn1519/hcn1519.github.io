---
layout: post
comments: true
title:  "Swift Property"
excerpt: "Swift의 property에 대해 알아봅니다."
categories: Swift property
date:   2017-03-02 00:30:00
tags: [Swift, Language, Property]
image:
  feature: swiftLogo.jpg
---


#### 기본 컨셉

<code>Property</code>라는 개념은 다른 언어의 멤버변수와 같은 개념입니다. 엄밀한 의미에서 <code>property = 멤버변수</code>를 의미하지 않습니다만, 거의 같은 개념으로 이해하셔도 무방합니다. property는 class뿐만 아니라 structure, enum에서도 쓰입니다. 그 중 가장 기본이 되는 <code>property</code>는 <code>stored property</code>입니다.

## 1. Stored Property

{% highlight swift %}
class Info {
  // 많은 시간이 걸리는 자료 추가
}
class Rectangle {
    var _width: Double!
    var _height: Double!
    lazy var tag = Info()
}
var r1 = Rectangle().tag // <- 이 시점에 tag에 대한 데이터들을 가져옵니다.
{% endhighlight %}

위의 코드에서 바로 <code>_width</code>와 <code>_height</code>가 바로 <code>stored property</code>에 해당합니다. 말 그대로 값을 저장하는 속성입니다. 위의 코드에서 독특한 것이 바로 <code>lazy</code>입니다. <code>stored property</code>는 원래 인스턴스 생성시 바로 선언됩니다. 하지만, 앞에 <code>lazy</code> 키워드가 들어가게 되면 해당 <code>property</code>는 인스턴스 생성시 선언되지 않고, 해당  <code>property</code>를 호출하였을 때 선언됩니다. 이는 데이터가 많은 <code>property</code>를 저장할 때, 필요한 경우에 불러 올 수 있는 장점이 있습니다.<!--_-->

## 2. Computed property

<code>Computed property</code>는 getter와 setter의 개념을 포함한 property입니다. 즉, <code>Computed property</code>를 통해서 단순히 변수 값을 받아오거나 설정하는 것을 넘어서서, 값을 내부적으로 조작하는 것, 다른 property들로 값을 넘겨주는 것 등의 일을 할 수 있게 해주는 것이 <code>Computed property</code>입니다. 그 기본 형태는 아래와 같습니다.

{% highlight swift %}
var variableName: dataType {
    get {
        //code to execute
        return someValue
    }
    set(newValue) {
        //code to execute
    }
}
{% endhighlight %}

출처 : <a href="https://syntaxdb.com/ref/swift/getters-setters">SyntaxDB</a>

위에서 <code>variableName</code>에 들어가는 변수가 원하는 해당 <code>Computed property</code>의 이름이 됩니다. 즉, <code>className.variableName</code>의 표현으로 class(혹은 structure, enum) 내부의 변수들에 접근할 수 있게 되는 것이죠.

{% highlight swift %}
class Rectangle {
  private var _width: Double!

  var width: Double {
    get {
      // _width를 가져오기 전 작동하는 code
      return _width
    } set {
      // _width를 설정하기 전 작동하는 code
      _width = newValue
    }
  }
}
var r1 = Rectangle()
r1.width = 10
print(r1.width) // 10
{% endhighlight %}

이를 활용한 표현은 다음과 같습니다. 위에서 <code>r1.width</code>는 <code>var width: Double {</code> 이하를 통해 가능한 표현입니다. <code>r1.width</code>에 값을 설정하는 것은 setter를 통해 구현된 것이고, <code>r1.width</code>의 출력을 위해 가져오는 것은 getter를 통해 구현됩니다. 이 때 단순히 <code>_width</code>의 값을 설정하는 것뿐만 아니라, 일정한 코드를 넣어서 "계산"을 할 수 있습니다. 이 때문에 위 property는 <code>Computed property</code>로 불리는 것을 알 수 있습니다.<!--_-->

{% highlight swift %}
// nil을 먼저 체크하여 빈 String으로 변환
private var name: String!
var name: String {
  get {
    if name == nil {
      name = ""
    }
    return name
  }
}
{% endhighlight %}

위에서 <code>name</code>은 Optional이기 때문에 값을 가져올 때, nil일 수 있어서 에러를 만들 수 있습니다. 그렇기 때문에, <code>name</code>이 nil인지를 먼저 체크하여, nil이라면 빈 스트링("")을 넣어주는 작업(Compute)을 통해, 에러를 방지할 수 있게 해줍니다.

{% highlight swift %}
// progress가 0부터 1 사이에서 벗어나지 않도록 설정
var progress : CGFloat {
    set (newProgress) {
        if newProgress > 1.0 {
            _innerProgress = 1.0
        } else if newProgress < 0.0 {
            _innerProgress = 0
        } else {
            _innerProgress = newProgress
        }
    }
}
{% endhighlight %}

위의 코드의 경우에는 <code>_innerProgress</code>값을 설정하기 이전에 0부터 1 사이의 값인지를 체크하여 값을 0과 1사이의 값으로 고정하는 작업(Compute)을 수행합니다.<!--_-->

## 3. Property Observer

<code>Property Observer</code>는 stored property에 달 수 있는 것으로, 값의 변화를 주시하여 값이 변하기 직전(<code>willSet</code>)과 직후(<code>didSet</code>)에 어떤 행동을 할 수 있게 해주는 것입니다.

{% highlight swift %}
class StepCounter {
    var totalSteps: Int = 0 {
        willSet(newTotalSteps) {
            print("About to set totalSteps to \(newTotalSteps)")
        }
        didSet {
            if totalSteps > oldValue  {
                print("Added \(totalSteps - oldValue) steps")
            }
        }
    }
}
let stepCounter = StepCounter()
stepCounter.totalSteps = 200
// About to set totalSteps to 200
// Added 200 steps
stepCounter.totalSteps = 360
// About to set totalSteps to 360
// Added 160 steps
{% endhighlight %}

위의 경우와 같이 어떤 값을 설정할 경우 <code>Property Observer</code>는 그 값의 변화를 관찰하고, 값이 변하면 어떤 행동을 하는 것을 가능하게 해줍니다.

## 4. Type Property

<code>Type Property</code>는 <code>static</code>을 통해 설정하는 class 변수로 이해해도 무방합니다.

{% highlight swift %}
struct SomeStructure {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 1
    }
}
enum SomeEnumeration {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 6
    }
}
let s1 = SomeStructure()
// SomeStructure.storedTypeProperty, 올바른 표현
// s1.storedTypeProperty, 오류
{% endhighlight %}

위의 경우 <code>SomeStructure</code>에는 <code>storedTypeProperty</code>가 <code>static</code>으로 선언되어 있습니다. 이 말은 앞으로 만드는 모든 <code>SomeStructure</code>타입의 인스턴스에는 <code>storedTypeProperty</code>가 "Some value."으로 저장되는 것을 의미합니다. 그렇기 때문에 <code>Type Property</code>는(개별 인스턴스와 관련된 것이 아니라) 타입들 자체와 연관된 것이기 때문에, 인스턴스 별로 호출할 수 있는 것이 아니라, 타입 자체를 통해 접근할 수 있습니다.(<code>SomeStructure.storedTypeProperty</code>의 형태)

다만 class 타입에서는 <code>static</code> 키워드 대신 <code>class</code> 키워드를 사용하면, 해당 클래스를 상속 받은 자식 클래스가 해당 <code>Type Property</code>를 override할 수 있습니다.

{% highlight swift %}
class SomeClass {
    static var storedTypeProperty = "Some value."
    static var computedTypeProperty: Int {
        return 27
    }
    class var overrideableComputedTypeProperty: Int {
        return 107
    }
}
class Child: SomeClass {
    // static 키워드로 부모 클래스에 동일하게 선언되어 있으므로 에러
    override static var computedTypeProperty: Int {
        return 30
    }
    // class 키워드는 static과 동일한 역할을 하여 type property로 쓰일 수 있으면서 동시에 오버라이딩도 허용하여 Child 메소드의 값을 반환
    override class var overrideableComputedTypeProperty: Int {
        return 120
    }
}
var k = SomeClass.overrideableComputedTypeProperty // 107 출력
var x = Child.overrideableComputedTypeProperty // 120 출력
{% endhighlight %}

위의 코드처럼, Child 클래스가 SomeClass를 상속받을 경우, <code>class</code> 키워드로 만든 <code>Type Property</code>는 오버라이딩을 허용하여, 동일한 property명으로 <code>Type Property</code>를 만들면 자식 값을 반환합니다. 반면, <code>static</code> 키워드는 오로지 1개의 값만을 가지도록 합니다.


> 참고자료 : Apple Inc. The Swift Programming Language (Swift 3.0.1)

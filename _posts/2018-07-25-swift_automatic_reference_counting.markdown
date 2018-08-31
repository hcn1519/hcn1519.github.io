---
layout: post
title: "Swift ARC"
date: "2018-07-25 23:10:45 +0900"
excerpt: "Swift의 Automatic Reference Counting에 대해 알아봅니다."
categories: Memory ARC
tags: [Swift, Memory, ARC]
image:
  feature: swiftLogo.jpg
---

Swift에서는 메모리를 관리할 때 ARC(Automatic Reference Counting)라는 메모리 관리 전략을 사용합니다. 이번 글에서는 이 전략이 어떤 것이고 어떻게 사용되는지에 대해 알아보겠습니다.

## ARC is for reference type

ARC는 이름에서 알 수 있듯이 reference의 숫자를 자동으로 세는 메모리 관리 전략입니다. 이 말은 객체의 메모리 할당시 인스턴스에 reference를 저장하는 객체만 ARC의 영향을 받는다는 의미입니다. 즉, Swift의 value type은 ARC의 메모리 관리 대상이 아닙니다. ARC의 주요 관리 대상은 클래스, 클로저 같은 reference type의 데이터입니다.

## How ARC Works

ARC는 클래스 인스턴스를 생성하였을 때, 메모리를 할당합니다. 그리고 클래스 인스턴스가 더이상 필요하지 않을 때, ARC는 해당 메모리를 해제합니다. 이 때 ARC는 잘못된 메모리 접근을 막기 위해(해제된 메모리에 접근하는 경우, 사용중인 메모리를 덮어씌워버리는 경우) 얼마나 많은 properties, 상수, 변수들이 각각의 클래스 인스턴스를 참조하고 있는지 숫자(reference count)를 셉니다. Swift에서는 각 객체마다 retain count를 가지고 있고, 이 count 수를 통해 메모리가 해제되어야 하는지를 결정합니다. 그래서 reference count가 0이 되는 순간까지 ARC는 객체를 메모리에서 해제하지 않습니다.

## Strong Reference Cycle

ARC는 개발자가 메모리 관리를 직접 하지 않도록 도와주는 좋은 메커니즘이지만, 몇 가지 경우에서 주의가 필요합니다. 그 중 가장 대표적인 케이스가 Strong Reference Cycle(강한 상호 참조)입니다. 강한 상호 참조는 2개의 reference type 데이터가 서로를 strong 인스턴스로 참조하고 있어서 reference count가 0이 되지 않는 상황을 의미합니다. 간단한 강한 상호 참조 상황을 만들어 보겠습니다.

{% highlight swift %}
class Person {
    var house: House?
    deinit {
        print("Remove Person")
    }
}

class House {
    var person: Person?
    deinit {
        print("Remove House")
    }
}

// 1
var person: Person? = Person() // 인스턴스 생성 후 다음 값 출력시 CFGetRetainCount(person) -> 2 출력(기본 count)
var house: House? = House()

// 2
person?.house = house
house?.person = person

// 3
person = nil
house = nil
{% endhighlight %}

위의 코드는 강한 상호 참조를 보여주는 예시입니다. `person`, `house` 인스턴스를 생성하고 모두 `nil` 처리를 해주었음에도 불구하고, deinit에 있는 print문은 호출되지 않았습니다. 즉, `person.house`와 `house.person` 모두 해제가 되지 않았습니다. 왜 그런 것일까요? reference count 메커니즘을 통해 생각해보면 답을 알 수 있습니다.

1. `person`과 `house` 인스턴스를 각각 생성하였고, 각각의 인스턴스는 strong reference count가 1이 됩니다.
2. `person.house`와 `house.person`에 각각 `house`와 `person`을 할당하였기 때문에 두 인스턴스의 strong reference count는 2가 되었습니다.
3. `person`과 `house` 인스턴스를 nil처리 했기 때문에 두 인스턴스의 strong reference count는 1이 됩니다. 그리고 strong reference count가 0이 되지 않았기 때문에 메모리 해제는 일어나지 않습니다.

위의 과정에서 발생한 가장 큰 문제는 인스턴스의 메모리가 해제되지 않았는데 이에 접근할 방법이 없다는 것입니다. 즉, `person.house`는 메모리에 남아 있는데, `person` 자체가 없어져버렸기 때문에 이에 접근이 불가능합니다. 이러한 상황을 메모리 누수(memory leak)가 발생했다고 말하고, 이는 반드시 고쳐야 합니다.

> 메모리 누수는 작은 인스턴스로 시작하여 메모리에 큰 영향을 끼치지 않을 것이라고 생각할 수 있습니다. 하지만, 이 메모리 누수는 앱을 사용할 수록 점유하는 메모리가 커지는 성향이 있기 때문에 작은 메모리 누수로 인해 앱이 죽는 상황이 발생할 수 있습니다.


이와 같은 상황이 자주 발생하지 않는다고 생각할 수도 있지만, 생각보다 많은 경우에서 발생할 위험이 있습니다. 몇 가지 발생할 수 있는 예시로는 Parent View Controller - Child View Controller의 관계 설정시 서로 인스턴스를 소유하고 있을 경우, View Conroller의 SubView에서 ViewController를 인스턴스로 소유해서 무언가를 처리하려 할 경우, delegate 인스턴스를 만들어서 사용할 경우 등이 있습니다.

그런데 생각해보면 자신을 가지고 있는 인스턴스가 해제되었는데 그 property는 당연히 해제되어야 하는 것 아닌가 하는 의문이 들 수도 있습니다. 이런 개념을 담은 것이 바로 `weak`과 `unowned`이고, 이를 통해 Strong Reference Cycle을 제거할 수 있습니다.

## Strong Reference Cycle 없애기

강한 상호 참조를 없애는 핵심 원리는 **strong** reference count를 세지 않는 것입니다. 여기서 중요한 것은 reference count를 아예 세지 않는 것이 아니라, **strong** reference count를 세지 않는 것입니다. 즉, `weak`, 혹은 `unowned`를 사용하여 property를 선언하게 되면 해당 인스턴스에 대해서는 **strong** reference count를 카운팅하지 않고, weak reference count를 카운팅합니다. 이를 Swift 공식 문서에서는 weak reference, unowned referece가 property에 대해 strong hold를 하지 않는다고 표현합니다.

> Weak and unowned references enable one instance in a reference cycle to refer to the other instance without keeping a strong hold on it.

[The Swift Programming Language (Swift 4.1)](https://itunes.apple.com/kr/book/the-swift-programming-language-swift-4-1/id881256329?mt=11)

![img](https://dl.dropbox.com/s/ct7p10tglou2zkh/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202018-07-07%20%EC%98%A4%ED%9B%84%207.29.35.png)

앞서서 Swift의 객체는 retain count를 가지고 있고, ARC는 이를 기반으로 메모리 관리를 한다고 서술하였습니다. 이를 좀 더 자세하게 표현하면 ARC는 메모리의 유지, 해제를 retain count 중 strong reference count를 통해 관리합니다. 즉, count가 0이 되어 없어지는 객체는 strong referece count가 0이 된 객체입니다. 또한, ARC는 strong referece count가 0이 된 객체의 property 중 weak 혹은 unowned로 설정된 객체를 함께 메모리에서 해제합니다.

위에서 사용한 예제를 weak을 통해 수정해보겠습니다.

{% highlight swift %}
class Person {
    weak var house: House?
    deinit {
        print("Remove Person")
    }
}

class House {
    weak var person: Person?
    deinit {
        print("Remove House")
    }
}

// 1
var person: Person? = Person()
var house: House? = House()

// 2
person?.house = house
house?.person = person

// 3
person = nil
house = nil

// Remove Person
// Remove House
{% endhighlight %}


1. 앞선 예제와 동일하게 인스턴스를 생성하여 strong reference count가 1이 되었습니다.
2. `person.house`, `house.person` 모두 weak reference이기 때문에 참조 값은 할당 strong reference count가 올라가지 않고, weak reference count가 증가합니다.
3. ARC는 strong reference count를 통해 메모리 해제를 수행하기 때문에 `person = nil`을 수행하면(메모리에서 해제하면), weak reference도 모두 메모리에서 해제합니다.

이번에는 앞선 예제와 다르게 deinit이 호출되었습니다. 모든 변수가 문제 없이 메모리에서 해제된 것입니다. 이는 property 앞에 명시된 weak을 키워드로 인해 strong reference count가 올라가지 않았기 때문입니다. 즉 `person = nil`을 통해서  strong reference count가 0이 되어 `person`의 메모리가 해제되면서 그 안의 weak으로 설정된 객체인 `house`를 함께 메모리에서 해제한 것입니다.

이와 같은 방식으로 strong reference cycle은 weak을 사용하면 strong reference cycle을 해결할 수 있습니다.

> Weak reference는 ARC를 통해 런타임에서 nil이 될 수 있어야 하기 때문에 항상 옵셔널 타입으로 선언됩니다.

### weak을 사용한 예제

이러한 `weak`이 사용된 대표적인 경우는 바로 IBOutlet입니다. ViewController에서 storyboard를 통해 SubView를 생성하여 IBOutlet을 생성할 경우 다음과 같은 형태로 property가 설정됩니다.

{% highlight swift %}
class ViewController: UIViewController {
    @IBOutlet weak var myView: UIView!
}    
{% endhighlight %}

여기서도 weak이 사용되고 있습니다. 그 이유는 `UIViewController`와 `UIView` 모두 class로 작성된 reference type의 데이터이기 때문에 strong reference cycle이 발생할 수 있기 때문입니다.

## Closure Strong Reference Cycle

Strong Reference Cycle은 두 reference type간의 강한 상호참조를 의미합니다. 그래서 클로저 또한 reference type이기 때문에 클래스 - 클로저 간의 Strong Reference Cycle 또한 발생할 수 있습니다. 다음의 예제를 보면서 이 상황이 어떻게 발생하는지 알아보겠습니다.

{% highlight swift %}
import Foundation

class Person: CustomStringConvertible {

    var description: String {
        return "Person Description"
    }

    lazy var printDescription: () -> Void = {
        print(self.description)
    }

    deinit {
        print("Remove Person")
    }
}

var person: Person? = Person()
person?.printDescription()
person = nil

// Person - name: Hong
{% endhighlight %}

위의 예제에서는 메모리 누수가 발생했습니다. `person` 인스턴스를 nil 처리하였지만 deinit 블럭에 있는 Remove Person이 콘솔에서 출력되지 않았기 때문입니다. 이는 클로저에서 `self`를 사용하면서 `person`으로 새로운 strong reference를 만들었기 때문입니다. 클로저는 할당된 블럭을 실행할 때 자신의 주변 값을 capture 합니다. 클로저는 이를 통해서 블럭 안에서 값을 수정하거나, 새로운 참조를 생성하는 등의 행동을 수행할 수 있습니다.

> A closure can capture constants and variables from the surrounding context in which it is defined. The closure can then refer to and modify the values of those constants and variables from within its body, even if the original scope that defined the constants and variables no longer exists.

[The Swift Programming Language (Swift 4.1)](https://itunes.apple.com/kr/book/the-swift-programming-language-swift-4-1/id881256329?mt=11)

그리고 여기서 중요한 것은 클로저는 자신을 포함하고 있는 `self`에 대해서는 reference를 생성한다는 점입니다. 그렇기 때문에 클래스 안에서 클로저를 사용할 경우, 그리고 클로저 블럭 안에서 `self`를 통해 값에 접근하면 클래스 - 클로저 간의 Strong Reference Cycle이 발생합니다.

## Closure Strong Reference Cycle 없애기

클로저의 강한 상호 참조 또한 weak을 통해서 해결할 수 있습니다. 기본 원리는 위에서 클래스 간 강한 상호 참조를 없애는 방식과 동일합니다. 다만, 클로저는 주변 값을 capture할 때 weak으로 이 capture를 진행하면 됩니다. 방식은 다음과 같습니다.


{% highlight swift %}
lazy var printDescription: () -> Void = { [weak self] in
  print(self!.description)
}
{% endhighlight %}

클로저의 capture는 `[weak self]`를 통해서 참조 방식을 관리할 수 있습니다. 이 때 `self`는 weak 키워드를 사용한 모든 값이 옵셔널이어야 하기 때문에 옵셔널 타입으로 변경됩니다. optional unwrapping을 좀 더 깔끔하게 한다면 다음과 같이 작성할 수 있습니다.

{% highlight swift %}
lazy var printDescription: () -> Void = { [weak self] in
  guard let `self` = self else { return }
  print(self.description)
}
{% endhighlight %}

전체 코드는 아래와 같이 변경되고, 이 때 deinit 블럭이 정상적으로 호출됩니다.

{% highlight swift %}
import Foundation

class Person: CustomStringConvertible {

    var description: String {
        return "Person Description"
    }

    lazy var printDescription: () -> Void = { [weak self] in
        guard let `self` = self else { return }
        print(self.description)
    }

    deinit {
        print("Remove Person")
    }
}
var person: Person? = Person()
person?.printDescription()
person = nil

// Person Description
// Remove Person
{% endhighlight %}

## weak과 unowned의 차이

강한 상호 참조를 해결하기 위해 `weak`과 `unowned`를 사용할 수 있다고 하였는데, 위에서는 `unowned`를 전혀 사용하지 않았습니다. 사실 위의 예제에서 `weak`을 `unowned`로 변경해도 강한 상호 참조를 해결할 수 있습니다. 두 키워드는 모두 약한 상호 참조를 위해 사용되고, 그 차이점은 lifetime에 있습니다.

> Like a weak reference, an unowned reference does not keep a strong hold on the instance it refers to. Unlike a weak reference, however, an unowned reference is used when the other instance has the same lifetime or a longer lifetime.

[The Swift Programming Language (Swift 4.1)](https://itunes.apple.com/kr/book/the-swift-programming-language-swift-4-1/id881256329?mt=11)

`weak`과 `unowned`의 차이는 예시를 통해서 이해하는 것이 이해가 빠릅니다.

* `weak` - Person과 Apartment의 관계

다음의 두 객체 Person과 Apartment가 있다고 가정하겠습니다.

{% highlight swift %}
class Person {

}
class Apartment {

}
{% endhighlight %}

먼저 사람은 아파트에 입주할 수도 있고 그렇지 않을 수도 있습니다. 그래서 Person 객체는 Apartment 인스턴스를 옵셔널로 가지고 있게 됩니다.

{% highlight swift %}
class Person {
    var apartment: Apartment?
}
{% endhighlight %}

아파트의 경우에도 입주자가 존재할 수도 있고, 그렇지 않을 수도 있습니다.

{% highlight swift %}
class Apartment {
    var person: Person?
}
{% endhighlight %}

하지만 이런 경우에 두 인스턴스를 모두 strong으로 생성할 경우 강한 상호 참조 문제가 있다는 것을 알 수 있습니다. 그렇기 때문에 한 쪽의 참조를 `weak` 혹은 `unowned`으로 선언해주어야 합니다. 이 때, Apartment의 인스턴스를 약한 참조로 변경한다고 하였을 때, 생각해보아야 하는 부분은 lifetime입니다. 즉, 아파트는 입주자가 있어야만 존재할 수 있는가?에 대한 질문을 수행하여 아파트와 입주자 사이의 lifetime을 파악해야 합니다. 아파트의 경우 입주자가 없어도 존재할 수 있기 때문에 아파트 내의 사람 인스턴스의 lifetime은 아파트보다 짧습니다. 이런 경우 weak을 사용합니다.

{% highlight swift %}
class Apartment {
    weak var person: Person?
}
{% endhighlight %}

> 객체에서 property로 가지고 있는 인스턴스의 생명주기가 객체보다 짧다면 해당 property를 weak으로 사용합니다.

* `unowned` - Person과 Credit Card의 관계

앞의 예시와 비슷하게 다음의 두 객체 Person과 Credit Card가 있다고 가정하겠습니다.

{% highlight swift %}
class Person {

}
class CreditCard {

}
{% endhighlight %}

이 때도 사람은 신용카드를 가지고 있을 수도 있고, 그렇지 않을 수도 있습니다. 그렇기 때문에 Person은 CreditCard 인스턴스를 옵셔널로 가지고 있습니다.

{% highlight swift %}
class Person {
  var creditCard: CreditCard?
}
{% endhighlight %}

CreditCard의 경우, 아파트와는 다르게 명의자라는 것이 반드시 존재해야 합니다. 그렇기 때문에 CreditCard는 Person 정보를 가지고 있지만, Person과 lifetime이 같거나 더 깁니다. 그렇기 때문에 이 때, 강한 상호참조를 피하면서 lifetime을 적절히 표현하기 위해 `weak` 대신, `unowned` 키워드를 사용합니다.

{% highlight swift %}
class CreditCard {
  unowned var person: Person?
}
{% endhighlight %}

> 객체에서 property로 가지고 있는 인스턴스의 생명주기가 객체보다 길거나 같다면 해당 property를 unowned로 사용합니다.


---

## 참고자료
* [The Swift Programming Language (Swift 4.1)](https://itunes.apple.com/kr/book/the-swift-programming-language-swift-4-1/id881256329?mt=11)

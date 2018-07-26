---
layout: post
title: "Swift ARC"
date: "2018-07-25 23:10:45 +0900"
excerpt: "Automatic Reference Counting에 대해 알아봅니다."
categories: Memory ARC
tags: [Memory, ARC]
---

Swift에서는 메모리를 관리할 때 ARC(Automatic Reference Counting)라는 메모리 관리 전략을 사용합니다. 이번 글에서는 이 전략이 어떤 것이고 어떻게 사용되는지에 대해 알아보겠습니다.

## ARC is for reference type

ARC는 이름에서 알 수 있듯이 reference의 숫자를 자동으로 세는 메모리 관리 전략입니다. 이 말은 객체의 메모리 할당시 인스턴스에 reference를 저장하는 객체만 ARC의 영향을 받는다는 의미입니다. 즉, Swift의 value type은 ARC의 메모리 관리 대상이 아닙니다. ARC의 주요 관리 대상은 클래스, 클로저 같은 reference type의 데이터입니다.

## How ARC Works

ARC는 클래스 인스턴스를 생성하였을 때, 메모리를 할당합니다. 그리고 클래스 인스턴스가 더이상 필요하지 않을 때, ARC는 해당 메모리를 해제합니다. 이 때 ARC는 잘못된 메모리 접근을 막기 위해(해제된 메모리에 접근하는 경우, 사용중인 메모리를 덮어씌워버리는 경우) 얼마나 많은 properties, 상수, 변수들이 각각의 클래스 인스턴스를 참조하고 있는지 숫자(reference count)를 셉니다. 그리고 이를 가능하도록 하기 위해 변수에 클래스 인스턴스를 할당할 때마다 인스턴스에 `strong reference`라는 것을 생성합니다. 그리고 `strong reference` count가 0이 되는 순간까지 클래스 인스턴스는 메모리에서 해제되지 않습니다.

> strong의 의미는 weak unowned와 함께 뒤에서 설명합니다.

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


이와 같은 상황이 자주 발생하지 않는다고 생각할 수도 있지만, 생각보다 많은 경우에서 발생할 위험이 있습니다. 몇 가지 발생할 수 있는 예시로는 Parent View Controller - Child View Controller의 관계 설정시 서로 인스턴스를 소유하고 있을 경우, View Conroller의 SubView에서 ViewController를 인스턴스로 소유해서 무언가를 처리하려고 시도할 경우(절대 하지 마세요), delegate 인스턴스를 만들어서 사용할 경우 등이 있습니다.

그런데 생각해보면 자신을 가지고 있는 인스턴스가 해제되었는데 그 property는 당연히 해제되어야 하는 것 아닌가 하는 의문이 들 수도 있습니다. 이런 개념을 담은 것이 바로 weak과 unowned이고, 이를 통해 Strong Reference Cycle을 제거할 수 있습니다.

## Strong Reference Cycle 없애기

강한 상호 참조를 없애는 핵심 원리는 **strong** reference count를 세지 않는 것입니다. 여기서 중요한 것은 reference count를 아예 세지 않는 것이 아니라, **strong** reference count를 세지 않는 것입니다. 즉, `weak`, 혹은 `unowned`를 사용하여 property를 선언하게 되면 해당 인스턴스에 대해서는 **strong** reference count를 카운팅하지 않습니다. 위의 예제에서 이를 추가해보겠습니다.

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

이번에는 앞선 예제와 다르게 deinit이 호출되었습니다. 모든 변수가 문제 없이 메모리에서 해제된 것입니다. 이는 property 앞에 명시된 weak을 키워드로 인해 strong reference count가 올라가지 않았기 때문입니다. 즉 `person = nil`을 통해서  strong reference count가 0이 된 것입니다.

1. 앞선 예제와 동일하게 인스턴스를 생성하여 strong reference count가 1이 되었습니다.
2. `person.house`, `house.person` 모두 weak reference이기 때문에 참조 값은 할당 strong reference count가 올라가지 않고, weak reference count가 증가합니다.
3. ARC는 strong reference count를 통해 메모리 해제를 수행하기 때문에 `person = nil`을 수행하면(메모리에서 해제하면), weak reference도 모두 메모리에서 해제합니다.

Swift에서 객체는 strong reference count와 weak reference count를 별도로 관리합니다.

![img](https://dl.dropbox.com/s/ct7p10tglou2zkh/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202018-07-07%20%EC%98%A4%ED%9B%84%207.29.35.png)

ARC는 두 가지 reference count 중 strong reference count를 통해서만 객체의 메모리 해제를 관리합니다. 또한 ARC는 참조하고 있는 인스턴스가 deallocated 될 경우 자동으로 weak reference를 nil로 만들고 메모리를 해제합니다. 그렇기 때문에 weak을 사용하면 strong reference cycle을 해결할 수 있습니다.

> Weak reference는 ARC를 통해 런타임에서 nil이 될 수 있어야 하기 때문에 항상 옵셔널 타입으로 선언됩니다.

### weak을 사용한 예제

이러한 `weak`이 사용된 대표적인 경우는 바로 IBOutlet입니다. ViewController에서 storyboard를 통해 SubView를 생성하여 IBOutlet을 생성할 경우 다음과 같은 형태로 property가 설정됩니다.

{% highlight swift %}
class ViewController: UIViewController {
    @IBOutlet weak var myView: UIView!
}    
{% endhighlight %}

여기서도 weak이 사용되고 있습니다. 그 이유는 `UIViewController`와 `UIView` 모두 class로 작성된 reference type의 데이터이기 때문에 strong reference cycle이 발생할 수 있기 때문입니다.

## weak과 unowned의 차이

## Closure Strong Reference Cycle

---

---
layout: post
comments: true
title:  "Swift optionals - 2"
excerpt: "Swift의 optional Chaining에 대해 알아봅니다."
categories: Swift Language Optional
date:   2017-02-22 00:30:00
tags: [Swift, Language, Optional]
image:
  feature: swiftLogo.jpg
translate: false
---

이 글을 읽기 전에 optional에 대한 기본 개념을 모르시는 분들은 아래 글을 먼저 읽어 주세요. 여기서는 기본적인 optional 개념을 안다는 전제하에 Optional Chaining에 대해서만 서술합니다.

[Swift optional -1 ](https://hcn1519.github.io/articles/2017-01/swift_optionals)

## Optional Chaining 개념

Apple에서 설명하고 있는 Optional Chaining의 정의는 다음과 같습니다.

<div class="message">
  Optional chaining is a process for querying and calling properties, methods, and subscripts on an optional that might currently be nil. ... Multiple queries can be chained together, and the entire chain fails gracefully if any link in the chain is nil.
</div>

<div class="message">
  Optional Chaining이라는 것은 속성, 메소드, subscripts에 대해 질의하고, 호출하는 하나의 프로세스입니다. ... 여려 개의 query가 묶여서 나타날 수 있고, 전체 연결은 하나라도 nil이라면 실패합니다.(nil 반환)
</div>

일단은 감만 잡고, 아래에서 예제를 살펴 본 뒤 다시 한 번 의미를 생각해보시면 무슨 의미인지 이해하실 수 있습니다.

{% highlight swift %}
class Person {
    var residence: Residence?
}
class Residence {
    var numberOfRooms = 1
}
let john = Person()
{% endhighlight %}

다음과 같은 2개의 클래스 <code>Person</code>과 <code>Residence</code>를 정의하겠습니다. 그리고 <code>john</code>이라는 인스턴스를 생성하였습니다. 이 때 <code>john.residence!.numberOfRooms</code>는 어떤 값을 가질까요? 표현이 다소 어색할 수 있습니다만, 이런 표현은 Swift에서 자주 쓰입니다.
1. <code>john</code>은 <code>Person</code> class로 선언 되었으므로 residence 변수를 가지고, 해당 변수는 <code>Residence?</code>형입니다.
2. <code>Residence</code> class는 <code>numberOfRooms</code> property를 지니고 있으므로 <code>john</code>부터 시작하여 <code>numberOfRooms</code>까지의 **쿼리** 는 오류가 아닙니다.

하지만, 해당 코드의 결과는 에러입니다. 왜냐하면, <code>residence</code> 변수는 <code>Residence?</code>형인데, 아직 값이 없기 때문입니다.

{% highlight swift %}
print(john.residence!.numberOfRooms)
# error

john.residence = Residence()
print(john.residence!.numberOfRooms)
# 1
{% endhighlight %}

이처럼 <code>!</code>를 활용하여 Optional 값을 받아오는 것을 Forced unwrapping이라고 합니다. Forced unwrapping은 쉽게 에러를 낼 수 있기 때문에 항상 값이 있다고 보장할 수 있는 경우에만 사용하는 것이 권장됩니다. 그런데 Optional Chaining은 이러한 상황에서 좀 더 안전하게(nil이 안 나오도록) 코드를 짤 수 있게 해줍니다.

{% highlight swift %}
if let roomCount = john.residence?.numberOfRooms {
    print("residence에 값이 있습니다. 값 : \(roomCount)")
} else {
    print("residence is nil")
}
# residence is nil 출력
{% endhighlight %}

위의 코드를 보시면 unwrap과 다르게 <code>?</code>(<code>john.residence?.numberOfRooms</code>)를 사용하는 것을 볼 수 있습니다. 이 때, <code>if let roomCount = john.residence?.numberOfRooms</code>은 해당 chain에(<code>residence?</code>와 <code>numberOfRooms</code>) 값이 있는지 없는지를 체크하고, **하나라도** 없으면 false를 반환합니다.

정리하자면,
<div class="message">
  Optional Chaining은 Optional 값이 하나라도 포함되어 있는 질의의 연결(chain)을 처리하는 프로세스입니다.
</div>

<br/>

## Optional Chaining Drill Down

Optional Chaining의 유용함은 복잡하게 얽혀 있는 여러 모델들의 값을 drill down하여 (있는 경우에만) 가져올 수 있게 해주고, 값이 없는 경우 값을 설정할 수 있도록 해주는 것에 있습니다. 값을 있는 경우에 가져오는 예제는 앞서 서술한 예시를 통해 나타납니다.

{% highlight swift %}
if let roomCount = john.residence?.numberOfRooms {
    print("residence에 값이 있습니다. 값 : \(roomCount)")
} else {
    print("residence is nil")
}
# residence is nil 출력
{% endhighlight %}

위의 예제를 조금 변형해서 <code>numberOfRooms</code>의 값이 없는 경우 값을 설정할 수도 있습니다.

{% highlight swift %}
let john = Person()
john.residence = Residence
if let roomCount = john.residence?.numberOfRooms {
    john.residence?.numberOfRooms = 3
}
print(john.residence!.numberOfRooms)
# 3 출력
{% endhighlight %}

유의할 점은 Optional chaining에 속한 값은 항상 Optional 값만을 반환한다는 것입니다. 즉, <code>john.residence!.numberOfRooms</code>은 <code>Int</code>형을 반환하는 것이 아니라, <code>Int?</code>형을 반환합니다. 또한, Optional 변수가 여러개 연결되어 있어도 그 값은 Optional이 중첩되는 것이 아니라, 그냥 Optional입니다. 예를 들어 <code>john.residence?.place?</code>(place를 String? 타입으로 가정합니다.)는 <code>Optional(Optional(값))</code>이 아니고, 항상(설령 Optional chain이 더 길어져도) <code>Optional(값)</code>의 형태를 유지합니다.

좀 더 자세한 설명은 Apple Swift language 책을 참고해주세요.

<br/>

##### 더 볼만한 추가 자료
- [Apple blog - Optional Chaining](https://developer.apple.com/library/content/documentation/Swift/Conceptual/Swift_Programming_Language/OptionalChaining.html#//apple_ref/doc/uid/TP40014097-CH21-ID245)
- [Optional binding과 Optional Chaining 이해하기](http://rshankar.com/optional-bindings-in-swift/)

<br/>

> 참고자료 : Apple Inc. The Swift Programming Language (Swift 3.0.1)

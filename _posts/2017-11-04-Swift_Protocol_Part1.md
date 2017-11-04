---
layout: post
comments: true
title:  "Swift Protocol - Part1"
excerpt: "Swift의 Protocol의 기본문법에 대해 알아봅니다."
categories: Swift Protocol
date:   2017-11-03 00:30:00
tags: [Swift, Protocol]
image:
  feature: swiftLogo.jpg
---

이번 포스팅에서는 Swift의  `Protocol`에 대해 알아보고자 합니다.

<div class="message">
A protocol defines a blueprint of methods, properties, and other requirements that suit a particular task or piece of functionality.
</div>

`Protocol`은 자신을 따르는 어떤 객체가 구현해야 하는 필요 요건을 서술한 것입니다.   
1. 여기서 객체가 의미하는 것은 `class` 뿐만 아니라, `struct`, `enum`을 포함합니다.
2. 객체들이 `Protocol`을 따르게 되면 컴파일시 이 필요 요건을 충족하는 지 확인합니다.

## Protocol Syntax
`Protocol`은 다음과 같은 문법으로 사용됩니다.

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

`Protocol`은 `class` 상속과 유사한 형태로 사용됩니다. 다만 Swift에서 하나의 `class`만 상속할 수 있는 것을 달리 객체는 복수의 `Protocol`을  따를 수 있습니다. 또한, 특정 `class`는 부모클래스를 상속하면서 `Protocol`도 따르는 형태로 구현될 수도 있습니다.

## Requirements
`Protocol`을 따르는 객체가 충족시켜야하는 요건이라는 것은 일반적으로 **특정 프로퍼티를 필수로 구현해야 하는 것**, 혹은 **특정 메소드를 필수로 구현해아 하는 것** 과 그 의미가 거의 같습니다. 그렇기 때문에 `Protocol`에는 이를 따르는 객체들의 구현해야 할 프로퍼티와 메소드의 조건이 쓰여져야 합니다.

## Property Requirements
먼저 Property가 `Protocol`에서 어떻게 쓰여야하는지 살펴 보겠습니다.

{% highlight swift %}
protocol 프로토콜1 {
    var 변수1: Int { get set }
    var 변수2: String { get }
    var 변수3: String { get }
    var 변수4: String? { get }
}
{% endhighlight %}

1. `Protocol`에서 Property는 모두 `var`로 선언됩니다.
2. `Protocol`은 어떤 **조건** 이기 때문에, 변수의 이름과 타입만 쓰고 변수의 값은 쓰지 않습니다.
3. `Protocol`은 변수가 `gettable` 여부, `settable` 여부를 위의 예시처럼 표현합니다. 이 때, 상수형(let)을 적용하기 위해서는 변수가 `{get set}` 형태이어서는 안됩니다. 상수는 immutable하기 때문이죠.

위의 `Protocol`을 따르는 객체를 생성하면 다음과 같이 될 수 있습니다.

{% highlight swift %}
struct 어떤객체: 프로토콜1 {
    var 변수1: Int
    var 변수2: String
    let 변수3: String
    var 변수4: String?
}
{% endhighlight %}

## Method Requirements

메소드 같은 경우에도 `Protocol`에서는 메소드의 body를 작성하지 않고, 함수명, 파라미터, 리턴 타입만을 명시합니다.

{% highlight swift %}
protocol 프로토콜1 {
    var 변수1: Int { get set }
    var 변수2: String { get }
    var 변수3: String { get }
    var 변수4: String? { get }
}
protocol 프로토콜2 {
    var 변수5: Int { get set }
    func 메소드1(a: Int, b: String) -> Int

    // 값을 변경 시키는 메소드는 mutating 키워드를 사용해야 합니다.
    mutating func 메소드2()
}

struct 객체1: 프로토콜1, 프로토콜2 {
    var 변수5: Int

    func 메소드1(a: Int, b: String) -> Int {
        return -1
    }

    mutating func 메소드2() {
        변수1 += 1
    }

    var 변수1: Int
    var 변수2: String
    let 변수3: String
    var 변수4: String?
}
{% endhighlight %}

---
layout: post
comments: true
title:  "Swift ControlFlow"
excerpt: "Swift의 fallthrough, Labeled Statement, guard에 대해 알아봅니다."
categories: Swift ControlFlow, Optional
date:   2017-05-10 00:30:00
tags: [Swift, Language, ControlFlow, Optional]
image:
  feature: swiftLogo.jpg
---


일반적으로 프로그래밍 언어를 익힐 때, **ControlFlow** 라 하면 `if` 구문과 같은 것들을 활용하여 프로그램이 원하는 방향으로 작동되도록 하는 것을 말합니다. 여기서는 대부분 언어에서 발견할 수 있는 `if`, `switch`, `continue`, `break` 등에 대해 알아보기 보다는 Swift에서 발견할 수 있는 특징적인 **ControlFlow** 에 대해 알아보도록 하겠습니다.

## Value binding

<div class="message">
  Value binding은 switch문 실행시 조건문 안에서 활용할 수 있는 변수를 할당하는 것을 말합니다.
</div>

`Value binding`의 예제를 살펴보겠습니다.

{% highlight swift %}
let myCondition = 10

switch myCondition {
case let con:
    print("Condition이 \(con)입니다.")
case let con:
    print("Condition2 : \(con)")    
default:
  print("Switch default")
}
// 결과 : Condition이 10입니다.
{% endhighlight %}

위의 예제에서 `case let con:`은 해당 case의 구문 안에서 `con`이라는 변수를 사용할 수 있도록 해줍니다. 이것이 바로 `Value binding`입니다. 그런데 조금 의아한 부분이 있습니다. `Value binding` 자체가 하나의 조건이 될 수 있나하는 것인데, 테스트해보니 `Value binding`은 기본적으로 true가 되네요. `Value binding`은 모양 자체가 `if`에서 쓸 수 있는 `Optional binding`과 형태가 유사합니다. 다만 `Value binding`은 Optional 값을 unwrap 해주지는 않습니다. 반대로 `Optional binding`은 Optional 값일 때만 사용할 수 있는 차이점이 있습니다.

{% highlight swift %}
let test: Int?
test = 3

switch test {
case let con:
    print("값 - \(con)")
}

if let val = test {
    print("값 - \(val)")
}
// 결과 : 값 - Optional(3)
//       값 - 3
{% endhighlight %}

## Where

<div class="message">
  Where는 switch문 실행시 case에 추가적인 조건을 주는 기능을 합니다.
</div>

`Where`는 case 자체의 조건에 추가적인 조건을 부여할 수 있도록 해줍니다. 예시를 살펴보겠습니다.

{% highlight swift %}
let myCondition = 10
let condition2 = 3

switch myCondition {
case 10 where condition2 < 5:
    print("조건을 만족합니다.")
default:
    print("Switch default")
}
// 결과 : 조건을 만족합니다.
{% endhighlight %}

여기서 `myCondition`이 10인 case의 조건과 `condition2`가 5보다 작은 두 가지 조건을 모두 만족해야만 `조건을 만족합니다.`가 출력됩니다. 쉽게 생각하면 if의 `&&`로 조건을 연결하는 것을 생각하시면 됩니다.

## Fallthrough

`fallthrough`는 `switch`와 연관된 키워드로 `switch`를 사용할 때, `default` case가 항상 작동하도록 해주는 키워드입니다. Swift는 `switch`를 사용할 때 case별로 `break`를 따로 작성해주지 않아도 해당 case의 조건을 만족한다면, 그 case의 내용만 실행하고 `switch`에서 빠져나오게 됩니다. 그런데 여기서 `fallthrough`는 `fallthrough`가 작성된 시점에서 case를 더이상 실행하지 않고, 바로 `default`로 넘어가도록 해줍니다.

{% highlight swift %}
let myCondition = 10

switch myCondition {
case 10:
    print("Condition이 10입니다.")
    fallthrough
default:
    print("Switch 종료")
}
// 결과 : Condition이 10입니다.
//       Switch 종료
{% endhighlight %}

위의 예의 경우 `fallthrough`가 없다면 `Condition이 10입니다.`만 실행하고 switch는 종료됩니다. 하지만, `fallthrough`가 있기 때문에 `default` case도 함께 실행됩니다.

{% highlight swift %}
let myCondition = 10

switch myCondition {
case 10:
    fallthrough
    print("Condition이 10입니다.")
default:
    print("Switch 종료")
}
// 결과 : Switch 종료
{% endhighlight %}

두 번째 예에서는 `fallthrough`가 `print("Condition이 10입니다.")`보다 앞에 작성되어 있습니다. `fallthrough`를 만나면 바로 `default` case로 넘어가므로 해당 print문은 실행되지 않고 `default` case의 print만 실행됩니다.

## Labeled Statement

Swift에서는 `if`, `switch`, 혹은 `Loop`에 이름을 부여할 수 있습니다. 이렇게 부여된 이름은 여러개가 중첩된 조건문, 반복문에서 어떤 것을 `break`하고 `continue`할지를 명시할 수 있게 해줍니다. 이름은 해당 조건문, 반복문 시작에 쓰입니다. 예제를 살펴보겠습니다.

{% highlight swift %}
let myCondition = 10

LoopOne: for i in 1...5 {
    switchOne: switch myCondition {
    case 10 where i < 3:
        print("조건을 만족합니다.")
        break switchOne
    default:
        print("Switch default")
        break LoopOne
    }
}
// 결과 : 조건을 만족합니다.
//       조건을 만족합니다.
//       Switch default
{% endhighlight %}

위의 예제에서 나오는 for 루프는 `LoopOne`이라는 이름을 갖게 됩니다. 또한 switch 구문은 `switchOne`이라는 이름을 갖습니다.(이름을 갖는 것일 뿐, 변수로 선언되는 것은 아닙니다.) 그에 따라 `break 이름`이라는 형태를 사용할 수 있습니다. 특정 조건문, 반복문을 멈추는 것을 명시적으로 보여줄 수 있도록 해주는 것입니다.

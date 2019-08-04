---
layout: post
comments: true
title:  "Swift ControlFlow"
excerpt: "Swift의 Value binding, fallthrough, Labeled Statement, guard에 대해 알아봅니다."
categories: Swift ControlFlow Optional Language
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
//        값 - 3
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

`fallthrough`는 `switch`와 연관된 키워드로 `switch`를 사용할 때, 코드 순서상의 다음 조건문을 실행시켜 줍니다. 이 때, 다음 조건문이 없다면 컴파일 에러가 발생합니다. Swift의 `switch`는 case별로 `break`를 따로 작성해주지 않아도 해당 case의 조건을 만족한다면, 그 case의 내용만 실행하고 `switch`에서 빠져나오게 됩니다. 그런데 여기서 `fallthrough`는 `fallthrough`가 작성된 시점에서 case를 더이상 실행하지 않고, 바로 다음 조건문을 실행하고, `switch`를 종료합니다.

{% highlight swift %}
enum MyCase {
    case a, b, c
}

let myCase = MyCase.a

switch myCase {
case .a:
    print("a")
    fallthrough
    print("after a") // will never be executed
case .c:
    print("c")
case .b:
    print("b")
}

// 결과 : a c

switch myCase {
case .a, .b, .c:
    print("a b c")
    fallthrough // 'fallthrough' without a following 'case' or 'default' block
}
{% endhighlight %}

1. `fallthrough`는 조건문 작성 순서에 영향을 받습니다. 위의 예시에서 a 다음 b가 아닌 c가 출력된 것에서 이를 확인할 수 있습니다. 조건을 a 다음 b로 쓴다면 a, b가 출력됩니다.
1. `fallthrough`는 실행할 다음 조건문이 없다면 컴파일 에러가 발생합니다.

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
//        조건을 만족합니다.
//        Switch default
{% endhighlight %}

위의 예제에서 나오는 for 루프는 `LoopOne`이라는 이름을 갖게 됩니다. 또한 switch 구문은 `switchOne`이라는 이름을 갖습니다.(이름을 갖는 것일 뿐, 객체로 활용할 수 있는 것은 아닙니다.) 그에 따라 `break 이름`이라는 형태를 사용할 수 있습니다. 특정 조건문, 반복문을 멈추는 것을 명시적으로 보여줄 수 있도록 해주는 것입니다.

## guard

`guard`도 `if`나 `switch` 같은 조건문을 만드는 데 쓰이는 것입니다. 독특한 점은 항상 `else`를 동반한다는 점입니다. 그 기본 형태는 아래와 같습니다.

{% highlight swift %}
guard 조건 else {
  // 조건을 만족하지 않으면 실행
}
// 조건 만족시 계속 진행
{% endhighlight %}

형태는 이렇습니다만, `if`처럼 아무데나 쉽게 쓸 수 있지는 않습니다. 왜냐하면 `guard`는 **실행되는 위치(enclosing scope)에서 벗어나는 것** 을 항상 필요로 하기 때문입니다. 그래서 일반적으로 main thread에서 쉽게 `if`를 쓰는 것과는 달리, `guard`를 사용하게 되면 main thread를 빠져나가는(프로그램이 꺼지거나 죽는) 것을 만들어주어야 하는 것을 필요로 하므로 거의 사용하지 않습니다.(혹시 사용하는 예제가 있다면 알려주시면 감사하겠습니다.)

`guard`는 이러한 이유 때문에 주로 함수 안에서, 함수를 return하는 조건(실행되는 위치에서 벗어나는 조건)과 함께 사용됩니다. 예제를 살펴보면 다음과 같습니다.

{% highlight swift %}
func hello() -> Int {
    let a = 1
    guard a == 1 else {
        print("else 안입니다.")
        return 0
    }
    return 1
}
print(hello())
// 결과 : 1
{% endhighlight %}

위의 예제에서 `a==1`이라는 조건은 만족되므로, `else` 안은 실행되지 않고 그대로 통과합니다. 그러므로 1이 return 됩니다.

## guard with Optional binding

`guard`가 많이 사용되는 경우는 `Optional Binding`을 할 경우입니다. `guard`의 조건문은 `if` 조건문에서처럼 `Optional Binding`을 활용할 수 있습니다. 이 때, 값이 nil이 아니어서 변수가 할당 된다면 이는 `guard`가 끝난 후에도 남아 있어서 값이 unwrap된 상태로 사용할 수 있습니다. 예시를 봐보겠습니다.

{% highlight swift %}
func myPrint(name: String?) {
    guard let name = name else {
        print("exiting...")
        return
    }
    print("이름 - \(name)")
}
myPrint(name: "Tom")
myPrint(name: nil)

// 결과 : 이름 - Tom
//        exiting...
{% endhighlight %}

위의 예시에서 name은 `guard`를 통해 unwrap되고, `guard`가 끝난 후에도 남아 있습니다. 그렇기 때문에 `print`에서 name은 unwrap된 상태가 되고 Tom이 출력됩니다. 이 때, name의 값이 nil이라면 `exiting...`이 출력되면서 함수는 return됩니다.

## guard in Practice

`guard`의 가장 큰 장점은 가독성을 높여주는 것에 있습니다. 사용자가 회원가입을 하는 경우를 생각해보겠습니다. 이 때, 올바른 정보를 받기 위해서는 사용자가 어떤 정보를 누락하고, 어떤 정보를 입력했는지를 정확히 알 필요가 있습니다. 사용자에게 이름, 이메일, 비밀번호의 정보를 받는 회원가입을 할 경우를 `if let`으로 작성해보면 아래와 같습니다.

{% highlight swift %}
func checkValidation() {
  if let name = nameLabel.text {
    if let email = emailLabel.text where email.containsString("@") {
      if let password = passwordLabel.text {
        // 모든 경우 만족
        let newUser = User()
        newUser.name = name
        newUser.email = email
        newUser.password = password
      } else {
        // 비밀번호 nil
        passwordLabel.becomeFirstResponder()
      }
    } else {
      // 이메일 nil 혹은 @ 없음
      emailLabel.becomeFirstResponder()
    }
  } else {
    // 이름 nil
    nameLabel.becomeFirstResponder()
  }  
}
{% endhighlight %}

유저의 정보가 올바르게 입력됐는지 확인하기 위해서는 이처럼 중첩으로 `if let`을 사용해야 합니다. 이는 정보가 많아지면 잘못된 부분을 쉽게 고치기 어렵습니다. 이 때 `guard` 를 쓰면 가독성이 매우 좋아집니다. 위의 내용을 `guard`를 활용해서 써보면 다음과 같습니다.

{% highlight swift %}
func checkValidation() {
  guard let name = nameLabel.text else {
      // 이름 nil
      nameLabel.becomeFirstResponder()
      return
  }
  guard let email = emailLabel.text where email.containsString("@") else {
      // 이메일 nil 혹은 @ 없음
      emailLabel.becomeFirstResponder()
      return
  }
  guard let password = passwordLabel.text else {
      // 비밀번호 nil
      passwordLabel.becomeFirstResponder()
      return
  }

  // 모든 경우 만족
  let newUser = User()
  newUser.name = name
  newUser.email = email
  newUser.password = password
}
{% endhighlight %}

`guard`를 사용하면, 중첩으로 조건문을 사용하는 것을 방지할 수 있고 코드의 가독성이 좋아집니다. 이외에도 json 데이터를 parsing할 경우에도 누락된 데이터를 파악하기 위한 조건문을 작성할 때 코드의 가독성이 높아지게 만들 수 있습니다.


-----

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 3.1)
* Raywenderlich - Optional
* [swift guard vs if let]("http://stackoverflow.com/questions/32256834/swift-guard-vs-if-let")

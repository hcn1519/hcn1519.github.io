---
layout: post
comments: true
title:  "Swift optionals - 1"
excerpt: "Swift의 optionals에 대해 알아봅니다."
categories: Swift Language Optional
date:   2017-01-19 00:30:00
tags: [Swift, Language, Optional]
image:
  feature: swiftLogo.jpg
translate: false
---

## Optionals 기본 개념

Swift에는 optional이라는 개념이 있습니다. optional은 '?'을 통해 표현되는데, 그 의미는 다음과 같습니다. **"이 변수에는 값이 들어갈 수도 있고, 아닐 수도 있어(nil)"** Swift에서는 기본적으로 변수 선언시 nil 값이 들어가는 것을 허용하지 않습니다. 그러므로 첫 번째 줄의 코드는 에러이고, 두 번째 줄은 Optional type(String?)으로 선언했으므로 에러가 아닙니다.
{% highlight swift %}
var optionalString: String = nil
var optionalString: String? = nil
{% endhighlight %}

다음 예시의 경우, String을 Int로 캐스팅하는 경우입니다.

{% highlight swift %}
let possibleNumber = "123"
let convertedNumber = Int(possibleNumber)

print(convertedNumber)
// 출력 결과 : Optional(123)
{% endhighlight %}

여기서 "123"은 String이기 때문에, Int(possibleNumber) 초기화에 실패합니다. 이 경우 바로 에러가 나와야한다고 생각하실 수 있지만, Swift는 이 경우 convertedNumber를 **Optional Int** 형(Int?)으로 선언합니다.(Int가 아닙니다.)

<br/>

## nil

**nil** 은 optional 변수 이외에서 사용할 수 없습니다. 그런데 iOS 개발을 할 경우 상당히 많은 부분에서 nil을 사용합니다. 그러므로 optional에 대해서 잘 알아두셔야 합니다. 또한 nil값은 따로 초기화하지 않아도 기본으로 설정됩니다.

{% highlight swift %}
var optionalString: String?
var optionalString2: String? = nil
// 두 값 모두 nil
{% endhighlight %}

다만 유의할 점은 Swift의 **nil** 은 다른 언어에서 pointer가 존재하지 않는 값을 가리키는 것과는 다릅니다. Swift의 **nil** 은 value가 없는 것을 의미합니다. 주소값 비교와 value값 비교정도로 이해하면 될 것 같습니다.

<br/>

## Wrapping

Optional에 대해 보다보면, 많은 곳에서 **wrapping** 이라는 개념이 나옵니다. Optional 타입은 기본적으로 wrap되어 있는 상태입니다. 즉, Optional 변수들은 제대로된 value가 있는 것인지, nil인 것인지 wrap되어 있어서 모르는 상태라고 생각하시면 됩니다. 그렇기 때문에(컴파일러 입장에서는 변수가 nil일 수도 있기 때문에) wrap된 상태에서는 설령 변수에 value값이 있다고 하더라도 바로 value가 출력되지 않습니다. 아래 예제를 보시면,

{% highlight swift %}
var optionalString: String? = "Hello"
print(optionalString)
// 출력 결과: Optional("Hello")
{% endhighlight %}

이 경우, optionalString이 nil일 수도 있기 때문에, 결과값 "Hello"가 출력되지 않고, **Optional("Hello")** 가 출력됩니다.

<br/>

## Forced Unwrapping

nil은 많은 곳에서 쓰이기 때문에, 변수를 optional로 사용하는 경우가 정말 많습니다. 그런데 앞선 예제에서처럼 출력 결과가 **Optional("Hello")** 처럼 나오는 것은 대부분의 경우 원하는 출력값이 아닙니다. 이 때 올바른 출력을 위해 사용하는 것이 **!(exclamation mark)**, 즉 느낌표입니다. 즉, optional로 선언했지만, **무조건 변수가 있는 상황이 보장된 경우** 느낌표(!)를 쓰면 우리가 원하는 Hello을 출력할 수 있습니다.

{% highlight swift %}
var optionalString: String? = "Hello"
print(optionalString!)
// 출력 결과: Hello
{% endhighlight %}

변수명 뒤의 느낌표는 Optional을 **unwrap** 합니다. Optional은 unwrap된 상태에서만 값을 제대로 출력할 수 있습니다. 느낌표를 활용한 다른 예제를 살펴보겠습니다.

{% highlight swift %}
let value1: String? = nil
let value2: String! = nil // 여기서는 에러가 아닙니다.

print(value) // nil 출력
print(value2) // error
{% endhighlight %}

이 경우, value1과 value2는 모두 Optional 타입입니다. 다만 value1은 아직 wrap되어 있는 상태이므로 print에서 문제가 되지 않습니다. 다만 값이 있다면 **Optional(값)** 형태로 출력이 될 것입니다. 다음으로 value2의 경우, 느낌표에 의해 Optional 값이 자동으로 unwrap됩니다. unwrap된 상태에서 값을 출력하면 런타임 에러가 발생합니다. 그러므로 일반적으로 위처럼 value2가 unwrap된 상태로 print하도록 놔두기보다는 if를 통해 값이 nil인 경우를 체크하고 출력을 합니다.

{% highlight swift %}
let value2: String! = nil
if value2 != nil {
    print(value2)
}
{% endhighlight %}

이번에는 헷갈릴 수 있는 예제를 봐보겠습니다.

{% highlight swift %}
class Square {
    var sideLength: Double

    init(sideLength: Double){
        self.sideLength = sideLength
    }
}
// 클래스를 Optional 타입(?)으로 선언
// sideLength1도 Optional 타입(?)으로 선언
// 값 출력시 !를 쓰면 정상 출력
let optionalSquare1: Square? = Square(sideLength: 2.5)
let sideLength1 = optionalSquare1?.sideLength

// 클래스를 Optional 타입(?)으로 선언
// sideLength2를 Optional 타입(!)으로 선언
// 값은 unwrap 상태이므로 !가 없어도 출력(있으면 !를 2번 쓰므로 에러)
let optionalSquare2: Square? = Square(sideLength: 2.5)
let sideLength2 = optionalSquare2!.sideLength

// sideLength3를 Optional 타입(!)으로 선언
// 이를 Implicitly Unwrapped Optional이라고 부릅니다.
// 클래스와 sideLength3 모두 unwrap 상태이므로 !가 없어도 출력(있으면 !를 2번 쓰므로 에러)
let optionalSquare3: Square! = Square(sideLength: 2.5)
let sideLength3 = optionalSquare3!.sideLength

print(optionalSquare1) // Optional(Square)
print(optionalSquare2) // Optional(Square)
print(optionalSquare3) // Square
print(sideLength1)  // Optional(2.5)
print(sideLength2)  // 2.5
print(sideLength3)  // 2.5
print(sideLength1!) // 2.5
print(sideLength2!) // error
print(sideLength3!) // error
{% endhighlight %}

<a href="http://stackoverflow.com/questions/24034483/what-is-an-unwrapped-value-in-swift">원글(stackoverflow) 자료 보기</a>

<br/>

## Optional Binding

Optional Binding은 Optional 타입으로 선언된 변수에 값이 있는지 없는지를 확인할 수 있도록 해주는 기능입니다. Optional Binding을 사용하면 **느낌표 없이** Optional 타입의 변수 값을 출력할 수 있어서 좀 더 안전한 형태로 값을 얻을 수 있습니다. 기본적인 형태는 다음과 같습니다.

{% highlight swift %}
if let 변수명 = Optional 변수 {
  // 임시 변수에 Optional 변수의 value값이 할당됩니다.
}
{% endhighlight %}

무슨 의미인지 알기 위해 예제를 살펴 보겠습니다.

{% highlight swift %}
// Optional type으로 선언한 myNumber
let myNumber: Int? = 1234

if let actualNumber = myNumber {
    print("\(myNumber)은 실제로 \(actualNumber)입니다.")
} else {
    print("\(myNumber)는 변환될 수 없습니다.")
}
// 출력 결과 : Optional(1234)은 실제로 1234입니다.

print(actualNumber) // error
{% endhighlight %}

위의 예에서는 <code>myNumber</code>가 Optional 타입으로 선언되어 있습니다. 원래는 이 <code>myNumber</code>값을 출력하기 위해서는 !를 사용해야합니다. 하지만, Optional Binding은 먼저 이 myNumber의 값이 있는 경우와 없는 경우로 나누고, 값이 있는 경우를 <code>if let</code> 구문 안에 넣을 수 있습니다. 여기서는 <code>actualNumber</code>에 <code>myNumber</code>의 값을 할당하고, 값이 있다면 actualNumber에 이를 넘겨주어 바로 실제 값으로 사용할 수 있도록 해줍니다. 특이한 점은 actualNumber가 if문 안에서만 할당되는 로컬 변수라는 점입니다. if 밖에서는 actualNumber를 사용할 수 없습니다. 또한,

{% highlight swift %}
if let firstNumber = Int("4"), let secondNumber = Int("42"), firstNumber < secondNumber && secondNumber < 100 {
    print("\(firstNumber) < \(secondNumber) < 100")
}
// 출력 결과: 4 < 42 < 100
{% endhighlight %}

위의 경우처럼 Optional value가 nil인지 여부와 함께 boolean 결과를 콤마로 연결해서 사용할 수도 있습니다.

<div class="message">
  Optional Binding은 Optional type의 변수에 대한 nil 체크와 로컬변수에 이 값을 할당하는 두 가지 기능을 가지고 있습니다.
</div>

>내용 출처 : The swift Programming Language(3.0.1), stackoverflow(what is an unwrapped value in swift)

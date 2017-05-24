---
layout: post
comments: true
title:  "Swift의 함수 사용"
excerpt: "Swift의 함수 사용에서 특별한 기능들을 알아봅니다."
categories: Swift Function
date:   2017-05-23 00:30:00
tags: [Swift, Language, Function]
image:
  feature: swiftLogo.jpg
---

Swift 함수의 기본적인 형태는 다음과 같습니다.

{% highlight swift %}
func 함수명(인자이름 인자변수: 인자타입) -> (리턴 타입) {
  var answer = 0
  return answer
}

함수명(인자이름: 0)
{% endhighlight %}

다른 언어를 공부해보았다면 비슷한 부분이 많이 보일 것입니다. 여기서는 그 중 다른 언어에는 많지 않고, Swift에서 특별히 찾아볼 수 있는 것들을 살펴보겠습니다.

## Argument Label(인자 이름)

Swift에서는 함수의 인자를 정의할 때 `Argument Label(인자 이름)`이란 것을 정의해주어야 합니다. 인자이름이라는 것은 말 그대로 인자가 무엇을 위한 기능을 하는지 보여주는 이름으로, 따로 설정하지 않으면 인자변수명이 기본값으로 들어가게 됩니다. 굳이 이름이 존재하는 이유는 함수를 호출하는 곳에서 의미를 명확히 알고, 함수 내부에서는 이를 좀 더 유연하게 변형해서 쓰도록하기 위함이 아닌가 싶습니다.

{% highlight swift %}
func jump(height h: Int) {
  print("\(h)미터 점프")
}

jump(height: 5) // 5미터 점프
{% endhighlight %}

다만, 함수를 호출할 때에도 인자이름을 쓰는 것이 번거로울 경우도 있습니다. 이 때는 `_`를 통해 인자이름을 생략해서 쓸 수 있습니다.

{% highlight swift %}
func jump(_ h: Int) {
  print("\(h)미터 점프")
}

jump(5) // 5미터 점프
{% endhighlight %}

여기서 간단한 함수명 작성의 간단한 convention을 알려드리겠습니다. Swift 책이나 예제 같은 것들을 보면, `jump(height:)` 같은 표현을 찾아볼 수 있습니다. 분명 `jump`는 함수명인데 뒤에 `height:` 같은 것들이 붙어 있는 것입니다. 저것들이 바로 인자이름들입니다. 위에서 인자이름을 `height`이라고 지었다면 `jump(height:)` 다음과 같이 함수를 적습니다. 이 때 두 번째 예시에서처럼 인자이름을 생략했다면 `jump(_:)`이 됩니다. 인자가 여러 개라면, 위 조건에 맞추어 `jump(_:time:_:)` 함수명을 만들어 나가면 됩니다.

## 리턴 타입 명시

Swift는 함수에 리턴타입이 필요할 경우 이를 `->`를 이용하여 표현합니다. 이 때 `->` 뒤에 `(리턴타입)`을 써주어 어떤 데이터 타입을 리턴할 것인지를 표현합니다.

{% highlight swift %}
func getOlder(age a: Int) -> (Int) {
  return (a += 1)
}

let newYearAge = getOlder(age: 20) // newYearAge = 21
{% endhighlight %}

## Variadic Parameters

`Variadic Parameters`는 함수의 파라미터로 여러 개의 값을 넘길 수 있도록 해주는 기능입니다. 이는 `데이터타입...` 형태로 표현되고, 전달하는 파라미터를 배열로 받아서 함수 안에서 사용할 수 있도록 해줍니다.

{% highlight swift %}
func average(numbers: Double...) -> Double {
    var total = 0.0

    for item in numbers {
        total += item
    }
    return (total/Double(numbers.count))
}

let avg = average(numbers: 10, 15, 20) // 15
let avg2 = average(numbers: 1, 3, 5, 7, 9) // 5
{% endhighlight %}

파라미터로 배열을 쓰는 것과 큰 차이는 없어보입니다만, 배열 생성의 번거로움을 줄일 수 있기 때문에 유용한 기능이라고 생각됩니다.

## Inout Parameters

`Inout`은 함수에서 직접 파라미터 값에 접근할 수 있도록 해주는 기능입니다. 즉, 파라미터로 변수의 `주소값`을 넘겨 직접 접근할 수 있도록 해주는 기능입니다. 사용방법은 다음과 같습니다.

{% highlight swift %}
func swap(_ a: inout Int, _ b: inout Int) {
    let temp = a
    a = b
    b = temp
}

var x = 15
var y = 47

swap(&x, &y)

print(x) // 47
print(y) // 15
{% endhighlight %}

함수에 주소값을 넘기기 위해서는 위처럼 `inout` 키워드를 데이터 타입 앞에 써주어야 합니다. 그리고 함수를 호출할 때, 변수의 값을 넣는 것이 아니라, `&변수명`을 넣습니다. 이 떄 `inout`을 사용한 함수는 일반 Swift 함수와 다른 점이 있습니다. Swift의 함수는 기본적으로 함수의 모든 인자가 함수를 호출할 때 `상수`로 호출됩니다. 즉, 넘어온 값을 바꿀 수 없습니다. 그렇기 때문에,

{% highlight swift %}
func swap(_ a: Int, _ b: Int) {
    let temp = a
    a = b // error
    b = temp
}
func swap2(_ a: Int, _ b: Int) {
    var a = a // mutable하게 변경
    let temp = a
    a = b
    b = temp
}
{% endhighlight %}

위와 같은 식은 `a`의 값이 `immutable`하기 때문에 컴파일 에러입니다. 그래서, `a`의 값이 바뀔 수 있도록 허용하려면 위의 `swap2(_:_:)`처럼 `var a = a`를 써주어야 합니다. 하지만 `inout`을 사용한다는 것은 기본적으로 값을 `변경`하는 의미를 내포하고 있습니다. 그렇기 떄문에, 파라미터는 기본적으로 `mutable`합니다.

-----

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 3.1)

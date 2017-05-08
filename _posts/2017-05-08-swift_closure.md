---
layout: post
comments: true
title:  "Swift Closure"
excerpt: "Swift의 closure에 대해 알아봅니다."
categories: Swift Closure
date:   2017-05-08 00:30:00
tags: [Swift, Language, Closure]
image:
  feature: swiftLogo.jpg
---

Closure는 익명함수로 알려진 기능으로, 함수를 `func` 키워드로 선언하는 것이 아니라, 함수를 `변수에 선언하는 형태`를 취하고 있습니다. Closure는 코드를 간결하고, 직관적으로 작성하는 데 많은 도움을 주는 기능입니다. 일반 함수와 Closure의 사용 방식의 차이를 통해 Closure에 대해 알아보겠습니다.

#### 일반적인 함수 사용
{% highlight swift %}
var counter = 0
func addCounter() {
  counter += 1
}
addCounter()
addCounter()

print(counter) // 결과 2
{% endhighlight %}

일반적인 함수는 다음과 같이 함수명을 설정(`addCounter`)하고, 해당 함수명으로 함수를 호출하는 형태를 취합니다.

#### Closure 사용

{% highlight swift %}
var counter = 0
let addCounter = {
    counter += 1
}
addCounter()
addCounter()

print(counter) // 결과 2
{% endhighlight %}

Closure는 변수에 값을 선언하는 대신에 변수에 **함수** 를 선언합니다. 여기서는 `addCounter` 변수에 함수를 선언하였습니다. 그리고 이 변수는 함수처럼 호출을 할 수 있습니다.(`addCounter()` 형태)

## Closure 기본 형태

Closure는 기본적으로 **header** 와 **body** 를 가진 형태로 구성되어 있습니다.
{% highlight swift %}
var closure = { header in body }
{% endhighlight %}

여기서 header에서는 인자와 리턴타입을 명시합니다. body에서는 호출시 실행되는 함수의 내용을 작성합니다. `in` 키워드는 header와 body를 나누는 키워드입니다.

<img src="https://dl.dropbox.com/s/vtfw9hc6pavmzxl/closure%20Expression.png">

애플의 Swift 공식 가이드 문서에서는 Closure를 `sorted(by:)` 메소드를 통해 설명합니다. `sorted(by:)` 메소드는 Swift 내장 메소드로 배열을 by 이하의 기준에 따라 정렬하는 메소드입니다. 이 때 그 기준은 배열에 있는 데이터 타입들 간의 **대소 비교** 를 통해 이뤄집니다. 즉, 배열의 두 값을 가져와 그 크기를 비교하여 앞의 값이 뒤의 값보다 이전에 와야하면 `true`를 그렇지 않으면 `false`를 반환하는 것을 반복하고(오름차순 기준) 그 결과에 따라 정렬합니다.

{% highlight swift %}
let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]
let numbers = [4,3,2,6,1]

// 배열 내의 데이터 타입에 따라 필요한 인자가 다릅니다.
names.sorted(by: (String, String) -> Bool)
numbers.sorted(by: (Int, Int) -> Bool)
{% endhighlight %}

이 때, `by`에서 필요한 값은 Bool을 반환하는 함수의 형태로, 일반적인 함수 혹은 closure가 들어가게 됩니다. 이에 따라 다음과 같은 형태들이 `sorted(by:)`의 인자로 들어가게 됩니다.

{% highlight swift %}
let names = ["Chris", "Alex", "Ewa", "Barry", "Daniella"]

// s1이 s2보다 클 때, 앞에 와야한다를 의미
// "Chris"가 "Alex" 보다 크고 이 때 true이므로 "Chris"가 "Alex"보다 배열의 앞쪽에 위치합니다.
// 결과적으로 배열 전체가 내림차순으로 정렬됩니다.
func backward(_ s1: String, _ s2: String) -> Bool {
    return s1 > s2
}

var reversedNames = names.sorted(by: backward)

var reverse2 = names.sorted(by: { (s1: String, s2: String) -> Bool in return s1 < s2 })
{% endhighlight %}

위의 경우 `reversedNames`는 `sorted(by:)`의 인자를 일반 함수(`backward`)로 받은 형태이고, `reverse2`는 `sorted(by:)`의 인자를 closure로 받은 것입니다.

## Closure 축약

Closure의 짧지만 직관적인 코드 작성에 크게 기여하는 것이 바로 축약형입니다. 반대로, 어떤 경우 축약을 하는지 모른다면 어떻게 Closure가 작동하는지 모르게 되는 상황에 직면하게 됩니다. 여기서는 Closure에서 어떤 경우 표현을 생략할 수 있는지 알아보겠습니다.

#### 1. Type Inferring

<div class="message">
  Closure는 어떤 타입의 데이터가 인자로 들어오고, return 값이 어떤 것인지 미리 알고 있다면 이를 생략할 수 있습니다.
</div>

{% highlight swift %}
names.sorted(by: { (s1: String, s2: String) -> Bool in return s1 < s2 })

// 데이터 타입 생략
names.sorted(by: { (s1, s2) in return s1 < s2 })
{% endhighlight %}

앞서 언급한 `sorted(by:)` 메소드의 파라미터 함수는 항상 배열의 데이터 타입을 가진 인자 두 개를 지니고, `Bool` 타입을 리턴합니다. 즉, 어떤 데이터 타입이 필요한지 이미 알려져 있어서 closure는 이를 **추론** 할 수 있습니다. 그러므로 이는 모두 생략 가능합니다. 다른 예시를 살펴 보겠습니다.

{% highlight swift %}
var multiply: (Int, Int) -> Int = { (a: Int, b: Int) in return a * b }

// 데이터 타입 생략
var multiply: (Int, Int) -> Int = { (a, b) return a * b }
{% endhighlight %}

위에서 `multiply`는 받은 두 값을 곱한 값을 반환하는 변수입니다. 이 때, 여기서는 변수를 선언할 때 타입을 `(Int, Int) -> Int`로 명시를 했기 때문에, Closure에서 이미 어떤 데이터 타입이 인자로 오고 어떤 데이터 타입을 리턴하는지 알고 있습니다. 그러므로 Closure 내부에서는 이를 생략할 수 있습니다.

#### 2. Single Expression Closure의 "return" keyword 생략

<div class="message">
  Single Expression Closure는 `return` 키워드를 생략할 수 있습니다.
</div>

{% highlight swift %}
// return 키워드 생략
names.sorted(by: { (s1, s2) in s1 < s2 })
var multiply: (Int, Int) -> Int = { (a, b) a * b }
{% endhighlight %}

다음과 같이 `return` 키워드 없이 Closure를 작성할 수 있습니다.

#### 3. Short-hand argument name

<div class="message">
  Closure 내부로 들어오는 인자들은 항상 이름을 정의하지 않아도, 순서대로 `$0`, `$1`의 이름으로 사용할 수 있습니다.
</div>

{% highlight swift %}
// 축약형 인자 이름 사용
names.sorted(by: { $0 < $1 })
var multiply: (Int, Int) -> Int = { $0 * $1 }
{% endhighlight %}

다음과 같은 형태로 사용할 수 있습니다.

#### 4. Operator Methods를 통한 축약

위의 경우까지는 Closure에서 자주 통용될 수 있는 방법이고, operator(연산자)를 이용한 축약은 두 값을 연산하는 것이 결과로 나오는 특별한 경우이기 때문에 사용할 수 있는 축약입니다. 그 형태를 살펴보면,

{% highlight swift %}
names.sorted(by: <)
var multiply: (Int, Int) -> Int = (*)
{% endhighlight %}

다음과 같습니다. `sorted(by:)` 메소드는 항상 **두 값의 크기 비교를 통해 Bool을 반환** 하므로 연산자(`<`)만 쓰는 것으로도 그 의미를 알 수 있습니다. 또한 `multiply`의 경우에도 항상 **두 값을 곱한 값을 반환** 하므로 연산자(`*`)만으로도 연산을 모두 알 수 있습니다. 그렇기 때문에 위와 같은 축약이 가능합니다.

## 함수로 Closure 전달하기

Closure는 `변수`에 저장되기 때문에 변수를 함수에 넘길 수 있는 것처럼, Closure도 함수로 넘길 수 있습니다. 그 형태는 일반적인 변수를 넘기는 것과 동일하여 `func  함수명(label 변수명: 변수타입)` 이 조건에 맞게만 써주면 됩니다.

{% highlight swift %}
var hello: () -> Void = { print("Hello~") }

func runClosure(name aClosure: () -> Void) {
    aClosure()
}

runClosure(name: hello) // Hello~
{% endhighlight %}

#### Trailing Closure를 활용한 Syntax Sugar

Trailing Closure는 함수의 호출시 Closure를 인자로 넘길 때, Closure가 지나치게 길어질 경우 이를 함수와 분리해서 쓸 수 있는 Syntax Sugar입니다. 즉 위의 코드는 몇 가지 형태로 호출될 수 있습니다.

{% highlight swift %}
// 인자를 전달하는 형태
runClosure(name: hello) // Hello~
runClosure(name: { print("anther closure") })

runClosure() {
  // aClosure()가 호출된 시점에서 실행됩니다.
  print("trailing1")
}

// 인자가 Closure밖에 없다면 ()를 생략할 수 있습니다.
runClosure {
  print("trailing2")
}
{% endhighlight %}

인자가 한 개가 아닌 경우는 다음과 같이 사용할 수 있습니다.

{% highlight swift %}
func runClosure2(index: Int, name aClosure: () -> Void) {
  aClosure()
}
runClosure2(index: 2) {
  // index는 2로 넘기고, aClosure()가 호출된 시점에서 hi 출력
    print("hi")
}
{% endhighlight %}

`Alamofire`를 사용할 때 completionHandler로 나타나는 Closure 같은 것들은 이 때문에 몇 가지 형태로 쓸 수 있습니다.

{% highlight swift %}
// 인자를 전달하는 형태
Alamofire.request(URL).responseJSON(completionHandler: { response in
  // do something
  completed()
})

// Trailing Closure 활용한 형태
Alamofire.request(URL).responseJSON { response in
  // do something
  completed()
})
{% endhighlight %}

## Map Method


## 참고자료
- Apple Inc. The Swift Programming Language (Swift 3.1)
- Raywenderlich - Closure

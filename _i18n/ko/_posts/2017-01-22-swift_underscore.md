---
layout: post
comments: true
title:  "Swift underscore"
excerpt: "Swift에서 쓰이는 underscore(_)에 대해 알아봅니다."
categories: Swift Language
date:   2017-01-22 00:30:00
tags: [Swift, Language]
image:
  feature: swiftLogo.jpg
---

#### 함수에서의 _ (underscore)

Swift에서 함수를 보다보면 정체불명의 _ 가 있습니다. 이 _ 가 의미하는 것은 무엇일까요? 먼저 일반적인 함수 선언을 봐보겠습니다.

{% highlight swift %}
func greet(person: String, day: String) -> String {
    return "Hello \(person), today is \(day)."
}
greet(person: "Bob", day: "Tuesday")
{% endhighlight %}

위의 예제에서는 간단한 함수 <code>greet</code>이 선언되어 있습니다. 별 문제 없어 보입니다.(실제로 별 문제 없습니다.) 다음은 _ 이 있는 함수를 봐보겠습니다.

{% highlight swift %}
func greet(name person: String, _ day: String) -> String {
    return "Hello \(person), today is \(day)."
}

greet("John", on: "Wednesday")
{% endhighlight %}

동일한 함수 <code>greet</code>를 작성했는데 이번에는 _ 이 있습니다. 물론 이 함수도 정상 작동합니다. 둘 사이의 차이는 무엇일까요? 눈썰미가 좋은 분들은 이미 보셨겠지만, 함수 호출에서 그 차이가 있습니다.

{% highlight swift %}
greet(person: "Bob", day: "Tuesday")
greet(name: "John", "Wednesday")
{% endhighlight %}

뭔가 다르다!

네, Swift에서는 함수를 호출할 때, 함수로 전달하는 인자(argument)의 라벨이 있어야 합니다. 즉, **person: "Bob"** 에서 person 부분이 있어야 한다는 것입니다. 그렇다면 **person** 과 **day** 라벨은 어디서 온 것일까요? **바로 함수 선언시 argument의 이름입니다.** Swift는 함수의 argument 앞에 특정 라벨을 붙일 것을 요구합니다.(argument의 이름을 붙인다고 생각하면 쉬울 것 같습니다.) 다만, 따로 라벨을 쓰지 않으면 **default값으로 함수 선언시 사용한 argument를 라벨로 사용합니다.**

그렇다면 두 번째 함수 호출은 어떻게 된 것일까요? 먼저 **name:** 부분은 argument 작성시 **name person: String** 부분에서 따로 라벨을 설정해준 것을 확인할 수 있습니다. 자 그 다음은 _ 입니다. 보이나요? greet 함수 호출시 파라미터 앞에 라벨이 없습니다. 네 _ 는 이처럼 argument에 라벨을 따로 붙이고 싶지 않을 때 사용합니다. 정리하자면,

> Swift는 함수 호출시 넘기는 파라미터 앞에 라벨을 생략하기 위해 _ 를 사용한다.

{% highlight swift %}
func iGotIt(_ understand: String, _ argument: String, _ label: String) -> String {
  return "Are \(understand) \(argument) \(label)?"
}

print(iGotIt("you", "understand", "label"))
{% endhighlight %}

마지막 예제처럼 기이하게 함수를 호출해도 무슨 말인지 이해하시겠죠?

<a href="http://stackoverflow.com/questions/30876068/what-is-in-swift-telling-me">
  참고한 stackoverflow 원글 보기
</a>

#### for loop에서의 _ (underscore)

이 _ 는 for loop에서도 종종 발견됩니다.

{% highlight swift %}
for _ in 0..<4 {
  print("hello")
}
for index in 0..<4 {
  print("hello")
}
{% endhighlight %}

위의 _ 는 for loop에서 인덱스를 할당하지 않겠다는 의미로 사용됩니다.

> 내용 출처 : The swift Programming Language(3.0.1), stackoverflow(what is in swift telling me)

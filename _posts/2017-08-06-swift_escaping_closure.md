---
layout: post
comments: true
title:  "Swift Escaping Closure 이해하기"
excerpt: "Swift의 Escaping Closure에 대해 알아봅니다."
categories: Swift Closure, EscapingClosure
date:   2017-08-06 00:30:00
tags: [Swift, Closure, EscapingClosure]
image:
  feature: swiftLogo.jpg
---

<div class="message">
  A closure is said to escape a function when the closure is passed as an argument to the function, but is called after the function returns.
</div>

클로저가 함수로부터 `escape`한다는 것의 의미는 해당 함수의 인자로 클로저가 전달되지만, 함수가 반환된 후 실행되는 것을 의미합니다. 많은 `async` 형태의 함수들은 `completionHandler`를 파라미터로 가지고 있습니다. 이 때, `completionHandler`는 함수가 반환된 이후에 실행됩니다. 그렇기 때문에 `completionHandler`는 대표적인 `escape` 속성을 지닌 클로저라고 할 수 있습니다. 또한 `Escaping closure`는 함수 외부에서 실행되어야 하므로, 해당 함수로부터 **빠져나올 수(outLive)** 있는 속성을 가지고 있습니다.

Swift3에서는 기본적으로 함수의 인자로 들어오는 클로저가 함수 밖에서 사용할 수 없도록 되어 있습니다. 즉 클로저를 함수 외부의 저장소에 저장하거나, GCD를 이용하여 다른 쓰레드에서 해당 클로저를 실행시키는 것이 불가능합니다. 이렇게 함수 외부로 클로저를 내보내고자 할 때(빠져나오게 만드는) 사용하는 것이 `Escaping closure`입니다. `Escaping closure`의 사용방법은 클로저의 타입 앞에 `@escaping` 키워드만 넣어주면 됩니다. 애플 공식 문서에 서술되어 있는 예제를 통해서 이를 설명해보겠습니다.

#### 클로저를 함수 외부에 저장하기

{% highlight swift %}
// 함수 외부에 클로저를 저장하는 예시
// 클로저를 저장하는 배열
var completionHandlers: [() -> Void] = []

func withEscaping(completion: @escaping () -> Void) {
    // 함수 밖에 있는 completionHandlers 배열에 해당 클로저를 저장
    completionHandlers.append(completion)
}

func withoutEscaping(completion: () -> Void) {
    completion()
}

class MyClass {
    var x = 10
    func callFunc() {
        withEscaping { self.x = 100 }
        withoutEscaping { x = 200 }
    }
}
let mc = MyClass()
mc.callFunc()
print(mc.x)
completionHandlers.first?()
print(mc.x)

// 결과
// 200
// 100
{% endhighlight %}

위의 예시에서는 MyClass의 함수 `callFunc()`는 클로저를 인자를 가지는 `withEscaping(completion:)`과 `withoutEscaping(completion:)`을 각각 호출합니다. 이 때 `withEscaping(completion:)`은 `completion`의 파라미터가 `escaping closure` 형태로 구현되어 있습니다. 위의 예제에서는 `completionHandlers.append(completion)`코드를 통해 `withEscaping(completion:)` 외부에 클로저를 저장합니다. 즉, 클로저가 함수에서 빠져나갔습니다. 이렇게 함수를 호출하는 도중에 해당 함수 외부에 클로저를 저장하기 위해서는 클로저는 `escaping closure`이어야 합니다.

<div class="message">
  Note: 이 때, 클로저가 탈출한다는 의미는 해당 함수의 실행을 중간에 끊고, 탈출(escape)하는 의미가 아닙니다. 여기서의 탈출(escape)은 클로저를 외부로 보낼 수 있다는 의미입니다.
</div>

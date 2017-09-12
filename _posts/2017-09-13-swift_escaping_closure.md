---
layout: post
comments: true
title:  "Swift Escaping Closure 이해하기"
excerpt: "Swift의 Escaping Closure에 대해 알아봅니다."
categories: Swift Closure, EscapingClosure
date:   2017-09-12 00:30:00
tags: [Swift, Closure, EscapingClosure]
image:
  feature: swiftLogo.jpg
---

## Escaping Closure 개념

본 글은 Closure에 대한 기본 개념을 알고 있다는 전제 하에 글을 진행합니다. 그러니 Closure에 대한 이해가 부족하다면 [Swift Closure](https://hcn1519.github.io/articles/2017-05/swift_closure) 다음 글을 보고 이 글을 읽으면 도움이 될 것입니다.

<div class="message">
  A closure is said to escape a function when the closure is passed as an argument to the function, but is called after the function returns.
</div>

클로저가 함수로부터 `Escape`한다는 것은 해당 함수의 인자로 클로저가 전달되지만, **함수가 반환된 후 실행** 되는 것을 의미합니다. 함수의 인자가 함수의 영역을 탈출하여 함수 밖에서 사용할 수 있는 개념은 기존에 우리가 알고 있던 변수의 `scope` 개념을 무시합니다. 왜냐하면 함수에서 선언된 로컬 변수가 로컬 변수의 영역을 뛰어넘어 **함수 밖** 에서도 유효하기 때문입니다.

사실 일반 로컬 변수(주로 값들: `Int`, `String` 등등)가 함수 밖에서 살아있는 것은 전역 변수를 함수에 가져와서 값을 새로 주는 것과 크게 다르지 않기 떄문에 이와 같은 `Escape` 개념이 크게 의미가 없어 보입니다. 하지만, 클로저는 다릅니다. 클로저는 어떤 **함수** 이기 때문에 특정 작업을 지정할 수 있습니다. 정리하자면, `Escaping Closure`를 통해 `A 함수가 마무리된 상태에서만 B 함수가 실행되도록` 할 수 있습니다.

> Escaping Closure를 활용하면 통해서 함수 사이에 실행 순서를 정할 수 있습니다.

함수의 실행 순서를 보장 받을 수 있는 것은 상당히 중요한 기능입니다. 왜냐하면, 이 순서 보장은 비동기 함수의 경우도 포함하기 때문입니다. 서버에서 Json 형식의 데이터를 가져와 화면에 이를 보여주는 앱을 생각해보겠습니다. 이 때 HTTP 통신을 위해 `Alamofire` 라이브러리를 사용합니다. `Alamofire` 라이브러리는 이 같은 경우 흔히 아래와 같은 형태로 사용됩니다.

{% highlight swift %}
Alamofire.request(urlRequest).responseJSON { response in
  // handle response
}
{% endhighlight %}

`Alamofire.request(urlRequest)` 메소드는 서버로 `Request`를 전송합니다. 여기서는 GET 방식으로 Json 형식의 데이터를 받아옵니다. 그리고 그 결과는 `Response` 객체를 통해 받을 수 있습니다. 일반적으로 서버에 `Request`를 전송하고 그 `Response` 받아오는 함수들은 비동기로 작동하여 `Request`를 보낸 직후 반환 되어버리는데, 어떻게 이 같은 `Response`가 `Request` 결과를 기다리게 하는 형태로 함수를 작성할 수 있는 것일까요? 답은 `Escaping Closure`에 있습니다. `responseJSON` 메소드를 파라미터를 간단히 들여다보면 다음과 같이 되어 있습니다.

{% highlight swift %}
@discardableResult
    public func responseJSON(
        queue: DispatchQueue? = nil,
        options: JSONSerialization.ReadingOptions = .allowFragments,
        completionHandler: @escaping (DataResponse<Any>) -> Void)
        -> Self
    {

    }
{% endhighlight %}

`responseJSON(queue:options:completionHandler:)`에서 `queue`와 `options`는 기본값이 지정되어 있기 때문에, 값을 주지 않아도 해당 함수는 작동합니다. 눈여겨 볼 부분은 `completionHandler`입니다. 이 `completionHandler`는 `Escaping Closure` 형태로 작성되어 있습니다. 즉, `completionHandler`는 `responseJSON(queue:options:completionHandler:)` 함수가 반환되고(완전히 서버로부터 값을 가져 온 상태에서) 실행됩니다. 그 부분이 바로 `trailing closure` 형태로 작성되어 있는 `{ response in }` 부분입니다.

<div class="message">
  Escaping closure를 통해서 클로저 인자는 함수로부터 빠져나올 수(outLive) 있습니다. Swift3 이후부터는 기본적으로 함수의 인자로 들어오는 클로저가 함수 밖에서 사용할 수 없도록 되어 있습니다. 즉 클로저를 함수 외부의 저장소에 저장하거나, GCD를 이용하여 다른 쓰레드에서 해당 클로저를 실행시키는 것이 불가능합니다. 이 때 `Escaping closure`를 사용하려면 클로저의 타입 앞에 `@escaping` 키워드를 넣어주면 됩니다.
</div>

앞서 작성한 예시만으로 이해가 잘 안될 수 있기 때문에 여기서부터는 어떤 방식으로 `Escaping closure`을 활용해야하는지에 대해 서술하고자 합니다. 먼저 Apple의 공식 문서에서 `Escaping closure`를 설명하는 예시를 살펴보겠습니다.

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

## Async Inside Async

앞서 언급한 것처럼 `Escaping closure`는 HTTP 통신에서 `completionHandler`로 많이 사용됩니다. 다만, 위에서처럼 `Alamofire` 메소드를 개별적으로 사용하지는 않습니다. 일반적으로 서버에 요청하는 Restful API 기반의 `Request`들은 하나의 클래스 안에서 static 함수 형태로 관리하는 것이 좋습니다.

{% highlight swift %}
class Server {
  static getPerson() {
    // doSomething
  }
}
{% endhighlight %}

그래서 위의 예시는 `Server.getPerson()` 형태로 앱의 어디에서는 호출할 수 있습니다.

여기서, 앞에서 들었던 서버에서 Json 정보를 가져와 앱 화면을 보여주는 경우를 다시 생각해보겠습니다. 이 메소드를 static 함수 형태로 관리하려면 어떻게 해야할까요? 여기서 생각해야하는 점은 데이터를 받아오는 것과 데이터로 화면을 업데이트하는 것이 모두 비동기로 이루어져야 한다는 점입니다. 그리고 데이터를 받아오고나서 화면이 업데이트 되는 것이 **보장** 되어야 합니다. 그렇기 때문에 이와 같은 경우에는 두 개의 `Escaping closure`를 함께 사용합니다.

{% highlight swift %}
class Server {
  static var persons: [Person] = []

  static getPerson(completion: @escaping (Bool, [Person]) -> Void) {
      // 순서 2.
      Alamofire.request(urlRequest).responseJSON { response in
          persons.append(데이터)
          DispatchQueue.main.async {
              // 순서 3.
              completion(true, persons)
          }

      }
  }
}
// Usage, ex) ViewController.swift
// 순서 1.
Server.getPerson { (isSuccess, persons) in
  // 순서 4.
  if isSuccess {
      // update UI
  }
}
{% endhighlight %}

가장 먼저 `Server` 클래스의 함수 `getPerson(completion:)`이 호출됩니다. 그리고 `Alamofire`를 통해 서버로 `Request`가 전송되고 `responseJson`은 `Escaping closure`이므로 `{ response in }` 부분은 결과가 모두 들어 온 이후에 실행됩니다. 다음으로 화면 UI 업데이트를 위해 main 쓰레드에서 `getPerson` 함수의 `completion` 블럭을 호출합니다. 이 함수가 main 쓰레드에서 실행되려면 `completion`도 `getPerson` 함수를 빠져나가므로 `Escaping closure`로 작성되어야 합니다. 그리고 마지막으로 UI 업데이트를 진행하면 원하는 결과를 얻을 수 있습니다.

---

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 3.1) - Escaping Closure
* [escaping closure swift3](https://learnappmaking.com/escaping-closures-swift-3/)
* [What do mean @escaping and @nonescaping closures in Swift?](https://medium.com/@kumarpramod017/what-do-mean-escaping-and-nonescaping-closures-in-swift-d404d721f39d)
* [Completion handlers in Swift 3.0](https://stackoverflow.com/questions/41745328/completion-handlers-in-swift-3-0)

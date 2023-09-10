---
layout: post
comments: true
title:  "Swift의 표준입출력"
excerpt: "Swift의 표준입출력(StdIO)에 대해 알아봅니다."
categories: Swift StandardIO CommandLine
date:   2017-05-17 00:30:00
tags: [Swift, Language, StandardIO, CommandLine]
image:
  feature: swiftLogo.jpg
translate: false
---

알고리즘 문제 같은 것을 풀기 위해 자주 사용되는 `Standard Input`을 Playground 위주로 공부하다보면 Swift에서 어떻게 사용하는지 모르는 경우가 발생합니다. 이번 포스팅에서는 간단히 커맨드라인에서 Swift를 사용하는 것과 표준입출력에 대해 알아보겠습니다.

## REPL(Read Eval Print Loop)

`REPL` 방식은 python 같은 언어를 처음 접할 때 주로 사용하는 방식입니다. 코드를 입력하고 엔터를 누르면 바로 결과가 출력되는 형식으로 실행도 간단합니다.

{% highlight Bash shell scripts %}
$ swift
{% endhighlight %}

## Compile Swift

`swiftc` 커맨드를 통해서도 Swift 파일을 컴파일하고 실행할 수 있습니다. 먼저 Swift 파일을 생성하고 간단히 내용을 작성합니다.


{% highlight Bash shell scripts %}
$ touch hello.swift
{% endhighlight %}

그리고 다음 내용을 입력하고 파일을 저장합니다.

{% highlight swift %}
// hello.swift
print("Hello Swift")
{% endhighlight %}

커맨드라인에서 Swift 파일을 만든 디렉토리로 이동 후, Swift 파일을 컴파일합니다.

{% highlight Bash shell scripts %}
$ swiftc hello.swift
$ ./hello
// 결과 : Hello Swift
{% endhighlight %}

## Swift 표준 입력

커맨드라인에서 사용자의 입력을 받기 위해서 Swift는 `readLine()` 메소드를 사용합니다. 주의할 점은 모든 값이 `Optional` String 타입으로 들어 온다는 점입니다. 새로운 파일을 만들어서 예제를 보도록 하겠습니다.

{% highlight Bash shell scripts %}
$ touch stdio.swift
$ open stdio.swift
{% endhighlight %}

그리고 해당 파일 안에 다음 내용을 입력합니다.

{% highlight swift %}
// stdio.swift
if let result = readLine() {
    print("이것은 \(result)")

    // 타입 캐스팅 + readLine에서 Int가 들어오지 않은 것도 걸러줍니다.
    if let resultInt2 = Int(result) {
        print("Unwrapped Number \(resultInt2)")
    }
}
{% endhighlight %}

`Optional`은 항상 nil 값이 들어오는 것을 조심해야 하기 때문에 위에서는 `Optional Binding`을 사용하였습니다. 또한 이 `Optional Binding`은 잘못된 타입 캐스팅도 걸러주기 때문에 표준입력에서 자주 사용하는 것이 좋은 것 같습니다.

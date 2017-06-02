---
layout: post
comments: true
title:  "Swift 표준입력 라이브러리"
excerpt: "Swift의 표준 입력을 수월하게 해주는 라이브러리를 제작하였습니다."
categories: Swift StandardIO
date:   2017-06-02 00:30:00
tags: [Swift, Language, StandardIO]
image:
  feature: swiftLogo.jpg
---

요즘 알고리즘 문제 사이트에서 문제를 푸는데, Swift로 답안을 제출할 수 있어서 종종 Swift로 답안을 작성합니다. 다만, 대부분 알고리즘 문제들은 콘솔에서 입력을 받기 때문에 콘솔의 입력을 다루는 메소드를 작성해야 합니다. 그런데.. Swift에서는 아직까지 지원하는 메소드가 `readLine()`밖에 없어서 `Int`형 데이터, `Double`형 데이터를 별도로 캐스팅해주어야 하고, 개별 `String`에 접근하려면 라인 전체를 읽고, 이를 잘라서 접근해야만 했습니다.

또한... `Optional`은 코드의 안전성을 높여주긴 하지만, 일반적으로 표준 입력을 받는 알고리즘 문제들은 값이 보장되어 있는 경우가 대부분이므로 값을 unwrap하는 일도 상당히 성가십니다. 그래서 이제까지는 문제별로 코드를 작성했었는데, 인내심의 한계에 도달해서 직접 input을 받는 Struct를 제작하였습니다. 코드는 아래와 같습니다.

## 소스 코드

{% highlight swift %}
// Swift 3.1
import Foundation

protocol StandardInput {
    mutating func read() -> String
    mutating func readInt() -> Int
    mutating func readDouble() -> Double
    mutating func readLineToArray() -> [String]
}

struct ReadInput: StandardInput {

    private var currentIndex: Int = 0
    private var inputArray: [String] = []

    // 데이터를 배열로 변환
    public mutating func readLineToArray() -> [String] {
        let result = readLine()!
        let resultArray = result.components(separatedBy: " ")
        return resultArray
    }

    // 띄어쓰기 단위로 String 읽기
    public mutating func read() -> String {
        if inputArray.count == 0 {
            inputArray = self.readLineToArray()
        }
        let result = inputArray[inputArray.index(after: currentIndex-1)]
        currentIndex += 1

        if currentIndex == inputArray.count {
            self.inputArray.removeAll()
            self.currentIndex = 0
        }
        return result
    }

    // Int 데이터 읽기
    public mutating func readInt() -> Int {
        guard let result = Int(self.read()) else {
            fatalError("Int형 데이터가 아닙니다.")
        }

        return result
    }

    // Double 데이터 읽기
    public mutating func readDouble() -> Double {
        guard let result = Double(self.read()) else {
            fatalError("Double형 데이터가 아닙니다.")
        }

        return result
    }

}
{% endhighlight %}

코드를 사용하기 위해서는 `Foundation`을 import해야 합니다. 굳이 `protocol`을 쓸 필요는 없지만.. 한 번 써봤습니다. 제공하는 메소드는 크게 4가지입니다.

{% highlight swift %}
protocol StandardInput {
    mutating func read() -> String // 개별 String 읽기
    mutating func readInt() -> Int // 개별 Int 읽기
    mutating func readDouble() -> Double // 개별 Double 읽기
    mutating func readLineToArray() -> [String] // 한 라인 배열로 변환
}
{% endhighlight %}

메소드들은 자바의 `next()`, `nextInt()` 등의 기능과 비슷합니다. `read()`는 단일 String을 읽고, `readInt()`, `readDouble()`은 숫자를, `readLineToArray()`는 읽은 라인을 배열로 변환한 데이터를 리턴합니다.

## 사용법

사용법은 매우 간단합니다.

{% highlight swift %}
let ri = ReadInput()

let str1 = ri.read() // String 리턴
let num1 = ri.readInt() // Int 리턴
let num2 = ri.readDouble() // Int 리턴
let line = ri.readLineToArray() // [String] 배열 리턴
{% endhighlight %}

자바에서 `Scanner` 인스턴스를 만들듯이, `ReadInput` 인스턴스를 만들고 필요한 메소드를 사용하면 됩니다.

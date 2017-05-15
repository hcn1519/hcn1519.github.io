---
layout: post
comments: true
title:  "Swift String 다루기"
excerpt: "Swift의 String method들에 대해 알아봅니다."
categories: Swift String
date:   2017-05-15 00:30:00
tags: [Swift, Language, String]
image:
  feature: swiftLogo.jpg
---

이번 포스팅에서는 Swift의 String에 대해 알아보고자 합니다. Swift의 String의 가장 기본적인 특징은 다음과 같습니다.


<div class="message">
  Swift에서 String의 Character들은 인덱스로 접근할 수 없다.
</div>

아시다시피, String 데이터는 배열에 하나하나의 문자를 저장한 형태입니다. 그렇기 때문에 일반적으로 다음과 같은 표현이 가능합니다.

{% highlight swift %}
let str = "hello"
print(str[2]) // error
{% endhighlight %}

하지만 Swift에서는 위와 같이 각각의 **Character에 인덱스로 접근할 수 없습니다.** 그 이유가 무엇일까요?

## Extended Grapheme Clusters(확장적 문자소 집합)

Swift에서 하나의 Character는 `Single Extended Grapheme Clusters`를 나타냅니다. `Extended Grapheme Clusters`라는 것은 사람이 읽을 수 있는 하나의 문자를 지칭합니다. 여기서 "사람이 읽을 수 있다"의 의미는 영어에만 적용되는 것이 아니라, 다른 나라의 언어도 포함합니다. Apple의 공식문서에서 한글을 예로 드는데요. 이를 살펴보겠습니다.

{% highlight swift %}
let precomposed: Character = "\u{D55C}"                  // 한
let decomposed: Character = "\u{1112}\u{1161}\u{11AB}"   // ᄒ, ᅡ, ᆫ
// 둘 모두 Character 타입 "한"을 지칭합니다.
{% endhighlight %}

`decomposed`는 놀랍게도 Character 타입에 3개의 `scala`(이 때 `scala`라는 것은 최소 의미를 담은 Character 값(ex: `\u{D55C}`)들을 의미합니다.)가 들어갑니다. 즉, Extended Grapheme Clusters에서는 **1 scala = 1 Character** 가 아니라, **1 Character = 1개 혹은 여러개의 scala** 가 되는 것입니다. 인덱스를 통해서 String을 다룰 수 없는 이유가 여기서 나타납니다. 각각의 Character가 여러 개의 scala 값을 지닐 수 있기 때문에 동일한 메모리로 한정된 저장공간을 가지기 어렵습니다. 그렇기 때문에 String을 만들 때 Character별로 동일한 크기의 메모리를 할당할 수 없고, 이는 인덱스를 통한 접근을 불가능하게 만드는 것입니다.

<div class="message">
  Swift에서 채택한 Extended Grapheme Clusters는 다양한 언어를 직관적으로 표시할 수 있게 도와준다. 하지만, Extended Grapheme Clusters는 서로 다른 크기의 Character를 만들기 때문에 String[Int]를 통한 String의 개별 Character로의 접근은 불가능하다.
</div>

## Swift의 String 접근하기

Swift에서는 `String[Int]`를 통해 개별 문자에 접근하기 어렵기 때문에, Swift에서 제공하는 메소드들을 사용해야만 합니다. Swift에서는 `String.index` 메소드를 통해서 개별문자 혹은 범위로의 접근을 할 수 있습니다. 가장 기본이 되는 2가지 메소드는 `startIndex`와 `endIndex`입니다.

#### 개별 Character 접근하기(startIndex, endIndex)

{% highlight swift %}
let str = "Hello"

print(str.startIndex) // Index(_base: Swift.String.UnicodeScalarView.Index(_position: 0), _countUTF16: 1)
print(str.endIndex) // Index(_base: Swift.String.UnicodeScalarView.Index(_position: 5), _countUTF16: 0)
{% endhighlight %}

위와 같은 경우 `str.startIndex`는 `0`을 반환하고, `str.endIndex`는 `5`를 반환합니다. 조심해야할 부분은 `endIndex` 값이 4가 아니라 5라는 점입니다. `Hello`는 5글자이고, 0부터 시작하면 4까지인데, `endIndex`는 5라는 것이죠. 즉, `endIndex`는 전체 String의 길이를 반환한다는 것을 알 수 있습니다. 위의 메소드들을 통해서 String의 Character들을 접근할 수 있습니다.

{% highlight swift %}
let str = "Hello"

print(str[str.startIndex]) // H

print(str[str.index(before: str.endIndex)]) // o
print(str[str.endIndex]) // error
{% endhighlight %}

위의 예시처럼 `str[메소드를 통해 접근한 특정 인덱스]`의 표현을 통해 개별 Character에 접근할 수 있습니다.(여기서 숫자로 접근하면 에러입니다.) 그래서, `str[str.startIndex]`이 `H`를 출력하는 것은 직관적입니다. 하지만, `str[str.endIndex]`의 경우 상황이 조금 다릅니다. 왜냐하면 전체 문자는 0부터 4까지인데, `str.endIndex`는 5이기 때문이죠. 그래서 `str[str.endIndex]`는 에러이고, 마지막 문자에 접근하기 위해서는 `endIndex` 앞의 인덱스에 대한 접근이 필요합니다.

Swift는 이와 같은 앞쪽 혹은 뒤쪽 문자에 대한 접근을 위해 `str.index[before:]`와 `str.index[after:]` 메소드를 제공합니다. 여기서는 `endIndex` 앞의 문자를 접근해야 하므로, `str.index(before: str.endIndex)`이 마지막 문자 `o`를 가리키는 인덱스가 됩니다. 비슷한 원리로 `str.index(after: str.startIndex)`를 사용하면, `H` 다음의 문자 `e`에 접근할 수 있습니다.

#### 개별 Character 접근하기(offsetBy)

`startIndex`와 `endIndex`는 String의 시작과 끝(흑은 그 앞뒤 인덱스)으로의 접근만 가능할 뿐, 중간에 있는 문자에 대한 접근은 어렵습니다. 그래서 Swift는 중간에 있는 문자에 접근하기 위한 `index(_:offsetBy:)` 메소드를 별도로 제공합니다.

<div class="message">
  offsetBy 메소드는 시작 지점부터 떨어진 정수 값만큼을 더한 위치를 반환합니다.
</div>

사용방법은 다음과 같습니다.

{% highlight swift %}
let str = "Hello World"

print(str[str.index(str.startIndex, offsetBy: 0)]) // H
print(str[str.index(str.startIndex, offsetBy: 6)]) // W

print(str[str.index(str.endIndex, offsetBy: -1)]) // d
print(str[str.index(str.endIndex, offsetBy: -3)]) // r
{% endhighlight %}

위의 예시에서 4개의 출력 중 위의 2개는 `str.startIndex`를 시작지점으로 정한 것입니다. `str.startIndex`에서 0만큼 떨어진 것은 자기 자신이므로 `H`가 되고, 6만큼 떨어진 것은 `W`입니다.(자기자신의 인덱스에서 6을 더한 것) 다음으로 아래 2개의 예시는 뒷쪽에서 접근하는 방법입니다. `str.endIndex`는 전체 String의 가장 마지막 값입니다. 여기서 `str.endIndex`은 전체 길이를 반환하므로 -1을 **더하면** 전체 String의 마지막 문자를 지칭하는 인덱스가 됩니다. 이와 같은 원리로 -3을 **더하면** `r`이 나오는 것입니다.

#### 루프를 통해 전체 String에 접근하기

다음은 루프를 통한 String 접근입니다. 크게 3가지 방법이 있습니다. 첫 번째는 `str.character`를 사용하여 개별 문자(value)에 접근하는 방식입니다.

{% highlight swift %}
let str = "Hello"

for char in str.character {
  print(char) // H e l l o 각각 접근
}
{% endhighlight %}

다음은 `indice`를 활용하여 인덱스에 접근하는 방식입니다.

{% highlight swift %}
for index in str.character.indice {
  // 정수 인덱스가 아닌 Swift에서 만들어낸 인덱스에 접근합니다.
  print(index) // Index(_base: Swift.String.UnicodeScalarView.Index(_position: 0), _countUTF16: 1)...
}
{% endhighlight %}

마지막으로 인덱스와 개별 문자에 동시에 접근하는 방식입니다.

{% highlight swift %}
for (index, value) in str.characters.enumerated() {
    // index는 정수입니다.
    print("index: \(index), value : \(value)")  // index: 0, value : H
}
{% endhighlight %}

## Swift String Insert, Remove

Swift의 String Insert는 **어떤 내용을 어떤 곳에** 할 것인지를 통해 나타납니다. 이 때 사용하는 메소드는 `insert(_:at:)`(`insert(contentsOf:at:)`)입니다.

{% highlight swift %}
let str = "Hello"

str.insert("A", at: str.startIndex) // 결과 : AHello
str.insert(contentsOf: " World", at: str.endIndex) // 결과 : AHello World
{% endhighlight %}

위처럼 개별 Character를 삽입할 때는 `contentsOf`를 사용하지 않아도 됩니다.

String Remove의 경우에도 Insert와 유사한데, 문자를 삭제할 위치 및 범위를 지정해주면 됩니다. 이 때는 `remove(_:at:)`(`removeSubrange(_:)`) 메소드를 사용합니다.

{% highlight swift %}
let str = "AHello World"

str.remove(at: str.startIndex) // 결과 : Hello World

let rangeOfWorld = str.index(str.endIndex, offsetBy: -6)..<str.endIndex
str.removeSubrange(rangeOfWorld) // 결과 : Hello
{% endhighlight %}

여기서 `remove(_:at:)` 메소드는 직관적으로 이해할 수 있습니다. 반면 `range`의 경우에는 아무 `range`나 사용해서는 안됩니다.(하나의 배열도 `range`가 될 수 있습니다.) 여기서 말하는 `range`는 **String.index** 를 사용하여 닫힌 `range`를 의미합니다. 즉 위의 예시처럼, `str.index` 혹은 `str.endIndex` 같은 것들로 닫힌 `range`를 지칭하는 것입니다.

## Prefix와 Suffix(접두사, 접미사)

`hasPrefix(_:)` 메소드와 `hasSuffix(_:)` 메소드는 String의 앞쪽 혹은 뒷쪽에 찾고자 하는 문자가 있는지를 확인할 수 있도록 해주는 메소드입니다. 특정 문자열이 앞에서부터(혹은 뒤에서부터) 포함되어 있는지 확인할 때 좋은 메소드라고 생각됩니다.

{% highlight swift %}
var s = "한글"

if s[s.startIndex] == "한" {
    print("앞 글자가 한")
}
if s.hasPrefix("한") {
    print("앞 글자가 한")
}

if s.hasSuffix("한글") {
    print("뒷 쪽이 한글")
}

{% endhighlight %}

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 3.1)

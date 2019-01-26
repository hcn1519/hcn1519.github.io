---
layout: post
comments: true
title:  "iOS 다국어 지원 설정하기"
excerpt: "iOS 다국어 지원 설정에 대해 알아봅니다."
categories: iOS l10n
date:   2017-03-16 00:30:00
tags: [iOS, l10n]
image:
  feature: iOS10.png
---

## Localization 설정

이 포스트에서는 iOS에서 아이폰에 설정된 언어에 따라서 앱의 언어를 바꾸는 방법에 대해 알아보겠습니다. 먼저 프로젝트 최상단 파일을 선택 후, Project를 선택합니다. 그리고 `Localization` 파트에서 원하는 언어를 추가합니다.

<img src="{{ site.imageUrl}}/2017-03/iOS_LanguageSupport/lang1.png">

이렇게 추가를 하게 되면 타겟을 설정하라고 나올텐데, 그냥 생성하시면 됩니다.(참고: Launch Screen Story Board의 글씨는 Localization 지원이 되지 않습니다. 따라서 이에 대한 설명은 생략합니다.)

<img src="{{ site.imageUrl}}/2017-03/iOS_LanguageSupport/lang2.png">

Localization을 적용하면 다음과 같이 `Main Story Board`와 `Launch Screen Story Board`에 다음과 같이 `Main.strings (Korean)`와 `Launch Screen Story Board.strings (Korean)`이라고 생성된 것을 확인할 수 있습니다.

<img src="{{ site.imageUrl}}/2017-03/iOS_LanguageSupport/lang3.png">

다음으로 `Localizable.strings` 파일을 생성해야 합니다.

<img src="{{ site.imageUrl}}/2017-03/iOS_LanguageSupport/lang5.png">

위처럼 프로젝트에서 string file을 생성하고 이름을 `Localizable.strings`으로 지정합니다. 각각의 파일들의 역할은 다음과 같습니다.

* `Main.strings (Korean)` - 스토리보드 상의 label들에 대한 번역
* `Localizable.strings` - 프로젝트 곳곳에 있는 string들에 대한 번역

`Main.strings (Korean)` 파일은 스토리보드에서 생성한 label들에 대한 번역 내용들을 담고 있습니다. 다만 label들이 코드로 내용이 바뀌게 된다면 해당 label의 내용은 `Localizable.strings`에서 변경해주어야 합니다. `Localizable.strings`에는 각각의 문자열들이 어떤 내용으로 바뀌어야 하는지에 대한 서술을 넣습니다.

이제 Localization이 제대로 작동하도록 각각의 파일에 Localize 옵션을 추가해줍니다.(`Main.storyboard (Base)`와 `Localizable.strings` 모두 적용)

<img src="{{ site.imageUrl}}/2017-03/iOS_LanguageSupport/lang4.png">

이 때, 기본적으로 Base는 영어로 되어 있으므로, 영어와 한국어를 지원하도록 만든다고 하면, 한국어만 체크해주시면 됩니다.

## Main StoryBoard에 Localization 적용

Main StoryBoard의 경우에는 적용이 매우 간단합니다. 그냥 영어 버전에는 Label들을 영어로, 한국어 버전에는 Label들을 한국어로 바꾸어주면 됩니다.


## 일반 코드에 Localization 적용

다음으로 일반 코드에 Localization을 적용하는 경우입니다. 먼저 번역하고자 하는 문자열을 key, 번역된 문자열을 value로 하는 딕셔너리들을 다음과 같이 생성합니다.

{% highlight swift %}
// Localization.strings (Base)
"Edit" = "Edit";
"Done" = "Done";

// Localization.strings (korean)
"Edit" = "편집";
"Done" = "완료";
{% endhighlight %}

그리고 나서 문자열이 적용된(여기서는 "Edit") 코드로 가서 이를 다음과 같이 변경해줍니다.

{% highlight swift %}
editLabel.text = "Edit" // 다음과 같이 설정되어 있을 경우,

editLabel.text = String(format: NSLocalizedString("Edit", comment: "")) // 이렇게 바꿔줍니다.
{% endhighlight %}

### Swift 스타일 Localization

Swift에서는 `extension`을 통해 위 코드보다 좀 더 간결하게 코드를 작성할 수 있습니다. 이를 위해서 `StringExtension.swift` 파일을 생성하고 아래 코드를 넣어줍니다.

{% highlight swift %}
// StringExtension.swift
import Foundation

extension String {
    var localized: String {
        return NSLocalizedString(self, tableName: nil, bundle: Bundle.main, value: "", comment: "")
    }
}
{% endhighlight %}

이렇게 써넣으면, `"myString".localized`를 통해 좀 더 간결하게 구현할 수 있습니다.

{% highlight swift %}
editLabel.text = "Edit"

editLabel.text = "Edit".localized // extension으로 구현
{% endhighlight %}

## 변수가 포함된 문자열 Localization

위의 경우는 모두 문자열에 변수가 없는 경우만 적용 가능합니다. 그런데 출력하는 문자열에 변수가 포함된 경우에는 어떻게 해야 할까요? 다음 예제를 보시면 쉽게 이해할 수 있습니다.

{% highlight swift %}
let myName = "Sam"
let friend = "Tom"
let myNum = 10

titleLabel.text = String(format: NSLocalizedString("Hello %@, This is %@", comment: ""), myName, friend) // Hello Sam, This is Tom
titleLabel.text = String(format: NSLocalizedString("Hello %d", comment: ""), myNum) // Hello 10
{% endhighlight %}

String 타입의 경우 `%@`를 Int 타입의 경우 `%d`를 넣으면 해당 변수가 올바르게 출력되는 것을 확인할 수 있습니다.

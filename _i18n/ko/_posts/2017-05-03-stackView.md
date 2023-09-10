---
layout: post
comments: true
title:  "UIStackView 기초"
excerpt: "UIStackView의 기본에 대해 알아봅니다."
categories: iOS UIStackView
date:   2017-05-03 00:30:00
tags: [iOS, UIStackView]
image:
  feature: iOS.png
translate: false
---

**UIStackView** 는 iOS 9에서 나온 개념으로 여러 개의 View를 한 셋트로 만들어주는 역할을 하는 View입니다. 그래서 항상 StackView 안에는 몇 개의 View 들이 있는데, 이를 **arrangedSubViews** 라고 합니다. 이 subView들은 일정한 규칙에 따라 StackView 안에서 배치됩니다. 그리고 이 규칙은 크게 4가지가 있습니다.(axis, alignment, distribution, spacing) 이는 StackView를 스토리보드에서 생성하면 Attribute Indicator 최상단에서 다음과 같이 확인할 수 있습니다.

<img src="{{ site.imageUrl}}/2017-05/stackView/stackviewComponents.png">

- axis는 StackView의 가로, 세로 형태를 설정합니다.
- alignment는 StackView안의 view들이 Y축 정렬을 설정합니다.
- distribution은 StackView안의 view들이 X축 정렬을 설정합니다.
- spacing은 view들간의 간격을 설정합니다.

<img src="{{ site.imageUrl}}/2017-05/stackView/stackViewComponents2.png">

## UIStackView AutoLayout

#### Pin(x,y position)

StackView는 포함하고 있는 첫 번째 View와 마지막 View를 기준으로 AutoLayout을 설정합니다. 즉, 가로 StackView라고 한다면, 첫 번째 View의 Leading edge(anchor)가 StackView의 Leading edge가 되고, 마지막 View의 Trailing edge가 StackView의 Trailing edge가 됩니다. 이는 세로 StackView에서도 동일하게 적용됩니다.

#### Size(width, height)

StackView를 사용할 때는 일반적으로 StackView 자체에 대한 Constraints만 적용하고 그 안의 Views들은 StackView의 속성을 통해 결정하는 것이 일반적입니다. 예를 들어 내부 Views들의 Intrinsic Size를 사용하고 싶다면, StackView의 Top과 Leading Constraints만 적용하는 방식으로 사용하고, 사이즈를 조정하고 싶은 부분에 대한 constraints를 적절히 적용하여 내부 Views들의 크기를 조정하면 됩니다.

## UIStackView programatically

#### StackView 생성

StackView는 Class로 다음과 같이 생성합니다. 또한 속성들은 다음과 같이 생성합니다.

{% highlight swift %}
// UIStackView in Swift 3.0
let stackView = UIStackView()

stackView.axis = .horizontal
stackView.distribution = .fillEqually
stackView.alignment = .fill
stackView.spacing = 8
stackView.translatesAutoresizingMaskIntoConstraints = false

// stackView에 View 추가
stackView.addArrangedSubview(view1)
{% endhighlight %}

#### StackView AutoLayout

그리고 다음 예제는 stackView의 모든 부분에 pin을 준 형태입니다.
{% highlight swift %}
// UIStackView Constraints
stackView.leadingAnchor.constraint(equalTo: view.leadingAnchor).isActive = true
stackView.trailingAnchor.constraint(equalTo: view.trailingAnchor).isActive = true
stackView.centerXAnchor.constraint(equalTo: view.centerXAnchor).isActive = true
stackView.centerYAnchor.constraint(equalTo: view.centerYAnchor).isActive = true
{% endhighlight %}

StackView 내부의 Views에 접근하기 위해서는 앞서 언급한 arrangedSubViews 속성을 사용하면 됩니다. 다음 예제는 내부 View 중 첫 번째 view의 height와 width를 같게 만드는 constraint 예제입니다.

{% highlight swift %}
stackView.arrangedSubviews[0].heightAnchor.constraint(equalTo: stackView.arrangedSubviews[0].widthAnchor).isActive = true
{% endhighlight %}


-----

## 참고 자료
* [UIStackView - Apple API Reference](https://developer.apple.com/reference/uikit/uistackview)

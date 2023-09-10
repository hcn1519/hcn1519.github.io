---
layout: post
comments: true
title:  "iOS View 아키텍쳐 이해하기"
excerpt: "iOS의 기본 View의 아키텍쳐에 대해 알아봅니다."
categories: iOS UIView
date:   2017-06-23 00:30:00
tags: [iOS, UIView]
translate: false
---

https://developer.apple.com/library/content/documentation/WindowsViews/Conceptual/ViewPG_iPhoneOS/WindowsandViews/WindowsandViews.html#//apple_ref/doc/uid/TP40009503-CH2-SW1

iOS에서 화면 UI 구성을 담당하는 핵심적인 요소 중 하나가 바로 *View* 입니다. *View* 는 *UIKit* 과 다른 프레임워크들을 통해 제공됩니다. *View* 라는 것은 하나의 공간입니다. 이 공간에는 여러가지 요소들이 담길 수 있고, 여러 components를 보여주는 용도로도 사용됩니다.


## View Architecture Fundamental

iOS에서 모든 앱의 밑바탕에는 *UIWindow* 가 있습니다.
<div class="message">
  UIWindow - An object that provides the backdrop for your app’s user interface and provides important event-handling behaviors.
</div>

 *UIWindow* 는 그 자체로 보여주는 것은 없고, Container View로서만 작동합니다. Xcode로 iOS 프로젝트를 생성하면 *UIWindow* 가 생성됩니다. 이 *UIWindow* 는 사실 거의 건드릴 일이 없습니다만, Status Bar에 layer를 씌우거나 하는 작업을 위해서는 접근이 필요합니다. 그 때는 `AppDelegate.swift`에서 `var window: UIWindow?`와 같은 변수를 통해 접근할 수 있습니다.

#### View Hierarchies and Subview Management
 *View* 는 앞서 언급한 것처럼, 다른 *View* 혹은 components들을 담을 수 있습니다. 이 때 하나의 *View* 에 다른 *View* 를 담게 되면 둘 사이는 **부모-자식 관계** 가 성립하고, 이 때 부모를 **SuperView** 라 하고, 자식을 **SubView** 라고 합니다. 스토리보드를 통해 예를 들어 보겠습니다. 스토리보드에서 하나의 View Controller를 생성하면 기본적으로 Top Layout Guide, Bottom Layout Guide, View라는 3 가지 인스턴스가 생성됩니다. 이 3 가지 인스턴스는 모두 *UIWindow* 의 SubClass이고, 이 때 *UIWindow* 와 *View* 는 특별히 **SuperView** 와 **SubView** 의 관계에 있다고 할 수 있습니다. 아래 그림에서 앞서 언급한 부모-자식 관계를 확인할 수 있습니다.

<img src="https://dl.dropbox.com/s/kyb1081t524xziw/viewArc1.png">

**SuperView** 는 **SubView** 들을 배열의 형태로 저장합니다. 그래서 이 때 **SubView** 들이 겹치게 될 경우, 먼저 추가한 것이 아래 쪽에 위치합니다. 또한, **SuperView** 의 크기를 변화시키면 **SubView** 의 크기에도 영향을 미치므로, 오토레이아웃 설정시 **SuperView** 를 수정할 경우 **SubView** 도 수정해주어야 하는 것이 일반적입니다.

그리고 모든 *View* 에는 그에 상응하는 *layer* 가 존재합니다. 특별한 *layer* 추가 없이 다음과 같은 코드를 써본 적이 있을 것입니다.

{% highlight swift %}
self.view.layer.cornerRadius = 5.0
{% endhighlight %}

네, *View* 의 모서리를 둥글게 만드는 `cornerRadius` 속성은 *layer* 에 포함되어 있습니다. *view* 의 속성과 *layer* 속성을 적절히 섞어서 *view* 의 모양이나 애니메이션에 적절한 효과를 줄 수 있습니다.


#### The View Drawing Cycle

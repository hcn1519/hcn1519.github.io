---
layout: post
comments: true
title:  "Swift 애니메이션 다루기"
excerpt: "Swift의 기본적인 애니메이션을 알아봅니다."
categories: Swift animate transition
date:   2017-07-17 00:30:00
tags: [Swift, Animate, Transition]
image:
  feature: swiftLogo.jpg
---

## View의 모양 변화주기(transition)

`transition(with:duration:options:animations:completion:)` 메소드를 사용하면 특정 View에 transition을 줄 수 있습니다.

{% highlight swift %}
UIView.transition(with: containerView, duration: 0.5, options: .transitionCrossDissolve,
                  animations: {
                     self.targetView.isHidden = false
                     // 에니메이션 적용할 메소드 작성
                  }, completion: { finished in
                    // 에니메이션 완료 후 실행되는 클로저
                    // finished 파라미터는 에니메이션의 완료를 Bool 타입으로 받습니다.
                  })
{% endhighlight %}

유의할 점은 `transition(with: containerView)`에서 with의 매개변수로 에니메이션을 적용할 view를 넣는 것이 아니라, 해당 view의 superView를 넣는다는 점입니다. 또한 위의 코드는 `layoutIfNedded()` 메소드를 통해 코드의 순서를 변경할 수도 있습니다.

{% highlight swift %}
// targetView가 그냥 사라지지 않고, 에니메이션을 통해 없어집니다.
self.targetView.isHidden = false
UIView.transition(with: containerView, duration: 0.5, options: .transitionCrossDissolve,
                  animations: {
                     self.containerView.layoutIfNedded()
                  }, completion: nil)
{% endhighlight %}

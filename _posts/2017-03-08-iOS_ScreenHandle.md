---
layout: post
comments: true
title:  "iOS 디바이스별 화면 다루기"
excerpt: "iOS에서 디바이스 종류에 따라 다른 뷰 설정하기"
categories: iOS
date:   2017-03-08 00:30:00
tags: [iOS, UIKit, UIDevice]
image:
  feature: iOS.png
---

iOS에서 디바이스별로 다양한 화면을 지원함에 따라 view를 설정할 때, 세부적으로 해야할 필요성이 늘어나고 있습니다. iPhone 종류만 iPhone 7, iPhone 7 plus, iPhone SE가 있고, iPad도 프로 모델까지 합하면 설정시 못 해도 6개 이상을 해주어야 합니다. iOS에서는 여러 화면에 대응할 수 있도록 <code>UIDevice</code>를 통해 화면별로 코드를 수정할 수 있도록 해줍니다.

{% highlight swift %}
// ScreenExtesion.swift
import UIKit

extension UIDevice {
    public var isiPhone: Bool {
      if UIDevice.current.userInterfaceIdiom == UIUserInterfaceIdiom.pad {
          return true
      }
      return false
    }
    public var isiPad: Bool {
        if UIDevice.current.userInterfaceIdiom == UIUserInterfaceIdiom.pad {
            return true
        }
        return false
    }
}
{% endhighlight %}

프로젝트에 <code>UIDevice</code>에 대한 <code>extension</code>을 설정해두시면, 프로젝트 어디에서든 해당 화면에 대한 구분을 할 수 있습니다. 즉, view에다가 아래 코드를 입력하여 아이폰에만 적용되는 코드, 아이패드에만 적용되는 코드를 넣을 수 있습니다.

{% highlight swift %}
if UIDevice.current.isiPhone {
  // iPhone         
} else if UIDevice.current.isiPad {
  // iPad
}
{% endhighlight %}

다만, 요즘엔 아이폰과 패드에 대한 구분 이상으로 더 세세하게 나눌 필요가 있습니다. 그래서, 기기별로 좀 더 세세하게 나눠보면,

{% highlight swift %}
// ScreenExtesion.swift
import UIKit

extension UIDevice {
    public var isiPhoneSE: Bool {
        if UIDevice.current.userInterfaceIdiom == UIUserInterfaceIdiom.phone && (UIScreen.main.bounds.size.height == 568 || UIScreen.main.bounds.size.width == 320) {
            return true
        }
        return false
    }
    public var isiPhonePlus: Bool {
        if UIDevice.current.userInterfaceIdiom == UIUserInterfaceIdiom.phone && (UIScreen.main.bounds.size.height == 736 || UIScreen.main.bounds.size.width == 414) {
            return true
        }
        return false
    }

    public var isiPad: Bool {
        if UIDevice.current.userInterfaceIdiom == UIUserInterfaceIdiom.pad && (UIScreen.main.bounds.size.height == 1024 || UIScreen.main.bounds.size.width == 768) {
            return true
        }
        return false
    }
    public var isiPadPro12: Bool {
        if UIDevice.current.userInterfaceIdiom == UIUserInterfaceIdiom.pad && (UIScreen.main.bounds.size.height == 1366 || UIScreen.main.bounds.size.width == 1366) {
            return true
        }
        return false
    }
}
{% endhighlight %}

다음과 같이 나눌 수 있고, 이는 아래 코드들을 사용할 수 있게 해줍니다.

{% highlight swift %}
if UIDevice.current.isiPadPro12 {
  // iPad Pro 12.9          
} else if UIDevice.current.isiPad {
  // iPad Air2, iPad Pro 9.7  
} else if UIDevice.current.isiPhonePlus {
  // iPhone 7+
} else if UIDevice.current.isiPhoneSE {
  // iPhone SE  
} else {
  // iPhone 7
}
{% endhighlight %}

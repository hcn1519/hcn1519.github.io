---
layout: post
title: "iOS 다크모드 알아보기"
date: "2020-03-13 00:53:17 +0900"
excerpt: "iOS에서 다크모드를 적용하기 위해 알아야 하는 내용을 정리하였습니다."
categories: iOS, WWDC, DarkMode, UIKit
tags: [iOS, WWDC, DarkMode, UIKit]
image:
  feature: iOS.png
---

다크모드 도입에 있어서 필요한 정보를 조사하면서 실제 구현과 관련된 내용을 정리해보았습니다. 공식 문서 및 영상을 보면서 관련 내용을 같이 참고하시면 좋을 것 같습니다.(해당 내용의 대부분은 [WWDC - Implement Dark Mode](https://developer.apple.com/videos/play/wwdc2019/214/)을 기반으로 작성되었습니다.)

## 목차

#### 1. UITraitCollection

1. [UITraitCollection.current](./ios_darkmode#1-uitraitcollectioncurrent)
1. [traitCollectionDidChange(_:)](./ios_darkmode#2-traitcollectiondidchange)
1. [`TraitCollection`을 활용하여 라이트/다크 모드 강제 설정하기](./ios_darkmode#3-raitcollection을-활용하여-라이트다크-모드-강제-설정하기)

#### 2. 다크모드 주요 구현 대상

1. [색상](./ios_darkmode#1-색상)
1. [이미지](./ios_darkmode#2-이미지)
1. [기타 Components](./ios_darkmode#3-기타-components)

## UITraitCollection

- [UITraitCollection](https://developer.apple.com/documentation/uikit/uitraitcollection)은 iOS의 인터페이스 환경에 대한 정보를 가지고 있는 객체입니다. 인터페이스 환경 정보에는 iOS 12부터  `userInterfaceStyle`라는 Property가 추가되었고, 이 값을 통해 라이트/다크 모드에 대해서 판별을 할 수 있습니다.(iOS 12에서는 다크모드가 지원되지 않는데, macOS의 다크모드가 지원되면서 API만 미리 추가된 것으로 보입니다.)
- `UITraitCollection`은 앱 실행시 1개의 값만 존재하는 것이 아니라, 각각의 View, ViewController마다 존재합니다. `UITraitCollection` 값은 시스템으로부터 UIScreen으로 전달되고, View 계층 구조 상으로 최하단의 View까지 그 값이 전달됩니다.

![dark1](https://user-images.githubusercontent.com/13018877/76678327-343fca00-661a-11ea-8cb2-5894562c8569.png)

- UIKit은 특정 UIView 객체를 생성할 때, 적합한 `traitCollection`이 무엇인지 예상하여 값을 설정해줍니다. 즉, `addSubView` 과정에서 `traitCollection`을 설정하지 않아도 상속, 사용자 설정 값 등에 기반하여 값이 알아서 설정됩니다.

![dark2](https://user-images.githubusercontent.com/13018877/76678329-373aba80-661a-11ea-910e-bb681c887511.png)

### 1. UITraitCollection.current

- [UITraitCollection.current](https://developer.apple.com/documentation/uikit/uitraitcollection/3238080-current)은 iOS 13에서 추가된 static 변수로 현재의 `traitCollection`을 알려줍니다. UIKit은 UIView를 그릴 때 `UITraitCollection.current`를 해당 View의 `traitCollection`으로 설정하여 `UITraitCollection.current`이 현재의 View에 대한 `traitCollection`을 나타낼 수 있도록 합니다.

```swift
class BackgroundView: UIView {
    override func draw(_ rect: CGRect) {
        // UIKit sets UITraitCollection.current to self.traitCollection
        UIColor.systemBackground.setFill()
        UIRectFill(rect)
    }
}
```

- `TraitCollection.current`은 `layoutSubViews()` 호출 이전에 반드시 업데이트 됩니다. 그러므로,  아래와 같은 layout 메소드에서는 `TraitCollection`이 부모의 것을 획득한 것이 보장됩니다.
- 그래서 라이트/다크 모드 전환시에 업데이트가 필요한 View는 `viewDidLoad()`가 아니라 `layoutSubViews()`에서 업데이트가 진행이 되어야 합니다.
- `layoutSubViews()`는 레이아웃을 그릴 때 반복적으로 호출되는 메소드이므로 코드 작성시 유의해야 합니다.

![dark3](https://user-images.githubusercontent.com/13018877/76678330-3c980500-661a-11ea-8e49-675ab1ae1a1d.png)

```swift
class ViewController: UIViewController {
    override func viewWillLayoutSubviews() {
        super.viewWillLayoutSubviews()
        updateTitle()
    }
    private func updateTitle() {
        if #available(iOS 13.0, *) {
            guard traitCollection.userInterfaceStyle == .dark else {
                self.title = "라이트 모드"
                return
            }
            self.title = "다크 모드"
        } else {
            self.title = "라이트 모드"
        }
    }
}
```

- 이 때 `traitCollection`이 변경될 경우 `traitCollectionDidChange()`이 호출됩니다.

![dark4](https://user-images.githubusercontent.com/13018877/76678332-40c42280-661a-11ea-95f6-07a8dc933471.png)

- `layoutSubViews()`, `traitCollectionDidChange()` 함수 외부에서 `self.view`와 `UITraitCollection.current`는 동일한 값을 보장하지 않습니다.
- 애플에서는 이와 같은 경우에 다음과 같이 3가지 방식으로 대응할 것을 권장하고 있습니다.

```swift
let layer = CALayer()
let traitCollection = view.traitCollection

// Option 1 - resolvedColor를 통해 traitCollection 반영
let resolvedColor = UIColor.label.resolvedColor(with: traitCollection)
layer.borderColor = resolvedColor.cgColor

// Option 2 - performAsCurrent 클로저 활용
traitCollection.performAsCurrent {
    layer.borderColor = UIColor.label.cgColor
}

// Option 3 - 직접 current TraitCollection 업데이트
// 이 경우 UITraitCollection은 동작하는 Thread에서만 적용되어 다른 Thread에 영향을 주지 않습니다.
// 이 방식은 performAsCurrent의 내부 동작과 동일합니다.
let savedTraitCollection = UITraitCollection.current
UITraitCollection.current = traitCollection
layer.borderColor = UIColor.label.cgColor
UITraitCollection.current = savedTraitCollection
```

### 2. traitCollectionDidChange

- [traitCollectionDidChange(_:)](https://developer.apple.com/documentation/uikit/uitraitenvironment/1623516-traitcollectiondidchange)은 인터페이스 환경 변화에 대한 옵저빙 메소드로 `UITraitCollection`이 변경될 때마다 호출이 됩니다.
- iOS 13에서 `traitCollectionDidChange(_:)`는 초기화 과정에서 모든 traitCollection이 결정된 이후에만 호출되도록 API가 변경되었습니다. 이 때문에, 하위 버전에서 `traitCollectionDidChange(_:)`이 호출되던 케이스인데 iOS 13에서는 호출되지 않는 상황이 발생할 수 있습니다.
- `traitCollection`의 변경은 라이트/다크 모드에 국한된 것이 아니라, sizeClass 변경시에도 호출되기 때문에 아래와 같이 `userInterfaceStyle` 변경을 확인할 수 있는 별도의 API가 추가되었습니다.

```swift
override func traitCollectionDidChange(_ previousTraitCollection: UITraitCollection?) {
    super.traitCollectionDidChange(previousTraitCollection)
    if traitCollection.hasDifferentColorAppearance(comparedTo: previousTraitCollection) {
        // Resolve dynamic colors again
    }
}
```

- `traitCollectionDidChange(_:)` 호출 시점에 대한 디버깅을 위해 별도의 argument가 추가되었습니다.

![dark5](https://user-images.githubusercontent.com/13018877/76678335-46ba0380-661a-11ea-926a-f34c76da0fea.png)

### 3. TraitCollection을 활용하여 라이트/다크 모드 강제 설정하기

- iOS 13부터 UIView와 UIViewController는 `overrideUserInterfaceStyle`이라는 property를 새롭게 제공합니다. 이 값에 대해서 `.light`, `.dark`와 같이 지정할 경우 그 하위의 SubView까지 스타일 값이 오버라이딩 됩니다.
- 전체 앱에 대해서 라이트/다크 모드를 강제하려면 Info.plist에 `UIUserInterfaceStyle` 값을 `.light`, `.dark`와 같이 설정해주면 됩니다.

![dark6](https://user-images.githubusercontent.com/13018877/76678338-49b4f400-661a-11ea-9ee5-68b5da4814d8.png)

## 다크모드 주요 구현 대상

### 1. 색상

Xcode에서는 아래와 같은 기능을 통해서 라이트/다크 모드에 대한 색상을 설정할 수 있습니다.

#### namedColor를 통한 지원

- `namedColor`는 **iOS 11 이상** 부터 지원되는 기능으로 Asset Catalog를 통해서 UIColor를 정의하여 사용하는 기능입니다.
- `namedColor`는 일반 이미지처럼 xcasset에 추가할 수 있습니다.
- 이 때, Attribute Inspector에서 appearance 설정을 Any, Dark, Light 설정시 1개의 이름으로 각 모드별 색상이 적용됩니다.

<div class="message">
    Use the Any Appearance variant to specify the color value to use on older systems that do not support Dark Mode.
</div>

![dark7](https://user-images.githubusercontent.com/13018877/76678341-4f123e80-661a-11ea-8182-80b68c2e458a.png)

이렇게 정의된 `namedColor`는 Interface Builder, 코드에서 각각 다음과 같이 사용할 수 있습니다.

- Interface Builder

![dark8](https://user-images.githubusercontent.com/13018877/76678462-95b46880-661b-11ea-86a0-fc0c28f6b21c.png)

- Code

```swift
let purColor = UIColor(named: "Pure")
```

#### System Color

- iOS 13에서는 다크 모드를 지원하는 `System Color`가 추가 되었습니다. `System Color`도 `namedColor`와 유사하게 동작하며 라이트/다크 모드에서 설정된 색상 값이 다릅니다.([색상 표, Human Interface Guidelines - Color](https://developer.apple.com/design/human-interface-guidelines/ios/visual-design/color/))
- `System Color`에는 사용 용도에 맞춰서 View의 이름으로 정의된 색상(semantically defined system color)도 존재합니다.

```swift
let color: UIColor = UIColor.systemBlue
let labelColor: UIColor = UIColor.label
```

`System Color` 이외에 기존에 사용되던 `UIColor.black`, `UIColor.white`와 같은 색상은 라이트/다크 모드 전환이 지원되지 않습니다. 그래서 다크 모드가 지원되는 화면에서는 해당 색상들이 `System Color`로 변경되거나, 적절히 정의된 `namedColor`로 설정되어야 합니다.

#### Resolved Color

- UIColor에는 [resolvedColor(:UITraitCollection)](https://developer.apple.com/documentation/uikit/uicolor/3238042-resolvedcolor) extension 메소드가 iOS 13에서 추가되었습니다.
- `resolvedColor`는 시스템의 라이트/다크 모드와 관계 없이 특정 View에 설정된 `UITraitCollection`에 맞춰서 정해진 색상을 반환합니다.

```swift
// ViewController와 subView의 UITraitCollection.userInterfaceStyle에 따라서 값이 다름
let vcBGColor = UIColor.systemBackground.resolvedColor(with: viewController.traitCollection)
let subViewBGColor = UIColor.systemBackground.resolvedColor(with: subView.traitCollection)
```

#### Dynamic Provider

iOS 13 이상에서 UIColor에 신규 API인 [UIColor.init(dynamicProvider:)](https://developer.apple.com/documentation/uikit/uicolor/3238041-init)이 추가되었습니다.

```swift
extension UIColor {
    @available(iOS 13.0, *)
    public init(dynamicProvider: @escaping (UITraitCollection) -> UIColor)
}
```

- 해당 생성자는 `UITraitCollection`에 따라서 색상을 리턴할 수 있는 기능을 지원합니다.
- 코드로 라이트/다크 모드에 대한 분기 처리가 필요할 때 사용할 수 있습니다.
- `dynamicProvider`는 `UITraitCollection.current`를 사용하여 `userInterfaceStyle`을 판별하므로 별도의 `traitCollection`을 인자로 넘기지 않고도 색상을 설정할 수 있습니다.

```swift
let myColor: UIColor = {
    if #available(iOS 13, *) {
        let color = UIColor(dynamicProvider: { traitCollection in
            if traitCollection.userInterfaceStyle == .dark {
                return UIColor.white
            } else {
                return UIColor.black
            }
        })
        return color
    } else {
        // 하위버전
        return UIColor.black
    }
}()
```

> Note: dynamicProvider 생성자를 활용해서 생성된 UIColor는 Interface Builder에서 사용할 수 없습니다.

### 2. 이미지

다크모드와 관련된 이미지 API의 경우에도 색상과 거의 동일한 API를 사용합니다. 이미지도 색상과 동일하게 Asset Catalog에서 라이트/다크 모드에 맞춰서 이미지를 노출하도록 설정 할 수 있습니다.

![dark9](https://user-images.githubusercontent.com/13018877/76678469-a1a02a80-661b-11ea-8ab5-23b8606097e2.png)

#### Template Image

- 아이콘과 같은 이미지의 경우에는 이미지의 `rendering mode`를 `template Image`로 설정하여 `tintColor`를 주어서 다크모드를 지원하는 방법도 있습니다. 이 방법 사용시에는 라이트/다크 모드에 맞춰서 `tintColor`를 적용하면 됩니다.
- Template Image도 Asset Catalog 설정, Code 설정 모두 지원합니다.

![dark92](https://user-images.githubusercontent.com/13018877/76678472-a5cc4800-661b-11ea-9379-09738bf2c7c4.png)

```swift
let image = UIImage(named: "dessert")?.withRenderingMode(.alwaysTemplate)
```

#### Resolved Image

이미지의 경우에도 `UITraitCollection`에 맞춰서 나타나는 이미지를 동적으로 변경할 수 있습니다. 다만 이는 `UIImage`의 extension으로 제공되는 것이 아니라, `UIImageAsset`의 extension으로 제공됩니다.

- 참고 - [Providing Images for Different Appearances - Apple Article](https://developer.apple.com/documentation/uikit/uiimage/providing_images_for_different_appearances)

```swift
open class UIImageAsset : NSObject, NSSecureCoding {
    open func image(with traitCollection: UITraitCollection) -> UIImage
}

// Usage
let image = UIImage(named: "HeaderImage")
let asset = image?.imageAsset
let resolvedImage = asset?.image(with: traitCollection)
```

#### Symbol Image

Symbol Image의 경우에는 애플에서 제작한 [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols/overview/) 기반으로 구성된 벡터 이미지입니다. 해당 Symbol을 커스텀해서 앱 디자인에 맞는 심볼을 제공할 수 있습니다.

- 참고 - [Configuring and Displaying Symbol Images in Your UI - Apple Article](https://developer.apple.com/documentation/uikit/uiimage/configuring_and_displaying_symbol_images_in_your_ui))

### 3. 기타 Components

#### 1. StatusBar

statusBarStyle에서 `darkContent` 옵션이 추가되었습니다.

```swift
public enum UIStatusBarStyle : Int {
    case `default` // Automatically chooses light or dark content based on the user interface style
    @available(iOS 7.0, *)
    case lightContent // Light content, for use on dark backgrounds
    @available(iOS 13.0, *)
    case darkContent // Dark content, for use on light backgrounds
}
```

#### 2. UIActivityIndicatorView

기존의 색상 이름으로 설정되던 스타일이 `.medium`, `.large`로 변경되었습니다.

```swift
UIActivityIndicatorView(style: .medium)
UIActivityIndicatorView(style: .large)
```

![스크린샷 2020-03-05 오후 5 50 56](https://media.oss.navercorp.com/user/10153/files/e1735d80-5f09-11ea-8c65-cb66b351fc67)

#### 3. AttributedString

AttributedString의 경우 **모두** `foregroundColor`를 라이트/다크 모드에 맞게 추가해주어야 합니다.

```swift
let attributes: [NSAttributedString.Key: Any] = [
    .font: UIFont.systemFont(ofSize: 36.0),
    .foregroundColor: UIColor.label
]
```

## 참고자료

- [WWDC - Implement Dark Mode](https://developer.apple.com/videos/play/wwdc2019/214/)
- [Apple Article - Supporting Dark Mode in Your Interface](https://developer.apple.com/documentation/xcode/supporting_dark_mode_in_your_interface)
- [NSHipster - Dark Mode on iOS 13](https://nshipster.com/dark-mode/)
- 기타 관련 API 문서 - 해당 링크는 설명 중간에 포함

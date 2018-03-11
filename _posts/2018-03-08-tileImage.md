---
layout: post
title: "이미지 타일링을 통한 고해상도 이미지 로딩"
excerpt: "타일 이미지를 활용하여 고해상도 이미지를 랜더링하는 방법에 대해 알아봅니다."
categories: TiledImage, Display
date: "2018-03-08 18:28:51 +0900"
tags: [TiledImage, Display, Swift]
image:
  feature: tiledimage.png
---

## 1. 요구사항: 고해상도 이미지 빠르게 보여주기

정말 당연한 얘기이지만, 용량이 큰 이미지를 화면에 로딩하는 것은 시간이 오래 걸립니다. 요즘 컴퓨터가 성능이 좋아져서 큰 이미지를 빠르게 로딩하는 능력도 좋아졌지만, 그에 맞춰 사용되는 이미지도 4K, 8K, 12K로 계속해서 그 사이즈가 커지고 있어서 큰 이미지를 화면에 랜더링하는 것은 여전히 시간이 많이 걸리는 작업입니다.

심지어 어떤 이미지는 너무 커서 아예 화면에 로딩하는 것이 불가능합니다. 이미지를 화면에 로딩하려면 메모리 공간에 이미지를 올려야 하는데 이미지 용량이 메모리보다 커버리면 아예 로딩이 안되는 것이지요.😞 이러한 이미지의 대표적인 예로는 지도 이미지나 인공위성 이미지 같은 것들이 있습니다. 이러한 이미지는 지구 전체를 일정 수준 이상의 퀄리티로 전부 커버해야하니 몇 기가로는 어림도 없는 상황인 것입니다.

## 2. 이미지 타일링 기법

이미지 타일링 기법은 이러한 거대한 이미지를 화면에 랜더링하기 위해 만들어진 기법입니다. 이미지 타일링은 이미지를 타일 형태로 조각내어 화면에 로딩하는 방식을 의미합니다.

<div class="message">
  Tiles - Tiling an image segments it into a number of smaller rectangular areas called tiles.
</div>
출처: [Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)

 그런데 당연하게도 `큰 이미지 사이즈 = 타일 이미지 사이즈 * n(타일 수)` 라는 공식은 무시할 수 있는 오차 수준 내에서 성립합니다. 그래서 단순히 타일 형태로 이미지를 자르는 것은 의미가 없어보입니다. 하지만, 이렇게 이미지를 조각내는 것은 전체 이미지에서 필요한 부분만 로딩할 수 있게 해주고 이는 많은 장점을 가지고 있습니다.

 * 타일 이미지는 메모리에 올릴 수 있습니다.

 타일 이미지는 전체 이미지를 조각낸 것이기 때문에 그 크기가 전체 이미지보다 작습니다. 그래서 디바이스의 허용 메모리에 맞게 이미지를 조각내면 타일 이미지들은 메모리보다 크기가 작으므로 화면에 표시될 수 있습니다.

* 거대한 이미지의 부분만 보여도 유용한 경우가 많습니다.

<img src="https://dl.dropbox.com/s/yqmf6e1ysigfvdv/requiredImage.png" style="max-width: 90%; margin: 0 auto;">

지도 서비스를 생각해보면 이 경우를 쉽게 알 수 있습니다. 네이버 지도 앱을 켜서 이미지 로딩을 유심히 살펴보면 화면에는 전체 지도 이미지가 나오지 않습니다. 사실 애초에 그럴 필요가 없습니다. 오히려 서울 지도가 필요한 사람이 제주도 쪽을 볼 것을 우려하여 사용자가 아직 제주도 지역으로 줌을 옮기지 않았는데도 미리 제주도 지도 이미지를 다운받는 것은 굉장한 **낭비**입니다. 따라서 지도 앱은 사용자가 보는 부분을 중심으로 꼭 필요한 부분의 이미지만 화면에 로딩하고, 나머지 이미지는 사용자가 줌을 옮길 때, 필요에 의해 이미지가 로딩됩니다. 이렇게 전체 지도 이미지를 로딩하지 않고 부분만 로딩하는 지도 앱이 유용하다는 것은 제가 굳이 설명하지 않아도 동의할 것이라 생각합니다.

* 타일 이미지는 자신이 표현하는 부분에 대해서는 전체 이미지보다 우선적으로 로딩될 수 있습니다.

<img src="https://dl.dropbox.com/s/j8qdm0q64d00hvn/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202018-03-09%20%EC%98%A4%ED%9B%84%209.37.32.png" style="max-width: 70%; margin: 0 auto;">

타일 이미지는 전체 이미지의 부분이기 때문에 `타일 이미지 용량 <= 전체 이미지 용량`이라는 등식은 항상 성립합니다. 그래서 기본적으로 타일 이미지 로딩은 전체 이미지 로딩보다 빠릅니다. 현대의 디바이스 혹은 브라우저들은 비동기 UI 업데이트를 지원합니다. 그래서 로딩이 완료된 타일 이미지는 우선적으로 화면에 업데이트 될 수 있습니다. 이는 사용자가 이미지의 특정 부분을 빠르게 볼 수 있도록 합니다.

## 3. Image Pyramids

이미지 타일링 기법만으로도 큰 이미지를 로딩할 수 있지만, 이미지 타일링만으로는 이미지 로딩속도가 충분히 빠르지 않습니다. 그래서 이를 보완하기 위해 서로 다른 **scale**의 이미지를 활용합니다. **Image Scaling**이라는 것은 이미지의 사이즈를 재조정하는 것을 의미하는데, 이 때 기본 이미지를 서로 다른 크기로 scaling한 일련의 이미지 집합을 **Image Pyramids**라고 합니다. 이 때, scale의 크기는 이미지의 크기와 반비례 값을 갖습니다.

<img src="https://dl.dropbox.com/s/i7cmu15sl93bdtt/img_pyrm.gif" style="max-wid
th: 100%; margin: 0 auto;">
출처: [Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)

### Gaussian Pyramids

**Image Pyramids**도 그 종류가 여러가지인데 그 중 **Gaussian Pyramids**은 이미지를 스케일링하는(사이즈 축소) 것뿐만 아니라, 이미지의 일정 픽셀을 버려서 이미지를 sub sampling하는(해상도 축소) 방식으로 이미지 집합을 만든 피라미드입니다. 그래서 **Gaussian Pyramids** 레벨마다 이미지의 크기가 매우 빠르게 줄어드는 특징을 가지고 있습니다.

<img src="https://dl.dropbox.com/s/i409yl3tipn0hkp/pyramid.png" style="max-width: 80%; margin: 0 auto;">
출처: [Pyramid (image processing) - Wikipedia](https://en.wikipedia.org/wiki/Pyramid_(image_processing))

## 4. Image Tiling과 Gaussian Pyramids

위에서 알아본 Image Tiling과 Gaussian Pyramids를 결합하여 고해상도 이미지 로딩을 위한 타일 이미지를 생성합니다. 즉, 각각의 피라미드 레벨에 해당하는 피라미드 이미지마다 타일이미지를 생성하는 것입니다. 이런 방식으로 타일 이미지를 생성하는 것은 기존 Image Tiling이 (x,y)의 좌표값만을 파라미터로 사용한 것에서 이미지 scale 값을 새로운 파라미터로 추가한 것이라고 이해하면 됩니다. 그래서 타일을 자를 때 각각의 타일 이미지는 자신의 위치를 위한 이미지 내에서의 (x,y) 값과 더불어 scale(줌 레벨) 값을 알고 있어야 합니다.

<img src="https://dl.dropbox.com/s/n507zqwlvc4co6h/Image_Tiling-21.jpg" style="max-width: 100%; margin: 0 auto;">
출처: [Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)

위의 그림은 점선으로 표현된 실제 기기에서 보여지는 부분이 이미지의 scale(사용자가 줌인 한 수준)에 따라 전체 이미지의 어떤 부분을 표현하는 것인지를 보여주는 그림입니다. 여기서는 줌을 확대할 수록(level 0에 가까울 수록) 원본 이미지에 가까워지게 되고, 줌을 축소할 수록(level 2에 가까울 수록) 저화질의 이미지가 화면에 나오게 됩니다.

<br>
<br>

# 코드 구현(THTiledImageView, Swift)

여기서부터는 위의 내용을 활용하여 실제로 iOS 플랫폼에서 위의 내용에 기반한 이미지뷰를 만든 방식에 대해 설명하고자 합니다. 먼저 코드는 [THTiledImageView](https://github.com/TileImageTeamiOS/THTiledImageView)에 CocoaPod을 통해 배포되고 있습니다. 그리고 구체적인 사용 예시는 [THStorytellingView](https://github.com/TileImageTeamiOS/THStorytellingView)에서 확인할 수 있습니다.

## 들어가기 전에

먼저 코드를 살펴보기 전에 코드를 수월하게 이해하기 위한 간단한 개념들을 살펴보고자 합니다. 이미 아는 내용이라면 건너뛰어도 무방합니다.

### View와 Layer

첫 번째로 `View`와 `Layer`에 대한 구분입니다. iOS에서 화면에 무엇인가를 표시하기 위해 기본적으로 `View` 클래스를 사용합니다.  

#### View

<div class="message">
  UIView - An object that manages the content for a rectangular area on the screen. Views are the fundamental building blocks of your app's user interface, and the UIView class defines the behaviors that are common to all views ...
</div>
출처: [UIKit - UIView](https://developer.apple.com/documentation/uikit/uiview)

애플에서 설명하는 정의해서 알 수 있듯이, `View`는 화면의 사각형 반경 내의 UI를 구성할 때 쓰이는 클래스를 통칭합니다. 일반적으로 MVC 패턴을 얘기할 때 V가 이 View를 의미하는 것으로 View는 사용자와의 직접적인 커뮤니케이션(보고, 터치하고 등)을 담당합니다. 그래서 iOS에서 `View`는 크게 다음과 같은 3가지 기능을 담당한다고 말할 수 있습니다.

1. Drawing and animation - 먼저 `View`는 UIKit이나 Core Graphics를 통해 View 안의 콘텐츠를 그릴 수 있습니다.(THTiledImageView는 이 방식을 통해 타일 이미지를 업데이트합니다.)
2. Layout and subview management - `View`는 `SubView`를 포함할 수 있어서 계층 구조 형태로 화면 레이아웃을 구성할 수 있도록 해줍니다.
3. Event handling - `View`는 터치나 다른 이벤트를 사용할 수 있습니다.

#### Layer

앞서서 View에 대해 알아보았으니 이번에는 `Layer`를 알아보겠습니다.

<div class="message">
  An object that manages image-based content and allows you to perform animations on that content. Layers are often used to provide the backing store for views but can also be used without a view to display content.
</div>
출처: [QuartzCore - CALayer](https://developer.apple.com/documentation/quartzcore/calayer)

`Layer`는 콘텐츠의 시각적인 부분을 담당하는 객체입니다. `Layer`는 View와는 다르게 Layer는 이벤트를 관리할 수 없고, 전적으로 콘텐츠의 Drawing, Animation 을 담당합니다. 앞서서 `View`가 콘텐츠의 Drawing, Animation을 담당한다고 서술하였는데, 이는 `View` 안에 기본적으로 포함되어 있는 `Layer`를 통해 이뤄지는 작업입니다. 즉, 하나의 `View`에는 기본적으로 해당 `View`의 bounds만큼을 차지하는 `Layer`가 있고, 이 `Layer`가 콘텐츠의 Drawing, Animation을 담당합니다. 애플은 `Layer`를 다양한 화면 구성을 할 수 있도록 여러가지 `Layer`를 제공합니다. 해당 `Layer`들의 종류와 쓰임새는 다음  [raywenderlich - CALayer Tutorial for iOS: Getting Started](https://www.raywenderlich.com/169004/calayer-tutorial-ios-getting-started)에서 확인할 수 있습니다.

### CGRect, CGPoint, CGSize

다음으로 화면에 어떤 위치에 View가 들어가기 위해 필요한 좌표 및 View의 사이즈를 담당하는 객체를 소개하고자 합니다.

{% highlight shell %}
CGRect - A structure that contains the location and dimensions of a rectangle.
CGPoint - A structure that contains a point in a two-dimensional coordinate system.
CGSize - A structure that contains width and height values.
{% endhighlight %}

View가 화면안에서 표현되기 위해서는 위치와 사이즈 값을 갖고 있어야 하는데 이를 `frame`이라고 합니다. 그리고 이 `frame`은 `CGRect` 타입으로 모든 View는 이 값을 갖고 있어야 화면에 표현될 수 있습니다.

<img src="https://dl.dropbox.com/s/5rwfsqzsawe1e33/rect.png" style="max-width: 80%; margin: 0 auto;">

iOS에서는 기본적으로 좌측 상단이 (x,y)값이 (0,0)인 좌표시스템을 갖고 있습니다. 그래서 위의 경우에서 파란색 View는 다음과 같은 `frame` 값을 지닙니다.

{% highlight swift %}
blueView.frame = CGRect(origin: CGPoint(30, 120), size: CGSize(width: 240, height: 120))
{% endhighlight %}

<br>

## Image Tiling in THTiledImageView

여기서부터는 `THTiledImageView`에서 어떤 방식으로 타일 이미지를 화면에 불러내는지에 대해 코드를 통해 설명하고자 합니다. 여기서 설명하고자 하는 코드는 [THTileImageView.swift](https://github.com/TileImageTeamiOS/THTiledImageView/blob/master/THTiledImageView/THTiledImageView/THTileImageView.swift)에 있는 코드들입니다.

### THTiledImageView의 구조

`THTiledImageView`는 `UIView` 클래스를 상속합니다. 그리고, View를 그리기 위한 정보는 `THTiledImageViewDataSource` 객체가 가지고 있고, `THTiledImageView`는 이를 reference 형태로 가지고 있습니다.

{% highlight swift %}
class THTiledImageView: UIView {
    var dataSource: THTiledImageViewDataSource?
}
{% endhighlight %}

그래서 `THTiledImageView` 만들 때, 생성자(init)에서 전체 이미지 사이즈(originalImageSize), 사용할 타일 이미지의 레벨 범위(minTileLevel, maxTileLevel)를 지정합니다.

{% highlight swift %}
convenience init(dataSource: THTiledImageViewDataSource) {
    self.init(frame: CGRect(origin: CGPoint.zero, size: dataSource.originalImageSize))

    guard let layer = self.layer as? TiledLayer else { return }

    let scale = UIScreen.main.scale
    layer.contentsScale = scale

    let min = dataSource.minTileLevel
    let max = dataSource.maxTileLevel

    layer.levelsOfDetail = max - min + 1

    let tileSize = dataSource.tileSize
    layer.tileSize = tileSize[0]

    frame = CGRect(origin: CGPoint.zero, size: dataSource.originalImageSize)
}
{% endhighlight %}

### THTiledImageView Drawing

#### draw(rect:)

`THTiledImageView`는 View를 사용하는 여러가지 방법중에 `Drawing(draw(rect: CGRect))`을 사용합니다. 이는 `THTiledImageView`가 하나의 이미지 파일로 이뤄진 것이 아니라, 하나의 UIView 안에 여러 타일 이미지를 보여주어야 하기 때문입니다. `draw(rect:)` 함수는 최대 60hz(1초에 60번) 호출되는 함수로 업데이트 되어야 하는 `rect`를 갖고 호출됩니다.

{% highlight swift %}
class THTiledImageView: UIView {
  override func draw(_ rect: CGRect) {
    // 아이폰 기준으로 최대 60hz 수준으로 호출됩니다.
  }
}
{% endhighlight %}

`draw(rect:)`는 시스템에서 업데이트가 필요할 때 우선적으로 호출되고 모든 화면의 업데이트가 끝나면 더이상 호출되지 않습니다. 바꿔말하면, 화면에 나타나는 부분이 모두 업데이트 되면 메소드는 종료됩니다. 그래서 해당 View의 화면을 이동하고 나서 추가적으로 로딩이 필요한 View를 업데이트 하기 위해서는 `setNeedsDisplay(rect:)`를 호출합니다. 이 함수를 호출하면 해당 rect에 대해서 `draw(rect:)`가 재호출됩니다.

#### CTM

iOS에서는 사용자가 사용하는 (x, y) 좌표값을 화면에 출력될 위치로 변환하기 위해 `Current Transformation Matrix(이하 CTM)`라는 3x3 행렬을 사용합니다. 여기서 x값에 관여하는 값이 ctm 행렬의 a이고 이를 통해 화면상에서의 이미지 scale 값을 도출할 수 있습니다.

{% highlight swift %}
override func draw(_ rect: CGRect) {
    // ctm 사용을 위한 context 호출
    let context = UIGraphicsGetCurrentContext()!

    // 디바이스 scale 고려하여 zoomScale 도출
    let scaleX = context.ctm.a / UIScreen.main.scale

    // 사용자의 zoomScale 값
    let x = round(log2(Double(scaleX)))
    let level = dataSource.maxTileLevel + Int(x)
}
{% endhighlight %}

#### Tile Loading

이렇게 이미지의 zoomLevel을 파악하고 난 후 타일 이미지를 화면에 맞게 호출합니다. 개별 타일 이미지는 사이즈 정보와 어떤 level(scale)에서, 어떤 (x,y)에 쓰이는지 정확히 알 수 있도록 `{imageName_imageSize_level_x_y}.jpg`의 형태로 이름을 갖고 있습니다. 이미지는 2차원 형태이기 때문에 전체 사각형 안에서 2중 루프를 돌면서 타일을 채워야 합니다. `draw(rect:)` 함수는 비동기로 작동하여 화면을 업데이트 하기 때문에 화면은 루프 순서대로 업데이트 되지는 않습니다.

{% highlight swift %}
// 부가적인 부분은 제거한 코드입니다.
override func draw(_ rect: CGRect) {
    let firstColumn = Int(rect.minX / length)
    let lastColumn = Int(rect.maxX / length)
    let firstRow = Int(rect.minY / length)
    let lastRow = Int(rect.maxY / length)

    for row in firstRow...lastRow {
        for column in firstColumn...lastColumn {
          if let tile = imageForTileAtColumn(imageSize: size[level - 1], tileRect: tileRect, column, row: row, level: level) {
              tile.tileImage.draw(in: tileRect)
          }      
        }
    }
}

private func imageForTileAtColumn(imageSize: CGSize, tileRect: CGRect, _ column: Int, row: Int, level: Int) -> THTile? {
    guard let dataSource = dataSource else { return nil }

    let sizeInt = Int(imageSize.width)
    // 타일 이미지 Key 값
    let imageKey = dataSource.thumbnailImageName + "_\(sizeInt)_\(level)_\(column)_\(row).\(dataSource.imageExtension)"

    if let image = THImageCacheManager.default.retrieveTiles(key: imageKey) {
        return THTile(tileImage: image, tileRect: tileRect)
    } else {
        return nil
    }
}
{% endhighlight %}

> 타일 이미지를 서버로부터 다운로드 받아서 처리하는 것은 downloadAndRedrawImages 함수에서 수행됩니다. 가장 먼저 이미지가 캐싱되어 있는지 확인하고, 이미지 다운로드가 진행됩니다. 그리고 그 이후는 타일마다 이미지 다운로드 -> 캐싱 -> setNeedsDisplay(rect:) 호출 -> draw(rect:) -> 다운로드된 이미지 업데이트 순서로 수행됩니다.

-----

## 참고자료
* [Display in iOS](https://developer.apple.com/library/content/documentation/DeviceInformation/Reference/iOSDeviceCompatibility/Displays/Displays.html)
* [Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)
* [Scale Space와 이미지 피라미드(image pyramid)](http://darkpgmr.tistory.com/137)
* [UIKit - UIView](https://developer.apple.com/documentation/uikit/uiview)
* [QuartzCore - CALayer](https://developer.apple.com/documentation/quartzcore/calayer)

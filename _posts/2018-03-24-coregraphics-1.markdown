---
layout: post
title: "Core Graphics 1"
date: "2018-03-24 00:53:17 +0900"
excerpt: "Core Graphics에 대해 학습한 내용을 정리합니다."
categories: CoreGraphics iOS
tags: [CoreGraphics, iOS]
image:
  feature: iOS.png
---

> 이 시리즈는 애플의 [CoreGraphics](https://developer.apple.com/library/content/documentation/GraphicsImaging/Conceptual/drawingwithquartz2d/dq_overview/dq_overview.html#//apple_ref/doc/uid/TP30001066-CH202-CJBBAEEC) 문서를 기반으로 정리한 내용을 담고 있습니다.

`Core Grahics`는 애플의 플랫폼에서 2차원 그래픽을 담당하는 기술을 의미합니다. `Core Grahics`는 `Quartz 2D`라는 엔진을 통해 구현되는데, 이 때 `Quartz 2D`에서 제공하는 API를 활용하여 개발자는 디바이스 화면에 이미지를 로딩한다든지, 도형을 그린다든지 하는 일련의 그래픽 작업을 수행할 수 있습니다. 이 포스팅에서는 `Quartz 2D`의 몇 가지 기본 개념 및 컨셉에 대해 알아보고자 합니다.

## Painter draws an Image on paper in Quartz 2D

`Quartz 2D`에서는 *Painter* model라는 것을 기반으로 그래픽을 화면에 표시합니다. *Painter* model은 다음 2가지 단계를 통해 그래픽을 구현합니다.

1. 각각의 연속적인 Drawing(그림)은 layer에 그려지고, 이 그림은 canvas(page)에 표현된다.
2. 이 page에 표현된 그림은 추가적인 그림을 겹치는 형태로 수정된다.

<img src="https://dl.dropbox.com/s/70doq0y7d4rlpaa/coreGraphicsFig1.png" style="margin: 0 auto;">

이러한 과정은 여러개의 그림을 투명한 종이에 그려놓고 이 그림을 겹쳐서 하나의 그림을 만든다고 생각하면 이해가 쉽습니다. 다만 이 때 특정 그림을 앞에 두어서 뒤에 있는 그림이 가려지는 경우가 생기는데 *Painter* model도 그 영향을 받아서 그림을 그리는 순서를 잘 지켜야 원하는 그래픽을 얻을 수 있습니다.

## Drawing Destinations: Graphic Context

<div class="message">
  A graphics context is an opaque data type (CGContextRef) that encapsulates the information Quartz uses to draw images to an output device, such as a PDF file, a bitmap, or a window on a display.
</div>

`Graphic Context`은 Quartz가 출력 기기(pdf, bitmap, display 등)에 이미지를 그리기 위한 정보들을 담고 있는 데이터 타입입니다. 그래서 `Graphic Context`은 그래픽 drawing parameters나 기기별 page의 paint 정보가 담겨 있습니다. `Graphic Context`는 그래픽 출력 형식에 따라 다른 타입을 사용합니다.

<img src="https://dl.dropbox.com/s/j4qhae761uypuan/core2.png" style="margin: 0 auto;">

이렇게 `Graphic Context`가 기기별로 이미지를 그리기 위한 정보를 담고 있기 때문에, 이는 그림이 표현되는 목적지로 이해가 될 수 있습니다. 이 말은 `Graphic Context` 자체가 디바이스별 이미지 정보를 모두 담고 있기 때문에 `Graphic Context`만 알아도 이미지가 어떻게 출력될 것인지 알 수 있다는 것을 의미합니다. 그래서 사용자가 하나의 이미지를 여러 기기에 출력하고 싶을 때 상황별 `Graphic Context`만 제공하면 `Quartz`가 기기별 차이 계산을 알아서 수행합니다.

## Graphic State

Quartz는 현재의 `Graphic state`에 따라서 drawing의 결과를 수정합니다. `Graphic state`에는 `Drawing Routines`가 인자로 포함되어 있습니다. `Drawing Routines`은 `Graphic state`을 참조하여 결과를 랜더링(화면을 그리는) 방식을 사용합니다. 그래서 `Graphic state`에 색을 칠하거나, 현재 위치를 바꾸거나, 텍스트 사이즈를 바꾸는 것과 같은 것들을 적용하면 그리는 대상의 형태도 바뀐 형태로 나타납니다.

`Graphic context`는 `Graphic state`를 그래픽의 적용 순서를 유지하기 위해 스택의 형태로 저장합니다. `Graphic context`는 현재의 상태를 저장하기 위해 `CGContextSaveGState` 함수를 호출하는데, 이 때 `Graphic state`의 복사본이 스택에 push되고, 저장된 그래픽을 불러올 때는 `CGContextRestoreGState` 함수를 호출하여 `Graphic state`의 복사본을 pop합니다.

## Quartz 2D Coordinate systems

Coordinate system(좌표 시스템)은 그래픽의 위치와 크기를 정의하는 것으로 floating-value(CGFloat) 형태로 정의됩니다. Quartz는 Current Transformation Matrix(CTM)을 사용하여 사용자가 지정한 그래픽의 위치와 사이즈를 기기별로 독립적인 좌표 시스템을 사용하는 화면의 device space로 매핑합니다.

> 간단히 생각하면, Quartz는 UIView에서 지정한 Frame 값을 디바이스의 적절한 위치에 놓아 화면에 나타나도록 하는 역할을 담당한다고 보면 됩니다.

CTM은 Affine Transform이라는 매트릭스 타입의 한 종류로 하나의 좌표를 다른 하나의 좌표로 전환하는 역할을 수행합니다. 그리고 이 때, CTM은  translation, rotation, scaling operations를 활용하여 대상이 그려지는 형태를 변환하는 역할도 맡습니다. 예를 들어서 박스를 45도 기울인 형태로 그리고 싶으면 박스를 그리기 전에 ctm을 45도 기울이면 됩니다.

{% highlight swift %}
import UIKit

class RotatedView: UIView {

    override func draw(_ rect: CGRect) {
        super.draw(rect)

        let context = UIGraphicsGetCurrentContext()!

        context.setFillColor(UIColor.green.cgColor)

        // Context Origin 설정
        let centerX = rect.origin.x + rect.size.width / 2
        context.translateBy(x: centerX, y: rect.origin.y)

        // Context 사이즈 조정
        context.scaleBy(x: 1/sqrt(2), y: 1/sqrt(2))

        // Context 회전
        context.rotate(by: CGFloat(45 * Double.pi / 180))
        context.fill(rect)
    }
}
{% endhighlight %}


---

## 참고자료
* [Overview of Quartz 2D Programming Guide](https://developer.apple.com/library/content/documentation/GraphicsImaging/Conceptual/drawingwithquartz2d/dq_overview/dq_overview.html#//apple_ref/doc/uid/TP30001066-CH202-TPXREF101)

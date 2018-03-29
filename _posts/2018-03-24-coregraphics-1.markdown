---
layout: post
title: "Core Graphics 1"
date: "2018-03-24 00:53:17 +0900"
excerpt: "Core Graphics에 대해 학습한 내용을 정리합니다."
categories: CoreGraphics
tags: [CoreGraphics]
---

> 이 시리즈는 애플의 [CoreGraphics](https://developer.apple.com/library/content/documentation/GraphicsImaging/Conceptual/drawingwithquartz2d/dq_overview/dq_overview.html#//apple_ref/doc/uid/TP30001066-CH202-CJBBAEEC) 문서를 기반으로 정리한 내용을 담고 있습니다.

`Core Grahics`는 애플의 플랫폼에서 2차원 그래픽을 담당하는 기술을 의미합니다. `Core Grahics`는 `Quartz 2D`라는 엔진을 통해 구현되는데, 이 때 `Quartz 2D`에서 제공하는 API를 활용하여 개발자는 디바이스 화면에 이미지를 로딩한다든지, 도형을 그린다든지 하는 일련의 그래픽 작업을 수행할 수 있습니다. 이 포스팅에서는 `Quartz 2D`의 몇 가지 기본 개념 및 컨셉에 대해 알아보고자 합니다.

## Painter draws an Image on paper in Quartz 2D

`Quartz 2D`에서는 *Painter* model라는 것을 기반으로 그래픽을 화면에 표시합니다. *Painter* model은 다음 2가지 단계를 통해 그래픽을 구현합니다.

1. 각각의 연속적인 Drawing(그림)은 layer에 그려지고, 이 그림은 canvas(page)에 표현된다.
2. 이 page에 표현된 그림은 추가적인 그림을 겹치는 형태로 수정된다.

<img src="https://dl.dropbox.com/s/70doq0y7d4rlpaa/coreGraphicsFig1.png" margin: 0 auto;">

이러한 과정은 여러개의 그림을 투명한 종이에 그려놓고 이 그림을 겹쳐서 하나의 그림을 만든다고 생각하면 이해가 쉽습니다. 다만 이 때 특정 그림을 앞에 두어서 뒤에 있는 그림이 가려지는 경우가 생기는데 *Painter* model도 그 영향을 받아서 그림을 그리는 순서를 잘 지켜야 원하는 그래픽을 얻을 수 있습니다.

## Drawing Destinations: Graphic Context

<div class="message">
  A graphics context is an opaque data type (CGContextRef) that encapsulates the information Quartz uses to draw images to an output device, such as a PDF file, a bitmap, or a window on a display.
</div>

`Graphic Context`은 Quartz가 출력 기기(pdf, bitmap, display 등)에 이미지를 그리기 위한 정보들을 담고 있는 데이터 타입입니다. 그래서 `Graphic Context`은 그래픽 drawing parameters나 기기별 page의 paint 정보가 담겨 있습니다. `Graphic Context`는 그래픽 출력 형식에 따라 다른 타입을 사용합니다.

<img src="https://dl.dropbox.com/s/j4qhae761uypuan/core2.png" margin: 0 auto;">

이렇게 `Graphic Context`가 기기별로 이미지를 그리기 위한 정보를 담고 있기 때문에, 이는 그림이 표현되는 목적지로 이해가 될 수 있습니다. 이 말은 `Graphic Context` 자체가 디바이스별 이미지 정보를 모두 담고 있기 때문에 `Graphic Context`만 알아도 이미지가 어떻게 출력될 것인지 알 수 있다는 것을 의미합니다. 그래서 사용자가 하나의 이미지를 여러 기기에 출력하고 싶을 때 상황별 `Graphic Context`만 제공하면 `Quartz`가 기기별 차이 계산을 알아서 수행합니다.

## Quartz Data Type, Graphic State

* Quartz Data Type

Quartz는 Graphic Context뿐만 아니라, 그래픽을 위한 다른 데이터 타입을 API로 제공합니다.



---

## 참고자료
* [Overview of Quartz 2D Programming Guide](https://developer.apple.com/library/content/documentation/GraphicsImaging/Conceptual/drawingwithquartz2d/dq_overview/dq_overview.html#//apple_ref/doc/uid/TP30001066-CH202-TPXREF101)

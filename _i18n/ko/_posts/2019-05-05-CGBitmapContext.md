---
layout: post
title: "CGBitmapContext 정리"
date: "2019-05-04 00:53:17 +0900"
excerpt: "CGBitmapContext에 대해 학습한 내용을 정리합니다."
categories: CoreGraphics iOS CGBitmapContext
tags: [CoreGraphics, iOS, CGBitmapContext]
image:
  feature: iOS.png
translate: false
---

Core Graphics에서는 화면 drawing을 위해 기본적으로 비트맵 이미지와 이미지 마스크를 사용합니다. 비트맵 이미지라는 것은 픽셀의 집합으로, Core Graphics에서는 `CGBitmapContext`를 사용하여 `CGImage`를 픽셀 단위로 처리할 수 있습니다.

## CGBitmapContext의 스펙

`CGBitmapContext`를 만들기 위해서는 아래와 같은 정보가 필요합니다.

#### 1. 이미지의 크기

* 픽셀 단위의 width, height

#### 2. 이미지에 사용되는 픽셀 관련 정보

* `bitsPerComponent` - ColorSpace에서 사용되는 각각의 Component가 사용하는 비트 수(i.e. 32bits RGBA colorSpace를 사용하면, 각각의 R, G, B, A가 8bits를 사용하므로 `bitsPerComponent`는 8이 됩니다.)
* `bytesPerRow` - 각 행별 바이트 수(i.e. 32bits RGBA ColorSpace를 사용할 경우,`bitsPerComponent` * 4(= 32) * imageWidth가 됩니다.)
* `bitsPerPixel` - 개별 픽셀별 사용되는 비트 수(최소 `bitsPerComponent` * `componentPerPixel` 이상)

#### 3. ColorSpace 정보

* ColorSpace는 pixel마다 색상을 저장하는 형식을 의미합니다. CoreGraphics에서는 `RGB`, `CMYK`, `GrayScale`에 대한 색상 포맷을 지원합니다. 일반적으로 많이 사용하는 `RGB` 색상 포맷은 픽셀마다 24 bits를 사용합니다. 즉, 각각의 색상(R, G, B)마다 8 bits를 사용하고 256색을 표현할 수 있습니다. 여기에 alpha에 대한 정보를 포함하고 싶다면 `RGBA`(혹은 `ARGB`) 포맷을 사용하여 총 32  bits로 하나의 pixel을 표현하면 됩니다.

<img width="623" alt="스크린샷 2019-05-05 오후 6 52 57" src="https://user-images.githubusercontent.com/13018877/57192049-31d70300-6f67-11e9-9e81-d7de43e12811.png">

> 위에서 언급한 RGB 스펙은 sRGB(standard Red Green Blue)와 동일합니다.

#### 4. CGBitmapInfo

* 각 픽셀이 어떤 비트 배치 룰을 따르고, 어떻게 픽셀의 데이터를 읽을 것인지 설정하는 옵션입니다. 그래서 해당 옵션에서는 `CGImageAlphaInfo`를 통해 alpha 값에 대한 옵션을 설정하고, `CGBitmapInfo`를 통해 byte order 설정(little endian, big endian), floating value 사용 여부 등을 설정합니다.

> Constants that specify whether the bitmap should contain an alpha channel, the alpha channel’s relative location in a pixel, and information about whether the pixel components are floating-point or integer values.

## CGBitmapContext Usage

```swift
extension CGImage {
    var bitmapContext: CGContext? {
        let colorSpace = CGColorSpaceCreateDeviceRGB()
        let width = self.width
        let height = self.height
        let imageSize = CGSize(width: CGFloat(width), height: CGFloat(height))

        let bitsPerComponent = self.bitsPerComponent
        let bytesPerRow = self.bytesPerRow

        let totalBytes = bytesPerRow * height
        var pixelValues = [UInt32](repeating: 0, count: totalBytes)

        // pixel value는 개별 pixel 값에 접근하여 값을 사용할 경우에 사용합니다.
        // pixel을 사용할 일이 없다면, CGContext 생성시 data: nil을 설정하면 됩니다.
        let context =  CGContext(data: &pixelValues,
                                 width: width,
                                 height: height,
                                 bitsPerComponent: bitsPerComponent,
                                 bytesPerRow: bytesPerRow,
                                 space: colorSpace,
                                 bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue | CGBitmapInfo.byteOrder32Little.rawValue)

        context?.draw(self, in: CGRect(origin: .zero, size: imageSize))
        return context
    }
}
```

> Note: CGBitmapContext 관련 코드들은 Swift3에서 사용 방식이 많이 변경되었습니다. 아래 코드는 Swift 5.0 환경에서 작성한 예제입니다.

---

# 참고 자료

* [CoreGraphics - Bitmap Images and Image Masks](https://developer.apple.com/library/archive/documentation/GraphicsImaging/Conceptual/drawingwithquartz2d/dq_images/dq_images.html#//apple_ref/doc/uid/TP30001066-CH212-TPXREF101)

* 바이트를 읽는 형식에 대해서는 [
Understanding Big and Little Endian Byte Order](https://betterexplained.com/articles/understanding-big-and-little-endian-byte-order/) 참고

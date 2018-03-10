---
layout: post
title: "이미지 타일링"
excerpt: "iOS 플랫폼에서 타일 이미지로 고해상도 이미지를 랜더링하는 방법에 대해 알아봅니다."
categories: TiledImage, Display
date: "2018-03-08 18:28:51 +0900"
tags: [TiledImage, Display]
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
출처: [Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)

타일 이미지는 전체 이미지의 부분이기 때문에 `타일 이미지 용량 <= 전체 이미지 용량`이라는 등식은 항상 성립합니다. 그래서 기본적으로 타일 이미지 로딩은 전체 이미지 로딩보다 빠릅니다. 현대의 디바이스 혹은 브라우저들은 비동기 UI 업데이트를 지원합니다. 그래서 로딩이 완료된 타일 이미지는 우선적으로 화면에 업데이트 될 수 있습니다. 이는 사용자가 이미지의 특정 부분을 빠르게 볼 수 있도록 합니다.


## Image Pyramids

이미지 타일링 기법만으로도 큰 이미지를 로딩할 수 있지만, 이미지 타일링만으로는 이미지 로딩속도가 충분히 빠르지 않습니다. 그래서 이를 보완하기 위해 서로 다른 **scale**의 이미지를 활용합니다. **Image Scaling**이라는 것은 이미지의 사이즈를 재조정하는 것을 의미하는데, 이 때 기본 이미지를 서로 다른 크기로 scaling한 일련의 이미지 집합을 **Image Pyramids**라고 합니다. 이 때, scale이 크기는 이미지의 크기와 반비례 값을 갖습니다.

<img src="https://dl.dropbox.com/s/1uuol5qdlba0snp/img_pyrm.gif" style="max-wid
th: 100%; margin: 0 auto;">

### Gaussian Pyramids

**Image Pyramids**도 그 종류가 여러가지인데 그 중 **Gaussian Pyramids**은 이미지를 스케일링하는(사이즈 축소) 것뿐만 아니라, 이미지의 일정 픽셀을 버려서 이미지를 sub sampling하는(용량 축소) 방식으로 이미지 집합을 만든 피라미드입니다. 그래서 **Gaussian Pyramids** 레벨마다 이미지의 크기가 매우 빠르게 줄어드는 특징을 가지고 있습니다.

<img src="https://dl.dropbox.com/s/i409yl3tipn0hkp/pyramid.png" style="max-width: 100%; margin: 0 auto;">
출처: [Pyramid (image processing) - Wikipedia](https://en.wikipedia.org/wiki/Pyramid_(image_processing))

## Image tiling with Image Pyramids



<img src="https://dl.dropbox.com/s/n507zqwlvc4co6h/Image_Tiling-21.jpg" style="max-width: 100%; margin: 0 auto;">
출처: [Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)


-----

## 참고자료
* [Display in iOS](https://developer.apple.com/library/content/documentation/DeviceInformation/Reference/iOSDeviceCompatibility/Displays/Displays.html)
[Working with Image Objects - Dartmouth edu](http://northstar-www.dartmouth.edu/doc/idl/html_6.2/Image_Tiling.html)

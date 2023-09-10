---
layout: post
title: "UIBarButtonItem에 Circle Image Button 넣기"
date: "2018-03-29 21:52:11 +0900"
excerpt: "UIBarButtonItem에 원형 이미지 버튼을 넣는 방법에 대해 알아봅니다."
categories: Debugging UIBarButtonItem
tags: [Debugging, UIBarButtonItem]
translate: false
---

이번 글에서는 `UINavigationBar`에 사각형 이미지를 가지고 원형 이미지 버튼을 만드는 방법에 대해 알아보고자 합니다. 그렇게 어려운 내용은 아니지만, 처음에 잘못 접근한 부분이 있어서 이를 기록으로 남깁니다.

## 1. Core Graphics로 이미지 버튼 추가하기(잘못된 방법)

`UINavigationBar`에 버튼을 추가하려면 `UIBarButtonItem`을 활용하여 버튼을 추가해야 합니다. 그래서 이미지 버튼을 만들어야하기 때문에 다음과 같은 방식으로 버튼을 추가하는 것을 생각해볼 수 있습니다.

{% highlight swift %}
self.navigationItem.rightBarButtonItem = UIBarButtonItem(image: image, style: .plain, target: nil, action: nil)
{% endhighlight %}

### 1. 이미지 크기 조정

이렇게 하면 이미지 사이즈가 화면에서 출력되는 사이즈와 동일하지 않으면 프레임을 무시하고 출력됩니다. 그래서 이를 위해 이미지를 resize할 필요가 있습니다. 그래서 아래와 같은 `resizeImage(size:)`와 같은 메소드로 이미지 사이즈를 우선 조정하고 이를 버튼에 적용해볼 수 있습니다.

{% highlight swift %}
extension UIImage {
  func resizeImage(size: CGSize) -> UIImage {
    let originalSize = self.size
    let ratio: CGFloat = {
        return originalSize.width > originalSize.height ? 1 / (size.width / originalSize.width) :
                                                          1 / (size.height / originalSize.height)
    }()

    return UIImage(cgImage: self.cgImage!, scale: self.scale * ratio, orientation: self.imageOrientation)
  }
}
// 원하는 사이즈 적용
let scaledImage = image.resizeImage(size: CGSize(width: 26, height: 26))
self.navigationItem.rightBarButtonItem = UIBarButtonItem(image: scaledImage, style: .plain, target: nil, action: nil)
{% endhighlight %}

### 2. 이미지 랜더링 모드 변경

이제 사이즈는 제대로 조정이 되지만, 이미지가 하얗게 나오는 문제가 있습니다. 그래서 이미지의 rendering mode를 조정해주어야 합니다.

{% highlight swift %}
let scaledImage = image.resizeImage(size: CGSize(width: 26, height: 26)).withRenderingMode(.alwaysOriginal)
{% endhighlight %}

### 3. 이미지 원형으로 만들기

이제 이미지를 원형으로 만드는 과정만 남았습니다. 그런데 이게 생각보다 쉽지 않습니다. 일반적으로 이미지를 원형으로 만들 때 사용하는 방법은 `UIImageView`의 layer에서 `cornerRadius` 값을 조정하는 것입니다. 그런데 지금까지 `UIImageView`로 이미지를 추가하지 않고 `UIImage`를 `UIBarButtonItem`에 추가하는 방식으로 이미지를 넣었습니다. 그래서 `Graphic Context`를 활용하여 이미지를 새롭게 그려주어야 합니다.

{% highlight swift %}
extension UIImage {
    var roundedImage: UIImage {
        let rect = CGRect(origin: .zero, size: self.size)

        UIGraphicsBeginImageContextWithOptions(self.size, false, 1)

        let path = UIBezierPath(ovalIn: rect)
        path.addClip()

        self.draw(in: rect)
        return UIGraphicsGetImageFromCurrentImageContext()!
    }
}

let scaledImage = image.resizeImage(size: CGSize(width: 26, height: 26)).withRenderingMode(.alwaysOriginal).roundedImage
self.navigationItem.rightBarButtonItem = UIBarButtonItem(image: scaledImage, style: .plain, target: nil, action: nil)
{% endhighlight %}

위의 방식은 `Graphic Context` 위에 이미지를 `UIBezierPath` 안에만 그리는 방식입니다. 그런데.. 이 방식은 *비트맵 방식으로 이미지를 그린다*는 큰 문제가 있습니다. 그래서 이미지가 원형으로 나오지만, 이미지 테두리가 비트맵 때문에 오돌토돌하게 나타납니다. 그래서 위의 방식으로 원형 이미지 버튼을 만들면 안됩니다.

## 2. UIImageView로 이미지 넣기

결론적으로 `UIImageView`를 사용한 방식으로 `UIBarButtonItem`을 만들어야 합니다. 물론 이 때 앞서서 사용했던 이미지 사이즈를 줄이는 익스텐션은 동일하게 사용됩니다.

{% highlight swift %}
let scaledImage = image.resizeImage(size: CGSize(width: 26, height: 26))
let imageView = UIImageView(image: scaledImage)
imageView.frame = CGRect(origin: .zero, size: scaledImage.size)
imageView.layer.cornerRadius = imageView.frame.size.width / 2
imageView.clipsToBounds = true

self.navigationItem.rightBarButtonItem = UIBarButtonItem(customView: imageView)
{% endhighlight %}


---

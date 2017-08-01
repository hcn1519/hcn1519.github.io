---
layout: post
comments: true
title:  "iOS에서 객체간 비동기 데이터 전송하기"
excerpt: "iOS에서 객체간 비동기 데이터를 전송하는 세 가지 방식에 대해 알아봅니다."
categories: iOS NotificationCenter EscapingClosure Delegate
date:   2017-08-01 00:30:00
tags: [iOS, NotificationCenter, EscapingClosure, Delegate]
image:
  feature: iOS10.png
---

통신을 하는 iOS 앱을 만드는 경우 다음과 같은 흐름을 통해 데이터를 주고 받습니다. 대표적으로 데이터를 받아오는 경우

1. 네트워크를 다루는 객체를 통해 비동기 방식으로 데이터를 전달 받고
2. 해당 데이터를 알맞은 모델 객체로 저장하여
3. 컨트롤러에서 모델에 기반하여 데이터를 적절히 보여줍니다.

![process](https://dl.dropbox.com/s/kppv4nyggcbbv86/networkprocess.png)

이 경우, 우리는 네트워크를 다루는 객체에서 컨트롤러 객체에 데이터를 넘겨주어야 합니다. 단, 네트워크에서 받는 데이터는 비동기 방식으로 처리되어야 합니다. 여기서는 3가지 방법을 통해 이를 구현하는 방법을 알아보겠습니다.


## NotificationCenter 활용하기

`NotificationCenter`는 observer 패턴을 활용하여 객체에 알람을 전송하는 메커니즘입니다.

<div class="messages">
  A notification dispatch mechanism that enables the broadcast of information to registered observers.
</div>

`NotificationCenter` 특정 객체에 이름을 지닌 `observer`를 달아서, 앱 어딘가에서 자신을 호출하는 `post` 메소드가 호출되면 selector가 실행되는 형태를 가지고 있습니다.

{% highlight swift %}
// PlayGround EX
struct Data {
    var name: String
}
class NetworkModule1 {
    // 2
    static func getData() {
        let myData = Data(name: "노티 통한 전송")

        NotificationCenter.default.post(name: NSNotification.Name(rawValue: "getData"),
                                        object: nil, userInfo: ["data": myData])
    }
}


class SomeViewController {
    // 1
    func viewDidload() {
        NotificationCenter.default.addObserver(self,
                                               selector: #selector(self.getDataFinished),
                                               name: NSNotification.Name(rawValue: "getData"),
                                               object: nil)
    }

    @objc
    func getDataFinished(_ notification: Notification) {
        if let data = notification.userInfo?["data"] as? Data {
            print("데이터가 전달된 이후 실행")
            print("\(data.name)")
        }
    }
}

let viewController = SomeViewController()

viewController.viewDidload()

NetworkModule1.getData()

// 결과
// 데이터가 전달된 이후 실행
// 노티 통한 전송
{% endhighlight %}

1. 가장 먼저 `viewDidload()`메소드를 호출하여 `viewController`에 `NotificationCenter`의 observer를 달아줍니다. 이 때 `selector`를 통해 해당 observer가 호출되면 실행되는 메소드를 `getDataFinished`로 지정하였습니다.
2. 다음으로 `NetworkModule1.getData()`를 호출하는데 이 때 `NotificationCenter`로 post를 전달합니다. 이 때 `userInfo` 파라미터를 통해서 딕셔너리 형태의 데이터를 전달할 수 있으며, 이는 `selector`에서 지정된 함수에서 받을 수 있습니다.

이와 같이 `NotificationCenter`를 데이터를 받아오고 난 이후에 post를 전달하는 형태로 작성하면, 비동기 데이터도 처리할 수 있게 됩니다. 다만, `NotificationCenter`는 observer도 달고, `selector` 함수도 별도로 작성해야 하기 때문에 코드가 다소 길어지는 경향이 있습니다. 그렇기 때문에 다수의 observer로부터 값을 주고 받는 경우에 사용하는 것이 좋습니다.

## Escaping Closure 활용하기

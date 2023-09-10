---
layout: post
comments: true
title:  "Swift, 객체간 비동기 데이터 전송하기"
excerpt: "Swift에서 객체간 비동기 데이터를 전송하는 세 가지 방식에 대해 알아봅니다."
categories: Swift NotificationCenter EscapingClosure Delegate
date:   2017-08-01 00:30:00
tags: [Swift, NotificationCenter, EscapingClosure, Delegate]
image:
  feature: swiftLogo.jpg
translate: false
---


통신을 하는 iOS 앱을 만드는 경우 다음과 같은 흐름을 통해 데이터를 주고 받습니다. 대표적으로 데이터를 받아오는 경우

1. 네트워크를 다루는 객체를 통해 비동기 방식으로 데이터를 전달 받고
2. 해당 데이터를 알맞은 모델 객체로 저장하여
3. 컨트롤러에서 모델에 기반하여 데이터를 적절히 보여줍니다.

![process](https://dl.dropbox.com/s/kppv4nyggcbbv86/networkprocess.png)

이 경우, 우리는 네트워크를 다루는 객체에서 컨트롤러 객체에 데이터를 넘겨주어야 합니다. 단, 네트워크에서 받는 데이터는 비동기 방식으로 처리되어야 합니다. 여기서는 3가지 방법을 통해 이를 구현하는 방법을 알아보겠습니다.


## NotificationCenter 활용하기

`NotificationCenter`는 observer 패턴을 활용하여 객체에 알람을 전송하는 메커니즘입니다.

<div class="message">
  A notification dispatch mechanism that enables the broadcast of information to registered observers.
</div>

`NotificationCenter`는 특정 객체에 이름을 지닌 `observer`를 달아서, 앱 어딘가에서 자신을 호출하는 `post` 메소드가 호출되면 selector가 실행되는 형태를 가지고 있습니다.

{% highlight swift %}
class NetworkModule1 {
    // 2
    static func getData() {
      let defaultSession = URLSession(configuration: .default)

      guard let url = URL(string: "\(BASEURL)") else {
          print("URL is nil")
          return
      }

      // Request
      let request = URLRequest(url: url)

      // dataTask
      var dataTask: URLSessionDataTask?
      dataTask = defaultSession.dataTask(with: request) { data, response, error in
          // getting Data Error
          guard error == nil else {
              print("Error occur: \(String(describing: error))")
              return
          }

          if let myData = data, let response = response as? HTTPURLResponse, response.statusCode == 200 {
              // data update
              // self.updateData(index: index, data: data)
              NotificationCenter.default.post(name: NSNotification.Name(rawValue: "getData"),
                                              object: nil, userInfo: myData)
          }
      }

      dataTask?.resume()
    }
}
{% endhighlight %}

{% highlight swift %}
class SomeViewController: UIViewController {
    // 1
    func viewDidload() {
        super.viewDidload()
        NotificationCenter.default.addObserver(self,
                                               selector: #selector(self.getDataFinished),
                                               name: NSNotification.Name(rawValue: "getData"),
                                               object: nil)
    }
    // 3
    func getDataFinished(_ notification: Notification) {
        // userInfo를 통해 데이터 전달
        // update instance here

        DispatchQueue.main.async {
            // update tableView or collectionView
            // self.tableView.reloadData()
        }
    }
}

let viewController = SomeViewController()
viewController.viewDidload()
NetworkModule1.getData()
{% endhighlight %}

1. 가장 먼저 `viewDidload()`메소드를 호출하여 `viewController`에 `NotificationCenter`의 observer를 달아줍니다. 이 때 `selector`를 통해 해당 observer가 호출되면 실행되는 메소드를 `getDataFinished`로 지정하였습니다.
2. 다음으로 `NetworkModule1.getData()`를 호출하는데 이 때 `NotificationCenter`로 post를 전달합니다. 이 때 `userInfo` 파라미터를 통해서 딕셔너리 형태의 데이터를 전달할 수 있으며, 이는 `selector`에서 지정된 함수에서 받을 수 있습니다.
3. 받아 온 데이터를 GCD를 통해 `Main` 큐에서 뷰를 업데이트 합니다.

이와 같이 `NotificationCenter`를 통해 데이터를 받아오고 난 이후에 post를 전달하는 형태로 코드를 작성하면 데이터가 전달된 후 다음 작업을 하는 것이 보장되기 때문에 비동기 데이터를 처리할 수 있습니다. 다만, `NotificationCenter`는 observer도 달고, `selector` 함수도 별도로 작성해야 하기 때문에 코드가 다소 길어지는 경향이 있습니다. 그렇기 때문에 다수의 observer로부터 값을 주고 받는 경우에 사용하는 것이 좋습니다.

## Escaping Closure 활용하기

`Escaping closure`를 사용하면 해당 함수가 실행된 후 클로저가 실행되는 것을 **보장** 할 수 있습니다.

{% highlight swift %}
class NetworkModule2 {
  // 2
  static func getDataFromClosure(completion: @escaping ([myData]) -> Void) {
      let defaultSession = URLSession(configuration: .default)

      guard let url = URL(string: "\(BASEURL)") else {
          print("URL is nil")
          return
      }

      // Request
      let request = URLRequest(url: url)

      // dataTask
      var dataTask: URLSessionDataTask?
      dataTask = defaultSession.dataTask(with: request) { data, response, error in
          // getting Data Error
          guard error == nil else {
              print("Error occur: \(String(describing: error))")
              return
          }

          if let data = data, let response = response as? HTTPURLResponse, response.statusCode == 200 {
              // 3
              // data update
              // self.updateData(index: index, data: data)

              DispatchQueue.main.async {
                  completion(myDatas)
              }
          }
      }
      dataTask?.resume()
  }
}
class SomeViewController: UIViewController {

    func viewDidload() {
        super.viewDidload()
        // 1
        NetworkHandler2.getDataFromClosure() { [weak self] results in
            // 4
            // update tableView or collectionView
            // self?.tableView.reloadData()
        }
    }
}
{% endhighlight %}

1. 가장 먼저 `getDataFromClosure(completion:)` 함수를 호출합니다.
2. `getDataFromClosure(completion:)`은 파라미터로 `escaping closure`를 받습니다. 그렇기 때문에 `completion`은 해당 함수가 실행된 이후에 실행됩니다.
3. 받아온 데이터를 serialize하고 `completion` 클로저를 호출합니다. 이 때, 일반적으로 `completion`은 받아온 데이터들을 화면에 적절히 뿌려주는 작업을 하기 때문에, main 쓰레드에서 클로저를 호출합니다.
4. `completion` 클로저의 body 부분으로 `escaping closure` 형태로 `completion`이 작성되어 있기 때문에 항상 `getDataFromClosure()`가 실행된 이후 실행되는 것이 보장됩니다.

## Delegate 패턴 활용하기

-----

## 참고자료
* Apple Inc. The Swift Programming Language (Swift 3.1)
* [What do mean @escaping and @nonescaping closures in Swift?](https://medium.com/@kumarpramod017/what-do-mean-escaping-and-nonescaping-closures-in-swift-d404d721f39d)
* [Completion handlers in Swift 3.0](https://stackoverflow.com/questions/41745328/completion-handlers-in-swift-3-0)

---
layout: post
comments: true
title:  "Swift로 파일 다루기"
excerpt: "Swift의 FileManager를 이용하여 Local에 있는 File들을 다루는 법에 대해 알아봅니다."
categories: Swift FileManager
date:   2017-07-15 00:30:00
tags: [Swift, Foundation, FileManager]
image:
  feature: swiftLogo.jpg
---

이번 포스팅에서는 Swift를 통해 로컬(macOS)에 있는 파일들을 다루는 방법에 대해 알아보고자 합니다.

## 기본적인 macOS 파일 시스템

macOS의 파일 시스템은 domain(영역)으로 파일들의 위치를 결정합니다. 어떤 파일이 특정 domain에 속해 있는 경우 그 파일은 무조건 해당 domain의 루트 디렉토리보다 아래에 위치해야 합니다. 바꿔말하면, domain을 설정해주면 다른 domain의 파일들이 변경되는 것을 미리 방지할 수 있다는 말입니다. macOS에는 기본적으로 `user`, `local`, `network`, `system` domain을 제공합니다. 아래 그림을 통해 domain과 디렉토리, 파일들의 관계를 쉽게 이해할 수 있습니다.

<img src="https://dl.dropbox.com/s/jk555owekupnw3w/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202017-07-15%20%EC%98%A4%ED%9B%84%209.08.01.png" style="width: 50%;margin: 0 auto;">


macOS에서 로그인 후 터미널에서 최상단 루트에서 `pwd` 명령어를 치면 나오는 경로는 `/Users/userName`의 형태입니다. 즉, 사용자들은 기본적으로 `user` domain에 속해서 대부분의 작업들을 수행하는 것이죠. 좀 더 자세한 내용을 확인하고 싶다면 아래 링크를 확인해주세요.

[File System Basics](https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html#//apple_ref/doc/uid/TP40010672-CH2-SW2)

## FileManager

Swift에서는 파일들을 다루기 위한 클래스로 `FileManager`를 제공하고 있습니다. `FileManager`는 `FileManager.default` 인스턴스를 기본으로 제공하며, 원하면 자신만의 인스턴스를 새롭게 생성할 수도 있습니다. 파일시스템에서 파일 혹은 디렉토리들은 모두 경로를 가지고 있습니다. `FileManager`는 `URL` 혹은 `String` 데이터 타입을 통해 파일에 접근할 수 있도록 해줍니다. 다만, Apple에서는 `URL`을 통한 파일 접근을 권장하고 있습니다.

<div class="message">
  The preferred way to specify the location of a file or directory is to use the NSURL class. Although the NSString class has many methods related to path creation, URLs offer a more robust way to locate files and directories. For apps that also work with network resources, URLs also mean that you can use one type of object to manage items located on a local file system or on a network server.
</div>

[FileManager](https://developer.apple.com/documentation/foundation/filemanager)

#### Directory 접근하기

가장 먼저 디렉토리의 내용을 보는 방법을 알아보겠습니다. 가장 쉬운 방법은 `contentsOfDirectory(atPath:)` 메소드를 쓰는 것입니다.

{% highlight swift %}
// FileManager 인스턴스 생성
let fileManager = FileManager()

// 해당 디렉토리 경로
let desktopPath = "/Users/userName/Desktop"

do {
    // contentsOfDirectory(atPath:)가 해당 디렉토리 안의 파일 리스트를 배열로 반환
    let contents = try fileManager.contentsOfDirectory(atPath: desktopPath)

    // subpathsOfDirectory(atPath:)가 해당 디렉토리의 하위에 있는 모든 파일을 배열로 반환
    let deeperContents = try fileManager.subpathsOfDirectory(atPath: desktopPath)

    print(contents)
    print(deeperContents)
} catch let error as NSError {
    print("Error access directory: \(error)")
}
{% endhighlight %}

`contentsOfDirectory(atPath:)` 메소드는 설정한 경로의 디렉토리 안에 있는 파일들을 `[String]` 형태로 반환합니다. 또한, `subpathsOfDirectory(atPath:)`와 같은 메소드는 설정한 경로에 있는 디렉토리들을 모두 탐색하여 그 안에 있는 파일들을 `[String]` 형태로 반환합니다.


#### Directory 생성하기

디렉토리를 생성하는 방법도 접근하는 것과 크게 다르지 않습니다. 여기서는 `createDirectory(atPath:withIntermediateDirectories:attributes:)` 메소드를 사용합니다.

{% highlight swift %}
// FileManagerTest.swift
// FileManager 인스턴스 생성
let fileManager = FileManager()

// document 디렉토리의 경로 저장
let documentsDirectory = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first!

// 해당 디렉토리 이름 지정
let dataPath = documentsDirectory.appendingPathComponent("FileManger Directory")

do {
    // 디렉토리 생성
    try fileManager.createDirectory(atPath: dataPath.path, withIntermediateDirectories: false, attributes: nil)

} catch let error as NSError {
    print("Error creating directory: \(error.localizedDescription)")
}
{% endhighlight %}

과정은 다음과 같습니다.
1. `urls(for:in:)` 메소드를 통해 특정 경로에 접근한다.
2. 해당 경로에 추가 경로를 지정하는 방식으로 디렉토리 명을 추가한다.
3. 디렉토리를 생성한다.

`urls(for:in:)` 메소드는 `SearchPathDirectory`와 `SearchPathDomainMask`를 파라미터로 받고, `SearchPathDomainMask`의 범위에서 `SearchPathDirectory`를 찾는 메소드입니다. `SearchPathDirectory`는 enum 형태로 구현되어 있으며 `.desktopDirectory`, `.documentDirectory`, `.downloadsDirectory`처럼 실제로 사용자가 사용하는 디렉토리 경로를 지칭합니다.

`SearchPathDomainMask`의 경우 `.userDomainMask`, `.systemDomainMask`, `localDomainMask`처럼 앞서 언급했던 `domain`을 기준으로 만들어져 있습니다. 파일 시스템 설명에서 알 수 있듯이 domain은 directory보다 큰 개념입니다. 또, `domainMask`라는 것은 존재하는 상위 URL을 숨기는 것을 의미합니다. 정리하자면, `SearchPathDomainMask`를 `userDomainMask`로 설정하면, `/Users`보다 위에 있는 디렉토리는 접근할 수 없게 됩니다. 또한 `SearchPathDomainMask`보다 상위에 있는 디렉토리를 찾으려고 한다면 에러가 나게 됩니다.


다음으로 `appendingPathComponent(_:)`를 사용하면, 경로 URL에 추가적인 경로를 붙일 수 있습니다. 위에서는 접근한 디렉토리 아래에 새롭게 생성할 디렉토리 명을 추가했습니다.


다음으로 디렉토리의 생성입니다. `createDirectory(atPath:withIntermediateDirectories:attributes:)`는 `atPath`에서 설정된 경로에 디렉토리를 생성합니다. 디렉토리의 경로는 확장자 없이 끝나는 형태이어야 합니다.

#### 파일 만들고 쓰기

`FileManger()`를 사용하여 파일 생성과 텍스트 쓰기도 가능합니다.
{% highlight swift %}
// FileManagerTest.swift에 추가
do {
    // 파일 이름을 기존의 경로에 추가
    let helloPath = dataPath.appendingPathComponent("Hello.txt")

    // 쓸 내용
    let text = "Hello File From Swift"

    do {
        // 쓰기 작업
        try text.write(to: helloPath, atomically: false, encoding: .utf8)
    }
} catch let error as NSError {
    print("Error Writing File : \(error.localizedDescription)")
}
{% endhighlight %}

파일 생성과 쓰기의 경우에도 파일을 만들 디렉토리를 지정하고, 그 경로에 텍스트를 쓰면 됩니다. 이 때, `String.write(to:atomically:encoding:)` 메소드를 사용하면 됩니다.


#### 파일 읽기

파일 읽기도 읽을 때 `String(contentsOf:encoding:)` 메소드를 쓰는 것만 제외하면, 쓰기와 그 과정이 동일합니다.

{% highlight swift %}
// FileManagerTest.swift에 추가
do {
    // 파일 이름을 기존의 경로에 추가
    let helloPath = dataPath.appendingPathComponent("Hello.txt")

    // 내용 읽기
    let text2 = try String(contentsOf: helloPath, encoding: .utf8)

    print(text2)
}
catch let error as NSError {
    print("Error Reading File : \(error.localizedDescription)")
}
{% endhighlight %}

최종 소스코드는 아래에서 볼 수 있습니다.

[https://gist.github.com/hcn1519/05f6088279331452fedffdf0742c0f62](https://gist.github.com/hcn1519/05f6088279331452fedffdf0742c0f62)

## 번외 : iOS 프로젝트에서 로컬 이미지 읽고 보여주기

위의 내용들을 사용하여 간단히 로컬에 있는 이미지를 iOS 앱에서 보여주는 프로젝트를 만들어 보겠습니다. 결과 앱은 다음과 같습니다.

<img src="https://dl.dropbox.com/s/0jx630j5j4lxmmk/result.png" style="width: 50%; border: 1px solid gray; margin: 0 auto; padding: 10px">

먼저 테스트 이미지 파일은 아래 링크에서 다운받고, `/Users/Documents`에 저장합니다.

[이미지 샘플](https://dl.dropboxusercontent.com/s/rnmu9em96d3840u/apple.jpg)

그리고 Xcode에서 Single View Application 앱을 생성하고, `UIImageView`를 ViewController에 만들어서 imageView라는 이름으로 `IBOutlet`을 연결합니다.

![프로젝트 이미지](https://dl.dropbox.com/s/unmnrq4akzkfc09/xcode.png)

다음으로 `ViewController`의 코드를 다음과 같이 수정합니다.

{% highlight swift %}
import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var imageView: UIImageView!

    override func viewDidLoad() {
        super.viewDidLoad()

        let apple = loadImage()

        if let appleImage = apple {
            imageView.image = appleImage
        }
    }
    func loadImage() -> UIImage? {

        guard let documentsDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first else { return nil }

        let imageFile = "apple.jpg"
        let imageURL = documentsDirectory.appendingPathComponent(imageFile)

        print(imageURL)

        do {
            let imageData = try Data(contentsOf: imageURL)

            return UIImage(data: imageData)

        } catch let err as NSError {
            print("이미지 로딩 에러 : \(err)")
        }

        return nil
    }
}
{% endhighlight %}

흐름은 간단합니다. 로컬에 있는 **apple.jpg** 파일을 가져와서 `UIImage` 인스턴스를 만든 후, 이 인스턴스를 통해 뷰에 만든 imageView에 이미지를 보여줍니다. 하지만 앱을 컴파일하고 실행해보면 해당 파일을 찾을 수 없다고 나옵니다. 분명 우리는 이미지를 `Documents`에 놔두었고, `url(for:in:)` 메소드를 `.documentsDirectory`로 잘 설정해두었는데도 말이죠.

이 문제는 해당 경로를 출력해보면 쉽게 알 수 있습니다. 위에서 출력된 `imageURL`은 `/Users/Documents/apple.jpg`가 되어야 우리가 원하는 결과를 도출할 수 있는데, 실제로는 `file:///Users/userName/Library/Developer/CoreSimulator/Devices/52EFC32B-305F-4EB6-8C73-2B2F7A4680E8/data/Containers/Data/Application/E28F4A30-935D-4EFE-815C-213A08B6D2DF/Documents/apple.jpg
`과 같은 경로가 출력됩니다. 경로를 간단히 살펴보면 `FileManager`는 시뮬레이터 안에 있는 documents에 접근하는 것을 확인할 수 있습니다. 그렇기 때문에 `apple.jpg` 파일은 해당 경로로 옮겨주어야 합니다. 터미널을 실행하여 Documents 디렉토리에 있는 `apple.jpg`를 위의 경로로 옮기도록 하겠습니다. 단, 위의 Devices 이하의 경로는 시뮬레이터마다 다르므로 그대로 복사하면 안 되고, 경로를 한 번 출력해보고 그 곳에 가져다 놓으면 됩니다.

{% highlight swift %}
$ mv Documents/apple.jpg /Users/userName/Library/Developer/CoreSimulator/Devices/52EFC32B-305F-4EB6-8C73-2B2F7A4680E8/data/Containers/Data/Application/E28F4A30-935D-4EFE-815C-213A08B6D2DF/Documents/apple.jpg
{% endhighlight %}

이제 다시 실행하면 이미지가 올바르게 뜨는 것을 확인할 수 있습니다.

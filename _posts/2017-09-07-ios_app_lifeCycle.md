---
layout: post
comments: true
title:  "iOS Application Life Cycle 이해하기"
excerpt: "iOS 앱을 실행하면 일어나는 일들과 이를 설정하는 방법에 대해 알아 봅니다."
categories: iOS, LifeCycle
date:   2017-09-07 00:30:00
tags: [iOS, LifeCycle]
---



## iOS에서 앱을 실행하면 무슨 일이 벌어질까요?

예전에 어떤 분이 제가 iOS 개발을 한다고 했을 때, iOS 앱이 실행되는 과정에 대해서 물어본 적이 있습니다. 그 당시에는 이에 대한 공부를 한 적이 없어서 잘 모른다고 대답을 했었는데, 생각해보면 이는 꽤 중요한 주제입니다.
C언어 기반의 프로그래밍 언어에서는 `main`이라는 함수가 앱의 시작이 됩니다. iOS의 앱 또한 ObjectiveC 기반에서(C언어 기반) 돌아가기 때문에 앱은 `main` 함수에서 시작합니다. 다만, iOS의 핵심 라이브러리인 `UIKit framework`가 `main` 함수를 관리하여 앱 개발자들이 직접 `main` 함수에 코드를 작성하지 않습니다.  
그렇다고 앱의 실행에 앱 개발자가 관여할 수 없는 것은 아닙니다.  `UIKit`은  `main` 함수를 다루는 과정에서 `UIApplicationMain` 함수를 실행합니다. 이 함수를 통해 `UIApplication` 객체가 생성되는데 이 객체를 통해 앱 개발자는 앱의 실행에 부분적으로 관여할 수 있습니다. 이처럼, 앱 개발자가 앱을 실행할 때 접근할 수 객체가  `UIApplication` 이기 때문에 앱이 어떤 과정으로 실행되는지 자세히 알아보려면 `UIApplication`에 대해 좀 더 알 필요가 있습니다.

<div class="message">
  iOS도 C언어 기반의 언어로 만들어졌기 때문에, main 함수가 존재합니다. 이 main 함수는 앱의 시작점이 됩니다. 다만, main 함수는 숨겨져 있기 때문에 프로젝트를 생성해도 파일이 나타나지는 않습니다.
</div>

#### UIApplication

<div class="message">
UIApplicationMain 정의 - Creates the application object and the application delegate and sets up the event cycle.
</div>

모든 iOS 앱들은 `UIApplicationMain` 함수를 실행합니다. 이 때 생성되는 것 중 하나가 `UIApplication`  객체입니다.  `UIApplication`  객체는 `singleton` 형태로 생성되어, `UIApplication.shared`의 형태로 앱 전역에서 사용할 수 있습니다.
`UIApplication` 객체의 가장 중요한 역할은 user의 이벤트(터치, 리모트 컨트롤, 가속도계, 자이로스코프 등)에 반응하여 앱의 초기 routing(초기 설정)을 하는 것입니다. 구체적인 예를 들자면, `UIApplication` 객체는 앱이 Background에 진입한 상태에서 추가적인 작업을 할 수 있도록 만들어주거나, 푸쉬 알람을 받았을 때 어떤 방식으로 이를 처리할지 등에 대한 것을 다룹니다.

## Main Run Loop
Main Run Loop라는 것은 유저가 일으키는 이벤트들을 처리하는 프로세스입니다. `UIApplication` 객체는 앱이 실행될 때, Main Run Loop를 실행하고, 이 Main Run Loop를 View와 관련된 이벤트나 View의 업데이트에 활용합니다. 또한, Main Run Loop는 View와 관련되어 있기 때문에 Main 쓰레드에서 실행됩니다.

![Main Run Loop](https://dl.dropbox.com/s/i6ed655jlzrizs1/IMG_1006.PNG)
출처: [App Programming Guide for iOS - The App Life Cycle](https://developer.apple.com/library/content/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/TheAppLifeCycle/TheAppLifeCycle.html)

유저가 일으키는 이벤트의 처리 과정을 다음과 같은 순서로 정리할 수 있습니다.

1. 유저가 이벤트를 일으킨다.
2. 시스템을 통해 이벤트가 생성된다.
3. UIkit 프레임워크를 통해 생성된 port로 해당 이벤트가 앱으로 전달된다.
4. 이벤트는 앱 내부적으로 Queue의 형태로 정리되고, Main Run Loop에 하나씩 매핑된다.
5. UIApplication 객체는 이때 가장 먼저 이벤트를 받는 객체로 어떤 것이 실행되야하는지 결정한다.

## 앱의 상태 변화
앞선 내용까지 사용자가 앱에 이벤트를 전달한 후 앱의 실행까지 어떤 과정을 통해 이뤄지는지 알아보았습니다. 여기서부터는 iOS 앱의 실행 전 상태, 혹은 실행 후 상태 등을 세분화하여 알아보고, 각각의 상태별로 접근하기 위한 방식에 대해 알아보고자 합니다.

#### App State
앱의 상태라는 것은 여러가지 의미를 내포한 폭넓은 의미로 받아들여질 수 있습니다만, Apple에서 정의하는 앱의 상태(App State)는 크게 5가지로 구분됩니다.

![App State](https://dl.dropbox.com/s/wpmf59gfnaiuafr/IMG_1008.PNG)
출처: [App Programming Guide for iOS - The App Life Cycle](https://developer.apple.com/library/content/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/TheAppLifeCycle/TheAppLifeCycle.html)

* Not Running: 아무것도 실행하지 않은 상태
* InActive: 앱이 Foreground 상태로 돌아가지만, 이벤트는 받지 않는 상태, 앱의 상태 전환 과정에서 잠깐 머무는 단계입니다.
* Active: 일반적으로 앱이 돌아가는 상태
* Background: 앱이 Suspended(유예 상태) 상태로 진입하기 전 거치는 상태,
* Suspended: 앱이 Background 상태에 있지만, 아무 코드도 실행하지 않는 상태, 시스템이 *임의로* Background 상태의 앱을 Suspended 상태로 만듭니다.

위의 상태에서 몇 가지 알아두면 좋은 점들이 있습니다.
1. Background 상태에서는 일부 필요한 추가 작업을 수행할 수 있습니다. 또한, Background 상태에서 앱을 실행하면 InActive 상태를 거치지 않고 앱이 실행됩니다.(iOS에서 홈버튼을 두 번 눌러서 앱을 전환할 때, 앱이 재시작되지 않는다면 해당 앱은  Background 상태에 있던 앱입니다.)
2. 앱이 죽는 것(Suspended 상태에서 Not Running 상태로 진입하는 것)에는 알림을 받을 수 없습니다. 또한 Background 상태에서 Suspended 상태로 진입할 때 `willTerminate` 메소드가 실행되지만 이 또한 기기를 재부팅하면 실행되지 않습니다.

<div class="message">
iOS 앱의 다양한 상태가 있지만, 주요한 작업은 Active, Background 상태에서 주로 이뤄지게 됩니다.
</div>


#### AppDelegate

앱의 상태에 대해서 알아보았으니, 이번에는 이 상태에 접근하기 위한 방법에 대해 알아보고자 합니다.  이 때 각각의 상태에 접근하기 위해 사용되는 파일이 `AppDelegate.swift`입니다. iOS 앱 프로젝트를 생성하면 `AppDelegate.swift`은 자동으로 생성됩니다.  `AppDelegate`은 이름 그대로 앱과 시스템의 연결을 위해 필요한 delegate 메소드를 담고 있습니다. 다만, 이름 때문에 그런 것은 아니고, `@UIApplicationMain`이라는 annotation이 있기 때문에 앱에서 `AppDelegate.swift`을 앱과 시스템을 연결하기 위한 파일로 인식합니다.  `AppDelegate.swift`의 코드를 살펴보면 다음과 같습니다.

{% highlight swift %}
// AppDelegate.swift
import UIKit

@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate {

    var window: UIWindow?

    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplicationLaunchOptionsKey: Any]?) -> Bool {
        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
    }

    func applicationWillTerminate(_ application: UIApplication) {
    }
{% endhighlight %}

`AppDelegate` 객체는 `UIResponder`, `UIApplicationDelegate`을 상속 및 참조하고 있습니다. 먼저 `UIResponder`는
앱에서 발생하는 이벤트들을 담고 있는 추상형 인터페이스 객체로 View와 사용자의 이벤트간의 연결을 관리하는 역할을 합니다.(이는 app life cycle과 관련이 적기 때문에 자세한 설명은 다음 링크를 참조하세요. [UIResponder](https://developer.apple.com/documentation/uikit/uiresponder)) 다음으로 `UIApplicationDelegate`은 `UIApplication` 객체의 작업에 개발자가 접근할 수 있도록 하는 메소드들을 담고 있습니다. 예를 들어 설명하자면, `didFinishLaunchingWithOptions`, `applicationWillResignActive` 등과 같은 메소드를 통해 앱의 상태가 변할 때 수행할 작업들을 설정할 수 있습니다. `UIApplicationDelegate`을 통해서 우리는 앱의 상태(Foreground, Background, Suspended 등)가 변하는 순간에 따라 앱에서 어떤 작업을 수행할 것인지 결정할 수 있습니다.


-----

## 참고자료
* [App Programming Guide for iOS - The App Life Cycle](https://developer.apple.com/library/content/documentation/iPhone/Conceptual/iPhoneOSProgrammingGuide/TheAppLifeCycle/TheAppLifeCycle.html)
* [UIApplication](https://developer.apple.com/documentation/uikit/uiapplication)
* [UIApplicationMain](https://developer.apple.com/documentation/uikit/1622933-uiapplicationmain?language=objc)
* [UIApplicationDelegate](https://developer.apple.com/documentation/uikit/uiapplicationdelegate)

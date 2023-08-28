---
layout: post
title: "MVC Design Pattern"
date: "2018-06-08 19:47:03 +0900"
excerpt: "MVC Design Pattern과 Cocoa에서 사용하는 MVC에 대해 알아봅니다."
categories: MVC Cocoa DesignPattern
tags: [MVC, Cocoa, DesignPattern]
---

`MVC` Design Pattern은 정말 널리 알려져 있는 디자인 패턴이지만, 이게 명확히 어떤 개념인지 잘 모르는 경우가 생각보다 많습니다.(저 포함) 그래서 이번 글에서는 `MVC`에 대해서 정리하고자 합니다.

디자인 패턴은 기본적으로 Application 내에서 각각의 객체들이 어떤 **역할**과 **책임**을 가져야 하는지에 대해 규정합니다. `MVC` 디자인 패턴도 객체의 역할과 책임에 따라 객체들을 크게 `Model`, `View`, `Controller`로 나눕니다.

> 아래에서는 사용하는 Model, View, Controller라고 지칭하는 것은 각각의 특징을 지닌 객체 집단을 의미한다고 생각하면 됩니다.

## Model

<div class="message">
   Model Objects Encapsulate Data and Basic Behaviors
</div>

`Model`은 앱내의 데이터를 가지고 있으며, 그 데이터를 처리하는 방식에 대한 로직을 가지고 있습니다. 그래서 앱에서 어떤 데이터가 로딩되기 위해선 반드시 `Model` 객체를 거쳐야만 합니다. `Model`은 화면에 직접적으로 데이터를 로딩하는 역할을 하지 않습니다. 그래서 `Model`은 `view`와 직접적으로 연관이 없도록 디자인해야 합니다. 예를 들어 Person 객체의 생일과 관련한 데이터를 화면에 로딩한다고 할 때, 생일정보는 `Model`에 있지만, 그 생일이 화면에 표현되는 것은 모델이 관리하지 않습니다.


`Model`에 속하는 객체들은 다음과 같습니다.

* Network Code - 네트워크의 커뮤니케이션을 관리하는 객체(NetworkManager의 형태)
* Persistence Code - CoreData, Realm에 저장되는 객체(디스크에 저장)
* Parsing Code - 네트워크의 response를 통해 생성되는 객체

## View

<div class="message">
   View Objects Present Information to the User
</div>

`View`는 데이터를 앱의 화면에 어떻게 보여줄 것인지에 대해 알고 있습니다. 그렇지만 `View`는 모델의 데이터가 어떻게 변경 되는지에 대해서는 관여하지 않습니다. `View`는 보통 재사용이 가능하며, 수정할 수 있고, 앱 사이의 일관성을 제공합니다. `View`는 `Model`의 데이터를 올바르게 보여주는 것을 보장해야 합니다. 그래서 일반적으로 `Model` 데이터의 변경에 대해 파악하고 있어야 합니다.(notification)

`View`에는 UIKit의 객체들중 다음의 것들이 포함됩니다.

* `UIView`와 `UIView`의 SubClass
* `UIViewController` - 논란의 여지가 있지만, `UIView`와 밀접하게 연관되어 있습니다.
* `Animation`, `Transition`
* Core Animation, Core Graphics의 class

`View`에서 다음의 체크리스트가 해당된다면 코드를 수정할 필요가 있습니다.

* Does it interact with the model layer?
* Does it contain any business logic?
* Does it try to do anything not related to UI?


## Controller

<div class="message">
   Controller Objects Tie the Model to the View
</div>

`Controller`는 각각의 `View`와 `Model` 사이의 연결을 보장해야 합니다. `Controller`는 또한 앱의 환경설정을 담당하고, 다른 객체들의 life cycle을 관리합니다.

`Controller`는 다음과 같은 일을 하는 것들입니다.

* What should be accessed first: the persistence or the network?
* How often should you refresh the app?
* What should the next screen be and in what circumstances?
* If the app goes to the background, what should be cleaned?


### Combining Roles

이들 `MVC`는 개별적으로 작동하지만, 동시에 2개의 기능을 가질 수도 있습니다. 그래서 `ViewController`는 `View`와 `Controller`의 속성을 지닌 객체입니다. 또한 `ModelController`는 `Model`과 `Controller`의 속성을 지닌 객체입니다.

## MVC as a Compound design pattern

전통적인(이론적인) MVC와 실제로 Cocoa에서 사용하는 MVC 패턴에는 몇 가지 차이가 있습니다. 그 중 가장 큰 차이는 `View`와 `Controller`의 역할분담입니다.

### Traditional MVC

전통적인 MVC는 다음과 같은 3가지 특징을 지니고 있습니다.

1. Composite - 모든 View는 동일한 규칙 아래에서 생성되어 협력한다. 테이블뷰, 개별 뷰, 버튼 등은 모두 사용자의 입력을 허용하고 다양한 레벨의 결과물을 보여준다.
2. Strategy - Controller는 하나 이상의 View 객체의 전략을 구현(model에 이벤트 전달, View의 데이터 업데이트 등)한다.
3. Observer - Model은 View의 상태에 대한 알림을 준다.

위와 같은 특징에 기반하면 다음과 같은 앱의 사용과정이 나타나게 됩니다.

1. 사용자는 View를 조작하고, 이는 이벤트를 만들어낸다.
2. Controller는 이 이벤트를 받아서 앱에 적용(앱의 전략을 구현)한다.
3. 이 때, 전략은 Model에 메시지를 보내어 Model의 상태나 값이 변경된다.
4. Model은 이러한 변화를 notification이 등록된 View에게 알려 화면을 업데이트한다.

그리고 이를 그림으로 나타낸 것이 아래 그림입니다.

<img src="{{ site.imageUrl}}/2018-06/mvc_design_pattern/f1.png">

### Cocoa MVC

#### Theoritical Problem

Cocoa MVC에서 전통적인 MVC에 대해 문제를 제기하는 부분은 바로 Model과 View의 Notification으로 연결된 관계입니다. Model과 View는 일반적으로 앱에서 재사용이 많이 될 수 있는 코드들입니다. 그런데 위와 같이 둘 사이를 Notification 연결하면 두 객체 사이의 데이터는 Notification Center를 통해 전달해야 합니다. 그래서 두 객체 사이에는 상호 의존성이 생기게 되고 이는 객체의 재사용성을 저해합니다.

그래서 Cocoa MVC에서는 이러한 문제를 해결하기 위해 Model과 View의 연결이 Controller를 통해 이뤄지도록 디자인하였습니다. 즉, Cocoa MVC는 Model이 변경된 것에 대한 notification을 controller를 통해서 View로 전달합니다. 이러한 디자인 패턴을 Mediator(중재자) Design Pat

<img src="{{ site.imageUrl}}/2018-06/mvc_design_pattern/f2.png">

#### Practical Problem

전통적인 MVC는 실제 코드 구현에 있어서도 문제가 있습니다. Cocoa MVC에서 Mediating Controller의 역할을 수행하도록 만들어진 것이 `NSController`의 SubClass입니다. 이 클래스는 Mediating Design Pattern을 적용할 수 있도록 기능을 제공합니다. 그런데 이를 사용하지 않는다면 View는 Model의 notification에 대해 반응하는 코드를 custom으로 작성해야 합니다.

<img src="{{ site.imageUrl}}/2018-06/mvc_design_pattern/f3.png">

## Massive View Controller?

앞서서 디자인 패턴은 객체의 역할과 책임을 정의한 것이라고 서술하였습니다. 그런데 iOS에서 코드를 작성하다보면 엄청난 길이의 `UIViewController`를 마주하게 됩니다. 그런데 이러한 코드는 리팩토링하기 어렵고 테스트도 어렵습니다. 그렇기 때문에 `UIViewController`의 라인을 130줄 이내로 줄이는 연습을 하는 것이 좋습니다. 그 방법은 다음과 같은 것들이 있습니다.

* View의 Customization은 View에서 작성한다.
* DataSource, Delegate은 `ViewController` 안에 작성하는 것이 아니라, 별개의 객체를 생성하여 관리한다.
* 너무 많은 Property를 가지고 있다면, 이를 여러 개의 `ViewController`로 나누어 처리하거나 새로운 `UIView`를 만드는 것을 생각해본다.

---

## 참고자료
* [Model-View-Controller](https://developer.apple.com/library/archive/documentation/General/Conceptual/CocoaEncyclopedia/Model-View-Controller/Model-View-Controller.html)
* [Model-View-Controller (MVC) in iOS: A Modern Approach](https://www.raywenderlich.com/132662/mvc-in-ios-a-modern-approach)

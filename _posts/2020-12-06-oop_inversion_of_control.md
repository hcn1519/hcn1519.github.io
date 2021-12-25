---
layout: post
title: "Inversion Of Control"
date: "2020-12-06 00:53:17 +0900"
excerpt: "제어흐름의 역전에 대해 알아봅니다."
categories: IoC, OOP, ControlFlow, Dependency
tags: [IoC, OOP, ControlFlow, Dependency]
image:
  feature: OOP.png
---

`Inversion of Control`은 단어의 뜻 그대로 제어 흐름이 **역전**되는 현상을 말합니다. 제어 흐름이 역전되는 것을 알기 위해서는 제어 흐름이 역전되지 않은 것을 이해할 필요가 있습니다. 따라서, 이 글에서는 역전되지 않은 제어의 흐름이 무엇인지 먼저 살펴보고, 이를 역전하는 `Inversion of Control`에 대해 살펴보겠습니다.
## Content

1. [제어의 흐름(Flow of Control)](./oop_inversion_of_control#1-제어의-흐름)
2. [제어 흐름의 역전(Inversion of Control)](./oop_inversion_of_control#2-제어-흐름의-역전)
3. [IoC를 통한 모듈의 확장](./oop_inversion_of_control#3-ioc를-통한-모듈의-확장)
4. [제어권 관점에서의 Library와 Framework](./oop_inversion_of_control#4-제어권-관점에서의-library와-framework)

### 1. 제어의 흐름

[제어의 흐름](https://en.wikipedia.org/wiki/Control_flow)은 코드가 시스템에 의해 수행되는 순서 혹은 흐름을 의미합니다. 일반적으로 소스 코드는 위쪽 코드가 먼저 실행되고 아래쪽 코드가 나중에 실행됩니다. 이 때, 경우에 따라서 조건문/반복문을 추가하여 동작을 제어하기도 합니다. 간단한 예시를 살펴보겠습니다.

> 여기에서 사용하는 예시는 [InversionOfControl - Martin Fowler](https://martinfowler.com/bliki/InversionOfControl.html)의 예시를 약간 변형한 것임을 밝힙니다.

{% splash %}
class ScreenPresenter {
    var name: String = ""
    var quest: String = ""

    func displayName() {
        print("Diplay User Input:", name)
    }

    func displayQuest() {
        print("Diplay User Input:", name)
    }
}

class User {
    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.name = "Hong"
        presenter.displayName()
        presenter.quest = "Do Something"
        presenter.displayQuest()
    }
}
{% endsplash %}

위 코드의 실행 순서는 다음과 같습니다.

1. `ScreenPresenter` 생성
2. `ScreenPresenter`의 property 중 `name`을 설정
3. `displayName()`을 호출하여 `name`을 출력
4. `ScreenPresenter`의 property 중 `quest`를 설정
5. `displayQuest()`을 호출하여 `quest`를 출력

장황하게 순서를 서술하였지만, 직관적으로 쉽게 이해가 가능한 흐름입니다. 이와 같이 시스템이 개발자가 작성한 코드를 호출하는 흐름을 제어의 흐름이라고 합니다.
 
제어의 흐름의 가장 큰 특징은 개발자가 작성한 코드가 시스템 동작의 제어권을 가지고 있다는 점입니다. 즉, 위의 예제에서 `displayName()`, `displayQuest()`를 호출하는 시점은 개발자가 결정합니다. 시스템은 이러한 호출에 따라서 명령을 수행합니다.

### 2. 제어 흐름의 역전

제어 흐름의 역전(`Inversion Of Control`)은 제어권을 가지고 있는 주체가 역전되는 현상을 의미합니다. 앞서서 제어의 흐름에서 시스템 동작의 제어권은 개발자가 가지고 시스템은 이를 따른다고 얘기하였습니다. IoC는 코드 수행의 제어권이 시스템쪽에 있는 현상을 의미합니다.

위에서 살펴 본 코드를 다르게 구현한 예시를 살펴보겠습니다.

```swift
class ScreenPresenter {
    var name: String = "" {
        didSet {
            didFinishWritingName?(name)
        }
    }

    var quest: String = "" {
        didSet {
            didFinishWritingQuest?(quest)
        }
    }

    var didFinishWritingName: ((String) -> Void)?
    var didFinishWritingQuest: ((String) -> Void)?
}

class User {
    func display(value: String) {
        print("Display User Input:", value)
    }

    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.didFinishWritingName = { nameInput in
            display(value: nameInput)
        }
        presenter.didFinishWritingQuest = { questInput in
            display(value: questInput)
        }
        presenter.name = "Hong"
        presenter.quest = "Do Something"
    }
}
```

위 코드의 실행 순서는 다음과 같습니다.

1. `ScreenPresenter` 생성
2. `name` 설정시 `display(value:)`가 호출되도록 설정
3. `quets` 설정시 `display(value:)`가 호출되도록 설정
4. ScreenPresenter의 property 중 `name`를 설정
5. ScreenPresenter의 property 중 `quest`를 설정

이 코드와 이전 예시의 가장 큰 차이점은 `display()` 함수를 누가 호출하는가입니다. 앞선 예시에서는 이를 개발자가 직접 호출하였습니다. 여기에서는 시스템이 호출합니다. 즉, 개발자-시스템 사이의 제어권이 역전(invert)되는 현상이 발생하였습니다.


> Ioc는 Hollywood Principle이라고도 불립니다.
> Hollywood Principle - Don,t call us, We will call you.

### 3. IoC를 통한 모듈의 확장

앞선 두 예제만 살펴봐도 제어 흐름을 역전시킨 코드는 그렇지 않은 코드보다 상대적으로 더 복잡합니다. 이는 제어 흐름을 역전하기 위해 제어권을 위임하는 장치를 추가하였기 때문입니다. 이 장치는 delegate이라고 불리는 객체를 의미하기도 하고, 위 예제에서 사용한 클로저/콜백 등을 지칭하기도 합니다. 하지만 이렇게 코드를 복잡하게 만드는 단점에도 불구하고, IoC는 의도적으로 사용됩니다. IoC를 활용하면 모듈을 매우 유연하게 확장할 수 있기 때문입니다 

IoC 현상을 활용하면, 사용하고 있는 모듈의 변경 없이 기능을 유연하게 변경할 수 있습니다. 위 예시에서 `display(value:)` 호출 이후에 화면을 reload하는 로직을 추가로 구현한다고 생각해보겠습니다. 첫 번째 예시는 아래와 같이 코드를 추가할 수 있습니다.

```swift
class ScreenPresenter {
    var name: String = ""

    func displayName() {
        print("Diplay User Input:", name)
    }
    
    func reloadScreenForName() {
        print("Reload Screen")
    }
}

class User {
    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.name = "Hong"
        presenter.displayName()
        presenter.reloadScreenForName()
    }
}
```

두 번째 예시는 아래와 같이 처리할 수 있습니다.

```swift
class ScreenPresenter {
    var name: String = "" {
        didSet {
            didFinishWritingName?(name)
        }
    }
    var didFinishWritingName: ((String) -> Void)?
}

class User {
    func display(value: String) {
        print("Display User Input:", value)
    }

    func reload(value: String) {
        print("Reload Screen")
    }

    func usePresenter() {
        let presenter = ScreenPresenter()
        presenter.didFinishWritingName = { nameInput in
            display(value: nameInput)
            reload(value: nameInput)
        }
        presenter.name = "Hong"
    }
}
```

두 예시에 나온 변경 사항의 가장 큰 차이점은 **소스코드의 어디를 수정하였는가** 입니다. 첫 번째 예시는 `ScreenPresenter`에 기능을 추가하였고, 두 번째 예시는 `ScreenPresenter`를 사용하는 사용자의 코드를 수정하였습니다. 만약 `ScreenPresenter`가 별도의 모듈에 포함되어 있는 코드라면 첫 번째 예시는 해당 모듈을 다시 컴파일해야 합니다. 반면, 두 번째 예시에서는 `ScreenPresenter`의 변경은 없기 때문에 해당 모듈을 다시 컴파일하지 않아도 됩니다. 

이러한 IoC를 통한 모듈의 재컴파일을 방지하는 특징은 모듈이 사용자의 코드를 신경쓰지 않고, 모듈의 기능을 확장할 수 있도록 합니다. 모듈은 사용자에게 필요한 적절한 인터페이스만 제공하면 됩니다.

### 4. 제어권 관점에서의 Library와 Framework

라이브러리와 프레임워크는 메소드와 클래스를 묶은 바이너리 관점에서 큰 차이가 없는 용어로 사용됩니다. 하지만, 제어권 관점에서 두 가지 용어는 명확히 구분됩니다. 

- 라이브러리 - Application에서 라이브러리의 함수를 호출하거나, 클래스를 만들어서 사용한다. 제어권이 Application에 있다.
- 프레임워크 -  Application에서 각 프레임워크에서 제공하는 인터페이스에 맞추어 메소드를 호출하거나, 서브클래싱 등을 수행(Insert Behavior)해야 한다. 제어권이 framework에 있다.

`UIKit`의 `UIViewController`를 사용할 때, 사용자는 `UIViewController`의 라이프 사이클에 맞추어서 코드를 작성합니다. 이 때, 사용자는 `UIViewController`의 라이프 사이클 관련 메소드를 직접 호출하지 않습니다. 인스턴스만 생성하면 관련 메소드들은 시스템에서 직접 호출합니다. 이 같은 기능을 보면, `UIKit`은 제어권 관점에서 프레임워크인 예시로 볼 수 있습니다.

> 애플 생태계의 개발 환경에서 라이브러리와 프레임워크는 리소스 포함 여부에 따라 구분되기도 합니다. 이에 대한 자세한 내용은 [Framework 이해하기](https://hcn1519.github.io/articles/2019-11/framework_basic)에서 확인하실 수 있습니다.

# 참고자료

- [InversionOfControl - Martin Fowler](https://martinfowler.com/bliki/InversionOfControl.html)
- [InversionOfControl - Just hack'em](https://justhackem.wordpress.com/2016/05/14/inversion-of-control/)
- [PlugIn - David Rice and Matt Foemmel](https://martinfowler.com/eaaCatalog/plugin.html)
- [ControlFlow - Wikipedia](https://en.wikipedia.org/wiki/Control_flow)
- [Inversion Of Control - Wikipedia](https://en.wikipedia.org/wiki/Inversion_of_control)
- [Clean Architecture - Robert C. Martin](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)
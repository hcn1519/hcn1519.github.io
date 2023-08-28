---
layout: post
title: "Xcode 프로젝트 파일"
excerpt: "Xcode에서 사용되는 workspace, project, target, scheme 등에 대해 알아 봅니다."
date: "2018-06-12 18:30:34 +0900"
categories: Xcode
tags: [Xcode]
---

Xcode에서는 프로젝트를 관리하거나 프로젝트를 빌드하는 용도의 파일 혹은 항목들이 있습니다. 이번 글에서는 이에 대해 알아보고자 합니다.

## Project

<div class="message">
  An Xcode project is a repository for all the files, resources, and information required to build one or more software products
</div>

`Project`는 Application을 빌드하기 위한 파일, 리소스, 정보를 담은 repository입니다. 처음 Xcode를 켜고 Single View Application을 생성하면 `Project`를 생성하게 됩니다. 이 때, 프로젝트의 디렉토리를 살펴보게 되면 `프로젝트명.xcodeproj`라는 파일이 생긴 것을 확인할 수 있습니다. 정확히 얘기하면 이는 파일이 아니라 이는 디렉토리입니다. 터미널을 통해 해당 파일로 들어가게 되면 `project.pbxproj`이라는 파일과 `xcuserdata`라는 디렉토리가 존재합니다.

* `project.pbxproj`가 실제 설정파일입니다.

`project.pbxproj`는 실제 프로젝트의 설정을 담은 파일입니다. 해당 파일을 열어보면 프로젝트 내부에서 생성된 파일들을 파일 유형에 따라 reference를 저장하고 있습니다.

> 이 project.pbxproj는 사실 git을 사용할 경우 충돌이 일어나는 주요 파일 중 하나입니다. 2명의 팀원이 작업을 위해 각자 A 파일, B 파일을 생성하여 각자 커밋한 경우 한 쪽에는 B 파일의 reference, 다른 쪽은 A 파일의 reference가 없습니다. 그래서 두 작업에서 사용된 project.pbxproj 파일은 서로 다른 reference를 가지고 있어서 conflict가 일어납니다. 그리고 이 충돌이 고치기 쉽지 않은 것이 project.pbxproj가 깨지면 프로젝트 자체가 열리지 않습니다. 그러므로 이럴 때는 에디터나 소스트리 같은 형상 관리 툴로 해당 충돌을 수정해야 합니다.

* `xcuserdata`는 프로젝트의 개인 설정을 담은 디렉토리입니다.

`xcuserdata`는 breakpoint, UI layout, 스냅샷 설정을 담은 프로젝트 자체에 크게 영향을 주지 않는 디렉토리입니다.

## Workspace

`Workspace`는 여러 개의 `Project`를 담아 관리할 수 있도록 해주는 개념입니다. `Workspace`는 대부분 CocoaPods을 처음 사용할 때 접해보았을 것입니다. CocoaPods는 본래의 프로젝트와는 별도로 `Project`를 만들어서 라이브러리 의존성을 관리할 수 있도록 해주는 도구입니다.

`Workspace`도 생성하게 되면 `Project.xcodeproj`와 유사한 디렉토리인 `project.xcworkspace`가 생성됩니다. 해당 디렉토리에 들어가보면 `contents.xcworkspacedata` 파일과 `xcuserdata`, `xcshareddata` 디렉토리가 있습니다.

* `contents.xcworkspacedata`는 프로젝트들의 referce를 저장하고 있습니다.

`contents.xcworkspacedata`는 `workspace`에 포함된 프로젝트들의 reference를 저장한 xml 파일입니다. 그래서 `workspace`에 프로젝트를 추가하면 해당 파일에 referece가 추가됩니다.

* `xcuserdata`는 workspace의 개인 설정을 담은 디렉토리입니다.

* `xcshareddata`는 workspace에 공유된 설정을 담은 디렉토리입니다.

### Workspace와 SubProject의 차이

Xcode는 여러 개의 프로젝트를 다룰 수 있도록 `Workspace` 만드는 기능도 제공하지만, 프로젝트 안에 SubProject를 생성하여 이를 관리할 수도 있습니다. 이와 같은 방식이 활용되는 경우는 오픈소스로 배포되는 라이브러리에서 라이브러리 코드가 담긴 `Project`와 라이브러리를 사용하여 만든 예제 `Project`를 나누고 싶은 경우가 있는데, 이 때 SubProject로 예제 `Project`를 활용할 수 있습니다.

물론 이 또한 `Workspace`를 통해 관리할 수도 있습니다. 다만, SubProject는 `Project` 사이의 부모-자식 관계가 생기므로 부모 프로젝트가 자식 프로젝트에 대한 reference를 가질 수 있습니다. 반대는 불가능합니다. 반면 `Workspace`를 통해 `Project`를 관리하면 `Project`들간의 관계는 형제 관계가 됩니다. 그래서 어떤 `Project`든 다른 `Project`의 reference를 지닐 수 있습니다.

## Target

<div class="message">
  Target은 프로젝트를 통해 생성되는 Application을 지칭합니다. 이는 일반적으로 하나의 모듈을 의미합니다.
</div>

"`Target`이 Application이다."라는 말의 의미는 좀 더 구체적으로 말하자면, "`Target`은 Xcode의 빌드를 통해 생성된 최종 product이다."와 의미가 같습니다. 즉, `Target`은 어떻게 프로젝트를 빌드할 것인지를 담당합니다.

Xcode에서 프로젝트에서 최상단 설정 파일을 누르게되면 project 하위에 target 섹션이 있고, 여기서 프로젝트의 target을 관리할 수 있습니다. 기본적으로 `Target`은 프로젝트 생성시 1개만 생성되지만, 목적에 따라서 하나의 프로젝트에 여러개의 `Target`을 생성할 수 있습니다.

* 각각의 target은 프로젝트의 build setting을 설정할 수 있습니다.
* 각각의 target은 프로젝트에서 포함될 객체, 리소스, 혹은 별도의 스크립트를 따로 설정할 수 있도록 해줍니다.
* Xcode에서는 target을 통해서 하나의 프로젝트를 여러 개의 배포판으로 사용할 수 있도록 해줍니다.(i.e. iPhone용 target, iPad용 target, 특정 라이브러리가 포함된 target 등)


## Scheme

<div class="message">
  An Xcode scheme defines a collection of targets to build, a configuration to use when building, and a collection of tests to execute.
</div>

`Scheme`은 `Target`이 프로젝트를 Build, Profile, Test등을 할 때 일어날 일들을 정의할 수 있도록 해주는 항목입니다. 일반적으로 `Target`은 1개 이상의 `Scheme`을 가지고 있습니다. 이 `Scheme`에서는 프로젝트 빌드시 사용되는 환경변수나 인자를 넘겨줄 수 있습니다.

### Scheme에서 Build Configuration 설정하기

`Scheme`은 앞서 언급한 것처럼 프로젝트의 런타임에서 일어날 일을 설정할 수 있습니다. 이 때 사용되는 대표적인 것 중 하나가 `Build Configuration`입니다. 기본적으로 `Build Configuration`은 `debug`, `release`가 생성됩니다. 이 `Build Configuration`은 실제 코드내에서 포함될 코드와 그렇지 않은 코드를 다르게 설정할 수 있도록 도와줍니다.

예를 들어 보겠습니다.

```swift
do {
  // do something
} catch let error {
  debugPrint(error)
}
```

다음과 같은 에러 처리 코드가 프로젝트에 있다고 했을 경우 `debugPrint`는 사실 실제 배포에 포함될 필요가 없는 코드입니다. 이러한 코드는 `Build Configuration`을 사용하여 배포 코드에 포함되지 않게 만들 수 있습니다.

```swift
do {
  // do something
} catch let error {
  #if DEBUG
    debugPrint(error)
  #endif
}
```

이렇게 코드를 작성하고 `Scheme`에서 `Build Configuration`을 `release`로 설정할 경우, `debugPrint`는 실행되지 않습니다. 이와 같은 것을 가능하게 해주는 것이 Xcode의 `PreProcessor`입니다.

---

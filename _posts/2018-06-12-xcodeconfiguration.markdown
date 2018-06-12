---
layout: post
title: "Xcode 설정 파일"
excerpt: "Xcode에서 사용되는 workspace, project, target, scheme 등에 대해 구분해봅니다."
date: "2018-06-12 18:30:34 +0900"
categories: Xcode
tags: [Xcode]
---

Xcode에서는 프로젝트를 관리하거나 빌드하는 것과 관련된 개념이 있습니다. 이번 글에서는 이에 대해 알아보고자 합니다.

## Project

`Project`는 앱 실행의 기본적인 단위라고 할 수 있습니다. 처음 Xcode를 켜고 Single View Application을 생성하는 것이 `Project`를 생성하는 것입니다. 이 때, 프로젝트의 디렉토리를 살펴보게 되면 `프로젝트명.xcodeproj`라는 파일이 생긴 것을 확인할 수 있습니다. 정확히 얘기하면 이는 파일이 아니라 이는 디렉토리입니다. 터미널을 통해 해당 파일로 들어가게 되면 `project.pbxproj`이라는 파일과 `xcuserdata`라는 디렉토리가 존재합니다.

1. `project.pbxproj`가 실제 설정파일입니다.

`project.pbxproj`는 실제 프로젝트의 설정을 담은 파일입니다. 해당 파일을 열어보면 프로젝트 내부에서 생성된 파일들을 파일 유형에 따라 reference를 저장하고 있습니다.

> 이 project.pbxproj는 사실 git을 사용할 경우 충돌이 일어나는 주요 파일 중 하나입니다. 2명의 팀원이 작업을 위해 각자 A 파일, B 파일을 생성할 경우 한 쪽에는 B 파일의 reference, 다른 쪽은 A 파일의 reference가 없기 때문입니다. 그리고 이 충돌이 고치기 쉽지 않은 것이 project.pbxproj가 깨지면 프로젝트 자체가 열리지 않습니다. 그러므로 에디터나 기타 소스 관리 툴로 해당 충돌을 수정해야 합니다.

2. `xcuserdata`는 프로젝트의 개인 설정을 담은 디렉토리입니다.

`xcuserdata`는 breakpoint, UI layout, 스냅샷 설정을 담은 프로젝트 자체에 크게 영향을 주지 않는 디렉토리입니다.

## Workspace

`Workspace`는 여러 개의 `Project`를 담아 관리할 수 있도록 해주는 개념입니다. 아마 `Workspace`는 CocoaPods를 처음 설정할 때 만들어봤을 경우가 많습니다. CocoaPods는 본래의 프로젝트와는 별도로 `Project`를 만들어서 라이브러리 의존성을 관리할 수 있도록 해주는 도구입니다.

`Workspace`도 생성하게 되면 `Project.xcodeproj`와 유사한 디렉토리인 `project.xcworkspace`가 생성됩니다. 해당 디렉토리에 들어가보면 `contents.xcworkspacedata` 파일과 `xcuserdata`, `xcshareddata` 디렉토리가 있습니다.

1. `contents.xcworkspacedata`는 프로젝트들의 referce를 저장하고 있습니다.

`contents.xcworkspacedata`는 `workspace`에 포함된 프로젝트들의 reference를 저장한 xml 파일입니다. 그래서 `workspace`에 프로젝트를 추가하면 해당 파일에 referece가 추가됩니다.

2. `xcuserdata`는 workspace의 개인 설정을 담은 디렉토리입니다.

3. `xcshareddata`는 workspace에 공유된 설정을 담은 디렉토리입니다.

### Workspace와 SubProject의 차이

Xcode는 여러 개의 프로젝트를 다룰 수 있도록 `Workspace` 만드는 기능도 제공하지만, 프로젝트 안에 SubProject를 생성하여 이를 관리할 수도 있습니다. 이와 같은 방식이 활용되는 경우는 오픈소스로 배포되는 라이브러리에서 라이브러리 코드가 담긴 `Project`와 라이브러리를 사용하여 만든 예제 `Project`를 나누고 싶은 경우가 있는데, 이 때 SubProject로 예제 `Project`를 활용할 수 있습니다.

물론 이 또한 `Workspace`를 통해 관리할 수도 있습니다. 다만, SubProject는 `Project` 사이의 부모-자식 관계가 생기므로 부모 프로젝트가 자식 프로젝트에 대한 reference를 가질 수 있습니다. 반대는 불가능합니다. 반면 `Workspace`를 통해 `Project`를 관리하면 `Project`들간의 관계는 형제 관계가 됩니다. 그래서 어떤 `Project`든 다른 `Project`의 reference를 지닐 수 있습니다.

## Target

`Target`은 프로젝트의 하위에 존재하는 개념입니다. 프로젝트 설정을 할 때, 각각의 project 하위에는 `Target`이 존재합니다. `Target`이라는 것은 product 혹은 binary가 어떤 방식으로 빌드될 것인지에 대한 설정을 하는 파일입니다. 기본적으로 `Target`은 프로젝트 생성시 1개만 생성되지만, 목적에 따라서 하나의 프로젝트에 여러개의 `Target`을 생성할 수 있습니다. 그래서 각각의 `Target`마다 라이브러리 포함 여부를 결정하든지, iPhone용, iPad용 빌드 파일을 별개로 하든지의 설정을 `Target`별로 할 수 있습니다.


## Scheme

`Scheme`은 `Target`이 프로젝트를 Build, Profile, Test등을 할 때 일어날 일들을 정의할 수 있도록 해주는 것입니다. 일반적으로 `Target`은 1개 이상의 `Scheme`을 가지고 있습니다. 이 `Scheme`에서는 프로젝트 빌드시 사용되는 환경변수나 인자를 넘겨줄 수 있습니다.

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

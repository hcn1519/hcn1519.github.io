---
layout: post
title: "Framework 이해하기"
date: "2019-11-16 00:53:17 +0900"
excerpt: "Framework에 대해 학습한 내용을 정리합니다."
categories: iOS, OS, Library, Framework
tags: [iOS, macOS, OS, Library, Framework]
image:
  feature: iOS.png
---

## 목차

1. [Framework 개념]({{ site.url }}{{ page.url }}#framework-개념)
1. [Framework 구조]({{ site.url }}{{ page.url }}#framework-구조)

## Framework 개념

### 1. Framework 정의

> A framework is a hierarchical directory that encapsulates shared resources, such as a dynamic shared library, nib files, image files, localized strings, header files, and reference documentation in a single package.

`Framework`는 공유 자원(`dynamic shared library`, nib 파일, 이미지 파일 등)을 단일 패키지 형태로 담고 있는 디렉토리입니다. `Framework`는 library와 달리 리소스를 포함할 수 있고 이는 `Framework`을 모듈 배포에 있어서 더 많이 활용할 수 있도록 해줍니다.

### 2. Framework은 Bundle의 한 종류입니다

`Framework`는 실행 바이너리를 포함한 디렉토리입니다. `Framework`는 파일 시스템의 Bundle로 패키징되어 Core Foundation Bundle Service를 이용할 수 있고, NSBundle class로 접근할 수 있습니다.

리소스는 해당 Bundle의 포함 여부에 따라 접근 가능 여부가 결정됩니다. 외부에서 `Framework` 사용시 `Framework`의 리소스에 접근하기 위해서는 해당 리소스가 포함된 bundle(Framework)을 명시해주어야 합니다. 이 말은 바꿔 말하면, 서로 다른 `Framework`에 포함된 동일한 리소스는 하나의 리소스로 인식되지 않고, 서로 다른 리소스로 인식된다는 것을 의미합니다..

`Framework`에 이미지 리소스가 포함되어 있을 때 해당 `Framework`를 사용하는 앱에서는 이 리소스에 다음과 같이 접근할 수 있습니다.

```swift
let bundle = Bundle(identifier: "com.hcn1519.ExampleFramework") // 해당 Framework의 Bundle Identifier 작성
let image = UIImage(named: "sampleImg", in: bundle, compatibleWith: nil)
```

> 여기서 `UIViewController`나 `UIImage`와 같은 클래스의 인스턴스를 생성할 때 왜 리소스 이름뿐만 아니라 bundle을 지정하는 파라미터가 왜 항상 붙어 있는지 이해할 수 있습니다. xib나 image 파일 등의 리소스를 필요로하는 인스턴스는 bundle 설정 없이는 접근할 수 없습니다.(이를 지정하지 않는 경우에 대부분 default 설정은 mainBundle이 됩니다) Bundle과 관련해서는 [Package, Bundle, NSBundle](https://hcn1519.github.io/articles/2018-12/bundle)에서도 관련 내용을 확인할 수 있습니다.

### 3. Framework은 Opaque Data Type이 아닙니다

일반적인 Bundle과는 다르게 `Framework`는 Opaque Data Type으로 취급되지 않고 이 때문에 일반적인 디렉토리로 접근됩니다. Opaque Data Type으로 취급된다는 것은 디렉토리이지만 Finder에서 실행 파일로 취급되는 것을 의미합니다. 대표적인 Bundle인 `.app`의 경우 finder에서 실행파일로 인식되어 더블 클릭하면 앱이 실행됩니다.(Bundle은 기본적으로 디렉토리이기 때문에 터미널로 `.app` 접근시 내부로 들어갈 수 있습니다.) 반면, `framework`는 finder에서 일반 디렉토리로 취급되어 더블 클릭시 내부 디렉토리로 들어갑니다.

### 4. Framework은 Application이 특정 작업을 수행할 수 있도록 기능을 제공합니다

가장 대표적인 `Framework`의 예시로는 `UIKit`, `Foundation`이 있습니다. 해당 `Framework`를 소스코드에서 import하게 되면 사용자는 `Framework`에서 제공하는 built-in 기능들을 바로 사용할 수 있습니다. 이는 라이브러리와 어느정도 같은 기능을 수행한다고 할 수 있는데, static library 혹은 dynamic library(`.a`, `.dylib`)와 `framework`은 아래의 차이점을 가지고 있습니다.

- Framework은 라이브러리보다 효율적으로 리소스를 관리할 수 있게 해줍니다.
- Framework은 리소스를 패키징된 형태로 함께 제공할 수 있지만, 라이브러리는 소스코드만 포함할 수 있습니다.
- Framework은 여러 버전을 동일한 Bundle에 포함하여 하위 버전 호환성을 지원할 수 있습니다.
- Framework은 물리적으로 메모리의 한 군데에서만 코드가 read-only 형태로 실행되기 때문에 메모리 사용량을 줄일 수 있습니다.

## Framework 구조

빌드된 `Framework` 내부 디렉토리를 살펴보면 아래 이미지와 그 형태가 유사합니다.

<img width="882" alt="frameworkDirectory_swift" src="https://user-images.githubusercontent.com/13018877/58764367-12042080-85a1-11e9-91c0-68a0eedb9187.png">

### 1. 바이너리 

- `Framework` 내부에는 `Framework`와 이름이 동일한 바이너리 파일이 존재합니다. 이 바이너리의 타입은 Build Setting에서 설정한 Mach-O Format에 따라 static, dynamic library가 됩니다.
- 해당 바이너리에 대해서 `nm` 명령어를 사용하면 symbol과 관련된 정보를 얻을 수 있습니다. 아래 명령어는 컴파일되어 나타나는 `.o` 파일이 어떤 것들이 있는지를 보여주는 간단한 명령어입니다.

```shell
nm -debug-syms ExampleFramework | grep "\.o"
```

### 2. Header

- Header의 경우 `Framework` 생성시 설정한 언어가 Swift인지 Objective-C인지에 따라 그 결과물이 바뀝니다. Xcode는 `Framework` 빌드시 Swift를 위한 별도의 Header 파일(`ExampleFramework-Swift.h`)을 생성합니다. Objective-C 기반 `Framework`는 이 파일이 생성되지 않습니다.
- `ExampleFramework.h`은 기본적으로 public header를 관리합니다. Objective-C로 작성된 객체를 외부에서 접근하기 위해서는 관련 header를 public으로 전환해주어야 합니다. 즉, `ExampleFramework.h`에 관련 header 파일을 작성해야 합니다. Swift 객체의 경우 접근 제어자 룰에 따라 외부 `Framework`에서 사용 가능 여부가 결정됩니다.

### 3. modulemap

- Swift는 `module` 단위로 소스코드를 관리합니다. 하나의 `module`은 import시 하나의 `module`이 됩니다. `modulemap`은 `module`과 header의 연결고리 역할을 하는 파일로, `module`에 포함되는 header가 무엇인지 정의하고, 어떤 implementation(`.a`, `.dylib`)가 `module`에 포함되는지를 알려주는 파일입니다. Xcode 빌드 설정에서 `DEFINE_MODULES` 옵션에 따라 해당 파일의 생성 여부가 결정됩니다.(default 설정은 true입니다.)

<img width="863" alt="스크린샷 2019-11-17 오후 6 52 22" src="https://user-images.githubusercontent.com/13018877/69006090-c9cd9480-096d-11ea-8045-b0a54f0038ba.png">

## 참고자료

- [Framework Programming Guide - What are Frameworks?](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/WhatAreFrameworks.html#//apple_ref/doc/uid/20002303-BBCEIJFI)
- [LLVM - modulemaps](https://clang.llvm.org/docs/Modules.html#module-maps)
- [Deep dive into Swift frameworks](https://theswiftdev.com/2018/01/25/deep-dive-into-swift-frameworks)
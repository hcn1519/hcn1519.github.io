---
layout: post
title: "Static Library"
date: "2019-07-01 00:53:17 +0900"
excerpt: "Static Library 대해 학습한 내용을 정리합니다."
categories: iOS, OS, Library, Framework
tags: [iOS, OS, Library, Framework]
image:
  feature: iOS.png
---

`Static library`는 아카이빙된 object file(`.o` 확장자)의 모음으로 `.a` 확장자 형태의 라이브러리입니다. `Static library`는 `Static archive library`, `static linked shared library`라고도 불립니다.

Xcode에서는 `Static library`를 만드는 템플릿을 제공하고 있으며, 아래 그림에서 볼 수 있듯이 `Cocoa touch Static Library`를 통해서 생성할 수 있습니다.

<img width="1512" alt="스크린샷 2019-06-24 오전 12 47 52" src="https://user-images.githubusercontent.com/13018877/59978668-bb2abd80-9619-11e9-9ff3-04d6792d8198.png">

* macOS/iOS의 소스 코드를 컴파일하게 되면 object files를 생성합니다. object file은 Mach-O 형식의 바이너리 데이터로 다음의 내용을 포함하고 있습니다.
    1. Header - 파일이 동작하는 아키텍쳐에 대한 정보를 명시한다(x86, arm64 등)
    2. Load Commands - 파일의 논리적 흐름에 대한 정보를 명시한다.
    3. Raw Segment Data - raw code와 data

> Mach-O is the native executable format of binaries in OS X and is the preferred format for shipping code. An executable format determines the order in which the code and data in a binary file are read into memory.

* https://developer.apple.com/library/archive/documentation/Performance/Conceptual/CodeFootprint/Articles/MachOOverview.html

### Static Library의 동작 과정

앱의 빌드 과정에서 object file은 linker(`static linker`)를 통해서 `executable` 파일로 합쳐집니다. `executable`  file은 앱이 메모리에 올라갈 준비가 완료된 형태의 파일로, 일반적인 Application 생성 프로젝트는 빌드의 결과물로 `executable`file을 생성합니다. 

<img width="420" alt="스크린샷 2019-06-24 오전 1 43 02" src="https://user-images.githubusercontent.com/13018877/59979337-8ae71d00-9621-11e9-979d-94fba9111ae4.png">

위의 그림의 `SampleProject.App`의 경로로 빌드 완료 후 아래 명령어를 실행하면 `executable` file이 생성된 것을 확인할 수 있습니다.

```shell
$ file SampleProject.app/SampleProject
SampleProject.app/SampleProject: Mach-O 64-bit executable arm64
```

static library는 앱의 라이브러리와 `static linker`를 통해 앱과 연결될 때, 앱의 `executable` file로 복사됩니다. 그리고, `static linker`는 object code와 library code를 하나의 `executable` file로 모아서 런타임에서 항상 코드를 메모리에 로드해놓습니다. 즉, 앱이 실행될 때 앱과 연결된 `Static Library`는 앱의 주소공간에 항상 로드되어 있습니다.

<img width="681" alt="staticLib" src="https://user-images.githubusercontent.com/13018877/59974188-0cb85580-95e4-11e9-8e07-ce9c9d892391.png">

### Static Library의 한계와 Dynamic Library

`Static Library`는 앱 실행시 앱의 주소 공간에 항상 로드되어 있기 때문에 라이브러리 코드의 실행 속도가 매우 빠릅니다. 하지만, `Static Library`는 앱의 `executable` file에 반드시 포함되어야 하기 때문에 아래의 문제를 일으킵니다.

* 앱의 초기 런칭 속도 저하
* 앱의 초기 메모리 사용량 증가
* `Static Library`의 버전 업데이트시 개발자는 앱의 object files를 새로운 버전의 `Static Library`로 연결해야 합니다. `Static Library`는 새로운 버전으로 빌드가 되어야 업데이트된 라이브러리를 사용할 수 있습니다.

---

## 참고자료

* [Overview of Dynamic Libraries - Apple Doc](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/OverviewOfDynamicLibraries.html#//apple_ref/doc/uid/TP40001873-SW1)
* [http://www.vadimbulavin.com/static-dynamic-frameworks-and-libraries/](http://www.vadimbulavin.com/static-dynamic-frameworks-and-libraries/)
* [Static Libraries vs. Dynamic Libraries](https://medium.com/@StueyGK/static-libraries-vs-dynamic-libraries-af78f0b5f1e4)
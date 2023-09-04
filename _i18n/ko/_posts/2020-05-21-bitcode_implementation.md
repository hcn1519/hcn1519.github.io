---
layout: post
title: "Bitcode 도입하기"
date: "2020-05-21 00:53:17 +0900"
excerpt: "Bitcode 도입을 위해 알아야 하는 것들에 대해 정리해보았습니다."
categories: Bitcode, AppStore, Xcode, iOS, BuildSystem, Symbol, CrashReport
tags: [Bitcode, AppStore, Xcode, iOS, BuildSystem, Symbol, CrashReport]
image:
  feature: iOS.png
table-of-contents: |
  ### Table of Contents          
  1. [About bitcode](./bitcode_implementation#about-bitcode)
    1. [bitcode 업로드 프로세스](./bitcode_implementation#bitcode-업로드-프로세스)
    1. [bitcode가 활성화된 앱의 Symbolication](./bitcode_implementation#bitcode가-활성화된-앱의-symbolication)
    1. [bcsymbolmap](./bitcode_implementation#bcsymbolmap)
  1. [Xcode Build Setting for bitcode](./bitcode_implementation#xcode-build-setting-for-bitcode)
    1. [ENABLE_BITCODE](./bitcode_implementation#enable_bitcode)
    1. [BITCODE_GENERATION_MODE](./bitcode_implementation#bitcode_generation_mode)
  1. [Library의 bitcode 지원](./bitcode_implementation#library의-bitcode-지원)
    1. [바이너리의 bitcode 지원 확인하기](./bitcode_implementation#바이너리의-bitcode-지원-확인하기)
    1. [CocoaPods을 통해 배포되는 라이브러리의 bitcode 지원](./bitcode_implementation#cocoaPods을-통해-배포되는-라이브러리의-bitcode-지원)
---

이번 글에서는 bitcode 도입을 위해 필요한 부분을 정리해보았습니다.

## About bitcode

### bitcode 업로드 프로세스

<div class="message">
    Bitcode is an intermediate representation of a compiled program
</div>

- bitcode는 앱스토어에서 App Thining을 위해 바이너리 빌드시 포함하는 [IR](https://en.wikipedia.org/wiki/Intermediate_representation)입니다. 앱스토어에서는 업로드된 바이너리에 bitcode가 포함되어 있을 경우 앱의 compile과 linking을 다시 수행하여, 디바이스의 아키텍쳐별로 최적화된 바이너리를 새롭게 생성하고 이를 배포합니다.
- 앱 사용자는 자신의 디바이스에 맞는 아키텍처에 대한 바이너리만 다운로드 받으면 되므로 bitcode 활성화시 사용자가 다운로드 받는 앱의 용량이 줄어들게 됩니다.
- 정리하면 앱 스토어에 바이너리 업로드시 다음의 과정이 수행됩니다.

1. bitcode가 적용된 하나의 바이너리를 앱스토어에 업로드합니다.
2. 앱 스토어에서 이 바이너리를 다시 컴파일하여 아키텍처별로 바이너리를 생성합니다.(arm64용 바이너리, armv7용 바이너리 등)
3. 앱 사용자는 각 디바이스의 아키텍처에 맞는 바이너리만 다운로드 합니다.(bitcode 적용 이전에는 바이너리가 나뉘어지지 않고, 한 개(fat binary)만 사용합니다.)

### bitcode가 활성화된 앱의 Symbolication

- 앱 스토어에서 다시 컴파일이 발생하는 것은 앱 개발자가 스토어 업로드를 위해 진행하는 아카이빙의 결과물로 나오는 dSYM을 사용할 수 없게 만듭니다. 앱 바이너리와 dSYM은 바이너리에 포함되는 UUID를 기반으로 매칭이 됩니다. 그래서 빌드가 다시 발생하면(설령 수정 사항이 없는 코드라도) 이전 빌드 결과물의 바이너리/dSYM은 이후의 것과 매칭될 수 없습니다. 그래서 아카이빙 과정에서 생성된 dSYM은 스토어 버전의 앱에서 발생하는 Crash Report를 Symbolicate할 수 없습니다.
- 따라서, bitcode 활성화 이후에 Third Party Crash 분석 플랫폼에 dSYM 업로드시에는 **반드시** Xcode Organizer나 iTunes Connect에서 파일을 다운로드 받아야 합니다.

### bcsymbolmap

- 아카이빙 진행시 iTunes Connect에 앱의 Symbol을 업로드할지 결정하는 체크 박스가 존재합니다. 이를 비활성화 할 경우 Xcode는 바이너리 업로드 이전에 앱의 dSYM 파일에 포함된 Symbol을 난독화합니다.(`"__hidden#109_"`와 같은 형태) 이렇게 난독화된 Symbol은 `.bcsymbolmap`이라는 파일을 통해 복호화됩니다. 그래서 bitcode를 지원하는 바이너리의 dSYM 파일은 그에 대응하는 `.bcsymbolmap`을 항상 함께 가지고 있습니다.
- Third Party Crash 분석 플랫폼에 dSYM을 업로드할 때, Xcode에서 다운로드 받는 dSYM은 복호화가 되어 있어서 바로 업로드해도 무방합니다. 하지만 iTunes Connect에서 직접 다운로드 받는 dSYM은 복호화를 직접해주어야 합니다.

```shell
xcrun dsymutil -symbol-map <xcarchive 내의 BCSymbolMaps 경로> <다운로드 받은 dSYM 디렉토리 경로>
```

## Xcode Build Setting for bitcode

- Xcode는 바이너리 빌드시 full bitcode를 포함하는 것과 bitcode가 있다는 것을 표시하는 marker를 포함하는 옵션이 존재합니다.

### ENABLE_BITCODE

ENABLE_BITCODE을 YES로 설정하면 소스코드 빌드/아카이브시 bitcode와 관련된 Flag가 추가됩니다. 이 때, Build Action에서는 `-embed-bitcode-marker`가 추가되고, Archive Action에서는 `-embed-bitcode`가 추가됩니다. 관련 정보는 실제 빌드/아카이빙 수행시 로그를 확인해보면 알 수 있습니다.

- 빌드 수행시 로그

```
// 빌드 로그 발췌
CompileSwift normal arm64 TestObj.swift (in target 'SomProject' from project 'SomProject')
...
/Debug-iphoneos/SomProject.build/Objects-normal/arm64/TestObj.o -embed-bitcode-marker 
...
```

- 아카이빙 수행시 로그

```
// 아카이빙 로그 발췌
SwiftCodeGeneration normal arm64 (in target 'SomProject' from project 'SomProject')
...
/Release-iphoneos/SomProject.build/Objects-normal/arm64/TestObj.bc -embed-bitcode -target arm64-apple-ios11.0 -Xllvm -aarch64-use-tbi -O -disable-llvm-optzns -module-name
...
```

### BITCODE_GENERATION_MODE

User Defined Settings에 `BITCODE_GENERATION_MODE`을 통해서도 `ENABLED_BITCODE`와 동일한 효과를 만들어 낼 수 있습니다. 이 때 value로 `maker`를 설정할 경우 `embed-bitcode-marker`가 컴파일 Flag로 전달되고, `bitcode`를 설정할 경우 `embed-bitcode`가 전달됩니다. 경우에 따라서 Build Action에서 full bitcode를 사용해야 하는 경우에 해당 설정 값을 변경하여 Build를 진행할 수 있습니다.

<img width="484" alt="스크린샷 2020-05-22 오전 12 59 59" src="https://user-images.githubusercontent.com/13018877/82578788-d73b3400-9bc7-11ea-9ff4-953814cbead4.png">

> Note: Other C Flag에 직접 `-fembed-bitcode`를 추가하여 bitcode를 활성화할 수도 있습니다.

## Library의 bitcode 지원

- bitcode의 가장 큰 단점은 사용하고 있는 라이브러리가 하나라도 bitcode를 지원하지 않을 경우, 앱에서는 bitcode를 활성화할 수 없다는 점입니다.
- 앱에서 사용하고 있는 라이브러리의 bitcode 관련하여 참고하면 좋은 내용을 정리하면 다음과 같습니다.

### 바이너리의 bitcode 지원 확인하기

- 특정 라이브러리가 bitcode를 지원하는지 확인하기 위해서는 해당 라이브러리의 바이너리가 LLVM Symbol을 포함하고 있는지를 확인하면 됩니다. 다만, 어떤 Symbol을 확인하면 되는지에 대한 여러 [이슈](https://stackoverflow.com/a/33105733/5130783)가 존재하여 확인에 혼돈이 오는 경우가 있습니다.
- 결론적으로 아래의 명령어를 통해 출력되는 Symbol이 존재한다면 해당 바이너리는 bitcode를 지원하는 것이라고 볼 수 있습니다.

```shell
$ otool -arch arm64 -l MyFramework/MyFramework | grep __LLVM
$ otool -arch armv7 -l  myLib.a | grep __LLVM
```

### CocoaPods을 통해 배포되는 라이브러리의 bitcode 지원

- bitcode는 link 과정에서 처리되는 것이 아니라, compile 과정에서 처리됩니다. 그래서 라이브러리의 빌드를 수행할 때, 해당 바이너리가 bitcode 지원을 하는지 안 하는지에 따라 해당 라이브러리의 bitcode 지원 여부가 결정됩니다. 따라서, **빌드된 바이너리로 배포되는 framework/library의 경우, 이전에 bitcode를 지원하지 않았다면, bitcode를 활성화하여 다시 빌드 후 재배포가 필요합니다.**
- CocoaPods의 경우 `vendored_framework`, 혹은 `vendored_libraries` 으로 배포되는 것들이 이에 해당합니다. 이 중 하나의 라이브러리라도 bitcode를 지원하지 않을 경우 라이브러리를 사용하는 앱에서는 bitcode를 사용할 수 없습니다.
- 반면, CocoaPods에서 빌드 바이너리 형태로 배포되는 Pod이 아닌 것들은 앱을 빌드할 경우 직접 빌드를 수행합니다. 그래서 앱의 PodFile 혹은 PodSpec에서 `ENABLED_BITCODE`를 명시적으로 `NO`로 설정하지 않으면 bitcode를 지원합니다.

# 참고자료

- [Understanding and Analyzing Application Crash Reports - bitcode](https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-SYMBOLICATION-BITCODE)
- [What is app thinning? (iOS, tvOS, watchOS)](https://help.apple.com/xcode/mac/11.0/index.html?localePath=en.lproj#/devbbdc5ce4f)
- [How to handle bitcode](https://www.slideshare.net/syoikeda/how-to-handle-bitcode)
- [How to check a static library is built contain bitcode?](https://stackoverflow.com/questions/32755775/how-to-check-a-static-library-is-built-contain-bitcode)
- [Static Libraries, Frameworks, and Bitcode](https://medium.com/@heitorburger/static-libraries-frameworks-and-bitcode-6d8f784478a9)
- [https://forums.developer.apple.com/message/7038#11344](https://forums.developer.apple.com/message/7038#11344)
- [https://www.guardsquare.com/en/blog/enable-bitcode](https://www.guardsquare.com/en/blog/enable-bitcode)

---
layout: post
title: "Crash Report Symbolication"
date: "2020-02-09 00:53:17 +0900"
excerpt: "Crash Report의 Symbolication에 대해 알아 봅니다."
categories: iOS, OS, BuildSystem, Symbol, CrashReport
tags: [iOS, macOS, OS, BuildSystem, Symbol, CrashReport]
image:
  feature: iOS.png
table-of-contents: |
  ### Table of Contents        
    1. [크래시 리포트의 생성](./crash_report_symbolication#1-크래시-리포트의-생성)
    2. [Symbol, Symbolication](./crash_report_symbolication#2-symbol-symbolication)
    3. [Crash Report Symbolication](./crash_report_symbolication#3-crash-report-symbolication)
    4. [Appendix](./crash_report_symbolication#4-appendix)
translate: true
---


이번 글에서는 앱에서 크래시 리포트가 어떻게 생성되고, 이를 AppStore Connect에서 확인할 수 있는지 알아보고자 합니다.

> Note: 시작하기에 앞서 이 글의 많은 내용이 [Understanding and Analyzing Application Crash Reports - Apple Doc](https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-INTRODUCTION)의 내용을 정리한 내용임을 밝혀둡니다.

## 1. 크래시 리포트의 생성

사용하고 있는 디바이스에서 크래시가 발생할 경우 시스템은 크래시 리포트를 생성하고 이를 디바이스 내부에 저장합니다. 크래시 리포트는 크래시가 발생한 시점에 대한 환경 정보나 기타 크래시 분석에 유용한 정보들을 담고 있습니다.

<div class="message">
    Crash reports describe the conditions under which the application terminated, in most cases including a complete backtrace for each executing thread, and are typically very useful for debugging issues in the application.
</div>

크래시 리포트는 크래시가 발생한 디바이스의 설정에서 확인할 수 있습니다.

> 설정 > 개인정보 보호 > 분석 및 향상 > 분석 데이터

이렇게 저장되어 있는 크래시 리포트를 확인하면 다음과 같은 내용을 담고 있습니다.

<img width="1237" alt="스크린샷 2020-01-27 오후 8 03 47" src="https://user-images.githubusercontent.com/13018877/73169775-27394b00-4140-11ea-9059-36d646a80dcd.png">

내용을 살펴보면 어떤 환경에서 크래시가 발생했는지 대략적으로 확인할 수 있습니다. 그런데 크래시가 발생한 Thread에서 나오는 BackTrace를 살펴보면 소스 코드의 어디에서 크래시가 나오는지 확인하기가 어렵습니다. 어떤 Framework에서 문제가 발생했는지는 대략적으로 알 수 있지만, 이는 너무 광범위해서 디버깅에 큰 도움이 되지 않습니다. 이렇게 BackTrace가 사람이 읽을 수 없는 형태로 나타나는 이유는 크래시 리포트가 `UnSymblicate` 상태이기 때문입니다. 크래시 리포트가 포함하고 있는 정보는 크래시 리포트가 `Symbolication` 되었는지, 아닌지에 따라 보여지는 포맷이 변경됩니다.

## 2. Symbol, Symbolication

### Symbol

여기까지 글을 읽으셨다면 개발자가 크래시 로그를 분석할 때, 크래시 리포트가 `Symbolication`된 상태이어야 한다는 것을 알 수 있습니다. 그렇다면 `Symbolication`은 어떤 과정일까요? `Symbolication`이 무엇인지 알기 위해서 우선적으로 `Symbol`이 무엇인지 알 필요가 있습니다.

<div class="message">
    Symbol - A symbol in computer programming is a primitive data type whose instances have a unique human-readable form.
</div>

`Symbol`은 **사람이 읽을 수 있는** 데이터 타입으로, 주로 해당 `Symbol`이 위치하는 scope 내에서 고유한 값이라는 특징을 지닙니다. `Symbol`의 예로는 전역 변수, 지역 변수, 함수의 이름, 인자 값 등이 있습니다.

`Symbol`은  주로 `Symbol Table`(Hash Table)의 형태로 저장 됩니다. `Symbol Table`은 각각의 Symbol이 소스코드의 어떤 의미를 지니는지를 담고 있는 자료구조입니다.

<div class="message">
    Symbol Table - In computer science, a symbol table is a data structure used by a language translator such as a compiler or interpreter, where each identifier (a.k.a. symbol) in a program's source code is associated with information relating to its declaration or appearance in the source.
</div>

`Symbol Table`은 일반적으로 빌드 바이너리와 별개로 관리됩니다. 즉, 앱 릴리즈시 빌드된 `.app`에 `Symbol Table` 정보가 포함되지 않도록 하는 것이 일반적입니다. 이렇게 하는 이유는 `Symbol Table`이 앱 동작에 직접적으로 관여하는 것도 아니고, `Symbol Table`의 용량이 생각보다 크기 때문입니다. 그래서 `Symbol Table`은 많은 경우에 컴파일러의 소스코드 해석 과정에서만 메모리 위에 존재하는데, 그 시점은 디버깅 과정, 크래시 리포트 `Symbolication` 과정에 정도입니다.

> 위와 같이 앱 빌드 과정에서 컴파일된 Object 파일에서 Symbol을 제거하는 작업을 [strip](https://www.computerhope.com/unix/strip.htm)이라고 하고, 릴리즈 앱 배포시에는 `strip` 된 바이너리를 사용합니다.

Symbol Table에 포함되는 정보는 언어마다 조금씩 다르지만, 대략적으로 아래와 같은 정보를 포함합니다.

* Symbol의 이름
* Symbol의 relocatable 특성(absolute, relocatable 여부 등)
* Symbol의 위치 혹은 주소 값
* 고차원 언어에서는 Symbol Table에 Symbol의 데이터 타입, 크기, 차원, 길이 등의 정보를 저장하기도 한다.

### Debug Symbol

`Debug Symbol`(`dSYM`)은 Symbol 중에서 디버깅을 위해 필요한 정보를 좀 더 많이 가지고 있는 Symbol을 말합니다.

<div class="message">
A debug symbol is a special kind of symbol that attaches additional information to the symbol table of an object file, such as a shared library or an executable.
</div>

그래서 `Debug Symbol`은 Symbol이 위치한 소스코드 라인 정보, Symbol의 크기, Symbol이 포함된 class, struct의 정보 등을 추가적으로 가지고 있습니다.

### Symbolication

이제 크래시 리포트의 `Symbolication`이 무엇을 의미하는지 알아보겠습니다.

<div class="message">
Symbolication is the process of resolving backtrace addresses to source code method or function names, known as symbols
</div>

`Symbolication`은 크래시 리포트에서 나타나는 BackTrace의 주소값을 `Symbol`로 전환하는 과정을 의미합니다. 주소값을 `Symbol`로 전환한다는 것의 의미는 사람이 봐도 의미를 모르는 주소값이 사람이 보면 무엇인지 알 수 있는 소스코드의 특정 `Symbol`로 전환이 되는 것을 의미합니다. 그래서 `Symbolication`된 크래시 리포트를 보게 되면 실제로 소스 코드의 어떤 부분에서 크래시가 발생하였는지 알 수 있게 됩니다.

## 3. Crash Report Symbolication

앞서서 크래시 리포트가 생성되어 디바이스에 저장되고 이를 export하는 과정을 간략히 살펴 보았습니다. 이처럼 사용자의 앱에 쌓이는 크래시 리포트를 직접 export하여 디버깅을 하기도 합니다. 하지만, 많은 크래시는 누구인지 모르는 사용자의 기기에서 발생합니다. 그리고 크래시를 분석하기 위해서 사용자의 디바이스의 크래시 로그를 보내달라고 하는 것은 매우 불편하고, 현실적인 크래시 분석 방법이 아닙니다.

이와 같은 문제를 해결하기 위해 애플은 동의를 얻은 사용자(혹은 Test Flight 사용자)에 한하여 iTunes Connect에서 크래시가 발생한 기기의 Diagnostic Data를 제공합니다.(`symbolicate` 된 크래시 리포트) 여기서는 애플이 이 Diagnostic Data를 어떻게 제공하는지 크래시 리포트 `Symbolication` 과정을 중심으로 살펴 보겠습니다.

각 과정에 대한 이미지는 [다음](https://developer.apple.com/library/archive/technotes/tn2151/Art/tn2151_crash_flow.png)에서 확인할 수 있습니다.

1. 컴파일러는 소스코드를 해석하면서 `Debug Symbol`을 함께 생성합니다. `Debug Symbol`은 컴파일된 바이너리의 machine instruction(주소값 정보)이 우리가 작성한 소스코드의 어떤 라인에 매핑되는지에 대한 정보를 가지고 있습니다.
2. 앱 스토어 배포를 위해 아카이빙을 수행할 경우, Xcode는 `.xcarchive` 파일을 `~/Library/Developer/Xcode/Archives` 경로에 생성합니다.
3. 앱 스토어에 앱을 배포하거나, Test Flight을 통해 베타 테스트를 진행할 경우, iTunes Connect에 `dSYM` 파일을 함께 업로드할 지 선택할 수 있습니다. 이 때, dSYM 파일을 함께 업로드한다고 설정하면 iTunes Connect의 Diagnostic Data에서 크래시 리포트 정보를 확인할 수 있습니다.
4. 앱에서 크래시가 발생할 경우, `UnSymbolicated`  상태의 크래시 리포트가 디바이스에 저장됩니다.
5. 해당 크래시 리포트는 사용자로부터 몇 가지 방법을 통해 얻을 수 있습니다. 사용자의 디바이스에 쌓인 크래시 리포트를 직접 export하여 얻을 수도 있고, 디바이스를 맥과 연결하여 Xcode를 통해 크래시 리포트를 얻을 수도 있습니다. 그리고 Diagnostic Data를 전송하기로 설정한 사용자의 크래시 리포트는 iTunes Connect에서 확인할 수 있습니다.
6. `UnSymbolicated` 상태의 크래시 리포트는 `dSYM` 파일을 통해 `symbolicate`할 수 있습니다. `Symbolicate` 과정을 통해 BackTrace의 주소값을 `Symbol`로 변경할 수 있게 됩니다.
사용자가 Diagnostic Data를 애플과 공유한다고 설정하였을 경우 크래시 리포트가 앱 스토어에 업로드됩니다.(혹은 Test Flight 환경)
7. iTunes Connect에서는 업로드된 dSYM과 크래시 리포트를 통해 Symbolicate 된 크래시 리포트를 생성합니다.

> `dSYM` 파일과 앱 바이너리는 `Build UUID`를 통해 서로를 식별합니다. 그리고 `Build UUID`는 매 빌드마다 새로 생성됩니다. 그렇기 때문에, 소스 코드 변경 없이 빌드를 수행하는 경우에도 이전에 생성된 `dSYM` 파일과 새로 생성된 앱 바이너리는 서로 다른 `Build UUID`를 가집니다.

## 4. Appendix

### Xcode - dSYM 설정

`Debug Symbol`은 Xcode Build Setting의 `Debug Information Format`에서 컴파일된 바이너리에 포함시킬지 여부를 결정할 수 있습니다.

<img width="707" alt="스크린샷 2019-12-14 오후 10 03 34" src="https://user-images.githubusercontent.com/13018877/70849116-9bd06700-1ebd-11ea-80db-19a2b04d7d7e.png">

일반적으로 Debug 모드에서는 `Debug Symbol`이 바이너리에 포함되고, Release 모드에서는 바이너리 사이즈를 줄이기 위해 이를 바이너리에 포함되지 않도록 설정합니다. 아래는 `Debug Information Format`을 `DWARF with dSYM File`으로 설정하고 빌드하였을 경우에 나타나는 빌드 결과물입니다.

<img width="1018" alt="스크린샷 2020-01-28 오전 2 25 59" src="https://user-images.githubusercontent.com/13018877/73197982-a39a5100-4175-11ea-8f90-fe21f809494c.png">

## 참고 자료

* [Understanding and Analyzing Application Crash Reports - Apple Doc](https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-INTRODUCTION)
* [Symbol](https://en.wikipedia.org/wiki/Symbol_(programming))
* [Symbol Table](https://en.wikipedia.org/wiki/Symbol_table)
* [Debug Symbol](https://en.wikipedia.org/wiki/Debug_symbol)
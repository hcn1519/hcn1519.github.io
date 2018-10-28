---
layout: post
title: "Code Signing iOS(macOS)"
excerpt: "Code Signing이 무엇이고, 어떻게 동작하는지 알아봅니다."
date: "2018-10-28 01:03:19 +0900"
categories: iOS CodeSigning ProvisioningProfile Certificate
tags: [iOS, CodeSigning, ProvisioningProfile, Certificate]
---

`Code Signing`이라는 것은 종이 계약서에 서명을 남기는 것처럼 코드에 서명을 남기는 작업입니다. 여기서 코드의 범주는 단순히 우리가 작성하는 코드뿐만 아니라, 데이터, 라이브러리, 툴 등 모든 코드로 이뤄진 것들을 포함합니다. 우리가 계약서에 서명을 한다고 하였을 때 중요한 것은 **계약서의 내용**과 계약 내용의 이행을 보장하는 **서명** 자체입니다. 즉, 계약서의 내용은 계약서에 서명한 이후에 바뀌어선 안 됩니다. `Code Signing`도 계약서의 서명과 동일한 동작을 보장해야 합니다. 그래서

1. `Code Signing`은 실제로 서명자가 서명했다는 것을 알려줄 수 있어야 하고,
2. 코드의 내용이 `Code Signing` 시점에서 변경되었는지, 아닌지를 알려줄 수 있어야 합니다.

이와 같은 기능을 포함하기 위해 `Code Signing`은 몇 가지 구성요소의 조합을 통해 구성됩니다. 여기서는 이 `Code Signing`이 어떻게 이루어져 있는지에 대해 살펴보겠습니다.

## Code Signing의 구성

### 1. Seal - 도장

`Code Signing`을 수행하는 소프트웨어는 최종 번들(앱, 라이브러리, 프레임워크)에서 여러 리소스를 사용하여 단방향 해싱 알고리즘으로 `seal(도장)`을 만듭니다. 이 `seal`은 짧은 문자열 묶음(해시)으로, 특정 input block에 대해 unique하고, original input을 재조립하는 데 사용할 수 없도록 만들어집니다.

코드를 평가하는 주체(시스템에서 코드 변경을 파악하는 주체)는 코드를 서명하는 주체와 동일한 해싱 알고리즘을 사용하여 결과를 생성합니다. 그리고 두 결과를 비교하여 코드의 변경 여부에 대해 파악합니다. 이와 같은 비교 과정은 해시가 변경되지 않았음이 보장될 때 유효합니다. 그리고 이를 보장하는 것이 `Digital Signature`입니다.

### 2. Digital Signature - 전자 서명

* 전자 서명의 기본적인 용도는 서명자의 신분을 인증하는 것입니다. 하지만, 전자 서명은 이것뿐만 아니라 서명 데이터가 변경되지 않는 것을 보장합니다.(문서에 워터마크를 심는 것과 비슷합니다)

#### 전자 서명의 생성
* 전자 서명은 공개키 암호화 방식을 사용하여 만들어집니다.
* 전자 서명은 Seal의 해시 값과 서명자의 개인키를 통해 생성됩니다.
* 서명자가 만들어낸 암호화된 해시와 `Certificate`가 종합적으로 전자 서명을 나타냅니다.

#### 전자 서명의 검증

* 서명 검증 소프트웨어는 앱의 코드와 데이터로부터 해시(1)를 생성합니다.
* `Certifcate`에 있는 공개키를 사용하여 서명자가 제출한 암호화된 해시를 해독하여 원래 해시(2)를 생성합니다.
* 두 해시(1, 2)를 비교하여 데이터 변화를 검증합니다. 여기서 둘의 결과가 같으면 동일한 서명을 가지고 있는 것이고, 그렇지 않으면 서로 다른 서명으로 판단합니다.

#### 서명된 코드의 포함 요소

* 앱의 bundle에 있는 데이터 컴포넌트(ex: `Info.plist` 등)에도 서명을 할 수 있습니다. 이 서명은 `_CodeSignature/CodeResources`에 들어가 있습니다.
* 라이브러리, 툴 등 앱 안에 있는 코드들도 서명될 수 있고 이 내용도 `_CodeSignature/CodeResources`에 들어갑니다.

![Code Signing](https://dl.dropbox.com/s/9v56ejijdd4ad9r/codeSigning.png)

위의 그림은 `_CodeSignature/CodeResources`의 일부분을 캡쳐한 것입니다. 자세히 들여다보면 각 파일 이름으로 key가 설정되어 있고, 일정한 해시가 value로 들어가 있는 것을 확인할 수 있습니다.

### 3. Code Requirement

`Code Requirement`는 `Code Signing`을 평가할 때 사용하는 규칙을 의미합니다. 시스템은 코드 `Code Signing`을 평가할 때 어떤 `Code Requirement`을 적용할지 판단합니다. 예를 들어서, 앱은 `Code Requirement`을 통해 앱 내에서 사용하는 모든 플러그인이 애플의 서명을 얻었는지 확인하는 절차를 거치도록 할 수 있습니다.

#### Internal Requirement

`Internal requirement`이란 `Code Requirement` 중 서명자에 의해 구체화되고, 코드 서명 안에 포함된 것을 의미합니다. `Internal requirement`는 시스템이 코드 서명을 확인할 때 사용할 수 있습니다. 하지만 시스템이 이를 반드시 사용하는 것은 아닙니다. 예를 들어서 앱에 포함된 플러그인도 `Internal requirement`을 가지고 있지만 시스템은 이를 쓰지 않을 수도 있습니다.

#### Designated Requirement

`Internal requirement`이면서 시스템에게 특정 코드를 어떻게 identifying하는지에 대한 규칙을 담고 있는 것을 `Designated Requirement`이라고 합니다.

* 특정 코드가 동일한 `Designated Requirement`을 가지고 있으면(그리고 정해진 확인 작업 거쳤다면), 두 코드는 동일하다고 할 수 있습니다. 이는 코드 서명자가 동일한 앱의 다른 버전을 배포할 수 있도록 해줍니다. 예를 들어 Apple Mail이라는 앱이 있을 때 동일한 `Designated Requirement`을 가지고 있고 동일한 identifier(`com.apple.mail`)를 가지고 있는 코드는 동일한 앱이라고 인식될 수 있습니다. `Designated Requirement`을 통한 비교는 완전히 다른 바이너리를 갖고 있어도 적용되기 때문에 다른 버전의 애플 메일 앱을 배포할 수 있도록 해줍니다.
* `Designated Requirement`는 `Info.plist`에 있는 `CFBundleIdentifier`와 코드 서명을 보호하는 서명 체인을 통해 생성됩니다.


---

# 참고자료

* [Understanding the Code Signature](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/AboutCS/AboutCS.html#//apple_ref/doc/uid/TP40005929-CH3-SW3)

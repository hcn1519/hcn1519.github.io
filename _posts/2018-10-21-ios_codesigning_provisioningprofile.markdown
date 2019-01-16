---
layout: post
title: " iOS 인증서, Provisioning Profile"
excerpt: "앱을 iOS 기기에 설치하기 위해 필요한 Certificate, Provisioning Profile 등에 대해 알아 봅니다."
date: "2018-10-21 17:01:31 +0900"
categories: iOS ProvisioningProfile Certificate Distribution Xcode
tags: [iOS, ProvisioningProfile, Certificate, Distribution, Xcode]
---

iOS에서 자신이 만든 앱을 시뮬레이터가 아닌 실제 단말기에서 구동하는 방식을 찾아보게 되면, 그 과정이 쉽지 않다는 것을 알 수 있습니다. 이 글에서는 내가 만든 앱을 기기에서 실행하는 과정에서 필요한 것들에 대해 알아보고자 합니다.

우선 iOS 기기에 자신이 만든 앱을 등록하는 과정이 어떤 것인지 대략적으로 이해하면 좋습니다.

1. 개발자는 애플로부터 iOS 기기에 앱을 설치할 수 있는 권한을 얻어야 합니다. 즉, 개발자는 애플에서 인증 받은 개발자가 되어야 합니다. 이 인증서를 통해 애플은 개발자를 식별할 수 있고, 앱 서명에 대한 권한을 얻을 수 있습니다.
2. 자신의 앱을 기기에 설치할 때, 기기에는 항상 만든 사람의 서명(signing)이 포함됩니다. 이 서명은 권한 정보가 포함되고, 애플에서 인증 받은 개발자만 앱을 기기에 설치할 수 있습니다.

아래에서는 위에서 설명한 과정에서 필요한 것들과 이들을 어떻게 만드는지 하나하나 알아보겠습니다.

## 애플에서 Certificate 발급 받기

앞서 언급한 것처럼 우리가 사용하는 iOS 기기에는 애플과 애플에서 인증한 개발자들이 만든 앱들만 설치할 수 있습니다. 일반 개발자는 애플 소속이 아니기 때문에 애플에서 요구하는 `애플에서 인증받은 개발자`가 되는 과정이 필요합니다. 이를 위해서 개발자는 애플에서 인증서(Certificate)를 받아야 합니다. 인증서를 받기 위해서는 맥에서 `CertSigningRequest(CSR)`을 생성하고 이를 애플에 제출해야 합니다.

### CertSigningRequest(CSR)

CSR 파일은 이름에서 알 수 있듯이 애플에 인증서를 요청하기 위한 파일입니다. 이 파일은 맥에 설치되어 있는 `KeyChainAccess(키체인 접근)`이라는 앱을 통해서 만들 수 있고, 그 과정은 다음과 같습니다.

> 키체인 접근 > 인증서 요청 > 인증 기관에서 인증서 요청

![csr1](https://dl.dropbox.com/s/dcepybw4qujsmeq/createCSR.png)

인증서 생성은 다음과 같은 작업을 수행합니다.

1. `CertificateSigningRequest.certSigningRequest`  파일 생성 - 애플에 등록할 인증 요청 파일입니다.
2. 인증서의 개인키와 공개키 생성 - 키체인 접근의 키 카테고리에를 확인하면, 인증서 생성시 등록한 `일반 이름` 항목으로 등록된 개인키와 공개키를 확인할 수 있습니다. 인증서를 주고 받고, 이를 사용하는 과정에서 [공개 키 암호 방식(비대칭 암호화) ](https://ko.wikipedia.org/wiki/%EA%B3%B5%EA%B0%9C_%ED%82%A4_%EC%95%94%ED%98%B8_%EB%B0%A9%EC%8B%9D) 방식을 사용합니다. 인증서를 애플로부터 발급 받고나서 그냥 사용하는 것이 아니라, 개인키가 반드시 필요하기 때문에 이 키는 잘 보관해야 합니다.

이렇게 CSR 파일을 생성 후, 애플 개발자 페이지에서 해당 CSR을 업로드하면 인증서(`myCertificate.cer` 형태)를 발급 받을 수 있습니다.

![csr2](https://dl.dropbox.com/s/8155k2ehxs2upwa/createCSR2.png)


이렇게 만든 인증서를 다운로드 후, 더블 클릭하면 인증서가 맥에 등록됩니다. 등록이 올바르게 되었는지 확인하기 위해서는 키체인 접근(`키체인 접근 > 키 카테고리 > 설정한 일반이름(개인키) > 등록한 인증서 확인`) 앱을 확인하면 됩니다.


# 기기로부터 신뢰 확보하기

위의 과정을 거치면 개발자는 `애플에서 인증 받은 개발자`가 되었다고 할 수 있습니다. 즉, 이제 개발자는 자신이 만든 앱에 서명할 때 애플의 인증 절차를 통과할 수 있습니다. 이제 `우리가 인증 받았다`라는 사실을 기기에 전달하기만 하면 되는데, 이를 위해 `Provisioning Profile`이 필요합니다.


## Provisioning Profile

애플에서 정의한 Provisioning Profile은 다음과 같습니다.

> provisioning profile is a type of system profile used to launch one or more apps on devices and use certain services.

[Provisioning profile](https://help.apple.com/xcode/mac/current/#￼/dev46a99ba04)

Provisioning Profile은 기기와 개발자 계정 사이를 연결하는 역할을 담당하는 profile입니다. 이 profile은 `myProfile.mobileProvision`의 형태의 파일입니다. Provisioning Profile에는 다음과 같은 것들이 들어갑니다.

![img1](https://dl.dropbox.com/s/nvvezw4tes2thrf/1%2A602qCx1Hyn_Ef7T1jrhS1w.png)

1. Certificate - 앞서서 만든 인증서가 Provisioning Profile에 들어갑니다.
2. App ID - 모든 iOS 앱은 앱 스토어에 등록되기 위해 Bundle Identifier 기반의 App ID가 필요합니다. 즉, App ID는 앱 스토어에서 사용되는 앱의 고유 ID라고 생각하면 됩니다.
3. Device - 모든 iOS 기기는 고유의 UDID(Unique Device Identifier)를 가지고 있고, 이 기기를 developer 사이트(멤버 센터)에 등록해두어야 테스트하려는 앱을 기기에 설치할 수 있습니다.


### Provisioning Profile 생성하기

`Provisioning Profile`은 Xcode에서 자동으로 생성되도록 할 수도 있고, 직접 developer 사이트에서 생성하고, import할 수도 있습니다. 직접 인증서를 모두 관리하는 환경에서는 Certificate, App ID, Device를 맞춰서 생성한 후 `Provisioning Profile`은 Xcode에서 관리하도록 하면 매우 편리합니다. 다만, `Provisioning Profile` 생성 과정에서 어딘가 꼬이는 상황이 발생할 수 있기 때문에 수동으로 `Provisioning Profile`을 생성하고 추가하는 방법도 알아두면 좋습니다.

* 수동으로 `Provisioning Profile` 생성하기

먼저 생성할 종류의 `Provisioning Profile`을 선택합니다.

![prov1](https://dl.dropbox.com/s/589b94dwof3vwmw/createProvision1.png)


다음으로 생성한 App ID를 선택합니다.

![prov2](https://dl.dropbox.com/s/mc9w6jy3rlco78c/createProvision2.png)

> App ID의 경우 위에서 별도로 생성 방식을 설명하지 않았지만, developer 사이트 > App ID 탭에서 필요한 서비스 선택 후 쉽게 생성할 수 있습니다.

그리고 연결할 Certificate를 선택합니다.

![prov3](https://dl.dropbox.com/s/pa0mogxwmu2u9eu/createProvision3.png)

이렇게 하면 `Provisioning Profile`을 생성할 수 있습니다.

> Device ID는 어디다가 포함시키는지 의아할 수 있습니다. 이는 App ID처럼 developer 사이트 > Device에서 등록할 수 있습니다. UDID는 기기를 맥에 연결한 후, itunes의 기기 정보에서 확인할 수 있습니다.

생성한 과정에서 몇 가지 알 수 있는 점이 있습니다.

* `Provisioning Profile`은 App ID마다 1개씩 생성할 수 있습니다.
* 기기의 UDID를 한 번 등록하면, 하나의 계정에서 여러 개의 앱을 만들 때, 별도의 등록 과정은 필요 없습니다.
* 개발 인증서와 배포 인증서가 나뉘어 있듯이 Provisioning Profile도 개발, 배포용이 나뉘어 있습니다.(유료 등록자가 아니면 배포용은 모두 만들 수 없습니다.)

## 앱 빌드와 기기에서 앱 실행시 동작 과정

이제 앞서서 언급한 2가지 조건(인증 받은 개발자, 기기에 인증 내용 전달)을 충족하였으므로 기기에 앱을 빌드할 수 있습니다. 빌드시 어떤 파일들이 생겨나는지 살펴보기 위해 커맨드 라인을 통해 앱을 빌드합니다.

```
$ xcodebuild -project myProject.xcodeproj
```

빌드를 진행하고, 성공적으로 완료되면 `build` 디렉토리가 생성됩니다. 여기서,

> build > Release-iPhoneOS > myProject

경로로 이동하고, myProject 파일을 오른쪽 클릭하여 패키지 내용 보기로 열어줍니다. 그러면 그 안에는 다음과 유사한 파일들이 있습니다.

![build](https://dl.dropbox.com/s/2zukk7yuqd1qm5y/build.png)

이 중에서 인증과 설치 허가와 관련된 것은 `_CodeSignature`와 `embedded.mobileProvision`입니다.

`_CodeSignature` 디렉토리에는 `CodeResources`라는 파일이 담겨 있고, 이는 코드 서명자(개발자)의 코드 서명이 담긴 해시 값이 담겨 있습니다. 이 해시 값은 iOS 시스템 내의 코드 서명 소프트웨어가 만들어낸 해시 값과 비교를 통해 코드 서명 시점으로부터 코드에 변경사항이 있는지 체크하는 방식으로 인증 절차를 수행합니다.
`embedded.mobileProvision`은 빌드시 사용된 `Provisioning Profile`의 복사본으로 애플의 서명을 확인하는 용도로 사용됩니다. 즉, `Provisioning Profile`은 컴파일, 설치, 그리고 실행 3단계에서 체크됩니다.

---

# 참고 자료

* [iOS 인증서와 코드 사이닝 이해하기](http://la-stranger.blogspot.com/2014/04/ios.html)
* [What is a provisioning profile & code signing in iOS?](https://medium.com/@abhimuralidharan/what-is-a-provisioning-profile-in-ios-77987a7c54c2)

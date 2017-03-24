---
layout: post
comments: true
title:  "iOS fastlane 스냅샷"
excerpt: "iOS에서 fastlane의 스냅샷 기능을 활용하여 디바이스별 스크린샷을 찍는 방법에 대해 알아봅니다."
categories: iOS UITest Fastlane
date:   2017-03-16 00:30:00
tags: [iOS, UITest, Fastlane]
image:
  feature: fastlane.png
---

## Fastlane의 필요성

iOS에서 앱을 배포하기 위해서는 기본적으로 앱의 모든 페이지에 대한 스크린샷을 찍어야 합니다. 앱을 Universal Setting으로 두고 배포를 하려고 할 경우 최소 5가지 화면에 대한 UI 스크린샷이 필요합니다.(iPhone 7, iPhone7 Plus, iPhone SE, iPad Retina, iPad Pro) 그런데 여기다가 디바이스 언어별로 앱스토어에서 다른 스크린샷이 보이길 원할 경우 언어별로 똑같은 스크린샷을 찍어야 합니다. 정리하자면,

<div class="message">
앱 모든 화면 개수 x 디바이스 5개 x 지원하는 언어 = 총 필요한 스크린샷 개수
</div>

다음과 같이 됩니다. 예를 들어 아이폰, 아이패드를 지원하고 한국어, 영어를 지원하는 앱의 경우 앱의 화면을 4개로 가정하면, 4x5x2 = 40개의 스크린샷이 필요합니다. 기본적으로 이 화면은 어떻게 찍을까요?

### 노가다

네, 말 그대로 시뮬레이터를 바꿔가면서 노가다를 해야합니다. 각 시뮬레이터를 켜면서


<figure class="animated_gif_frame" data-caption="GIF (2MB)">
  <img class="animated_gif" src="https://dl.dropboxusercontent.com/s/rmpcoi2cmvky85p/EAF4E0DD-C36F-4E0C-A12B-744E4B97D4A9-786-0000015E0F6EE379.gif" data-source="https://dl.dropboxusercontent.com/s/rmpcoi2cmvky85p/EAF4E0DD-C36F-4E0C-A12B-744E4B97D4A9-786-0000015E0F6EE379.gif" width="800" height="450">
  <figcaption>Click to play</figcaption>
</figure>

func testSnapshot() {

        let app = XCUIApplication()

        snapshot("1-Main")
        app.tables/*@START_MENU_TOKEN@*/.staticTexts["10 minutes Challange"]/*[[".cells.staticTexts[\"10 minutes Challange\"]",".staticTexts[\"10 minutes Challange\"]"],[[[-1,1],[-1,0]]],[0]]@END_MENU_TOKEN@*/.tap()

        snapshot("2-Circuit")
        app.navigationBars["CircuitWatch.CircuitVC"].children(matching: .button).matching(identifier: "Back").element(boundBy: 0).tap()

        let circuitwatchMainvcNavigationBar = app.navigationBars["CircuitWatch.MainVC"]
        circuitwatchMainvcNavigationBar.buttons["Add"].tap()

        snapshot("3-AddCircuit")
        app.navigationBars["CircuitWatch.AddCircuitVC"].children(matching: .button).matching(identifier: "Back").element(boundBy: 0).tap()
        circuitwatchMainvcNavigationBar.buttons["Edit"].tap()

        snapshot("4-MainEdit")
        circuitwatchMainvcNavigationBar.buttons["Done"].tap()

    }


## Trouble Shooting

fastlane snapshot reset_simulators

chmod 755 ~/Library/Preferences/

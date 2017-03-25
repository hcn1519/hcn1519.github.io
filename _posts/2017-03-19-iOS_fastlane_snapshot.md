---
layout: post
comments: true
title:  "iOS fastlane 스냅샷"
excerpt: "iOS에서 fastlane의 스냅샷 기능을 활용하여 디바이스별 스크린샷을 찍는 방법에 대해 알아봅니다."
categories: iOS UITest Fastlane
date:   2017-03-19 00:30:00
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
  <img class="animated_gif" src="https://dl.dropboxusercontent.com/s/10zogh25lzvi1gw/20A9F3A5-C2F1-4C06-AB66-87CD0BBEA107-786-0000075D1354DBCC.gif" data-source="https://dl.dropboxusercontent.com/s/10zogh25lzvi1gw/20A9F3A5-C2F1-4C06-AB66-87CD0BBEA107-786-0000075D1354DBCC.gif" width="100%" height="auto">
</figure>

한땀한땀 스크린샷을 찍어줘야 하는 것이죠. Fastlane snapshot은 이러한 지루하고 오래 걸리는 반복적인 과정을 자동화해주는 역할을 담당합니다. 테스트 결과 40장의 스크린샷도 컴퓨터만 켜놓으면 10분만에 찍어주는 퍼포먼스를 보여줍니다.

<img src="https://dl.dropbox.com/s/ymzuli6cx1hzekw/snapshotde.png">

## Fastlane snapshot 설치

Fastlane은 맥에 기본적으로 사용되는 ruby gem을 통해 설치됩니다.

{% highlight Bash shell scripts %}
sudo gem install fastlane
{% endhighlight %}

설치가 완료되면, 터미널에서 프로젝트 루트로 이동합니다. 그 후,

{% highlight Bash shell scripts %}
fastlane init
{% endhighlight %}

다음 명령어를 치게 되면, 3개의 파일(<code>snapfile</code>, <code>SnapshotHelper.swift</code>, <code>SnapshotHelper2-3.swift</code>)이 생성됩니다. 다음으로 스냅샷이 저장될 폴더를 생성합니다.

{% highlight Bash shell scripts %}
mkdir snapshots
{% endhighlight %}

## Fastlane Configuration

fastlane snapshot은 Xcode의 <code>UITest</code>라는 기능을 통해 작동합니다. 그러므로 UITest를 프로젝트에 추가하고 이에 대한 설정을 해주어야 올바르게 작동합니다.먼저 프로젝트에 <code>UITest</code>를 추가하도록 하겠습니다. 최상단 메뉴바에서 <code>File > New > Target</code>을 선택합니다. 다음으로, <code>UITestBundle</code>을 프로젝트에 추가합니다. 이렇게 하면 <code>ProjectNameUITests</code> 형태로 폴더가 생성됩니다.

<img src="https://dl.dropbox.com/s/asyjzz23c6zl70x/target.png">

다음으로 이전에 생성했던 <code>SnapshotHelper.swift</code>을 새롭게 생성된 <code>ProjectNameUITests</code>로 넣어줍니다. 그리고 폴더 안에 있는 <code>ProjectNameUITests.swift</code>의 코드를 변경합니다.

{% highlight swift %}
// ProjectNameUITests.swift
import XCTest
class ProjectNameUITests: XCTestCase {
  override func setUp() {
     super.setUp()
     continueAfterFailure = false
     let app = XCUIApplication()
     setupSnapshot(app)
     app.launch()
 }

 override func tearDown() {
     super.tearDown()
 }
 func testSnapshot() {
 }
}
{% endhighlight %}

다음으로 <code>snapfile</code>에 대한 설정입니다. <code>snapfile</code>은 fastlane snapshot을 사용할 때 설정할 수 있는 옵션들을 지정하는 파일입니다. 여기서, 스크린샷을 찍을 기기 설정, 언어 설정, 결과물 저장 경로 설정 등을 할 수 있습니다. 에디터를 통해 snapfile을 열고, 내용을 다음과 같이 수정하겠습니다.

{% highlight swift %}
// snapfile
// 스냅샷을 찍을 디바이스 리스트
devices([
  "iPhone 7",
  "iPhone 7 Plus",
  "iPhone SE",
  "iPad Retina",
  "iPad Pro (12.9-inch)"
])

// 언어 설정
languages([
 "en-US",
 "ko"
])
// 타겟 프로젝트
project "./CircuitWatch.xcodeproj"
// 스냅샷 저장 경로
output_directory './snapshots'
// 새로 스냅샷을 찍을 경우 기존에 폴더에 있던 사진 모두 삭제
clear_previous_screenshots true
{% endhighlight %}

## Fastlane with UITests

<code>UITests</code>는 말 그대로 UI들이 제대로 작동하는지를 테스트할 수 있게 도와주는 툴입니다. fastlane snapshots은 <code>UITests</code>를 통해 작동하는데 구체적으로 어떻게 하는지에 대해 알아보겠습니다. 먼저 Xcode에서 <code>ProjectNameUITests.swift</code>으로 이동합니다. 그리고 <code>커서</code>를 <code>testSnapshot()</code> 안으로 넣어둡니다. 그리고 밑에 보이는 빨간 버튼(레코드 버튼)을 누르게 되면, <code>UITests</code>가 구동되면서 시뮬레이터가 켜집니다. 그리고 켜진 시뮬레이터에서 버튼을 누르거나 하는 액션을 취하면 놀랍게도, 실시간으로 코드가 생성됩니다.

<figure class="animated_gif_frame" data-caption="GIF (2MB)">
  <img class="animated_gif" src="https://dl.dropboxusercontent.com/s/c4l55l2nhxkt4yv/5CE7B06E-28C6-43C0-8690-70237BCBF3FC-786-0000058543E86FAC.gif" data-source="https://dl.dropboxusercontent.com/s/c4l55l2nhxkt4yv/5CE7B06E-28C6-43C0-8690-70237BCBF3FC-786-0000058543E86FAC.gif" width="100%" height="auto">
</figure>

이 방식을 사용해서 스크린샷을 찍을 화면이 모두 나오도록 액션을 생성합니다. 다음으로 snapshot을 찍을 구간에 <code>snapshot("main")</code> 다음과 같이 snapshot 이름을 설정하여 코드를 집어넣습니다. 예시로

{% highlight swift %}
circuitwatchMainvcNavigationBar.buttons["Edit"].tap()
snapshot("EditPage")
circuitwatchMainvcNavigationBar.buttons["Done"].tap()
{% endhighlight %}

다음과 같은 경우에는, 앱에서 Edit 버튼을 누르고, EditPage라는 스크린샷을 촬영한 후 Done 버튼을 누르는 과정입니다. 이런 방식으로 스크린샷이 필요한 구간에 적절히 snapshot 문구를 넣어주면 스크린샷이 올바르게 찍히게 됩니다. 여기까지 하시면 fastlane snapshots을 구동할 수 있습니다. 한 번 돌려보겠습니다.

{% highlight Bash shell scripts %}
fastlane snapshot --stop_after_first_error
{% endhighlight %}

<img src="https://dl.dropbox.com/s/t1nxq4bj9x1u3b7/errorResult.png">

잘 되나요? 아마 위와 유사한 오류 메세지를 보게 될 것입니다. 결과가 다음과 같이 나오는 이유는 UITests에서 버튼들이 특정 언어에 한정되도록 설정되어 있기 때문입니다. 즉, 위에서 <code>"Edit"</code> 버튼은 한글 설정된 기기에서 <code>"편집"</code>으로 나올 경우 <code>UITests</code>가 같은 버튼으로 인식하지 못 하는 것입니다.

## Fastlane 언어 지원

위와 같은 문제로 인해, 코드를 언어에 관계없이 작동하도록 수정해주어야 합니다. 이 때 주로 활용되는 것이 <code>element(boundBy:)</code> 메소드입니다. <code>element(boundBy:)</code>는 여러 언어에 관계 없이 컴포넌트들이 인덱스를 통해 작동할 수 있도록 해줍니다. 버튼의 경우 아래 코드는 제가 실제로 사용했던 <code>UITests</code> 상의 코드입니다. 참고하시면 도움이 될 것이라 생각됩니다.

{% highlight swift %}
func testSnapshot() {

        let app = XCUIApplication()

        snapshot("1-Main")
        // 테이블의 첫 번째 셀 선택
        app.tables.cells.element(boundBy: 0).tap()

        snapshot("2-Circuit")
        // navigationBar에서 왼쪽 BarItem 클릭
        let backBtn = app.navigationBars["CircuitWatch.CircuitVC"].children(matching: .button).element(boundBy: 1)
        backBtn.tap()

        let circuitwatchMainvcNavigationBar = app.navigationBars["CircuitWatch.MainVC"]
        // navigationBar에서 오른쪽 BarItem 클릭
        circuitwatchMainvcNavigationBar.buttons.element(boundBy: 1).tap()

        snapshot("3-AddCircuit")
        let addBackBtn = app.navigationBars["CircuitWatch.AddCircuitVC"].children(matching: .button).element(boundBy: 1)
        addBackBtn.tap()

        let editBtn = app.navigationBars["CircuitWatch.MainVC"].buttons.element(boundBy: 0)
        editBtn.tap()
        snapshot("4-MainEdit")

        editBtn.tap()

    }
{% endhighlight %}

자 이제, 모든 설정이 끝났습니다. fastlane snapshot을 다시 구동해보겠습니다.

{% highlight Bash shell scripts %}
fastlane snapshot
{% endhighlight %}

결과 이미지는 다음과 같습니다.

<img src="https://dl.dropbox.com/s/m9li2qrbis6qozh/fastlaneResultTerminal.png">

이렇게 나오고, fastlane은 이미지가 모두 포함된 HTML 파일도 생성해줍니다.

<img src="https://dl.dropbox.com/s/dz5ykw2g64n04pz/fastlaneResulthtml.png">

## Trouble Shooting

과정을 잘 따라왔음에도 불구하고 안되는 경우가 있을 수 있습니다. 혹시나 다음과 같은 <code>Exit status: 1 Caught error... 1</code> 에러를 맞닥뜨린 분은 다음 명령어를 치고 다시 돌려보세요.

{% highlight Bash shell scripts %}
chmod 755 ~/Library/Preferences/
fastlane snapshot reset_simulators
{% endhighlight %}

## 더 볼만한 자료
* [FastLane Snapshot으로 배포용 스크린샷 자동으로 만들기 - iOS Tech Talk](https://realm.io/kr/news/automate-ios-screenshots-with-fastlane-snapshot/)
* [code tutsplus 자료](https://code.tutsplus.com/tutorials/how-to-automate-screenshots-with-fastlane--cms-26151)

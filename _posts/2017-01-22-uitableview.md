---
layout: post
comments: true
title:  "iOS UITableView 기초"
excerpt: "iOS의 UITableView에 대해 알아봅니다."
categories: iOS UIKit UITableView
date:   2017-01-22 00:30:00
tags: [iOS, UIKit, UITableView]
image:
  feature: iOS10.png
---

#### tableView의 기본 구조

iOS에서 UITabelView는 계층적으로 무언가를 보여줄 때 주로 사용합니다. 간단한 예를 들면 아이폰의 설정창입니다.

<img src="https://dl.dropbox.com/s/daap53vpn7elgo8/basictable.png">

tableView는 무조건 **1개의 column** 으로 구성되고, 위아래 스크롤만 할 수 있습니다. 그리고 table을 구성하는 요소로 **section** 과 **row** 가 있습니다.

<img src="https://dl.dropbox.com/s/w5dbga4sow9vx8p/tableviewBasic.png">

이미지 출처 : <a href="https://www.ralfebert.de/tutorials/ios-swift-uitableviewcontroller">
https://www.ralfebert.de/tutorials/ios-swift-uitableviewcontroller
</a>

**section** 과 **row** 는 위 그림을 보시면 쉽게 파악하실 수 있습니다. **Section** 이 여러 **row** 를 포함하는 구조를 가지고 있는 것이죠. 물론 section이 1개만 있고 여러 개의 rows만 있는 경우도 매우 많습니다. 몇 가지 예제를 더 살펴보자면,

<img src="https://dl.dropbox.com/s/93ifocbudi9aanj/types_of_table_views.jpg">


위 그림에서 첫 번째 예시에는 section이 없고, row만 있는 것을 확인하실 수 있습니다.

#### 필수 메소드

{% highlight swift %}
  // 실제 셀에 데이터를 반환하는 메소드, (필수)
  func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {

      let cell = tableView.dequeueReusableCell(withIdentifier: "lottoCell", for: indexPath as IndexPath) as! LottoCell
      let row: Int = indexPath.row

      cell.nameOfOutlet.text = "Hello world"

      return cell
  }

  // 해당 테이블에 섹션이 몇 개가 있는지?, (필수)
  func numberOfSections(in tableView: UITableView) -> Int {
      return 1
  }

  // 행의 개수(세로로 나열되는)
  func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
      return lottoNumbers.count
  }
{% endhighlight %}

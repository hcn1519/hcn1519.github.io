---
layout: post
title: "네트워크 기본 정리"
excerpt: "네트워크 강의 정리 2"
categories: Network ApplicationLayer HTTP
tags: [Network, ApplicationLayer, HTTP, Cookie, WebCache]
date: "2018-03-17 23:24:00 +0900"
---

> 본 내용은 kocw의 한양대학교 이석복 교수님 강의인 [컴퓨터 네트워크](http://www.kocw.net/home/search/kemView.do?kemId=1223614)를 듣고 정리한 내용입니다.

## Application Layer

`Application Layer`는 OSI 7계층 중 사용자가 인터넷을 사용하면서 실제 체감할 수 있는 서비스를 제공합니다. 여기서 말하는 서비스를 제공한다는 것은 특정 프로토콜을 지원한다는 의미로 이해하면 되는데, `Application Layer`에서 제공하는 가장 대표적인 프로토콜이 `HTTP` 프로토콜입니다.

### HTTP

<div class="message">
  HTTP - Hypertext Transfer Protocol, 하이퍼텍스트를 전송하는 프로토콜
</div>

* `HTTP`의 메세지는 요청(request)과 응답(response)으로 이뤄져 있다.

`HTTP`는 매우 단순한 프로토콜로 클라이언트의 요청과 서버의 응답으로 이뤄진 프로토콜입니다. 예를 들어 어떤 모바일 앱이 클라이언트고 모바일 앱에 정보를 제공하는 서버가 있다고 할 때, 클라이언트는 서버로부터 정보를 받아오기 위해 `GET`이든 `POST`든 어떤 요청을 서버쪽으로 전송합니다. 여기서 요청을 수행하는 방법은 URL을 접속하는 형태로 이뤄집니다. 그리고 서버는 클라이언트의 요청에 따른 응답을 클라이언트쪽으로 전달합니다.

* `HTTP`는 상태가 없다(stateless).

`HTTP`에서 클라이언트와 서버는 서로 지속적으로 연결되어 있는 상태가 아닙니다. `HTTP`에서는 데이터를 보내고 받는 순간에만 연결되기 때문에 `HTTP`는 상태가 없다고 얘기합니다. 즉, 클라이언트 측에서 앱 UI를 업데이트한다고 했을 때, `HTTP` 프로토콜을 사용하면 실시간으로 서버로부터 정보를 받아서 업데이트하는 것은 `HTTP`가 아닌 다른 프로토콜을 사용해야 합니다.

### Cookie

이러한 HTTP의 상태가 없는 속성은 효율적으로 네트워크 자원을 활용하는 장점도 있지만, 서버의 클라이언트에 대한 정보가 부족하다는 단점도 있습니다. 그래서 이를 보완하기 위해 브라우저는 `Cookie`라는 저장공간을 지원합니다.

<div class="message">
  An HTTP cookie (also called web cookie, Internet cookie, browser cookie, or simply cookie) is a small piece of data sent from a website and stored on the user's computer by the user's web browser while the user is browsing. Cookies were designed to be a reliable mechanism for websites to remember stateful information (such as items added in the shopping cart in an online store) or to record the user's browsing activity (including clicking particular buttons, logging in, or recording which pages were visited in the past).
</div>
출처: [HTTP Cookie - wikipedia](https://en.wikipedia.org/wiki/Circuit_switching)

쿠키를 활용되는 과정은 다음과 같습니다. 아래 과정은 일반 인터넷 사용자가 아마존 서버에 접속할 때의 상황을 서술합니다.

1. 사용자가 처음 아마존 서버에 접속하면 쿠키에는 아마존 관련 정보가 하나도 없기 때문에 사용자는 쿠키 데이터 없이 클라이언트는 아마존 서버에 요청을 보냅니다.
2. 이 때 아마존 서버는 클라이언트측 요청에 쿠키 관련 정보가 없는 것을 확인하고, 응답에 쿠키 번호를 함께 보냅니다.
3. 클라이언트에 있는 웹브라우저는 이 쿠키를 클라이언트 컴퓨터에 저장합니다.
4. 시간이 지나서 다음번에 클라이언트가 아마존 서버에 요청을 보내게 되었습니다. 이 때 웹브라우저는 아마존 서버에 대한 쿠키를 가지고 있기 때문에 쿠키번호를 요청에 같이 보냅니다.
5. 아마존 서버는 해당 쿠키번호와 클라이언트의 접속기록을 조합하여 사용자가 좋아할 법한 내용을 응답 html에 포함시켜서 전송합니다.

쿠키는 서버가 클라이언트의 특징을 파악하는데 도움을 주지만, 쿠키 데이터가 컴퓨터에 과도하게 쌓이게 되면 웹 브라우징 성능 저하의 원인이 됩니다. 그렇기 때문에 웹 브라우저 성능 개선을 위해 주로 삭제하는 데이터이기도 합니다.

### Web Caches(프록시 서버)

-----

## 참고자료
* [컴퓨터 네트워크](http://www.kocw.net/home/search/kemView.do?kemId=1223614)
* [HTTP Cookie - wikipedia](https://en.wikipedia.org/wiki/Circuit_switching)

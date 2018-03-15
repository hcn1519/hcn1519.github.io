---
layout: post
title: "네트워크 기본 정리"
excerpt: "네트워크 강의를 정리하는 글입니다."
categories: Network 패킷스위칭
tags: [Network, PacketSwitching, CircuitSwitching]
date: "2018-03-15 20:54:59 +0900"
---

> 본 내용은 kocw의 한양대학교 이석복 교수님 강의인 [컴퓨터 네트워크](http://www.kocw.net/home/search/kemView.do?kemId=1223614)를 듣고 정리한 내용입니다.

<div class="message">
  Protocol - 서로 다른 개체가 의사소통을 하기 위해 공유하는 룰, 규약
</div>

## Circuit Switching

<div class="message">
  Circuit switching is a method of implementing a telecommunications network in which two network nodes establish a dedicated communications channel (circuit) through the network before the nodes may communicate. The circuit guarantees the full bandwidth of the channel and remains connected for the duration of the communication session.
</div>
출처: [Circuit Switching - wikipedia](https://en.wikipedia.org/wiki/Circuit_switching)

Circuit Switching은 통신 방법 중 두개의 노드가 서로 통신을 예약해두고 정해진 회선을 사용하는 형태로 데이터를 교환하는 방법입니다. 일반적으로 유선전화 같은 것이 이와 같은 통신 방법을 사용합니다.

## Packet Switching

<div class="message">
  Packet switching is a method of grouping data transmitted over a digital network into packets which are composed of a header and a payload. Data in the header is used by networking hardware to direct the packet to its destination where the payload is extracted and used by application software. Packet switching is the primary basis for data communications in computer networks worldwide.
</div>
출처: [Packet Switching - wikipedia](https://en.wikipedia.org/wiki/Packet_switching)

`Packet Switching`은 인터넷에서 일반적으로 사용하는 데이터 통신 방식입니다. 이 통신 방식은 데이터를 패킷이라는 형태로 전송하고 회선끼리 통신을 예약하는 방식을 사용하는 것이 아니라, 서로 다른 노드가 섞여서 통신을 하는 형태를 지닙니다.

인터넷이 이러한 `Packet Switching` 통신 형태를 사용하는 이유는 사용자가 인터넷을 사용하는 패턴을 생각해보면 알 수 있습니다. 클라이언트는 일반적으로 서버와 지속적으로 통신을 유지하는 형태로 데이터를 주고받지 않고, 한 번 주고 받고 파일이 로딩되고 나면 그 화면에 꽤 오래 머무는 형태로 데이터를 주고 받습니다. 그렇기 때문에 지속적으로 통신할 것을 예약하는 것은 사실 손해이기 때문에 인터넷에서는 `Packet Switching` 방식으로 통신을 합니다. 또한 인터넷은 많은 클라이언트가 서버 컴퓨터쪽으로 접속하는 형태로 진행되기 때문에 서버가 여러 클라이언트의 요청을 받을 수 있어야 하는데 이 또한 인터넷이 `Packet Switching`을 채택하는 이유이기도 합니다.

### Packet Switching 문제점

`Packet Switching`은 통신 속도에 있어서 문제가 발생합니다. 대표적인 예로 사용자가 지원하는 `bandwidth`보다 더 많이 접속할 경우(회선 전달 속도보다 더 많은 데이터를 전송해야 할 경우) 통신속도가 느려집니다.

> Note: Bandwidth is also defined as the amount of data that can be transmitted in a fixed amount of time.

이와 같이 통신 속도가 느려지는 현상을 세분화해서 나눠보면 다음과 같이 구분할 수 있습니다.

#### Packet Switching delay

1. Processing delay - 최종 목적지에 따라 클라이언트에서 어디로 보낼지 파악할 때
2. Queueing delay - 다른 패킷이 이미 라우터의 큐에 등록되어 있어서 기다려야 하는 경우
3. Transmission delay - 내 패킷이 링크까지 이동하는데 시간
4. Propagation delay - 마지막 비트가 다음 라우터까지 가는데 걸리는 실제 물리시간(빛의 속도에 의존)

따라서 통신에서 발생하는 지연시간은 다음과 같습니다.

> Total Delay = (proc + queue + trans + prop) Delay

이러한 지연시간을 넓히기 위해서는 각각 다음과 같은 방식을 활용할 수 있습니다.

1. Processing Delay - 더 좋은 라우터를 사용한다.(고속도로에서 하이패스가 생겨 차가 더 빠르게 통행할 수 있는 원리와 같습니다.)
2. Transmission Delay - 대역폭(bandwidth)을 넓힌다(차선을 넓힌다)
3. Queueing Delay - 큐의 대기시간을 줄이는 것은 어렵다. 한마디로 추석에는 고속도로 차선이 넓고, 하이패스가 잘 되어 있어도 차가 막힌다. 즉 Queueing Delay는 군중의 행동패턴에 의존하기 때문에 줄이는 것이 어렵다. 많이 몰리면 답이 없다.
4. Propagation Delay - 빛의 속도에 의존하기 떄문에 줄이기 어렵다.

#### Packet Loss(패킷 유실)

패킷 유실은 라우터의 큐에 들어갈 공간이 없어서 패킷이 유실되는 문제입니다. 이 문제를 해결하기 위해 TCP는 유실된 패킷을 파악하여 다시 서버로 유실된 패킷을 전송합니다. 이 때 유실된 패킷을 담당하는 것은 클라이언트 측 TCP입니다. 중간에 거치는 라우터에서 유실된 패킷을 재전송할 수도 있지만, 중간에 있는 라우터는 일반적으로 단순 작업에 최적화되어 있습니다. 즉, 라우터는 단순 데이터 전송 성능이 좋도록 설계가 되어 있어 전체 네트워크 레이어에서 IP 계층까지만 알고 있습니다. 그래서 유실된 패킷은 모두 클라이언트 측 TCP가 재전송을 담당합니다.


-----

## 참고자료
* [컴퓨터 네트워크](http://www.kocw.net/home/search/kemView.do?kemId=1223614)
* [Packet Switching - wikipedia](https://en.wikipedia.org/wiki/Packet_switching)

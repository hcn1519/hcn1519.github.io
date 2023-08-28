---
layout: post
comments: true
title:  "OOP - Class와 Object"
excerpt: "Java를 통해 Class와 Object에 대해 알아봅니다."
categories: Java OOP Class
date:   2017-01-24 00:30:00
tags: [Java, OOP, Class]
---

## Class와 Object

Class는 하나의 **데이터 타입** 입니다. 즉, Class는 배열처럼 하나의 데이터를 저장하는 공간인 것이죠. Object는 Class에서 생성되는 하나의 **데이터** 입니다. 조금 더 자세하게 알아보기 위해 Class와 Object에 대한 추가적인 자료를 덧붙입니다.

* Object - Object는 *상태* 와 *행동* 을 지니고 있습니다. 예를 들어 개의 경우 색깔, 이름, 종 등의 *상태* 를 꼬리 흔들기, 짖기, 먹기 등의 *행동* 을 가지고 있습니다.(Instance와 Object는 *거의* 동의어로 사용됩니다.)
* Class - Class는 해당 유형의 Object가 지원하는 *상태* 와 *행동* 을 설명하는 템플릿입니다.

출처: <a href="https://www.tutorialspoint.com/java/java_object_classes.html">Java tutorialspoint - Class and Object</a>

예제를 통해서 조금 더 자세히 알아보겠습니다.

{% highlight java %}
class Location{
  // 멤버변수
  private double latitude;
  private double longitude;
  // constructor
  public Location(double latitude, double longitude){
    this.latitude = latitude;
    this.longitude = longitude;
  }
  // 메소드
  public double address(){
    return latitude * longitude;
  }
}
public class Main {
  public static void main(String[] args){
    // object 생성
    Location myPlace = new Location(38, 129);
  }
}
{% endhighlight %}

위의 예제는 <code>Location</code>이라는 **Class** 를 보여주고 있습니다. Location Class는 Location의 속성을 지닌 Object들이 어떤 속성을 지닐 수 있는지를 설명해줍니다. 여기서는 latitude, longitude(위도, 경도)의 멤버변수와 address 메소드를 Location Object가 지닐 수 있는 것을 Class가 보여주고 있습니다.

위에서 실제 Object는

{% highlight java %}
Location myPlace = new Location(38, 129);
{% endhighlight %}

다음을 통해서 생성됩니다. 생성된 **myPlace** 는 Location Class에서 서술된 속성을 지니고 있습니다. Object 생성은 객체 생성, 인스턴스 생성으로 부르기도 합니다.

>내용 출처 : Coursera, Object Oriented Programming in Java by University of California, San Diego

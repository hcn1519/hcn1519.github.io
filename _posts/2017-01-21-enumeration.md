---
layout: post
comments: true
title:  "Enumeration 개념"
excerpt: "Enumeration에 대해 알아봅니다."
categories: java swift
date:   2017-01-21 00:30:00
tags: [Java, Swift, Language]
---

#### 1. Java Enumeration

Java에서 상수 집합을 정의하기 위해서 **enum** 이라는 것을 사용합니다. 상수라는 것은 고유한 요소로 프로그램이 돌아갈 때 바뀌지 않는 변수로 이해하면 됩니다.(상"수"라고 숫자가 아닙니다.) 하나의 변수 혹은 클래스가 정의한 순간 이후로 바뀌지 않도록 하기 위해 **final** 이라는 것을 사용합니다. 아래의 경우 **Month** class는 각각의 월을 상수로 사용하기 위해 만들어진 클래스입니다.

{% highlight java %}
class Month{  
    public static final Month Jan = new Month();
    public static final Month Feb = new Month();
    public static final Month Mar = new Month();
}
{% endhighlight %}

보시면 **public static final Month** 이라는 문구가 반복적으로 쓰여 있는 것을 확인할 수 있습니다. 이것이 비효율적이라고 생각되어 나온 것이 **Enumeration** 입니다. enum은 앞서 언급한 것처럼 상수를 열거한 집합입니다.

{% highlight java %}
enum Day{
    MONDAY,TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY;
}
public class EnumEx {
    public static void main(String[] args) {

        Day myDay = Day.MONDAY;

        switch (myDay) {
            case MONDAY:
                System.out.println("월요일입니다.");
                break;
            case TUESDAY:
                System.out.println("화요일입니다.");
                break;
            case WEDNESDAY:
                System.out.println("수요일입니다.");
                break;
        }
    }
}
{% endhighlight %}

위의 예제에서 볼 수 있듯이 enum은 상수의 변하지 않는 속성 때문에 switch문에서 많이 사용합니다.

<a href="http://www.nextree.co.kr/p11686/">원문 출처: nextree</a>

#### 2. Swift switch문

Swift에도 switch문이 있습니다. 기본 용법을 보면 다음과 같습니다.

{% highlight swift %}
let vegetable = "red pepper"
switch vegetable {
  case "celery":
      print("Add some raisins and make ants on a log.")
  case "cucumber", "watercress":
      print("That would make a good tea sandwich.")
  case let x where x.hasSuffix("pepper"):
      print("Is it a spicy \(x)?")
  default:
      print("Everything tastes good in soup.")
}
{% endhighlight %}

Java의 switch문과 다른 점이 크게 2가지 있습니다.

1. switch문에 **break** 가 없다.(있어도 상관없습니다.)
2. case 조건문에서 임시 변수를 선언해서 조건문 안으로 보낼 수 있다.

{% highlight swift %}
let vegetable = "red pepper"
switch vegetable {
  case let x where x.hasSuffix("pepper"):
      print("Is it a spicy \(x)?")
  default:
      print("Everything tastes good in soup.")
}

let myString: String! = "Swift Programming"
if x = myString {
    print("\(x)은 재미있어요.")
}
{% endhighlight %}

<code>case let</code> 용법을 통해서 switch문에서 구문 안으로 임시 변수를 넣을 수 있습니다. Optional 타입의 <code>if let</code> 구문과 유사한 것 같네요.

#### 3. Swift Enumeration

{% highlight swift %}
enum Day{
    case MONDAY,TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

var myDay = Day.MONDAY
switch myDay {
    case Day.MONDAY:
        print("월요일입니다.") // 출력 됩니다.
    case Day.TUESDAY:
        print("화요일입니다.")
    case Day.WEDNESDAY:
        print("수요일입니다.")
    default:
        print("요일이 아닙니다.")
}
{% endhighlight %}

Enumeration 개념은 Java나 Swift 모두 비슷한 것 같네요. 다른 예제를 봐보겠습니다.

{% highlight swift %}
enum Rank: Int {
    case ace = 1
    case two, three, four, five, six, seven, eight, nine, ten
    case jack, queen, king

    func simpleDescription() -> String {
        switch self {
        case .ace:
            return "ace"
        case .jack:
            return "jack"
        case .queen:
            return "queen"
        case .king:
            return "king"
        default:
            return String(self.rawValue)
        }
    }
}
let ace = Rank.ace // 결과 : "ace"
let aceRawValue = ace.rawValue // 결과 : "1"
let aceDescription = ace.simpleDescription // 결과 : "ace"
{% endhighlight %}

이 경우 ace는 int 1로 선언됩니다. 기타 two, three 등은 "two", "three"의 String으로 초기화 됩니다. 흥미로운 점은 <code>simpleDescription</code> 함수에 있습니다. 여기서 simpleDescription은 switch문을 호출합니다. 이 때 넘기는 인자는 <code>self</code>로 <code>Rank</code> 자신입니다. Swift는 이런 경우 축약형을 쓰는 것을 허용합니다. 즉, <code>case .ace:</code>만 써도 이를 <code>self.ace</code>로 인식하여 올바른 결과를 출력할 수 있게 해준다는 것입니다. 또한 다음과 같은 것도 가능합니다.

{% highlight swift %}
enum Rank: Int {
    case jack, queen, king
}
var x = Rank.jack // x = "jack"
var x = .queen // x = "queen"
var x = .king// x = "king"
{% endhighlight %}

한 번 enum을 선언했던 변수에는 enum 객체 명(<code>Rank</code>)을 생략해도 올바른 결과가 나옵니다.

> 내용 출처 : The swift Programming Language(3.0.1), nextree - Java: enum의 뿌리를 찾아서...

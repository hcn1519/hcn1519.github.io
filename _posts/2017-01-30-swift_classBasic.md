---
layout: post
comments: true
title:  "Swift Class 기본"
excerpt: "Swift의 Class에서 쓰이는 constructor, getter, setter에 대해 알아봅니다."
categories: Swift Language OOP
date:   2017-01-30 00:30:00
tags: [Swift, Language, OOP]
image:
  feature: swiftLogo.jpg
---

객체지향 개념을 가지고 있는 언어들은 대부분 <code>class</code>와 <code>object</code>를 가지고 있습니다. Swift도 class 개념을 가지고 있으며, class 구성의 기본인 <code>constructor, getter, setter</code> 개념을 지니고 있습니다. 간단하게 이를 알아보도록 하겠습니다.

#### 1. Constructor(생성자)

{% highlight swift %}
class Rectangle {
    private var _width: Double!
    private var _height: Double!

    init(width: Double, height: Double){
        self._width = width
        self._height = height
    }
}
var r1 = Rectangle(width: 10, height: 20)
var r1 = Rectangle() // default 생성자가 없으므로 error
{% endhighlight %}

<code>Constructor</code>는 처음 Class를 생성할 때, 새로운 object를 만드는 메소드입니다. 즉, Class가 가진 멤버변수를 Class 생성과 함께 초기화하는 역할을 합니다. Swift에서는 이를 <code>init</code> 메소드로 호출하고, <code>self</code>를 통해서 object를 호출합니다. 여기서 object를 호출한다는 것의 의미는 생성된 object를 가져와서 멤버변수의 값을 설정하거나, 메소드에 활용하는 데 사용하는 것을 의미합니다. <code>self</code> 키워드는 자신이 속한 object의 주소값을 저장합니다.(<code>self</code>가 object를 reference한다고 표현하기도 합니다.)

{% highlight swift %}
var r1 = Rectangle(width: 10, height: 20)
{% endhighlight %}

즉, 다음과 같이 생성자를 사용할 때, r1 object를 우선적으로 만들고, 다음으로 constructor가 호출되어 생성된 r1을 불러와 r1의 멤버변수인 <code>_width</code>, <code>_height</code>을 설정하는 것입니다.<!--_-->

#### 2. getter & setter

getter와 setter는 class의 <code>private</code>로 감싸진 멤버변수를 설정하기 위해 주로 사용됩니다. 저는 처음 getter와 setter를 java로 배웠는데, Swift가 getter & setter의 코드 가독성 부분을 많이 보완했다고 생각합니다. 무슨 의미인지 아래 예제를 들어보겠습니다.

##### Java getter & setter

{% highlight java %}
class Rectangle {
    private double _width;

    // getter
    public double getWidth(){
      return _width;
    }
    // setter
    public void setWidth(double width){
      this._width = width;
    }
}
public class Main{
  public static void main(String[] args){
    Rectangle r1 = new Rectangle();

    // getter & setter
    r1.setWidth(10);
    double width = r1.getWidth();
  }
}
{% endhighlight %}

위의 코드는 일반적으로 Java에서 getter와 setter를 사용하는 경우입니다. <code>getWidth</code>와 <code>setWidth</code> 메소드로 getter와 setter를 설정하였습니다. 그런데, <code>getWidth()</code>와 <code>setWidth()</code> 메소드를 쓰는 것이 여러모로 불편할 때가 많습니다. 즉, <code>r1.width</code>로 쓰는 게 훨씬 직관적인데, 이를 사용하지 못 하게 되는 것이죠.

##### Swift getter & setter

Swift는 getter와 setter에서 바로 이 부분을 보완하였습니다. 아래의 Swift 코드를 봐보겠습니다.

{% highlight swift %}
var variableName: dataType {
    get {
        //code to execute
        return someValue
    }
    set(newValue) {
        //code to execute
    }
}
{% endhighlight %}

출처 : <a href="https://syntaxdb.com/ref/swift/getters-setters">SyntaxDB</a>

기본적인 Getter와 Setter의 형태는 위와 같습니다. <code>variableName</code>에 들어가는 변수가 원하는 멤버변수 호출을 담당합니다. 즉, <code>className.variableName</code>의 표현으로 멤버변수의 값에 접근할 수 있게 됩니다. 위의 Java 코드와 동일한 코드를 Swift로 적게 되면 아래와 같이 나옵니다.

{% highlight swift %}
class Rectangle {
  private var _width: Double!

  var width: Double {
    get {
      return _width
    } set {
      _width = newValue
    }
  }
}
var r1 = Rectangle()
r1.width = 10
print(r1.width) // 10
{% endhighlight %}

Swift는 <code>r1.width</code>라는 표현 하나로 getter와 setter 모두를 사용할 수 있게 해줍니다. 멤버변수를 <code>_width</code>로 선언했는데 어째서 <code>r1._width</code>가 아니고 <code>r1.width</code>인가요? 하고 생각하실 수 있습니다. 이는 <code>var width: Double...</code>로 선언되어 있기 때문에 그렇습니다. 즉, 우리가 선언한 변수명을 토대로 멤버변수에 접근하게 되고, <code>var width</code>는 어떤 다른 변수 명으로 바뀔 수 있습니다.<!--_-->

##### Little bit further(getter)

* Getter

Getter를 사용하면서 변수와 관련하여 생각해봐야 할 부분은 <code>Optional</code>입니다. iOS 프로그램은 상당히 많은 부분에서 nil값을 허용하기 위해 <code>Optional</code>을 활용합니다. 그래서 getter를 설정할 때 nil값을 설정할 수 있는 <code>Optional</code>을 쓰는 변수에 대해서는 프로그램이 nil 오류가 나지 않도록 다음과 같이 많이 씁니다.(주로 String을 다룰 때 주의하세요.)

{% highlight swift %}
// nil을 먼저 체크하여 빈 String으로 변환
private var name: String!
var name: String {
  get {
    if name == nil {
      name = ""
    }
    return name
  }
}
{% endhighlight %}

또한 getter는 setter 없이 쓰일 때 <code>get{}</code>를 생략할 수 있습니다.

{% highlight swift %}
private var name: String!
var name: String {
  if name == nil {
    name = ""
  }
  return name
}
{% endhighlight %}

* Setter

Setter를 사용할 때는 파라미터(anyName)를 넘길 수도 있고 넘기지 않을 수도 있습니다. 이 때 파라미터를 넘기지 않으면 <code>newValue</code>가 예약어가 되어 변수 설정을 할 수 있도록 해줍니다. 특별히 변수 이름을 설정할 이유가 없다면 더 간단한 것을 쓰는 것이 나아 보입니다.

{% highlight swift %}
set(anyName){
  target = anyName
}
set {
  target = newValue
}
{% endhighlight %}


> 내용 출처 : Apple Inc. The Swift Programming Language (Swift 3.0.1)

---
layout: post
comments: true
title:  "Swift 접근 제어자(Access Control)"
excerpt: "Swift의 접근제어자에 대해 간단히 정리했습니다."
categories: Swift AccessControl Language
date:   2018-01-16 00:30:00
tags: [Swift, AccessControl, Language]
image:
  feature: swiftLogo.jpg
---

Swift의 접근 제어자(Access Control)에 대해서 간단히 정리해보고자 합니다. 정의를 살펴보면,

<div class="message">
  Access control restricts access to parts of your code from code in other source files and modules.
</div>

다음과 같습니다.

접근 제어자는 코드를 작성하는 한 파일에서 다른 파일에 있는 코드에 대한 접근을 명시적으로 작성하여 이를 관리하는 것인데, `module`과 `source file`에 따라 다른 접근을 할 수 있습니다.

#### Module과 Source file

`module`이라는 것은 하나의 프레임워크를 의미합니다. 즉, `import` 키워드로 추가되는 것들이 `module`입니다. `UIKit`, `Foundation` 등이 모두 `module`입니다. 프로젝트의 하위에 있는 `targets`도 각각 모두 하나의 `module`입니다. `source file`은 각각의 `module` 안에 있는 파일들입니다. 예를 들어 `example.swift` 같은 파일들이 하나의 `source file`입니다.

#### Swift의 5가지 접근 제어자

이제 `module`과 `source file`을 기준으로 나뉘는 5가지 접근 제어자를 알아보고자 합니다. 그리고 여기서는 특정 접근 제어자가 적용되는 대상을 `entity`로 서술합니다. `entity`는 접근제어자를 작성할 수 있는 property, method, class, struct 등의 집합을 의미합니다.

1. `open`, `public` - 프로젝트 내의 모든 `module` 해당 entity에 접근할 수 있습니다.
2. `internal` - `default` 접근 제어자로, entity가 작성된 `module`에서만 접근할 수 있습니다.
3. `fileprivate` - entity가 작성된 `source file`에서만 접근할 수 있도록 합니다. 서로 다른 클래스가 같은 파일안에 있고 `fileprivate`로 선언되어 있다면 둘은 서로 접근할 수 있습니다.
4. `private` - 특정 객체에서만 사용할 수 있도록 하는 가장 제한적인 접근제어자입니다. `fileprivate`과 달리 같은 파일 안에 있어도 서로 다른 객체가 `private`로 선언되어 있다면 둘은 서로 접근할 수 없습니다.


#### open과 public의 차이

이 정리를 보면, 당연하게도 `open`과 `public`의 차이가 무엇인지 궁금할 것입니다. 둘의 차이는 `open`은 다른 모듈에서 `subclass`가 가능하지만, `public`은 그렇지 않다는 것입니다. 먼저 `open`은 `class`에만 사용될 수 있습니다. 그리고 한 모듈에서 만든 class를 `superClass`로 하는 `subClass`를 다른 모듈에서 만들기 위해서는 해당 `superClass`가 `open`으로 선언되어야 합니다. 당연히 `overriding`도 이 규칙이 적용됩니다.

#### 몇 가지 암묵적 룰

위에서 살펴본 특징 이외에도 따로 언급하지 않아도 적용되는 몇 가지 암묵적인 룰이 있습니다.

- 아무 접근 제어자도 적지 않으면 `internal`이 됩니다.

아무런 조건 없이 클래스, 변수 등을 만들면 해당 `entity`의 접근제어자는 기본적으로 `internal`이 됩니다.

- 어떠한 entity도 더 제한적인 접근제어자를 가진 entity로 정의 될 수 없습니다.

{% highlight swift %}
private struct Car {
  // error
  public var engine: String
}
{% endhighlight %}

위의 코드를 보면, `Car`는 `private`인데 그 안의 `engine`은 `public`입니다. 이런 접근 제어자 형태는 사용할 수 없습니다. 접근 제어자는 특정 entity로부터의 상대적인 기준이 적용되는 것이 아니라, 전체 프로젝트를 기준으로 적용됩니다. 그렇기 때문에 특정 entity 안의 변수, 메소드들은 기본적으로 해당 entity의 접근제어자보다 강하게만 적용될 수 있고, 더 약하게 적용될 수는 없습니다.

#### 유용한 기타 사항

- Unit Test는 `@testable` 키워드로 모듈을 import하여 public과 open이 아닌 entity들을 사용할 수 있도록 해줍니다.

{% highlight swift %}
@testable import {target_name}
{% endhighlight %}

특정 Unit test의 파일의 상단에 위처럼 선언을 하면 해당 모듈의 entity를 `internal` 형태로 사용할 수 있도록 해줍니다.

- Getter와 Setter에는 서로 다른 접근제어자를 적용할 수 있습니다.

Swift에서는 Setter를 Getter보다 더 제한적으로 설정할 수 있습니다.(반대는 불가능합니다.) 이 기능은 getter, setter를 모두 따로 작성하지 않아도 되는 매우 큰 장점을 제공합니다.

{% highlight swift %}
private(set) var name: String
{% endhighlight %}

다른 조건 없이 위와 같이 변수를 작성하였다면, getter는 `internal`이 되고, setter는 `private`이 됩니다.

{% highlight swift %}
public struct Car {
  fileprivate var _engine: String

  public var engine: String {
    get {
        return self._engine
    } set {
        self._engine = newValue
    }
  }
}

// 위의 코드를 getter와 setter에 대해 더 간결하고, 명확하게 정의할 수 있습니다.
public struct Car {
  fileprivate(set) var engine: String
}
{% endhighlight %}

다른 예시로 변수를 감싸고 있는 entity의 접근제어자가 `public`이면, 그 내부 entity들은 기본적으로 이를 따라가기 때문에 engine의 getter는 `public`, setter는 `fileprivate`이 됩니다.

- protocol에서 선언된 변수의 접근제어자는 조건을 만족한 경우에만 사용할 수 있습니다.

먼저 상황별로 관련된 예제는 다음 [링크](https://stackoverflow.com/a/38281420/5130783)에서 확인할 수 있습니다. 그 중 가장 필요하다고 생각되는 부분은 `private(set)`과 관련된 부분입니다. 즉, 아래 예제의 상황에서 protocol에 `private(set)`에 어떤 식으로 들어가야 하는지에 대한 문제입니다.

{% highlight swift %}
protocol Car {
  // 무엇이 들어가야 할까?
}

struct CarModel: Car {
  private(set) var engine: String
}
{% endhighlight %}

이는 protocol의 "변수가 `gettable`, `settable`하다."는 말에 "**외부 entity**에서 `gettable`, `settable`하다."라는 의미를 추가하면 문제를 해결할 수 있습니다. 즉, `private(set)`은 외부에서 `settable`하지 않기 때문에 protocol에는 `gettable`만 들어가게 됩니다.

{% highlight swift %}
protocol Car {
  var engine: String { get }
}

struct CarModel: Car {
  private(set) var engine: String
}
{% endhighlight %}

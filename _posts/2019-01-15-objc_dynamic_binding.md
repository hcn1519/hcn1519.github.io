---
layout: post
title: "Objc Dynamic Binding, Typing"
excerpt: "ObjectiveC의 동적 바인딩, 타이핑에 대해 알아봅니다."
date: "2019-01-15 01:03:19 +0900"
categories: ObjectiveC RunTime Binding Type
tags: [ObjectiveC, RunTime]
---

# 동적 바인딩

동적 바인딩(Dynamic Binding)은 객체에 호출되는 실제 메소드를 알아내는 시기를 컴파일 시점이 아니라, 프로그램 실행(런타임) 중으로 미루는 방법을 의미합니다. 예시를 통해 살펴보겠습니다.

```objectivec
// IntPoint.h
#import <Foundation/Foundation.h>

@interface IntPoint : NSObject

@property int x, y;
-(void)print;
-(void)set: (int)x and:(int)y;
-(IntPoint *)add: (IntPoint *)point;

@end

// IntPoint.m
#import "IntPoint.h"

@implementation IntPoint

- (void)print {
    NSLog(@"Point x: %d, y: %d", self.x, self.y);
}

- (void)set:(int)x and:(int)y {
    self.x = x;
    self.y = y;
}

- (IntPoint *)add:(IntPoint *)point {
    IntPoint *result = [[IntPoint alloc] init];

    result.x = self.x + point.x;
    result.y = self.y + point.y;
    return result;
}
@end
```

위와 같은 `IntPoint`라는 클래스를 생성하고, 아래와 같이 해당 클래스를 사용할 수 있습니다.

```objectivec
// Test
 id dataValue;

IntPoint *point1 = [[IntPoint alloc] init];
IntPoint *point2 = [[IntPoint alloc] init];

[point1 set:100 and:100];
[point2 set:30 and:20];
dataValue = [point1 add:point2]; // 1

[point1 print];    //        Point x: 100, y: 100
[point2 print];    //        Point x: 30, y: 20
[dataValue print]; //        Point x: 130, y: 120, 2
```

1. 위의 예시에서 `dataValue`는 `id`형으로 선언되어 있고, id형은 어떤 객체든 담을 수 있습니다.
1. 시스템은 `id`형 객체가 호출하는 메소드를 컴파일 시점이 아닌, 런타임 시점에 파악합니다.  그렇기 때문에 시스템은 `dataValue`가 호출하는 `print` 메소드가 `IntPoint`의 메소드라는 것을 알 수 있고, 이를 호출합니다.
1. 그렇기 때문에 동적 바인딩은 다형성 구현을 가능하게 합니다. 흔히 알고 있는 객체의 다형성의 경우 특정 `protocol` 타입으로 설정된 변수의 자리에 해당 `protocol`을 준수하는 객체는 무엇이든 들어갈 수 있는 것을 의미합니다. 동적 바인딩을 통한 다형성은 **각각의 객체가 동일한 이름의 메소드를 가지고 있는 상황에서 클래스에 관계 없이 시스템이 구현된 메소드를 파악하고 이를 호출하는 것**을 의미합니다.

## 동적 타이핑

## 동적 타이핑(Dynamic Typing)

객체의 타입을 명시적으로 지정하지 않고,(데이터 타입을 id로 지정) 런타임에서 객체의 타입을 설정하도록 하는 것을 동적 타이핑(Dynamic Typing)이라고 합니다. 이런 동적 타이핑이 가능한 이유는 ObjectiveC의 객체는 `isa`라는 클래스 타입(클래스 객체를 가리킴)을 지칭하는 포인터가 존재하기 때문입니다. 즉, 인스턴스가 id 타입이라도, 런타임에서 해당 인스턴스의 타입은 언제나 알 수 있습니다. `isa` 포인터는 `class()` 메소드를 통해 접근할 수 있습니다.

```objectivec
id dataValue;
IntPoint *point = [[IntPoint alloc] init];
dataValue = point;
NSLog(@"%@", [dataValue class]); // IntPoint
```

동적 타이핑은 정적 타이핑과 비교될 수 있습니다.

* 동적 타이핑 - 컴파일 시점이 아니라, **프로그램이 실행되는 단계에서 객체의 타입을 파악하는 방식**을 의미합니다.
* 정적 타이핑 - **특정 클래스의 객체로 타입을 지정**하는 것으로, 컴파일 타임에 변수의 타입을 지정하는 것을 의미합니다.

```objectivec
// 동적 타이핑
 id dataValue;

// 정적 타이핑
IntPoint dataValue;
```

동적 타이핑된 변수에 메시지를 전달할 때는 반드시 해당 변수가 메시지에 대해 respond 할 수 있어야 합니다. 그렇기 때문에 동적 타이핑된 인스턴스에 메시지 전달시에는 `respondsToSelector(SEL)`을 통해 예외처리를 해주는 것이 좋습니다.

```objectivec
id dataValue;
IntPoint *point = [[IntPoint alloc] init];
[point set:10 and:20];
dataValue = point;

// 다음과 같이 해당 selector에 respond할 수 있는지 우선적으로 체크해야 합니다.
if ([dataValue respondsToSelector:@selector(print)]) {
    [dataValue print];
}
```

id 데이터형을 활용한 동적 타이핑은 남용하면 안 됩니다. 이유는 다음과 같습니다.

1. 컴파일 타임에 잡지 못 한 오류는 사용자가 보게 될 수도 있습니다. 런타임 에러를 확인하기 위해서는 앱을 다시 빌드해야하므로 생산성도 떨어집니다.
2. 선언한 변수의 가독성이 높아집니다.

---

# 참고 자료

* 프로그래밍 오브젝티브-C 2.0
* [Cocoa Core Concepts - Dynamic Binding](https://developer.apple.com/library/archive/documentation/General/Conceptual/DevPedia-CocoaCore/DynamicBinding.html#//apple_ref/doc/uid/TP40008195-CH15-SW1)
* [Cocoa Core Concepts - Dynamic Typing](https://developer.apple.com/library/archive/documentation/General/Conceptual/DevPedia-CocoaCore/DynamicTyping.html#//apple_ref/doc/uid/TP40008195-CH62-SW1)

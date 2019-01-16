---
layout: post
title: "Objc selector"
excerpt: "ObjectiveC의 selector에 대해 알아봅니다."
date: "2019-01-16 01:03:20 +0900"
categories: ObjectiveC selector
tags: [ObjectiveC, selector]
image:
  feature: objc.png
---

# selector

> A selector is the name used to select a method to execute for an object, or the unique identifier that replaces the name when the source code is compiled

`selector`는 객체의 메소드를 지칭하는 고유한 이름입니다. 단순 string과 `selector`의 메소드 이름과 차이는 컴파일러가 해당 `selector`를 고유하게 인식하는지 여부입니다. `selector`는 `dynamic function pointer`처럼 사용되어 
클래스에 관계 없이 메소드 이름만으로 해당 메소드를 지칭할 수 있도록 해줍니다.

`selector`는 C 문자열로 Objc 런타임 시점에서 컴파일러에 의해 생성되고, 클래스가 load되는 시점에서 매핑됩니다.

> Note: 클래스의 load 시점 - The runtime sends the load message to each class object, very soon after the class object is loaded in the process's address space. For classes that are part of the program's executable file, the runtime sends the load message very early in the process's lifetime. For classes that are in a shared (dynamically-loaded) library, the runtime sends the load message just after the shared library is loaded into the process's address space.

```objectivec
@implementation ClassA
    - (void)print {
        NSLog(@"classA");
    }
}

@implementation ClassB
    - (void)print {
        NSLog(@"classB");
    }
    - (void)print2:(id)anotherClassA {
        if ([anotherClassA isKindOfClass:[ClassA class]]) {
             NSLog(@"classA and classB");
        }
    }
}

// Usage
SEL action;
action = @selector(print);

ClassA *classA = [[ClassA alloc] init];
[classA performSelector:action]; // classA

ClassB *classB = [[ClassB alloc] init];
[classB performSelector:action]; // classB
```

* `SEL`은 `selector`에 대한 타입입니다.
* 하나의 `selector`로 클래스에 관계 없이 `performSelector:` 메소드를 사용하면 메소드 이름을 통해 해당 메소드를 실행할 수 있습니다.

```objectivec
SEL action2;
action2 = @selector(print2:);

ClassA *classA = [[ClassA alloc] init];
ClassB *classB = [[ClassB alloc] init];

[classB performSelector:action2 withObject:classA]; // classA and classB
```

* `performSelector`는 다른 argument를 `withObject`를 통해 보낼 수 있습니다.

---

# 참고 자료

* [Cocoa Core Concepts - selector](https://developer.apple.com/library/archive/documentation/General/Conceptual/DevPedia-CocoaCore/Selector.html)
* [SEL - Apple Developer Documentation](https://developer.apple.com/documentation/objectivec/sel)
* [NSObject +load and +initialize - What do they do?](https://stackoverflow.com/a/13326633/5130783)

---
layout: post
title: "Dynamic Library"
date: "2019-09-06 00:53:17 +0900"
excerpt: "Dynamic Library 대해 학습한 내용을 정리합니다."
categories: iOS, OS, Library, Framework
tags: [iOS, OS, Library, Framework]
image:
  feature: iOS.png
---

[Static Library](https://hcn1519.github.io/articles/2019-07/static-library)는 컴파일 타임에 executable(실행 바이너리)에 포함되어야 합니다. 이 문제는 앱이 커질 수록 더 큰 문제가 되었고, 이를 해결하기 위해 나온 것이 `Dynamic Library`입니다. `Dynamic Library`는 `Static Library`와는 다르게 앱의 `executable` files에 포함되지 않습니다.  바꿔 말하면, `Dynamic Library`는 앱의 컴파일과 별개로 동작하여, 앱의 컴파일 없이 `Dynamic Library`의 코드는 변경될 수 있습니다.

또한, `Dynamic Library`는 앱의 `executable` files에 포함되지 않기 때문에, 앱의 초기 실행시 불필요하다면 메모리에 로드될 필요가 없습니다. 그렇기 때문에 앱 초기 실행에 필요 없는 `Static Library`를 `Dynamic Library`로 전환하면 앱 초기 실행 속도를 개선하고 메모리 사용량을 줄일 수 있습니다.

<img width="644" alt="dynamicLib" src="https://user-images.githubusercontent.com/13018877/59974192-1b067180-95e4-11e9-9d6c-2b7b6cdd1118.png">

Dynamic Library는 앱에서 사용되기 위해 Link와 Load의 과정을 거칩니다. 아래에서는 이 과정에 대해서 얘기해보려고 합니다.

## Dynamic Libraries Link

`Dynamic Library` 사용에서 핵심적인 역할을 담당하는 것으로 `Dynamic Linker`가 있습니다. `Dynamic Linker`에 대해서 wiki에 정의된 내용은 다음과 같습니다.

> In computing, a dynamic linker is the part of an operating system that loads and links the shared libraries needed by an executable when it is executed (at "run time"), by copying the content of libraries from persistent storage to RAM, filling jump tables and relocating pointers.

`Dynamic Linker`는 `executable` 실행시 외부로부터 필요한 라이브러리를 연결하는 역할을 담당합니다. macOS와 iOS의 기반인 Darwin OS에서는 프로젝트 빌드 시점에서 소스코드 컴파일 이후에 라이브러리를 Link합니다. 이 Link Time 시점에서 `Dynamic Linker` 파일 경로는 앱 번들에 포함됩니다.(`executable` target인 프로젝트 빌드시 Mach-O 명령어가 호출됩니다.) 이 때, executable이 필요로 하는 Dynamic Library의 파일 경로(`someLib.dylib`)도 함께 앱 번들에 포함됩니다.

> Note: executable 외부는 빌드된 `Example.app` 번들의 외부를 의미하는 것이 아니라, 해당 번들 안에서 컴파일된 소스코드의 외부를 의미합니다. 그래서 `Dynamic Library`를 적용한다고 하여서 앱의 사이즈가 줄어드는 것은 아닙니다.(오히려 늘어날 수 있습니다.) executable(실행 바이너리)이 줄어드는 것과 앱 번들이 줄어드는 것의 차이를 이해하면 좋습니다.

또한 `Dynamic Linker`는 Link Time 시점에 `executable`이 필요로 하는 라이브러리를 알 수 있도록 메모리에 각각의 라이브러리를 호출하는 `machine code functions`를 메모리에 로드해놓습니다. 그래서 Link Time 시점에서 `executable`은 필요로하는 라이브러리의 주소를 `Dynamic Linker`를 통해 획득할 수 있습니다.

이러한 일련의 과정은 런타임에서 수행되고, `Dynamic Linker`는 Library를 이미 실행되고 있는 프로세스(`executable`)에 연결합니다. 이러한 과정을 `Dynamic Linking`이라고 부릅니다.

정리하면 다음과 같습니다.

1. 개발자가 앱을 빌드합니다.
2. 소스코드 컴파일이 진행됩니다.
3. 소스코드가 컴파일되면 컴파일된 파일에서 필요로하는 라이브러리의 Link를 진행합니다.
4. Link 과정에서 `executable`이 필요로 하는 라이브러리의 주소를 `Dynamic Linker`가 제공합니다.

## Dynamic Libraries Load

Dynamic Library는 메모리 로드 시점 및 메모리 로드 방식에 따라서 크게 `Dependent Library`와 `Runtime Loaded Library`로 나눌 수 있습니다.

### 1. Dependent Library

`Dependent Library`는 `Dynamic Library`중 앱 자체가 의존성을 가지고 있어서 앱 시작시 바로 메모리에 로드되는 라이브러리를 의미합니다.

> A dependent library, from the client’s point of view, is a dynamic library the client is linked with. Dependent libraries are loaded into the same process the client is being loaded into as part of its load process. For example, when an app is launched, its dependent libraries are loaded as part of the launch process, before the main function is executed.

앱이 실행되는 과정에서 `Dependent Library`가 로드되는 과정은 다음과 같습니다.

1. 앱이 실행될 때 커널은 새로운 프로세스를 위해 할당된 주소 공간에 앱의 코드와 데이터를 로드합니다. 커널은 `Dynamic Loader`를 앱과 함께 로드하고, `Dynamic Loader`는 `Dependent Library`를 메모리에 로드합니다.(`Dynamic Linking` 과정에서 `executable`이 획득한 주소값을 활용하여 `machine code functions`를 호출합니다.)
2. `Static Linker`는 앱이 `Dependent Library`와 링크될 때마다 해당 `Dependent Library`를 사용한 소스코드 파일명을 기록합니다. 이 파일명은 `install name`이라고 부릅니다. `Dynamic Loader`는 `install name`을 활용하여 파일 시스템에 라이브러리의 위치를 설정합니다.
3. `Dynamic Loader`는 정의되지 않은 외부 symbols를 앱 실행 시점에 처리하고, 그 이외의 symbols는 앱이 실제로 사용할 때까지 방치됩니다.

### 2. Runtime Loaded library

`Runtime Loaded Library`는 `Dynamic Library`중 클라이언트가 런타임에서 직접 로드(`dl_open()` 호출)하는 라이브러리를 의미합니다. 클라이언트는 `Runtime Loaded Library`를 `static linker`에 연결된 라이브러리로 해당 라이브러리를 포함시키지 않고, 이 때문에 `Dynamic Loader`는 `Runtime Loaded Library`을 앱 실행시 로드하지 않습니다. 클라이언트는 앱에서 `Runtime Loaded Library`를 통해 export된 symbols를 사용할 때, 해당 라이브러리를 메모리에 로드합니다.

> Note: iOS에서는 Runtime Loaded library를 구현해서 테스트해 볼 수는 있지만, 실제로 이 기능을 사용하여 앱을 배포할 수 없습니다.(앱 스토어 심사 거절 사유) 애플 앱스토어 규정에 따르면 앱 실행 과정에서 동적으로 로드되는 코드는 그 실행에 있어서 많은 제약을 받습니다. 이 글은 iOS에 국한된 것이 아니라, Darwin OS 기반으로 설명을 작성하였기 때문에 위의 설명을 함께 정리하였습니다.

* [App Review GuideLine Software Requirements 2.5.2](https://developer.apple.com/app-store/review/guidelines/#software-requirements)
* [참고 소스코드 - ios runtime loading dynamic framework](https://github.com/patriknyblad/ios-runtime-loading-dynamic-framework)

#### 참고 - 다양한 플랫폼 대응 - DLC(Dynamic Loader Compatibility)

플랫폼마다 `Dynamic Loader`를 구현한 방법이 다르기 때문에, `Dynamic Loader`가 동작하기 위해서는 플랫폼별 인터페이스가 필요합니다. 이런 인터페이스를 제공하는 것이 DLC(Dynamic Loader Compatibility, `dlfcn.h`에 위치한다)입니다. DLC는 아래와 같은 메서드를 제공합니다.

```c
// dlfcn.h
extern int dladdr(const void *, Dl_info *);
extern int dlclose(void * __handle);
extern char * dlerror(void);
extern void * dlopen(const char * __path, int __mode);
extern void * dlsym(void * __handle, const char * __symbol);
```

* `dlopen` - 앱이 라이브러리에서 export된 symbols를 사용하기 전에 호출. `dlsym`, `dlclose`에 사용되는 handle을 리턴한다.(`dynamic library handle`) `dlopen` 호출시. `Dynamic Library`의 reference count를 증가시킨다.
* `dlsym` - `Dynamic Library`에 의해 export된 symbols가 위치하는 주소공간
* `dladdr` - 주소 공간에 대한 정보 제공. DL_info 타입의 struct로 정보가 제공된다.

```c
// dlfcn.h
typedef struct dl_info {
        const char      *dli_fname;     /* Pathname of shared object */
        void            *dli_fbase;     /* Base address of shared object */
        const char      *dli_sname;     /* Name of nearest symbol */
        void            *dli_saddr;     /* Address of nearest symbol */
} Dl_info;
```

---

## 참고자료

* [Overview of Dynamic Libraries - Apple Doc](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/OverviewOfDynamicLibraries.html#//apple_ref/doc/uid/TP40001873-SW1)
* [Dynamic Library Usage Guidelines - Apple Doc](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/DynamicLibraryUsageGuidelines.html#//apple_ref/doc/uid/TP40001928-SW10)
* [http://www.vadimbulavin.com/static-dynamic-frameworks-and-libraries/](http://www.vadimbulavin.com/static-dynamic-frameworks-and-libraries/)
* [Static Libraries vs. Dynamic Libraries](https://medium.com/@StueyGK/static-libraries-vs-dynamic-libraries-af78f0b5f1e4)
* [Dynamic_linker#macOS_and_iOS](https://en.wikipedia.org/wiki/Dynamic_linker#macOS_and_iOS)
* [It Looks Like You Are Trying to Use a Framework](https://www.bignerdranch.com/blog/it-looks-like-you-are-trying-to-use-a-framework/)
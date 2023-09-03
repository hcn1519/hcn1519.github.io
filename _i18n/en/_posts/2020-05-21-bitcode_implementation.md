---
layout: post
title: "Introducing Bitcode"
date: "2020-05-21 00:53:17 +0900"
excerpt: "I've compiled information about what you need to know to introduce Bitcode."
categories: Bitcode, AppStore, Xcode, iOS, BuildSystem, Symbol, CrashReport
tags: [Bitcode, AppStore, Xcode, iOS, BuildSystem, Symbol, CrashReport]
image:
  feature: iOS.png
---

## Table of Contents

1. [About Bitcode](./bitcode_implementation#about-bitcode)
1. [Xcode Build Settings for Bitcode](./bitcode_implementation#xcode-build-settings-for-bitcode)
1. [Bitcode Support for Library](./bitcode_implementation#bitcode-support-for-library)

In this post, I've compiled information about what you need to know to introduce Bitcode.

## About Bitcode

### Bitcode Upload Process

<div class="message">
    Bitcode is an intermediate representation of a compiled program.
</div>

- Bitcode is an [IR (Intermediate Representation)](https://en.wikipedia.org/wiki/Intermediate_representation) included in binary builds for App Thinning in the App Store. When the uploaded binary includes bitcode, the App Store recompiles and links the binary, generating optimized binaries for each device architecture.
- App users only download the binary for their device's architecture when bitcode is enabled, reducing the app size they need to download.
- To summarize, when uploading a binary to the App Store, the following process occurs:

1. Upload a single binary with bitcode to the App Store.
2. The App Store recompiles the binary to generate binaries for different architectures (e.g., arm64, armv7).
3. App users download the binary for their device's architecture. (Before bitcode, only a single "fat binary" was used.)

### Symbolication for Apps with Bitcode Enabled

- Recompilation by the App Store during archiving makes dSYM generated during app development unusable. Matching dSYM with the app binary is based on the UUID included in the binary. Hence, when a rebuild occurs (even if there are no code changes), the dSYM from the previous build cannot match the subsequent one. Therefore, dSYMs generated during archiving cannot be used to symbolicate Crash Reports in the App Store.
- Therefore, when uploading dSYMs to Third Party Crash Analysis platforms after enabling bitcode, it is **essential** to download the files from Xcode Organizer or iTunes Connect.

### bcsymbolmap

- During archiving, a checkbox in iTunes Connect decides whether to upload the app's Symbols. Turning off this checkbox causes Xcode to obfuscate the symbols included in the dSYM of the app before binary upload (e.g., "__hidden#109_"). These obfuscated symbols are decrypted using a file called `.bcsymbolmap`. Therefore, dSYM files for bitcode-enabled binaries always include the corresponding `.bcsymbolmap`.
- When uploading dSYMs to Third Party Crash Analysis platforms, dSYMs downloaded from Xcode are decrypted and can be uploaded directly. However, dSYMs downloaded directly from iTunes Connect need to be decrypted manually.

```shell
xcrun dsymutil -symbol-map <path to BCSymbolMaps in xcarchive> <path to downloaded dSYM directory>
```

## Xcode Build Settings for Bitcode

Xcode has options to include full bitcode or markers indicating bitcode during binary builds.

### ENABLE_BITCODE

Setting ENABLE_BITCODE to YES adds flags related to bitcode during source code build and archiving. During the build, the `-embed-bitcode-marker` flag is added, and during archiving, the `-embed-bitcode` flag is added. You can see this in the build and archive logs.

- Build Log

```
// Build log excerpt
CompileSwift normal arm64 TestObj.swift (in target 'SomeProject' from project 'SomeProject')
...
/Debug-iphoneos/SomeProject.build/Objects-normal/arm64/TestObj.o -embed-bitcode-marker 
...
```

- Archive Log

```
// Archive log excerpt
SwiftCodeGeneration normal arm64 (in target 'SomeProject' from project 'SomeProject')
...
/Release-iphoneos/SomeProject.build/Objects-normal/arm64/TestObj.bc -embed-bitcode -target arm64-apple-ios11.0 -Xllvm -aarch64-use-tbi -O -disable-llvm-optzns -module-name
...
```

### BITCODE_GENERATION_MODE

You can achieve the same effect as ENABLE_BITCODE using `BITCODE_GENERATION_MODE` in User-Defined Settings. Setting the value to `marker` adds the `-embed-bitcode-marker` compile flag, and setting it to `bitcode` adds the `-embed-bitcode` flag. You can change this setting to build with full bitcode for certain cases.

<img width="484" alt="Screenshot 2020-05-22 12 59 59" src="https://user-images.githubusercontent.com/13018877/82578788-d73b3400-9bc7-11ea-9ff4-953814cbead4.png">

> Note: You can also enable bitcode by adding `-fembed-bitcode` directly to Other C Flags.

## Bitcode Support for Library

- The main drawback of bitcode is that if any library you are using does not support bitcode, you cannot enable bitcode in your app.
- Here are some considerations for library bitcode support:

### Checking if Binary Support Bitcode

To check if a specific library supports bitcode, you can examine whether the library binary contains LLVM Symbols. However, there can be some confusion about which symbols to check, as there are various [issues](https://stackoverflow.com/a/33105733/5130783) regarding this. In general, you can use the following command to check if a binary supports bitcode:

```shell
$ otool -arch arm64 -l MyFramework/MyFramework | grep __LLVM
$ otool -arch armv7 -l myLib.a | grep __LLVM
```

### Bitcode Support for Library distributed via Cocoapods

- Bitcode is handled during compilation, not linking. Therefore, whether a library binary supports bitcode or not determines whether bitcode can be enabled in your app. For libraries distributed as built binaries or frameworks, if they previously did not support bitcode, you must allow bitcode and rebuild them before redistributing.
- In the case of CocoaPods, libraries marked as `vendored_framework` or `vendored_libraries` fall into this category. If any one library in your app does not support bitcode, your app cannot use bitcode.
- However, libraries built from source via CocoaPods are built during your app's build process. Therefore, if you don't explicitly set `ENABLE_BITCODE` to `NO` in your app's PodFile or PodSpec, these libraries will support bitcode.

## References

- [Understanding and Analyzing Application Crash Reports - Bitcode](https://developer.apple.com/library/archive/technotes/tn2151/_index.html#//apple_ref/doc/uid/DTS40008184-CH1-SYMBOLICATION-BITCODE)
- [What is app thinning? (iOS, tvOS, watchOS)](https://help.apple.com/xcode/mac/11.0/index.html?localePath=en.lproj#/devbbdc5ce4f)
- [How to handle bitcode](https://www.slideshare.net/syoikeda/how-to-handle-bitcode)
- [How to check a static library is built contain bitcode?](https://stackoverflow.com/questions/32755775/how-to-check-a-static-library-is-built-contain-bitcode)
- [Static Libraries, Frameworks, and Bitcode](https://medium.com/@heitorburger/static-libraries-frameworks-and-bitcode-6d8f784478a9)
- [https://forums.developer.apple.com/message/7038#11344](https://forums.developer.apple.com/message/7038#11344)
- [https://www.guardsquare.com/en/blog/enable-bitcode](https://www.guardsquare.com/en/blog/enable-bitcode)
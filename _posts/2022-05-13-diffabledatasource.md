---
layout: post
title: "DiffableDataSource로 안전하게 UIKit List 업데이트하기"
date: "2022-05-13 00:53:17 +0900"
excerpt: "UIKit의 DiffableDataSource를 사용하기 위한 방법에 대해 정리하였습니다."
categories: iOS, WWDC, DiffableDataSource, UIKit
tags: [iOS, WWDC, DiffableDataSource, UIKit]
image:
  feature: iOS.png
---

## Table of Contents

1. [WWDC - Advances in UI Data Sources](./diffableDataSource#1-wwdc---advances-in-ui-data-sources)
1. [실제 적용기](./diffableDataSource#2-실제-적용기)

# WWDC - Advances in UI Data Sources

`Diffable Data Source`는 `UICollectionView`와 `UITableView`의 DataSource 업데이트를 좀 더 안전하고, 편리하게 수행할 수 있도록 만들어진 API입니다. 이 글에서는 iOS 13부터 지원되는 `Diffable Data Source`를 소개하는 WWDC 주요 내용([Advances in UI Data Sources](https://developer.apple.com/videos/play/wwdc2019/220))을 정리하고, 이를 적용한 후기에 대해 작성해보았습니다.

## Current state-of-the-art

- `UICollectionView`, `UITableView`를 구성하기 위해서 개발자는 아래와 같은 DataSource 코드를 작성해야 했습니다.

![no1](https://user-images.githubusercontent.com/13018877/168228135-ae120e52-5c14-479f-814e-3cf9c3d26409.jpeg)

그리고 이 DataSource를 업데이트하기 위해서는 `reloadData()`나 `performBatchUpdates()` 사용해야 합니다. 전체 데이터를 갱신하는 `reloadData()` 는 작은 데이터를 갱신할 때에는 유용하지만, 보여주는 데이터의 양이 많아지거나 일부 Cell만 업데이트하고자 할 때에는 `performBatchUpdates()`를 통해 개별 Section, 혹은 Item을 업데이트해주어야 합니다. 하지만, `performBatchUpdates()` 업데이트가 잘못 되었을 때 아래와 같은 크래시가 발생합니다.

![no2](https://user-images.githubusercontent.com/13018877/168228171-19ff6cf6-5f89-4b23-8051-7873f535507e.jpeg)

## Diffable DataSource

- `Diffable DataSource`는 UI의 업데이트를 간단하고, 크래시 없이 수행할 수 있도록 하기 위해 iOS 13에서 새롭게 소개된 API입니다.
- `Diffable DataSource`는 Cell의 insert, delete 등의 동작을 사용자가 직접 수행하지 않도록 합니다. 그리고, 데이터의 업데이트를 `Snapshot`을 적용(apply)하는 방식으로 수행하도록 합니다.

![no3](https://user-images.githubusercontent.com/13018877/168228193-7237ae99-6c74-444b-b52d-59a8c4b81d52.jpeg)

### Snapshots

`Snapshot`은 UI의 상태를 가지고 있는 객체로 `Snapshot`을 통해 데이터 업데이트시 `IndexPath` 접근 없이 데이터를 업데이트 할 수 있습니다.
![no4](https://user-images.githubusercontent.com/13018877/168228214-24f2a0a0-0290-4d58-a899-b8a103e83d77.jpeg)

UI 업데이트가 필요할 경우 새로운 `Snapshot`을 만들거나, 기존에 반영된 `Snapshot`을 가져와서 DataSource에 `apply()`해주면 됩니다.

![no5](https://user-images.githubusercontent.com/13018877/168228230-05f92a53-3d00-4eda-98e0-89d448be7e70.png)

## How to Use

### 1. Diffable DataSource property 정의

UIKit에서는 `UICollectionView`, `UITableView`에 맞는 `Diffable DataSource`를 정의하여 다음과 같이 제공합니다.

```swift
@available(iOS 13.0, tvOS 13.0, *)
open class UITableViewDiffableDataSource<SectionIdentifierType, ItemIdentifierType> : NSObject, UITableViewDataSource 
    where SectionIdentifierType : Hashable, ItemIdentifierType : Hashable {

    public typealias CellProvider = (_ tableView: UITableView,
                                     _ indexPath: IndexPath,
                                     _ itemIdentifier: ItemIdentifierType) -> UITableViewCell?

    public init(
        tableView: UITableView,
        cellProvider: @escaping UITableViewDiffableDataSource<SectionIdentifierType, ItemIdentifierType>.CellProvider)
}
```

- Diffable DataSource를 생성시 제공해야 하는 `SectionIdentifierType`, `ItemIdentifierType`과 관련해서 유의해야 할점은 해당 타입이 모두 `Hashable`이어야 한다는 점입니다.

```swift
class ViewController: UIViewController {

    @available(iOS 13.0, *)
    private lazy var diffableDataSource: UITableViewDiffableDataSource<Int, ViewModel> = {
        return UITableViewDiffableDataSource<Int, ViewModel>(tableView: logTableView,
                                                             cellProvider: { [weak self] (tableView, indexPath, itemIdentifier) in

            guard let cell = tableView.dequeueReusableCell(withIdentifier: "MyTableViewCell",
                                                           for: indexPath) as? MyTableViewCell,
                  let viewModel = self?.viewModel else {
                      return tableView.dequeueReusableCell(withIdentifier: "UITableViewCell",
                                                           for: indexPath)
                  }

            let cellViewModel = ViewModel(identifier: itemIdentifier)
            cell.viewModel = cellViewModel
            return cell
        })
    }()

    override func viewDidLoad() {
        super.viewDidLoad()

        if #available(iOS 13.0, *) {
            tableView.dataSource = diffableDataSource
        } else {
            tableView.dataSource = self
        }
    }
}
```

- `Diffable DataSource`는 위처럼 사용할 수 있습니다. 여기서 `CellProvider`의 `cellProvider` 클로저는 기존의 `cellForItemAt()`의 로직을 대체하는 형태로 사용할 수 있습니다.
- `UITableViewDiffableDataSource`는 `UITableViewDataSource`를 따르고 있기 때문에 이를 사용하게 되면 기존의 `UITableViewDataSource`는 호출되지 않습니다.

### 2. 새로운 Snapshot 적용하기

위처럼 정의한 DataSource에 새로운 데이터를 추가하고 싶은 경우, 아래처럼 `NSDiffableDataSourceSnapshot`을 만들고 모델을 추가해주면 됩니다.

```swift
var snapshot = NSDiffableDataSourceSnapshot<Int, 퍋>()
snapshot.appendSections([0])
snapshot.appendItems(messages, toSection: 0)
self?.diffableDataSource.apply(snapshot,
                               animatingDifferences: false,
                               completion: { [weak self] in
    self?.scrollToBottom(animated: true)
})
```

## 유의사항 및 추가 내용

- `Diffable Data Source`를 적용한 시점부터는 `performBatchUpdates()`, `insertItems()`, `deleteItems()` 등의 API를 사용하면 안 됩니다.

![no6](https://user-images.githubusercontent.com/13018877/168228354-25666d0d-75de-4876-861c-bd08fce19825.jpeg)

- `Snapshot`은 새로운 인스턴스 혹은 기존 `Diffable Data Source`의 `Snapshot`을 통해 생성할 수 있습니다.

![no7](https://user-images.githubusercontent.com/13018877/168228380-36089083-a6b6-44d6-9f66-b2d677432403.jpeg)

- 모든 데이터 업데이트는 `Snapshot`을 통해 수행됩니다. 그에 따라 `Snapshot`은 모델을 업데이트하는 API를 제공합니다.

![no8](https://user-images.githubusercontent.com/13018877/168228394-a2ad2e51-42e3-4586-873a-4314e4724d21.jpeg)

## 성능

- `Diffable Data Source`에서 사용하는 Diff 알고리즘은 빠릅니다.
- 새로운 Snapshot을 적용하는 `apply()` 메소드는 기존 reload API들과 다르게 항상 메인 쓰레드에서 수행되지 않아도 됩니다. 하지만, 항상 동일한 Queue에서 `apply()`가 호출되어야 합니다.

![no9](https://user-images.githubusercontent.com/13018877/168228418-136c5999-d77e-4202-8cc9-83546807ede0.jpeg)

# 실제 적용기

`Diffable DataSource`는 유용하게 사용할 수 있지만, 적용시 고려해야 할 것들이 있습니다. 여기에서는 `Diffable DataSource`를 실제 프로젝트에 적용하면서 고려했던 내용들을 몇 가지 소개하고자합니다.

### 1. Hashable 타입

### Protocol Type

`Diffable DataSource`의 `SectionIdentifierType`, `ItemIdentifierType`은 모두 `Hashable`이어야 합니다. `Hashable`은 `Generic Type`을 사용하기 때문에 `Protocol`이 `Hashable`을 따를 경우 해당 `Protocol`은 타입으로 사용할 수 없습니다. 이 때문에 `SectionIdentifierType`, `ItemIdentifierType`은 `Hashable` 타입을 따를 수 있는 `Concrete Type`의 모델을 따로 구성해주어야 합니다.

예를 들어서, 다양한 ViewModel을 사용하는 ViewController는 ViewModel을 Protocol로 정의하여 사용하는 경우가 많습니다.

```swift
protocol ViewModelable {}

struct ViewModel1: ViewModelable {}
struct ViewModel2: ViewModelable {}
struct ViewModel3: ViewModelable {}

class ViewController: UIViewController {
    var viewModel: ViewModelable
}
```

그런데 `Diffable DataSource`를 적용하기 위해서는 해당 Protocol이 `Hashable`이어야 하는데 이 경우 `ViewModelable`을 타입으로 사용할 수가 없습니다.

```swift
protocol ViewModelable: Hashable {}

class ViewController: UIViewController {
    var viewModel: ViewModelable // compile error
}
```

이 문제를 해결하기 위한 방법은 해당 `Protocol`을 associated Value로 가지는 enum을 정의하는 것입니다.

```swift
enum ViewModel: Hasable {
    case normal(viewModel: ViewModelable)
    case error(viewModel: ViewModelable)
}

class ViewController: UIViewController {
    var viewModel: ViewModel
}
```

이와 같이 처리하게 되면, 해당 ViewModel에 다양한 타입을 추가하면서도 `Diffable DataSource`를 적용할 수 있게 됩니다.

### Concrete Type

또한, 기존 모델이 `Concrete type`인 경우에도 문제가 생길 수 있습니다. `Hashable`은 `Equatable`을 따르고 있는데, 이 `Equatable`을 위해 `==(lhs:rhs:)`을 구현하면서 상당히 많은 boilerplate 코드를 작성해야 합니다. 이를 회피하기 위해 기존 모델에 `UUID`를 주입하는 방식을 통해 `Hashable`을 따르는 모델을 쉽게 구성할 수 있습니다.

```swift
protocol UUIDHashable: Hashable {
    var uuid: UUID { get set }
}

extension UUIDHashable {
    func hash(into hasher: inout Hasher) {
        hasher.combine(uuid)
    }
}
```

### 2. 성능

데이터가 많고, UI 업데이트가 반복적으로 자주 발생하는 경우에 새로운 Snapshot을 새로 생성해서 사용할 경우 성능이 떨어지는 현상이 발생합니다. 예를 들어서, 새로운 Snapshot을 0.1초마다 생성해서 적용할 경우, 스크롤이 버벅이는 현상이 나타납니다.

```swift
var snapshot = NSDiffableDataSourceSnapshot<Int, ViewModel>()
snapshot.appendSections([0])
snapshot.appendItems(viewModels, toSection: 0)
diffableDataSource.apply(snapshot)
```

이는 `reloadData()`를 빠르게 여러번 수행할 경우 성능 저하가 발생하는 것과 유사한 이슈입니다. 따라서 이 문제를 개선하기 위해 항상 새로운 Snapshot을 만들고 적용하는 것이 아니라, `Diffable DataSource`에 바인딩된 `Snapshot`에 수정되는 모델만 추가, 제거하는 방식을 사용할 수 있습니다.

```swift
func applySnapshot(newItems: [ViewModel]) {
    var snapshot = diffableDataSource.snapshot()
    snapshot.appendItems(newItems, toSection: 0)
    diffableDataSource.apply(snapshot)
}
```

## 3. Background Queue

WWDC에 언급된 것처럼 `apply()` 메소드는 메인 쓰레드에서 수행되지 않아도 됩니다. 다만, 다른 Queue에서 업데이트를 수행할 때에는 `apply()` 메소드가 **명시적으로** 같은 Queue에서 호출되어야 합니다. 여기서 명시적이라는 말의 의미는 `apply()`가 로직상으로 같은 Queue에서 호출되는 것으로 예상할 수 있더라도, `apply()` 수행을 명시적으로 Queue로 감싸주어야 하는 것을 의미합니다. 이를 처리해주지 않으면 warning이 발생하고, 예상하지 못 한 상황에 크래시가 발생할 수도 있습니다.

또한, 한 번 다른 Queue에서 `apply()`가 수행된 경우에는 이를 Main Queue에서 업데이트해선 안됩니다. 즉, Queue를 바꿔가면서 `apply()`를 수행해서는 안됩니다.

```swift
let queue = DispatchQueue(label: "Update Queue")

// applyQueueToSnapshot()이 queue에서 호출되더라도 apply()는 queue로 감싸주어야 합니다.
func applySnapshot(newItems: [ViewModel]) {
    queue.async { [weak self] in
        guard let self = self else { return }
        var snapshot = self.diffableDataSource.snapshot()
        snapshot.appendItems(newItems, toSection: 0)
        self.diffableDataSource.apply(snapshot)
    }
}
```

## 참고자료

- [Advances in UI Data Sources](https://developer.apple.com/videos/play/wwdc2019/220)

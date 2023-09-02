---
layout: post
title: "Updating UIKit Lists Safely with DiffableDataSource"
date: "2022-05-13 00:53:17 +0900"
excerpt: "This article summarizes the use of UIKit's DiffableDataSource for iOS development."
categories: iOS, WWDC, DiffableDataSource, UIKit
tags: [iOS, WWDC, DiffableDataSource, UIKit]
image:
  feature: iOS.png
---

## Table of Contents

1. [WWDC - Advances in UI Data Sources](./diffableDataSource#wwdc---advances-in-ui-data-sources)
1. [Current State-of-the-Art](./diffableDataSource#current-state-of-the-art)
1. [Diffable DataSource](./diffableDataSource#diffable-datasource)
1. [How to Use](./diffableDataSource#how-to-use)
1. [Real-World Application](./diffableDataSource#real-world-application)
    1. [Hashable Types](./diffableDataSource#1-hashable-types)
    1. [Performance](./diffableDataSource#2-performance)
    1. [Background Queue](./diffableDataSource#3-background-queue)

## WWDC - Advances in UI Data Sources

The `Diffable Data Source` is an API introduced in iOS 13 to make updates to `UICollectionView` and `UITableView` data sources safer and more convenient. In this article, we'll summarize the key points from WWDC ([Advances in UI Data Sources](https://developer.apple.com/videos/play/wwdc2019/220)) that introduced the `Diffable Data Source` and share our experience applying it in real-world scenarios.

## Current State-of-the-Art

Developers used to write DataSource code like the one below to configure `UICollectionView` and `UITableView`:

![no1](https://user-images.githubusercontent.com/13018877/168228135-ae120e52-5c14-479f-814e-3cf9c3d26409.jpeg)

And to update this DataSource, we had to use methods like `reloadData()` or `performBatchUpdates()`. While `reloadData()` is useful for updating small data sets, when dealing with large amounts of data or updating specific cells, you would need to use `performBatchUpdates()`. However, improper use of `performBatchUpdates()` could lead to crashes like the one below:

![no2](https://user-images.githubusercontent.com/13018877/168228171-19ff6cf6-5f89-4b23-8051-7873f535507e.jpeg)

## Diffable DataSource

The `Diffable DataSource` was introduced in iOS 13 to simplify and make UI updates safer, eliminating the need for developers to handle actions like cell insertions and deletions manually. Instead, it relies on applying a `Snapshot` to update data.

![no3](https://user-images.githubusercontent.com/13018877/168228193-7237ae99-6c74-444b-b52d-59a8c4b81d52.jpeg)

A `Snapshot` is an object that holds the state of your UI. With a `Snapshot`, you can update data without the need for `IndexPath` access.

![no4](https://user-images.githubusercontent.com/13018877/168228214-24f2a0a0-0290-4d58-a899-b8a103e83d77.jpeg)

When you need to update the UI, you can create a new `Snapshot` or retrieve an existing one and apply it to the DataSource.

![no5](https://user-images.githubusercontent.com/13018877/168228230-05f92a53-3d00-4eda-98e0-89d448be7e70.png)

## How to Use

### 1. Define the Diffable DataSource Property

UIKit provides `Diffable DataSource` classes for both `UICollectionView` and `UITableView`. Here's an example for `UITableView`:

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

Note that both `SectionIdentifierType` and `ItemIdentifierType` must conform to the `Hashable` protocol.

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

`Diffable DataSource` can be used as shown above. The `cellProvider` closure in `UITableViewDiffableDataSource` replaces the logic of the traditional `cellForItemAt()` method. When you use `Diffable DataSource`, the existing `UITableViewDataSource` methods are no longer called.

### 2. Applying a New Snapshot

If you want to add new data to your DataSource, create an `NSDiffableDataSourceSnapshot` and add your models to it:

```swift
var snapshot = NSDiffableDataSourceSnapshot<Int, ViewModel>()
snapshot.appendSections([0])
snapshot.appendItems(messages, toSection: 0)
self?.diffableDataSource.apply(snapshot,
                               animatingDifferences: false,
                               completion: { [weak self] in
    self?.scrollToBottom(animated: true)
})
```

## Considerations and Additional Information

Once you've applied the `Diffable Data Source`, do not use methods like `performBatchUpdates()`, `insertItems()`, or `deleteItems()` to update your UI.

![no6](https://user-images.githubusercontent.com/13018877/168228354-25666d0d-75de-4876-861c-bd08fce19825.jpeg)

You can create a new `Snapshot` or use an existing one to update your data.

![no7](https://user-images.githubusercontent.com/13018877/168228380-36089083-a6b6-44d6-9f66-b2d677432403.jpeg)

All data updates are performed through the `Snapshot`. Therefore, the `Snapshot` provides APIs for updating your models.

![no8](https://user-images.githubusercontent.com/13018877/168228394-a2ad2e51-42e3-4586-873a-4314e4724d21.jpeg)

## Performance

- The diffing algorithm used by `Diffable Data Source` is fast.
- Unlike other reload APIs, the `apply()` method for applying a new `Snapshot` doesn't have to be executed on the main thread. However, it should always be called on the same queue.

![no9](https://user-images.githubusercontent.com/13018877/168228418-136c5999-d77e-4202-8cc9-83546807ede0.jpeg)

## Real-World Application

While `Diffable DataSource` is useful, there are considerations when applying it in real-world projects. Here are a few things we took into account when implementing `Diffable DataSource` in our projects.

### 1. Hashable Types

#### Protocol Type

Both `SectionIdentifierType` and `ItemIdentifierType` for `Diffable DataSource` must conform to the `Hashable` protocol. When you define a protocol that conforms to `Hashable`, you cannot use that protocol as a type. To address this, you can create an enum with associated values that represent different types conforming to the protocol.

For example, if your ViewController uses various ViewModels defined by a protocol:

```swift
protocol ViewModelable {}

struct ViewModel1: ViewModelable {}
struct ViewModel2: ViewModelable {}
struct ViewModel3: ViewModelable {}

class ViewController: UIViewController {
    var viewModel: ViewModelable
}
```

However, to use `Diffable DataSource`, you need your `ViewModelable` to be `Hashable`, which presents a problem:

```swift
protocol ViewModelable: Hashable {}

class ViewController: UIViewController {
    var viewModel: ViewModelable // compile error
}
```

To solve this, you can create an enum that includes associated values for your ViewModels:

```swift
enum ViewModel: Hashable {
    case normal(viewModel: ViewModelable)
    case error(viewModel: ViewModelable)
}

class ViewController: UIViewController {
    var viewModel: ViewModel
}
```

With this approach, you can use `Diffable DataSource` while accommodating different ViewModel types.

#### Concrete Type

Even when your models are concrete types, you may encounter challenges. `Hashable` requires you to implement `==(lhs:rhs:)` for equatability, which can lead to writing a lot of boilerplate code. To avoid this, you can inject a `UUID` into your models, making it easier to conform to `Hashable`.

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

### 2. Performance

In scenarios with large data sets and frequent UI updates, repeatedly creating and applying new Snapshots can lead to performance issues. For instance, if you create and apply a new Snapshot every 0.1 seconds, scrolling may become laggy.

```swift
var snapshot = NSDiffableDataSourceSnapshot<Int, ViewModel>()
snapshot.appendSections([0])
snapshot.appendItems(viewModels, toSection: 0)
diffableDataSource.apply(snapshot)
```

This is similar to the performance degradation you would experience when calling `reloadData()` multiple times rapidly. To improve performance, consider always working with the same Snapshot and modifying it by adding or removing items as needed.

```swift
func applySnapshot(newItems: [ViewModel]) {
    var snapshot = diffableDataSource.snapshot()
    snapshot.appendItems(newItems, toSection: 0)
    diffableDataSource.apply(snapshot)
}
```

### 3. Background Queue

As mentioned in WWDC, the `apply()` method does not have to run on the main thread. However, if you choose to run it on a different queue, you must explicitly ensure that `apply()` is called on the same queue where the `Diffable DataSource` is being used. Failure to do so will result in warnings and potentially unexpected crashes.

Additionally, once `apply()` has been called on a different queue, do not update it again on the main queue. In other words, avoid switching between queues when using `apply()`.

```swift
let queue = DispatchQueue(label: "Update Queue")

// Even if applyQueueToSnapshot() is called on a different queue, wrap apply() in the same queue.
func applySnapshot(newItems: [ViewModel]) {
    queue.async { [weak self] in
        guard let self = self else { return }
        var snapshot = self.diffableDataSource.snapshot()
        snapshot.appendItems(newItems, toSection: 0)
        self.diffableDataSource.apply(snapshot)
    }
}
```

## References

- [Advances in UI Data Sources](https://developer.apple.com/videos/play/wwdc2019/220)
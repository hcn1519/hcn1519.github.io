---
layout: post
title: "AVFoundation으로 비디오의 Thumbnail 생성하기"
date: "2018-05-22 00:09:34 +0900"
categories: AVFoundation UIImagePickerController AVAssetImageGenerator
tags: [AVFoundation, UIImagePickerController, AVAssetImageGenerator]
---

`AVFoundation`은 iOS에서 비디오 혹은 오디오를 다루기 위해 사용되는 프레임워크입니다. 사실 단순히 비디오, 오디오를 재생하는 것은 `AVKit`이라는 좀 더 high level의 프레임워크를 사용하면 되지만, 미디어 파일에 접근하여 파일을 편집하거나 새로운 파일을 만드는 것은 `AVFoundation`을 사용해야 합니다.

여기서는 `AVFoundation`을 활용하여 비디오에서 썸네일 이미지를 추출하는 방법에 대해 알아보고자 합니다. 과정은 다음과 같습니다.

1. 사용자의 앨범에서 비디오를 선택한다.
2. 선택된 비디오의 썸네일을 추출한다.

### 앨범에서 비디오 선택하기

미디어 파일을 처리하기 위해 바로 `ViewController`에서 `UIImagePickerController` 인스턴스를 만들고 이를 처리할 수 있지만, 미디어 파일 선택은 앱에서 다양한 상황에서 사용될 수 있기 때문에 따로 `Manager`를 생성하여 관리하는 것도 재사용 측면에서 나쁘지 않은 방법입니다. 그래서 저는 여기서 `MediaPickerManager`를 생성하여 이를 파일 선택과 파일 처리를 하는 역할을 담당하도록 하였습니다.


{% highlight swift %}
import UIKit
import AVFoundation
import MobileCoreServices
import Photos

protocol MediaPickerDelegate: class {
    func didFinishPickingMedia(videoURL: URL)
}

class MediaPickerManager: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

    // 1.
    weak var mediaPickerDelegate: MediaPickerDelegate?

    // 2.
    lazy var imagePicker: UIImagePickerController = {

        let imagePicker = UIImagePickerController()
        imagePicker.delegate = self
        imagePicker.sourceType = .photoLibrary
        imagePicker.allowsEditing = false
        imagePicker.mediaTypes = ["public.movie"]
        return imagePicker
    }()

    // 3.
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [String : Any]) {
        guard let mediaType = info[UIImagePickerControllerMediaType] as? String else { return }

        if mediaType == kUTTypeMovie as String {
            if let videoURL = info[UIImagePickerControllerMediaURL] as? URL {
                mediaPickerDelegate?.didFinishPickingMedia(videoURL: videoURL)
            }
        }
        picker.dismiss(animated: true, completion: nil)
    }
}
{% endhighlight %}

위의 코드에 대한 설명은 다음과 같습니다.

1. `MediaPickerDelegate`은 선택한 영상 파일의 URL을 ViewController 쪽으로 넘기기 위해 사용하는 delegate입니다.
2. 사용자의 앨범에서 비디오를 선택하는 것은 이미지를 선택할 때처럼, `UIImagePickerController`를 사용합니다. 다만, 영상 파일을 선택하기 위해서는 `mediaTypes` 옵션을 변경해주어야 합니다.
3. `UIImagePickerControllerDelegate`에서 제공하는 메소드입니다. 앨범에서 파일을 선택하고 확인을 눌렀을 때 호출되는 부분입니다.

위의 `Manager`는 ViewController에서 다음과 같이 사용됩니다.

{% highlight swift %}
class ViewController: UIViewController {

    // 1.
    let mediaPickerManager = MediaPickerManager()

    override func viewDidLoad() {
        super.viewDidLoad()

        mediaPickerManager.mediaPickerDelegate = self
    }

    // 2.
    @IBAction func imageBtnTapped(_ sender: UIButton) {
        PHPhotoLibrary.checkPermission { isSuccess in
            DispatchQueue.main.async {
                if isSuccess {
                    self.present(self.mediaPickerManager.imagePicker, animated: true, completion: nil)
                }
            }
        }
    }
}
// 3.
extension ViewController: MediaPickerDelegate {
    func didFinishPickingMedia(videoURL: URL) {
        // do something
    }
}
{% endhighlight %}

1. `MediaPickerManager`를 사용하기 위해 ViewController에 인스턴스를 생성합니다.
2. 사용자가 영상 선택 버튼을 클릭할 경우 `MediaPickerManager`의 `imagePicker`를 호출하여 앨범 선택 화면이 나타납니다. 이 때, 사용자의 앨범에 접근할 수 있는 권한이 필요하기 때문에 권한을 우선적으로 획득해야 합니다.
3. `MediaPickerDelegate`을 통해 앨범에서 파일 선택시 호출되는 함수입니다.


### 비디오에서 썸네일 추출하기

비디오에서 썸네일을 추출하기 위해 `AVFoundation`에서는 `AVAssetImageGenerator` 클래스를 제공합니다. `AVAssetImageGenerator`는 인스턴스 생성시 `AVAsset`이 반드시 필요하며, `AVAsset`은 local, remote URL을 통해 정의됩니다.

> AVAsset - The abstract class used to model timed audiovisual media such as videos and sounds.

그래서 위의 `didFinishPickingMedia(videoURL:)` 함수에서 delegate를 통해 넘어온 `videoURL`을 통해 `AVAsset` 인스턴스를 만들고 이를 통해 `AVAssetImageGenerator`를 생성하면 됩니다.

{% highlight swift %}
extension ViewController: MediaPickerDelegate {
    func didFinishPickingMedia(videoURL: URL) {

        let captureTime: [Double] = [12, 2, 3, 4]
        // 1.
        mediaPickerManager.generateThumbnailSync(url: videoURL, startOffsets: captureTime) { images in
            self.imageView.image = images.first!
        }
    }
}

extension MediaPickerManager {
    // 2.
    func imageGenerator(asset: AVAsset) -> AVAssetImageGenerator {
        let imageGenerator = AVAssetImageGenerator(asset: asset)
        imageGenerator.appliesPreferredTrackTransform = true
        imageGenerator.maximumSize = CGSize(width: 600, height: 600)

        // 사진을 캡쳐하는 시간의 오차와 연관된 옵션입니다.
        // 별도로 설정하지 않을 경우 offset 값과 실제 사진 결과 시간에 차이가 있을 수 있습니다.
        imageGenerator.requestedTimeToleranceAfter = CMTimeMake(1, 600)
        imageGenerator.requestedTimeToleranceBefore = CMTimeMake(1, 600)
        return imageGenerator
    }

    // 3.
    func generateThumnailAsync(url: URL, startOffsets: [Double],
                               completion: @escaping (UIImage) -> Void) {
        let asset = AVAsset(url: url)
        let imageGenerator = self.imageGenerator(asset: asset)

        let time: [NSValue] = startOffsets.compactMap {
            return NSValue(time: CMTimeMakeWithSeconds(Float64($0), asset.duration.timescale))
        }

        imageGenerator.generateCGImagesAsynchronously(forTimes: time) { _, image, _, _, _ in
            // 4.
            if let image = image {
                completion(UIImage(cgImage: image))
            }
        }
    }
}
{% endhighlight %}

1. `didFinishPickingMedia(videoURL:)`에 선택한 영상의 로컬 URL이 넘어오기 때문에 URL을 넘겨줍니다. 이 때, 영상에서 캡쳐를 찍으려면 몇분 몇초에 찍는 기준이 필요하기 때문에 캡쳐를 할 시간의 배열을 함께 넘겨줍니다.
2. URL을 가지고 생성된 `AVAsset`을 통해 `AVAssetImageGenerator`를 생성하는 함수입니다.
3. `AVAssetImageGenerator`를 통해 썸네일 이미지를 호출하는 부분입니다. `AVAssetImageGenerator`는 `generateCGImagesAsynchronously(forTimes:completion:)` 함수를 제공됩니다. 이 때, 필요한 `[NSValue]` 타입의 파라미터는 `startOffsets`을 통해 생성합니다.
4. `generateCGImagesAsynchronously(forTimes:completion:)`은 비동기적으로 작동하는 함수로 `completionHandler`를 통해 이미지 데이터를 반환합니다.

---

이와 관련한 [예시 코드](https://github.com/hcn1519/AVFoundationFrameCapture)에 실제 동작하는 데모 프로젝트를 올려두었습니다.

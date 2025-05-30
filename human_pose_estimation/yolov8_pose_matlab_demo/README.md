
# YOLO-v8 Full-Body Pose Estimation — MATLAB Online Demo

[![Open in MATLAB Online](https://www.mathworks.com/products/matlab-online/_images/open-in-matlab-online-badge.svg)](https://matlab.mathworks.com/open/github/v1?repo=CuteLoop/Matlab-demos&project=human_pose_estimation/yolov8_pose_matlab_demo)

Tiny, CPU-only demo that brings Ultralytics **YOLO-v8-Pose (`n` size, 17 key-points)**
into **MATLAB Online**.  
It shows how to

* download a pre-exported ONNX checkpoint,
* import it with the Deep Learning Toolbox,
* bolt on a lightweight custom decode layer,
* run single-image inference or a live-webcam loop.

---

## Quick start (1 minute)

1. Click the **badge** above to open this folder as a project in MATLAB Online.  
   (You’ll be prompted to log in with your MathWorks account.)

2. In the MATLAB Command Window run:

   ```matlab
   download_model          % one-time 7 MB download from Hugging Face
   net = setupNetwork;     % import ONNX + attach decode layer
   runPose(net,"people.jpg")   % replace with your own test image
   % liveWebcam(net)            % optional live demo (~5-8 FPS, CPU)
````

That’s it — you should see bounding boxes and 17-point skeletons over every person.

---

## Repository layout

```text
yolov8_pose_matlab_demo/
├─ models/                    ← empty; model is downloaded at runtime
└─ matlab/
   ├─ download_model.m        ← fetches yolov8n-pose.onnx (≈7 MB)
   ├─ setupNetwork.m          ← imports ONNX, registers decode layer
   ├─ yolov8PoseDecodeLayer.m ← **TODO:** fill in ~100 LoC decode math
   ├─ yolov8PosePost.m        ← **TODO:** add NMS + thresholding
   ├─ runPose.m               ← single-image inference + viz
   └─ liveWebcam.m            ← simple webcam loop
```

> **Note**
> The decode and post-processing stubs compile but return empty detections.
> Port the math from `ultralytics/utils/ops.py` (≈15 min copy-rewrite) to get real results.

---

## Requirements

* **MATLAB Online** (R2024a +)

  * Deep Learning Toolbox
  * Computer Vision Toolbox
  * ONNX Converter support (MATLAB will prompt to install if missing)

No local GPU needed — everything runs on MATLAB Online’s hosted CPU.

---

## Next steps

* ✏️ Finish `yolov8PoseDecodeLayer.predict` and `yolov8PosePost`.
* 🚀 Swap in a hand-keypoint model (21 joints) by changing `NumKeypoints`
  and re-exporting your checkpoint to ONNX.
* 💻 Use the decoded key-points for gesture recognition, tracking, or
  Simulink control blocks.

Happy hacking!



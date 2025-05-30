# YOLO-v8 Pose MATLAB Demo (17-keypoint full-body)

Quick, CPU-only pose-estimation demo for **MATLAB Online** using the
pre-exported **`yolov8n-pose.onnx`** checkpoint (17 COCO key-points).

* `matlab/download_model.m` – downloads the 7 MB ONNX file to your Drive  
* `matlab/setupNetwork.m`   – imports ONNX, attaches custom decode layer  
* `matlab/runPose.m`        – single-image inference + visualisation  
* `matlab/liveWebcam.m`     – webcam loop (~5-8 FPS in MATLAB Online)

> Tested with MATLAB R2024a Online (Deep Learning + Computer Vision TBx).

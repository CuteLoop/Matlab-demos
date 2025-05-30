
#!/usr/bin/env python3
"""
create_matlab_pose_demo.py
Scaffolds a MATLAB repository for YOLO-v8 full-body pose estimation.
"""

import os, textwrap, pathlib, sys

# ---------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------
def write(fname: pathlib.Path, content: str):
    fname.parent.mkdir(parents=True, exist_ok=True)
    fname.write_text(textwrap.dedent(content).lstrip(), encoding="utf8")
    print("  created", fname.relative_to(ROOT))

# ---------------------------------------------------------------------
# Repository root
# ---------------------------------------------------------------------
ROOT = pathlib.Path.cwd() / "yolov8_pose_matlab_demo"
if ROOT.exists():
    print(f"Destination {ROOT} already exists – aborting.", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------
# README
# ---------------------------------------------------------------------
write(ROOT / "README.md", """
# YOLO-v8 Pose MATLAB Demo (17-keypoint full-body)

Quick, CPU-only pose-estimation demo for **MATLAB Online** using the
pre-exported **`yolov8n-pose.onnx`** checkpoint (17 COCO key-points).

* `matlab/download_model.m` – downloads the 7 MB ONNX file to your Drive  
* `matlab/setupNetwork.m`   – imports ONNX, attaches custom decode layer  
* `matlab/runPose.m`        – single-image inference + visualisation  
* `matlab/liveWebcam.m`     – webcam loop (~5-8 FPS in MATLAB Online)

> Tested with MATLAB R2024a Online (Deep Learning + Computer Vision TBx).
""")

# ---------------------------------------------------------------------
# MATLAB: download_model.m
# ---------------------------------------------------------------------
write(ROOT / "matlab" / "download_model.m", r"""
function download_model()
% download_model  Fetch yolov8n-pose.onnx from Hugging Face (one-time)

modelDir = fullfile("drive","My Drive","models");
if ~exist(modelDir,"dir"), mkdir(modelDir), end
url      = "https://huggingface.co/Xenova/yolov8n-pose-onnx/resolve/main/yolov8n-pose.onnx";
savePath = fullfile(modelDir,"yolov8n-pose.onnx");

if exist(savePath,"file")
    fprintf("Model already exists at %s\n",savePath);
else
    fprintf("Downloading YOLO-v8 Pose model (≈7 MB)…\n");
    websave(savePath,url);
    fprintf("Saved to %s\n",savePath);
end
end
""")

# ---------------------------------------------------------------------
# MATLAB: setupNetwork.m
# ---------------------------------------------------------------------
write(ROOT / "matlab" / "setupNetwork.m", r"""
function net = setupNetwork()
% setupNetwork  Import ONNX + register YOLO-v8 pose decode layer
% Returns a dlnetwork ready for inference.

modelPath = fullfile("drive","My Drive","models","yolov8n-pose.onnx");
assert(isfile(modelPath), "Run download_model.m first!");

lgraph = importONNXLayers(modelPath, ImportWeights=true, ...
                          OutputLayerType="regression");

% --- anchor matrix from YOLO-v8 cfg (pixels at img=640)
anchors = [10  13; 16  30; 33  23; ...
           30  61; 62  45; 59 119; ...
           116 90; 156 198; 373 326];

decode = yolov8PoseDecodeLayer("NumKeypoints",17, ...
                               "Stride",[8 16 32], ...
                               "Anchors",anchors);

lgraph = replaceLayer(lgraph,"output",decode);
net    = dlnetwork(lgraph);

fprintf("Network ready – %d learnables, %d layers\n", ...
        numel(net.Learnables.Value), numel(net.Layers));
end
""")

# ---------------------------------------------------------------------
# MATLAB: yolov8PoseDecodeLayer.m (stub w/ TODO)
# ---------------------------------------------------------------------
write(ROOT / "matlab" / "yolov8PoseDecodeLayer.m", r"""
classdef yolov8PoseDecodeLayer < nnet.layer.Layer
% yolov8PoseDecodeLayer  Custom layer to turn raw YOLO-v8 logits into
% [x y w h conf keypoints] tensors.
%
% NOTE: This is a **functional stub**.  Fill in the math in predict().  A
% fully-worked version is ~100 LoC (see Ultralytics utils/ops.py).

properties
    NumKeypoints (1,1) double
    Stride       (1,:) double
    Anchors
end

methods
    function layer = yolov8PoseDecodeLayer(varargin)
        layer.Name = "yolo_pose_decode";
        p = inputParser;
        addParameter(p,"NumKeypoints",17);
        addParameter(p,"Stride",[8 16 32]);
        addParameter(p,"Anchors",[]);
        parse(p,varargin{:});

        layer.NumKeypoints = p.Results.NumKeypoints;
        layer.Stride       = p.Results.Stride;
        layer.Anchors      = p.Results.Anchors;
    end

    function Z = predict(layer, X)
        %#ok<*NASGU>  % Suppress unused-variable warnings
        % -------------------------------------------------------------
        %  X: B × N × (5 + K*3)   (raw logits)
        %  Z: M × (4 + 1 + K*2)   (decoded detections)
        % -------------------------------------------------------------
        error([layer.Name ' is a stub – implement the decode math here.']);
    end
end
end
""")

# ---------------------------------------------------------------------
# MATLAB: yolov8PosePost.m (NMS stub)
# ---------------------------------------------------------------------
write(ROOT / "matlab" / "yolov8PosePost.m", r"""
function [boxes,scores,keypoints] = yolov8PosePost(raw; varargin)
% yolov8PosePost  Placeholder post-processing (NMS, thresholding).
% Replace with your own code or port Ultralytics' Python NMS.

% For now, return empties to keep demo compiling.
boxes      = zeros(0,4);
scores     = zeros(0,1);
keypoints  = zeros(0,17,2);
end
""")

# ---------------------------------------------------------------------
# MATLAB: runPose.m
# ---------------------------------------------------------------------
write(ROOT / "matlab" / "runPose.m", r"""
function runPose(net, imgPath)
% runPose  Single-image inference + visualisation
I0 = imread(imgPath);
I  = imresize(I0,[640 640]);
dlI = dlarray(single(I)./255,'SSCB');

raw = predict(net, dlI);

[bboxes,scores,kpts] = yolov8PosePost(raw, ...
                           'ConfThreshold',0.25, ...
                           'NumKeypoints',17);

out = insertShape(I0,"Rectangle",bboxes(:,1:4),"LineWidth",3,"Color","yellow");
out = insertMarker(out,reshape(kpts,[],2),"o","Color","cyan","Size",4);

figure; imshow(out); title("YOLO-v8 full-body pose");
end
""")

# ---------------------------------------------------------------------
# MATLAB: liveWebcam.m
# ---------------------------------------------------------------------
write(ROOT / "matlab" / "liveWebcam.m", r"""
function liveWebcam(net)
% liveWebcam  Simple webcam loop (~5-8 FPS in MATLAB Online)
cam = webcam;
fig = figure('Name','YOLO-v8 Pose – Live');

while ishandle(fig)
    frame = snapshot(cam);
    dlF   = dlarray(single(imresize(frame,[640 640]))/255,'SSCB');
    raw   = predict(net, dlF);

    [b,s,k] = yolov8PosePost(raw,'ConfThreshold',0.3,'NumKeypoints',17);
    vis = insertShape(frame,"Rectangle",b(:,1:4),"LineWidth",2);
    vis = insertMarker(vis,reshape(k,[],2),"o","Color","magenta");

    imshow(vis); drawnow;
end
end
""")

print("\n✅  MATLAB demo skeleton is ready.")
print("   Next steps: 1) upload to MATLAB Drive  2) fill in the TODOs in the decode/post files.")

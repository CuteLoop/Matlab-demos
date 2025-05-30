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

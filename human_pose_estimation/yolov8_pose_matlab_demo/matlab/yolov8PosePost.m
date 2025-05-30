function [boxes,scores,keypoints] = yolov8PosePost(raw; varargin)
% yolov8PosePost  Placeholder post-processing (NMS, thresholding).
% Replace with your own code or port Ultralytics' Python NMS.

% For now, return empties to keep demo compiling.
boxes      = zeros(0,4);
scores     = zeros(0,1);
keypoints  = zeros(0,17,2);
end

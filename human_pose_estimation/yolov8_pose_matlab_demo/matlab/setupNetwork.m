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

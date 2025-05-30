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

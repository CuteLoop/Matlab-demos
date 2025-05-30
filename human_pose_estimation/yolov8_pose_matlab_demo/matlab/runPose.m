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

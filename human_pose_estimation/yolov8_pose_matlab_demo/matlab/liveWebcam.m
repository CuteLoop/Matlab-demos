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

% Brain Tumor Segmentation Demo - Inference Only

% Assert necessary toolboxes are available
assert(all(cellfun(@(t) license('test',t), {'image_toolbox','vision_toolbox','deep_learning_toolbox'})), ...
    'Required toolboxes (Image Processing, Computer Vision, Deep Learning) are missing. Please install them to run the demo.');

% 0. Add helper functions to path
addpath(fileparts(mfilename('fullpath')));

% 1. Create data directory
fprintf("Creating data directory...\n");
dataDir = fullfile(tempdir, "BraTS");
if ~exist(dataDir, 'dir')
    mkdir(dataDir);
end
fprintf("Data directory: %s\n", dataDir);

% 2. Download pretrained network and sample data if missing
fprintf("Checking for required files...\n");
if ~exist(fullfile(dataDir, "brainTumorSegmentation3DUnet_v2.mat"), "file")
    downloadTrainedNetwork(dataDir);
else
    fprintf("Pretrained network found.\n");
end

if ~exist(fullfile(dataDir, "BraTS446.mat"), "file") % Check for one of the sample files
    downloadBraTSSampleTestData(dataDir);
else
    fprintf("Sample test data found.\n");
end

% 3. Load one sample volume and labels
fprintf("Loading sample volume and labels (BraTS446.mat)...\n");
dataFile = fullfile(dataDir, "BraTS446.mat");
load(dataFile, "scanVolume", "labelVolume");
fprintf("Done.\n");

% 4. Build blocked-image pipeline and run semantic segmentation
fprintf("Building blocked-image pipeline and running semantic segmentation...\n");
blockSize = [128 128 128];
borderSize = [32 32 32]; % As per MathWorks example for this network

% Load the network
net = load(fullfile(dataDir, "brainTumorSegmentation3DUnet_v2.mat"));
net = net.net; % The network is stored in a struct field called 'net'

bim = blockedImage(scanVolume, BlockSize=blockSize, BorderSize=borderSize, Padding="symmetric");

% Prepare for semanticseg
% semanticseg expects a dlarray for input with 'SSCB' format (Spatial, Spatial, Channel, Batch)
% Our scanVolume is (H, W, D), so we permute and add channel and batch dimensions.

% Define a function to process each block
processBlock = @(blockStruct) {
    permutedBlock = permute(blockStruct.Data, [1 2 4 3]); % H, W, D -> H, W, 1, D (Channels, Batch for 2D-like slices)
    dlInput = dlarray(single(permutedBlock), 'SSCB');
    segmentedBlock = semanticseg(dlInput, net, OutputFormat="narrow"); % Using "narrow" output format for labels
    % semanticseg returns labels as H x W x NumClasses x NumSlices
    % We need to extract the class with the highest score (argmax) and permute back
    [~, segmentedBlockMax] = max(extractdata(segmentedBlock), [], 3);
    permutedSegmentedBlock = permute(uint8(segmentedBlockMax), [1 2 4 3]); % H, W, 1, D -> H, W, D
    permutedSegmentedBlock
};

% Apply semantic segmentation using blockedImage
% Note: batchSize = 1 is handled by processing each block individually. semanticseg itself can handle batches if prepared correctly.
segmentedVolumeBIM = apply(bim, processBlock, BatchSize=1, PadPartialBlocks=true, OutputSizeMode="same", DisplayWaitbar=true);

% Reconstruct the segmented volume
segmentedVolume = reconstruct(segmentedVolumeBIM);
fprintf("Done.\n");

% 5. Show a side-by-side montage (ground truth vs. prediction, centre slice)
fprintf("Displaying montage of ground truth vs. prediction (centre slice)...\n");
centerSliceIdx = round(size(scanVolume,3)/2);
sliceGT = labelVolume(:,:,centerSliceIdx);
slicePred = segmentedVolume(:,:,centerSliceIdx);

figure;
montage({sliceGT, slicePred}, "Size", [1 2], "BorderSize", 5);
title(['Ground Truth (Left) vs. Prediction (Right) - Slice: ', num2str(centerSliceIdx)]);
fprintf("Done. Please check the figure window.\n");

% 6. Print Sørensen-Dice score for that scan
fprintf("Calculating Sørensen-Dice score for the entire volume...\n");
% The labels are: 1=necrotic/non-enhancing tumor, 2=edema, 4=enhancing tumor. 0=background.
% We evaluate Dice for the whole tumor region (classes 1, 2, 4 combined).
labelVolumeBinary = labelVolume > 0;
segmentedVolumeBinary = segmentedVolume > 0;

diceScore = dice(segmentedVolumeBinary, labelVolumeBinary);
fprintf("Sørensen-Dice Score (whole tumor): %.4f\n", diceScore);

fprintf("Demo finished.\n"); 
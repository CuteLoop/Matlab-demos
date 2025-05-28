function downloadTrainedNetwork(destination)
% downloadTrainedNetwork Downloads the pretrained brain tumor segmentation network.
%   downloadTrainedNetwork(destination) downloads the network to the
%   specified destination directory.

    trainedNetworkFile = "brainTumorSegmentation3DUnet_v2.mat";
    trainedNetworkURL = "https://www.mathworks.com/supportfiles/vision/data/brainTumorSegmentation3DUnet_v2.mat";

    if ~exist(fullfile(destination, trainedNetworkFile), "file")
        fprintf("Downloading pretrained network (1 file, 24 MB)...\n");
        if ~exist(destination, 'dir')
            mkdir(destination);
        end
        try
            websave(fullfile(destination, trainedNetworkFile), trainedNetworkURL);
            fprintf("✔ Pretrained network downloaded to: %s\n", fullfile(destination, trainedNetworkFile));
        catch ME
            fprintf("Error downloading pretrained network: %s\n", ME.message);
            fprintf("Please check your internet connection and the URL: %s\n", trainedNetworkURL);
            % Optionally rethrow the error if you want the script to stop
            % rethrow(ME);
        end
    else
        fprintf("Pretrained network already exists: %s\n", fullfile(destination, trainedNetworkFile));
    end
end 
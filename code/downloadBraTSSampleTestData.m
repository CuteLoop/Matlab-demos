function downloadBraTSSampleTestData(destination)
% downloadBraTSSampleTestData Downloads the sample BraTS test data.
%   downloadBraTSSampleTestData(destination) downloads the data to the
%   specified destination directory.

    sampleDataFile = "BraTSSampleTestData.zip";
    sampleDataURL = "https://www.mathworks.com/supportfiles/vision/data/BraTSSampleTestData.zip";

    if ~exist(fullfile(destination, "BraTS446.mat"), "file") % Check for one of the unzipped files
        fprintf("Downloading sample test data (1 file, 53 MB)...\n");
        if ~exist(destination, 'dir')
            mkdir(destination);
        end
        try
            websave(fullfile(destination, sampleDataFile), sampleDataURL);
            fprintf("✔ Sample data zip downloaded. Unzipping...\n");
            unzip(fullfile(destination, sampleDataFile), destination);
            delete(fullfile(destination, sampleDataFile)); % Remove zip file after extraction
            fprintf("✔ Sample test data extracted to: %s\n", destination);
        catch ME
            fprintf("Error downloading or extracting sample test data: %s\n", ME.message);
            fprintf("Please check your internet connection and the URL: %s\n", sampleDataURL);
            % Optionally rethrow the error if you want the script to stop
            % rethrow(ME);
        end
    else
        fprintf("Sample test data already exists in: %s\n", destination);
    end
end 
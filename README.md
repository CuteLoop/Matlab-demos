# Brain Tumor Segmentation in MATLAB Online (Inference Only)

This repository allows you to run the inference part of MathWorks' "3-D Brain Tumor Segmentation Using Deep Learning" example entirely within MATLAB Online. No local MATLAB installation is required to try out the segmentation on a sample 3D brain scan.

[![Run in MATLAB Online](https://img.shields.io/badge/Run%20in-MATLAB%20Online-orange?logo=MathWorks)](https://matlab.mathworks.com/open/github/v1?repo=CuteLoop/BrainTumorDetection-Matlab&project=project/BrainTumorSegmentation.prj)


## Quick Start

1. Click the "Run in MATLAB Online" badge above.
2. Once the project is open in MATLAB Online, run the following commands in the MATLAB Command Window:

```matlab
cd code
brain_tumor_segmentation_demo
```

This will download the pre-trained network and sample data, then perform segmentation on one scan, display a montage of the ground truth vs. the prediction, and print the Dice similarity coefficient.

## Note

This repository covers the **inference only** portion of the original MathWorks example. Performing the full training of the U-Net model requires the complete BraTS dataset (approximately 7 GB) and a GPU-enabled MATLAB installation or a suitable cloud VM, which is beyond the scope of this lightweight online demo. 

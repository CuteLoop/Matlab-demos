# Brain Tumor Segmentation 3D Project Roadmap

# Phase 0 · Project skeleton & tooling (\~30 min)

| Task                         | Details                                                                                         |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| 0.1 **Toolbox sanity check** | `ver; license('test','Image_Toolbox'); …`  Expect the three toolboxes to return `1` (licensed). |
| 0.2 **Create project root**  | Inside *MATLAB Online* » **Home ▸ New ▸ Project from Folder** → `BrainTumorSeg3D`.              |
| 0.3 **Add folders**          | `code/`, `data/raw/`, `data/processed/`, `figures/`, `experiments/`, `report/`.                 |
| 0.4 **Init Git (optional)**  | `!git init` → commit an empty `.gitignore` (e.g. `*.mat`, `*.zip`, `*.tar`) and `README.md`.    |

**Checkpoint 0** – you can `cd code` and run `pwd` without errors.

---

# Phase 1 · Minimum-viable inference (\~45 min)

| Task                                           | Details      |
| ---------------------------------------------- | ------------ |
| 1.1 **Create temp data dir**                   | \`\`\`matlab |
| dataDir = fullfile(tempdir,"BraTS");           |              |
| if \~exist(dataDir,"dir"), mkdir(dataDir); end |              |

````|
| 1.2 **Grab pretrained weights** | ```matlab
url = "https://…brainTumorSegmentation3DUnet_v2.zip";
downloadTrainedNetwork(url,dataDir);
load(fullfile(dataDir,"brainTumorSegmentation3DUnet_v2.mat"),"trainedNet")
``` |
| 1.3 **Download 5-case sample** | `downloadBraTSSampleTestData(dataDir)` (helper is in example page). |
| 1.4 **Smoke-test inference loop** | ```matlab
testDir = fullfile(dataDir,"sampleBraTSTestSetValid");
files = dir(fullfile(testDir,"imagesTest","*.mat"));
for k = 1:5
  V = load(fullfile(files(k).folder,files(k).name));
  bim = blockedImage(V.cropVol);     % convert volume
  % --- semantic seg in blocks (see Phase 3 for full fn) ---
end
``` |

**Artifacts**: A `log_run1.txt` capturing wall-clock time & memory usage.  
**Checkpoint 1**: middle-slice overlay appears and no OOM on MATLAB Online.

---

# Phase 2 · Pretty visualisations (~30 min)

| Task | Details |
|------|---------|
| 2.1 **Overlay helper** | Put in `code/overlaySlice.m`: draws grayscale MRI with colored label mask (use `labeloverlay`). |
| 2.2 **Loop montage** | Build a 1×2 montage for each case: ground-truth vs. prediction. |
| 2.3 **Export figs** | ```exportgraphics(gcf, fullfile("figures",sprintf("case%d_center.png",k)));``` |

**Artifacts**: 5 PNGs ready for the Results section.  
**Checkpoint 2**: `figures/` folder contains 10 images (5 GT, 5 pred or 5 double-panels).

---

# Phase 3 · Evaluation on the sample set (~40 min)

| Task | Details |
|------|---------|
| 3.1 **Reusable block-seg function** | Save `code/segmentVolumeBlocks.m` – wraps `blockedImage` ➜ `apply` ➜ reconstruct. |
| 3.2 **Metrics** | Write `code/evalSampleSet.m` that builds `imageDatastore` + `pixelLabelDatastore`, runs loop, calls `evaluateSemanticSegmentation`. |
| 3.3 **Write CSV** | Store dataset metrics to `experiments/sample_metrics.csv`. |

**Artifacts**: CSV with GlobalAccuracy/MeanIoU etc.  
**Checkpoint 3**: MeanIoU ≈ 0.95 (matches MathWorks tutorial).

---

# Phase 4 · (Optional) Full BraTS download & preprocess (≈ 1 h download + 30-40 min prep)

| Task | Details |
|------|---------|
| 4.1 **Manual download** | Grab `Task01_BrainTumour.tar` → upload to `data/raw/` (**hint**: use Split-ZIP if browser quota small). |
| 4.2 **Untar in MATLAB Online** | `untar('Task01_BrainTumour.tar','data/raw')`. |
| 4.3 **Run helper** | ```matlab
sourceData = fullfile("data/raw","Task01_BrainTumour");
targetData = fullfile("data/processed");
preprocessBraTSDataset(targetData,sourceData);
``` |
| 4.4 **Split list file** | Save `train.txt`, `val.txt`, `test.txt` listing file names – helps reproducibility. |

**Artifacts**: `preprocess_log.mat` with runtime + voxel counts.  
**Checkpoint 4**: `imagesTr/`, `labelsTr/` appear under processed dir.

---

# Phase 5 · Custom datastores & patch extraction (~30 min)

| Task | Details |
|------|---------|
| 5.1 **`matRead` helper** | Copy from example into `code/matRead.m`. |
| 5.2 **Build datastores** | ```matlab
classNames = ["background","tumor"]; pixelID=[0 1];
voldsTrain = imageDatastore("…/imagesTr",FileExtensions=".mat",ReadFcn=@matRead);
pxdsTrain  = pixelLabelDatastore("…/labelsTr",classNames,pixelID,FileExtensions=".mat",ReadFcn=@matRead);
``` |
| 5.3 **Patch DS** | ```patchSize=[132 132 132]; ppi=16; mb=4;
patchdsTrain = randomPatchExtractionDatastore(voldsTrain,pxdsTrain,patchSize,PatchesPerImage=ppi);
patchdsTrain.MiniBatchSize = mb;
``` |

**Checkpoint 5**: `preview(patchdsTrain)` returns a 4-element cell array.

---

# Phase 6 · Build / tweak U-Net (~20 min)

| Task | Details |
|------|---------|
| 6.1 **Create network** | ```[lgraph,outPatch]=unet3d([132 132 132 4],2,ConvolutionPadding="valid");``` |
| 6.2 **Swap input layer** | Replace normalization, set `Name="input"`. |
| 6.3 **Write `generalizedDiceLoss.m`** | Copy code; put in `code/`. |
| 6.4 **Augment & crop** | Implement `augmentAndCrop3dPatch` in `code/`. (**tip**: skip rotation for val). |

---

# Phase 7 · Training run(s) (2-6 h CPU, ~45 min mid-range GPU)

| Task | Details |
|------|---------|
| 7.1 **Training options** | Use Adam, 50 epochs, initial LR = 5e-4, LR drop ×0.95 every 5 epochs. |
| 7.2 **Start run** | ```[netTr,info] = trainnet(dsTrain,lgraph,@generalizedDiceLoss,opts);``` |
| 7.3 **Save checkpoints** | In `opts`, set `CheckpointPath="experiments/checkpoints"`. |
| 7.4 **Log experiment** | After training, save `info`, final `net`, Git commit hash in `experiments/run_01/`. |

**Artifacts**: `training-progress.png`, `info.mat`, final `trainedNet.mat`.  
**Checkpoint 7**: training curve shows Dice ↑, val plateau not diverging.

---

# Phase 8 · Comprehensive evaluation (~1 h)

| Task | Details |
|------|---------|
| 8.1 **Inference on test set** | Re-use `segmentVolumeBlocks` over 55 test volumes. |
| 8.2 **Confusion matrices** | Save per-volume confusion matrices to `experiments/run_01/cmats.mat`. |
| 8.3 **Metric plots** | Make bar chart of per-case IoU, boxplot of Dice. |
| 8.4 **Compare to baseline** | Table baseline vs. custom in `experiments/comparison.xlsx`. |

---

# Phase 9 · Hyperparameter & ablation studies (advanced)

| Experiment | What to vary | Expected learnings |
|------------|--------------|--------------------|
| 9.A **Patch size sweep** | 96³, 160³ | Trade-off: GPU RAM vs. contextual info. |
| 9.B **Batch size** | 2, 8 | Impact on BN stability. |
| 9.C **Loss function** | Weighted BCE, Tversky | Which handles class imbalance best. |
| 9.D **Border overlap** | 8, 16, 24 voxels | Edge artifact mitigation. |

Automate with `experiments/grid_search.m` that loops settings → saves `summary.csv`.

---

# Phase 10 · Reporting & packaging (~1-2 days)

| Task | Details |
|------|---------|
| 10.1 **Write Live Script outline** | `report/BrainTumorSegmentation.mlx` sections: Intro · Methods · Results · Discussion · Limitations · Future Work. |
| 10.2 **Embed figs & code** | Use `insertCode` / `includeFigure` live-script tools. |
| 10.3 **Auto-generate Tables** | Read `summary.csv` → `uitable` or LaTeX export. |
| 10.4 **Discussion narrative** | - Hardware limits of MATLAB Online - Effect of Dice weighting - Comparison with BraTS leaderboard. |
| 10.5 **Create project archive** | Use **Home ▸ Export** → ZIP; verify README lists: MATLAB RYYx, toolboxes, dataset license. |

**Final deliverables**:  
* `BrainTumorSeg3D.zip` (code + figs + trained net).  
* `BrainTumorSegmentation.pdf` (exported Live Script).  
* Optional 2-min screencast demo GIF.

---

## How to use this roadmap day-to-day

1. Start at the next unchecked task.  
2. Paste the **Dev tasks** code into MATLAB Online (or ask ChatGPT to elaborate).  
3. When you hit the **Checkpoint**, take a screenshot or note the metric.  
4. Push artifacts to Git / save in the indicated folder.  
5. Move on.

By the time you finish Phase 3 you will already have a working demo. Phases 4–9 progressively turn that demo into a reproducible, well-evaluated study, and Phase 10 polishes everything into a publication-ready report.

Happy segmenting!
````

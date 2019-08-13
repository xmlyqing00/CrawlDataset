# Label Dataset for Video Object Segmentation

Yongqing Liang

Aug 12, 2019

## 1. Background

### Dataset format

It includes $M$ video sequences from surveillance cameras which are stored in subfolder. Each video sequence contains $N_i$ frames. We requires pixel-level annotations of each frame.

In the package, you are supposed to see a folder named `FarsonWater_sample`, it contains the original frames. A folder named `FarsonWater_sample_annotations` is the folder containing annotations. It has a subfolder named `worcester`, which contains two **example** **annotations** in JSON format.

### Labeling tool

Labelme is a graphical image annotation tool written in Python. The installation is simple:

```shell
pip install labelme
```

If you are running Python in Windows, Anaconda is recommended. More details can be found in the official website: https://github.com/wkentaro/labelme

## 2. Step-by-step instructions

- **Open** a command console and type `labelme` to run the Labelme program.

- **Open** an image which needs to be annotated. You are supposed to see the screen like this:

  ![](/Ship01/Sources/CrawlDataset/FarsonDigitalWaterCams/instruction_imgs/open.png) 

- **Create a new polygon** (right click on the picture), click the boundary corners of the target object (water in our task) in either clockwise or counter-clockwise. 

  ![](/Ship01/Sources/CrawlDataset/FarsonDigitalWaterCams/instruction_imgs/labeling.png)

- **Click the first point** that you chose to finish labeling. When you select an enclosed polygon, enter `water` as the label name.

  ![](/Ship01/Sources/CrawlDataset/FarsonDigitalWaterCams/instruction_imgs/finish.png)

- **Save** the annotation in JSON format in a separate folder, please follow the file structure tree of the original video sequences. Specifically, the annotations of each video sequence are stored in the same folder. The final file tree is:

  — videos

  ||— video0

  ||||— img0

  ||||— img1

  ||— video1

  ||||— img0

  ||||— img1

  — annotations

  ||— video0

  ||||— img0

  ||||— img1

  ||— video1

  ||||— img0

  ||||— img1


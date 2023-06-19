# Documentat Extraction
<p align="center">
  <img src="pipeline.png" width="800">
</p>

This repo implements the document components extraction (`trained model` and `prediction`) for the following two paper:

(1) DeepPaperComposer: A Simple Solution for Training Data Preparation for Parsing Research Papers. [Paper](https://aclanthology.org/2020.sdp-1.10.pdf)  
(2) Document Domain Randomization for Deep Learning
Document Layout Extraction. [Paper](https://arxiv.org/pdf/2105.14931.pdf)

## Prerequisite
The document extraction model is based on the tensorflow implementation of the Faster-RCNN model by Tensorpack. [Link](https://github.com/tensorpack/tensorpack/tree/master)

1. Install the tensorpack package to your machine following the above link. Create an environment if needed (e.g., frcnn).
2. Check to make sure it is successfully installed - the package path will be saved to environment path, and you can run the BALLOON exmaple provided in ./examples/FasterRCNN/.
3. Clone this repo to a folder on your machine (need not to be under the tensorpack path).

## Trained Model
The trained model consisting of two files is contained in a zip file on google drive.
1. Download the zip file [here](https://drive.google.com/file/d/13i7JaHeQp5hCpyDAVHoGjA1pnhJWTQa_/view?usp=sharing)
2. Unzip them to the root path of the cloned repo where ddr_YOLO_output.py is located.

## Paper Images
To be done

## Extracting...
To be done

## Paper Scraping Example Code
To be done
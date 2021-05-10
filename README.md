# Traffic Detection HLS

Simple implementation of OpenSSD Mobilenet V1 in TensorFlow to manage HLS video stream.

## Usage

To run it, ensure that you have all of the files necessary:

- Video stream data
- Model & class label file
- Installed required packages

And then you can run

HLS Server:

```bash
node generator/index.js
```

Object Detector:

```bash
python main.py
```

## Generating Video Files

As of now, you have to modify the `inputFile` in `modify.js` to the file that you specify. Currently, it's hardcoded to `input.mp4`. Then you can run

```bash
node modify.js
```

## Code Structure

```
traffic-detection-hls
 ├── 📜main.py              # Main Script
 ├── 📂internal             # Internal Code
 │ ├── 📜detector.py
 │ ├── 📜logger.py
 │ ├── 📜model.py
 │ ├── 📜params.py
 │ ├── 📜utils.py
 │ └── 📜visualizer.py
 ├── 📂generator            # HLS Server
 │ ├── 📂streams
 │ ├── 📜modify.js          # Code to generate video stream data
 │ └── 📜index.js           # Code to run HLS Server
 ├── 📂models               # Tensorflow Models Stored
 │ └── 📜labels.txt         # Class labels
 └── 📜requirements.txt       
```

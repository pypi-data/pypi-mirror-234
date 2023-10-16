# Marketing Tool
This package is a tool help you do follow marketing job:

1. Transcribe the speech in video
2. Insert a video into antho video
3. Translate subtitle files
4. Insert text into video
5. Remove water mark from video
6. Convert video

### Install requirement
This program require python 3.9 installed

### How to install
```
pip install Marketingtool
```

### How to use

Transcribe the speech in video
```
Marketingtool --action transcribe -f /path/to/video -o /path/to/captions
```

Insert Video into another video
```
 Marketingtool -a insertVideo -f /path/to/video -o ~/result/video.mp4 --insert-video /insert/video.mp4
```

Translate subtitle files
```
Marketingtool --action translate -f /path/to/subtitle/file -o /path/to/output --source-lang zh-CN --target-lang en
```

Remove watermark from video
```
Marketingtool --action removeWatermark -f /path/to/video -o /path/to/output
```

Insert text into video
```
Marketingtool --action inserttextinvideo -f ./path/to/video --insert-text-path ./path/to/text.txt --insert-text-step 50 --insert-text-num 30 --insert-text-frontsize 20 --insert-text-color green --insert-text-duration 15 -o ./path/to/result
```

Convert video
```
Marketingtool --action convertvideo -f /path/to/video -o /path/video/output
```

### How to develop
You can also install python package comfortably with pip:

```
python3 -m venv path/to/project
cd path/to/project
source ./bin/activate
pip3 install -e .
```

#### Update depend python package for requirement.txt
```
pip3 freeze > requirements.txt
```

#### How to test
test edit movie function
```
python3 -m unittest Tests.test_videoedit.VideoeditTestCase.test_insert_text
```
test remove water mark
```
python3 -m unittest Tests.test_watermark.WatermarkTestCase.test_remove_watermark
```


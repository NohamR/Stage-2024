# Images :
```bash
python3 tracker/track_demo.py --device cpu/0 --obj /tracking_images --detector yolov7 --tracker sort --detector_model_path best.pt --save_dir /tracking --save_images
```

Ex :
```bash
python3 tracker/track_demo.py --device cpu --obj /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking_images --detector yolov7 --tracker sort --detector_model_path /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/yolov7x-datasetv2_2024072211/weights/best.pt --save_dir /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking --save_images
```

# Video :
```bash
python3 tracker/track_demo.py --device cpu/0 --obj video.mp4 --detector yolov7 --tracker sort --detector_model_path best.pt --save_dir /tracking --save_videos
```

Ex :
```bash
python3 tracker/track_demo.py --device cpu --obj /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/sources/2016-100m.mp4 --detector yolov7 --tracker sort --detector_model_path /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/yolov7x-datasetv2_2024072211/weights/best.pt --save_dir /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking --save_videos
```
<!-- 
```bash
python3 tracker/track_demo.py --device cpu --obj /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/2018-100m.mp4 --detector yolov7 --tracker sort --detector_model_path /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/yolov7x-datasetv2_2024072211/weights/best.pt --save_dir /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking --save_videos
``` -->

# Examples :
- [2016-200m_tracked.mp4](../tracking/2016-200m_tracked.mp4) ([2016-200m.mp4](../VoTT-v2/2016-200m.mp4))
- [2018-100m_tracked.mp4](../tracking/2018-100m_tracked.mp4) ([2018-100m.mp4](../VoTT-v2/2018-100m.mp4))
- [2023-100m_tracked.mp4](../tracking/2023-100m_tracked.mp4) ([2023-100m.mp4](../VoTT-v2/2023-100m.mp4))


# Fixes :
```text
self.other_param['stride'] -> 32
np.float -> np.float64 in /tracker/trackers/tracklet.py
````

Error :
```
File "/Users/noham/Documents/GitHub/Stage-2024/test/yolov7-tracker/tracker/trackers/tracklet.py", line 44, in __init__
    self.kalman_filter = MOTION_MODEL_DICT[motion]()
KeyError: 'default'
```

Fix :
```
line 43 :
self.motion = 'sort'
motion = 'sort'
````

Les méthodes de tracking disponibles (seulement testé SortTracker) :
```python
TRACKER_DICT = {
    'sort': SortTracker, 
    'bytetrack': ByteTracker, 
    'botsort': BotTracker, 
    'c_bioutrack': C_BIoUTracker, 
    'ocsort': OCSortTracker, 
    'deepsort': DeepSortTracker
}
```
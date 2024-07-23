Images :
```bash
python3 tracker/track_demo.py --device cpu --obj /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking_images --detector yolov7 --tracker sort --detector_model_path /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/yolov7x-datasetv2_2024072211/weights/best.pt --save_dir /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking --save_images
```

Video :
```bash
python3 tracker/track_demo.py --device cpu --obj /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/sources/2016-100m.mp4 --detector yolov7 --tracker sort --detector_model_path /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/yolov7x-datasetv2_2024072211/weights/best.pt --save_dir /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking --save_videos
```

```bash
python3 tracker/track_demo.py --device cpu --obj /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/vids/400m_2.mp4 --detector yolov7 --tracker sort --detector_model_path /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/yolov7x-datasetv2_2024072211/weights/best.pt --save_dir /Users/noham/Documents/GitHub/Stage-2024/VoTT-v2/tracking --save_videos
```


Fixes :
self.other_param['stride'] -> 32
np.float64 in /tracker/trackers/tracklet.py

File "/Users/noham/Documents/GitHub/Stage-2024/test/yolov7-tracker/tracker/trackers/tracklet.py", line 44, in __init__
    self.kalman_filter = MOTION_MODEL_DICT[motion]()
KeyError: 'default'
line 43 :
self.motion = 'sort'
motion = 'sort'

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
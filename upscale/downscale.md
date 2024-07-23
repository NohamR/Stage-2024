ffmpeg -i input.mp4 -vf "scale=640:360" -c:a copy output.mp4

ffmpeg -i 400m.mp4 -ss 00:00:10.000 -vframes 1 output_frame.jpg 
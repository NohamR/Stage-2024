Doc :
```bash
docker run -it --rm --device=/dev/dri -v $PWD:/host ghcr.io/k4yt3x/video2x:$TAG -i input.mp4 -o output.mp4 -p3 upscale -h 720 -a waifu2x -n3
```

Command :
```bash
docker run -it --rm --device=/dev/dri -v $PWD:/host ghcr.io/k4yt3x/video2x:latest -i 400m.mp4 -o 400m_480p.mp4 -p3 upscale -h 480p -a waifu2x -n3
```
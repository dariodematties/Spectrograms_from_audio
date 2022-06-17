# Spectrograms_from_audio

### For generating the container

`sudo docker build -t python:latest .`

### Building from scratch

`sudo docker build --no-cache --pull -t python:latest .`

### For running the container

`sudo docker run --rm -it --entrypoint bash python:latest`

### And inside the container

`python main.py --i audio_sample/`

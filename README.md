# SenseVoiceDocker

This repository provides a Docker image for [SenseVoice](https://github.com/FunAudioLLM/SenseVoice), enabling you to deploy the SenseVoice ASR service within a Docker container.

## Usage

To run this Docker container, you’ll need a machine with NVIDIA GPU support and the NVIDIA Container Toolkit installed. For detailed installation steps, please refer to the [NVIDIA Container Toolkit](https://notes.xiaowu.ai/%E5%BC%80%E5%8F%91%E7%AC%94%E8%AE%B0/AI/NVIDIA#%E5%AE%89%E8%A3%85+NVIDIA+Container+Toolkit) guide.

### Build the Docker image

```shell
$ docker build -t sensevoice .
```

### Using docker command

```shell
$ docker run -d --name sensevoice_server -p 8080:8080 \
         --runtime=nvidia \
         -e NVIDIA_DRIVER_CAPABILITIES=all \
         -e NVIDIA_VISIBLE_DEVICES=all \
         sensevoice
```

### Using docker compose

1. Create a `docker-compose.yml` file:
```yaml
services:
  sensevoice_server:
    image: sensevoice
    container_name: sensevoice_server
    ports:
      - "8080:8080"
    restart: always
    runtime: nvidia
    environment:
      NVIDIA_DRIVER_CAPABILITIES: all
      NVIDIA_VISIBLE_DEVICES: all
```
2. Start the container:
```shell
$ docker compose up -d
```

## Testing

To test the API, use `curl`:

```shell
# download url audio file example
curl -X 'POST' \
  'http://127.0.0.1:8080/api/v1/asr' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'url=https://iic-sensevoice.ms.show/file=/tmp/gradio/1f7cfa14376cc0bb5f6071a7b0d7bea610842119/zh.mp3'

# upload audio file example
curl -X 'POST' \
  'http://127.0.0.1:8080/api/v1/asr' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@vad_example.wav' \
  -F 'language=auto'
```
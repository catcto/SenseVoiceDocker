# SenseVoiceDocker

This repository provides a Docker image for [SenseVoice](https://github.com/FunAudioLLM/SenseVoice), Deploy the SenseVoice ASR service in a Docker container.

## Usage

To run this Docker container, you’ll need a machine with NVIDIA GPU support and the NVIDIA Container Toolkit installed. For detailed installation steps, please refer to the [NVIDIA Container Toolkit](https://notes.xiaowu.ai/%E5%BC%80%E5%8F%91%E7%AC%94%E8%AE%B0/AI/NVIDIA#%E5%AE%89%E8%A3%85+NVIDIA+Container+Toolkit) guide.

### Build the Docker image

```shell
$ docker build -t sensevoice .
```

### Using docker command

```shell
$ docker run -d --name SenseVoice -p 8080:8080 \
         --runtime=nvidia \
         -e NVIDIA_DRIVER_CAPABILITIES=all \
         -e NVIDIA_VISIBLE_DEVICES=all \
         sensevoice
```

### Using docker compose

1. Create a `docker-compose.yml` file:
```yaml
services:
  SenseVoice:
    image: sensevoice
    container_name: SenseVoice
    restart: always
    ports:
      - "8080:8080"
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
$ curl -X POST http://127.0.0.1:8080/api/v1/asr -H "Content-Type: application/json" -d '{"url": "https://isv-data.oss-cn-hangzhou.aliyuncs.com/ics/MaaS/ASR/test_audio/vad_example.wav", "language": "auto"}'
```

## Performance Testing

The following are the test results when running on an RTX 4090:
```shell
```

The source code is available on [GitHub](https://github.com/catcto/SenseVoiceDocker)
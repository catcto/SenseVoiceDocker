FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

# Install system dependencies
RUN apt-get update && apt-get install -y \
	ffmpeg libsndfile1 git && \
	rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /root/app

# Clone SenseVoice
RUN git clone https://github.com/FunAudioLLM/SenseVoice.git /root/app
# RUN git clone https://gh.catcto.com/https://github.com/FunAudioLLM/SenseVoice.git /root/app

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host pypi.mirrors.ustc.edu.cn

# Set environment variables
ENV API_HOST=0.0.0.0
ENV API_PORT=8080

# Download model
COPY download_model.py .
RUN python download_model.py

# Run the application
COPY api.py .
CMD ["python", "api.py"]
FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04 as base
RUN apt-get update && apt-get install -y \
    ffmpeg \
    tar \
    wget \
    git \
    bash \
    vim

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
ENV PATH="/root/miniconda3/bin:${PATH}"

# Install requirements
RUN conda config --add channels conda-forge
RUN conda install python==3.8
RUN git clone https://github.com/FunAudioLLM/SenseVoice.git /root/SenseVoice
WORKDIR /root/SenseVoice
RUN pip install -r requirements.txt

ENV SENSEVOICE_DEVICE=cuda:0
ENV API_HOST=0.0.0.0
ENV API_PORT=8080
COPY api.py .
RUN python api.py
CMD python api.py --start
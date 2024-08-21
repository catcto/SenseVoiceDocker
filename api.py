#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess
import requests
import os
import uuid

class AsrRequest(BaseModel):
    url: str
    language: str = "auto"

class AsrResponse(BaseModel):
    text: str

app = FastAPI()

model = AutoModel(model="iic/SenseVoiceSmall",
				  vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
				  vad_kwargs={"max_single_segment_time": 30000},
				  trust_remote_code=True,
				  )

def download_file(url: str, save_path: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error downloading file: {str(e)}")

@app.post("/api/v1/asr", response_model=AsrResponse)
def asr(request: AsrRequest):
    unique_id = str(uuid.uuid4())[:8]
    local_file_path = f"/tmp/{unique_id}_{os.path.basename(request.url)}"

    download_file(request.url, local_file_path)
    
    res = model.generate(
        input=local_file_path,
        cache={},
        language=request.language,  # "auto", "zh", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
    )

    text = rich_transcription_postprocess(res[0]["text"])

    if os.path.exists(local_file_path):
        os.remove(local_file_path)

    return AsrResponse(text=text)

if __name__ == "__main__":
    api_port = os.getenv("API_PORT")
    api_host = os.getenv("API_HOST")
    import uvicorn
    uvicorn.run(app, host=api_host, port=int(api_port))
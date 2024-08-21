#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from pydantic import BaseModel
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess


class AsrRequest(BaseModel):
    url: str
    language: str = "auto"


class AsrResponse(BaseModel):
    text: str

model = AutoModel(
    model="iic/SenseVoiceSmall",
    vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    vad_kwargs={"max_single_segment_time": 30000},
    trust_remote_code=True,
)

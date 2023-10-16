#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""constants"""

import re
from typing import Final

USER_AGENT: Final[
    str
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, \
like Gecko) Chrome/111.0.0.0 Safari/537.36"

DEFAULT_ALPACA_7B_API: Final[
    str
] = "https://us-central1-arched-keyword-306918.cloudfunctions.net/run-inference-1"

DEFAULT_GPT_API: Final[str] = "https://apis.scrimba.com/openai/v1/chat/completions"
GPT4_PATTERN: Final[re.Pattern[str]] = re.compile(r"{\"youChatToken\": \"(.*?)\"}")

DEFAULT_POLLINATIONS_API: Final[str] = "https://image.pollinations.ai/prompt/"

DEFAULT_PRODIA_API: Final[str] = "https://api.prodia.com"
DEFAULT_PRODIA_NEG: Final[
    str
] = "(nsfw:1.5),verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.5)\
,cross-eyed,sketches, (worst quality:2), (low quality:2.1), (normal quality:2), \
lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin \
blemishes, bad anatomy, DeepNegative, facing away, tilted head, {Multiple people}, \
lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer \
digits, cropped, worstquality, low quality, normal quality, jpegartifacts, signature\
, watermark, username, blurry, bad feet, cropped, poorly drawn hands, poorly drawn \
face, mutation, deformed, worst quality, low quality, normal quality, jpeg \
artifacts, signature, watermark, extra fingers, fewer digits, extra limbs, extra \
arms,extra legs, malformed limbs, fused fingers, too many fingers, long neck, \
cross-eyed,mutated hands, polar lowres, bad body, bad proportions, gross \
proportions, text, error, missing fingers, missing arms, missing legs, extra digit, \
extra arms, extra leg, extra foot, repeating hair"
DEFAULT_PRODIA_STEPS: Final[int] = 50
DEFAULT_PRODIA_CFG: Final[float] = 9.5
DEFAULT_PRODIA_SLEEP: Final[int] = 1

DEFAULT_DEEPAI_API: Final[str] = "https://api.deepai.org/api"

DEFAULT_INFERKIT_STARNDARD_API: Final[
    str
] = "https://api.inferkit.com/v1/models/standard/generate?useDemoCredits=true"
DEFAULT_INFERKIT_LEN: Final[int] = 200
DEFAULT_INFERKIT_TEMP: Final[float] = 1
DEFAULT_INFERKIT_PROB: Final[float] = 0.9

DEFAULT_DEEPL_API: Final[str] = "https://www2.deepl.com/jsonrpc"

DEFAULT_H2O_FALCON_API: Final[str] = "https://gpt-gm.h2o.ai"

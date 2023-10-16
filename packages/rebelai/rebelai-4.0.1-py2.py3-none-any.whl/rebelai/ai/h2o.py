#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""h2o models"""

import json
import typing
from uuid import uuid4

import aiohttp

from .. import const


async def falcon_40b(
    prompt: str,
    api: str = const.DEFAULT_H2O_FALCON_API,
    temperature: float = 0.6,
    repetition_penalty: float = 1.25,
    request_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
    request_headers: typing.Optional[typing.Dict[str, typing.Any]] = None,
    session_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Optional[str]:
    """falcon model ( 40 b neurons )

    *prompt(str): the prompt passed to the ai
    api(str): api url for the alpaca model
    temperature(float): model creativity
    repetition_penalty(float): how much can it repeat itself
    request_args(dict[str, Any] | None): arguments passed to `session.post()`
    request_headers(dict[str, Any] | None): request headers
    session_args(dict[str, Any] | None): arguments passed to `aiohttp.ClientSession()`

    return(str | None): the ai output as a string or nothing if no output was
                        generated"""

    request_args = request_args or {}

    async with aiohttp.ClientSession(**(session_args or {})) as session:
        headers = {
            "User-Agent": const.USER_AGENT,
            "Referer": api,
            **(request_headers or {}),
        }

        async with session.post(
            f"{api}/settings",
            headers=headers,
            data={
                "ethicsModalAccepted": "true",
                "shareConversationsWithModelAuthors": "true",
                "ethicsModalAcceptedAt": "",
                "activeModel": "h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1",
                "searchEnabled": "true",
            },
            **request_args,
        ), session.post(
            f"{api}/conversation",
            headers=headers,
            json={"model": "h2oai/h2ogpt-gm-oasst1-en-2048-falcon-40b-v1"},
            **request_args,
        ) as conversation_resp:
            conversation_id_data = await conversation_resp.json()
            conversation_id = conversation_id_data["conversationId"]

            async with session.post(
                f"https://gpt-gm.h2o.ai/conversation/{conversation_id}",
                headers={
                    "User-Agent": headers["User-Agent"],
                },
                json={
                    "inputs": prompt,
                    "parameters": {
                        "temperature": temperature,
                        "truncate": 2048,
                        "max_new_tokens": 2048,
                        "do_sample": True,
                        "repetition_penalty": repetition_penalty,
                        "return_full_text": False,
                    },
                    "options": {
                        "id": str(uuid4()),
                        "response_id": str(uuid4()),
                        "is_retry": False,
                        "use_cache": False,
                        "web_search_id": "",
                    },
                },
            ) as response:
                return (
                    json.loads(
                        (await response.text()).replace("\n", "").split("data:")[-1]
                    )["generated_text"]
                    or None
                )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gpt models"""

import typing

import aiohttp

from .. import const


async def gpt3(
    prompt: str,
    api: str = const.DEFAULT_GPT_API,
    profile: str = "",
    request_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
    session_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Optional[str]:
    """access to the gpt3 generation model

    *prompt(str): the prompt passed to the ai
    api(str): openai gpt api
    profile(str): openai gpt3 profile
    request_args(dict[str, Any] | None): arguments passed to `session.post()`
    session_args(dict[str, Any] | None): arguments passed to `aiohttp.ClientSession()`

    return(str | None): the ai output as a string or nothing if no output was
                        generated"""

    async with aiohttp.ClientSession(**(session_args or {})) as session:
        async with session.post(
            url=api,
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": profile},
                    {"role": "user", "content": prompt},
                ],
            },
            **(request_args or {}),
        ) as response:
            return (await response.json())["choices"][0]["message"]["content"] or None


async def gpt4(
    prompt: str,
    api: str = const.DEFAULT_GPT_API,
    profile: str = "",
    request_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
    session_args: typing.Optional[typing.Dict[str, typing.Any]] = None,
) -> typing.Optional[str]:
    """access to the gpt4 generation model

    *prompt(str): the prompt passed to the ai
    api(str): openai gpt api
    profile(str): openai gpt3 profile
    request_args(dict[str, Any] | None): arguments passed to `session.post()`
    session_args(dict[str, Any] | None): arguments passed to `aiohttp.ClientSession()`

    return(str | None): the ai output as a string or nothing if no output was
                        generated"""

    async with aiohttp.ClientSession(**(session_args or {})) as session:
        async with session.post(
            url=api,
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": profile},
                    {"role": "user", "content": prompt},
                ],
            },
            **(request_args or {}),
        ) as response:
            return (await response.json())["choices"][0]["message"]["content"] or None

# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
import pathlib
import os
from typing import Any

import aiofiles
from headless.types import IResponseCache


class DiskResponseCache(IResponseCache):
    __module__: str = 'headless.core'
    cache_dir: pathlib.Path

    def __init__(self, cache_dir: str | pathlib.Path):
        if not isinstance(cache_dir, pathlib.Path):
            cache_dir = pathlib.Path(cache_dir).joinpath('headless.cochise.io')
        self.cache_dir = cache_dir
        if not self.cache_dir.exists():
            os.makedirs(self.cache_dir)
        self.cache_dir = self.cache_dir.absolute()

    def get_local_filepath(self, key: str) -> pathlib.Path:
        return self.cache_dir.joinpath(f'{key}.json')

    def open(self, path: str, mode: str = 'r') -> aiofiles.threadpool.AiofilesContextManager:
        return aiofiles.open(path, mode)

    async def get(self, key: str) -> Any:
        fp = self.get_local_filepath(key)
        if not fp.exists():
            return None
        async with self.open(fp) as f:
            return await f.read()

    async def set(self, key: str, value: str) -> None:
        assert self.cache_dir.exists()
        fp = self.get_local_filepath(key)
        async with self.open(fp, 'w') as f:
            await f.write(value)

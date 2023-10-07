# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

from headless.ext.vies import VIESClient


async def main():
    async with VIESClient.test() as client:
        result = await client.lookup('NL863726392B01')
        print(result.is_valid())


if __name__ == '__main__':
    asyncio.run(main())
# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

from headless.ext.refurbed import DefaultClient as RefurbedClient


async def main():
    async with RefurbedClient() as client:
        for invoice in await client.list_orders("SHIPPED"):
            print(invoice)

if __name__ == '__main__':
    asyncio.run(main())
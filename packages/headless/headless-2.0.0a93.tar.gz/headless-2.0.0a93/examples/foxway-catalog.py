# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import sys
from typing import Any

import yaml
from headless.ext.foxway import FoxwayClient
from headless.ext.foxway.v1 import PricelistProduct


FEATURE_MAPPING: dict[str, str] = {
    'Color'                 : 'color',
    'Appearance'            : 'molano.nl/grade',
    'Boxed'                 : 'packaging',
    'CPU Laptops'           : 'cpu',
    'RAM'                   : 'workmem',
    'Drive'                 : 'primaryhd',
    'Battery status'        : 'battery-health',
    'COA'                   : 'operating-system',
    'LCD Graphics array'    : 'screen-sharpness',
    'GPU laptops'           : 'gpu.laptop',
    'Keyboard'              : 'keyboard-layout',
    'Functionality'         : 'functionality'
}

FEATURE_VALUES: dict[str, dict[str, str]] = {
    'molano.nl/grade': {
        'Grade A+'  : 'A+',
        'Grade A'   : 'A',
        'Grade B+'  : 'B+',
        'Grade B'   : 'B',
        'Grade C+'  : 'C+',
        'Grade C'   : 'C',
    }
}


def get_feature_value(key: str, value: str) -> str:
    try:
        return FEATURE_VALUES[key][value]
    except KeyError:
        return value


async def main():
    async with FoxwayClient() as client:
        params: dict[str, str] = {
            'dimensionGroupId': '11',
            'itemGroupId': '12',
            'vatMargin': 'false'
        }
        products: list[Any] = []
        async for dto in client.listall(PricelistProduct, 'working', params=params):
            must_continue = False
            for dimension in dto.dimension:
                if dimension.key == 'PC Fault Descriptions':
                    #print(f"- Skipping item with fault: {dimension.value}")
                    must_continue = True
                if dimension.key == 'PC Additional Fault':
                    #print(f"- Skipping item with fault: {dimension.value}")
                    must_continue = True
                if dimension.key == 'Battery status' and dimension.value == 'Worn Battery':
                    #print(f"- Skipping item with unacceptable battery status: {dimension.value}")
                    must_continue = True
                if dimension.key == 'Functionality' and dimension.value != 'Working':
                    #print(f"- Skipping item with unacceptable functional state: {dimension.value}")
                    must_continue = True

            if must_continue:
                continue

            print(dto.product_name, file=sys.stderr)
            #for dimension in dto.dimension:
            #    print(f'- {dimension.key}: {dimension.value}', file=sys.stderr)
            product: dict[str, str | list[dict[str, str]] | dict[str, str]] = {
                'product_name': dto.product_name
            }
            product['identifiers'] = {
                'foxway.shop/sku': dto.sku
            }
            product['features'] = [{
                'kind': 'Generic',
                'category': FEATURE_MAPPING[dimension.key],
                'applicable': 'REQ',
                'label': get_feature_value(FEATURE_MAPPING[dimension.key], dimension.value)
            } for dimension in dto.dimension if dimension.key not in {'Battery cycles'}]

            products.append(product)
        print(yaml.safe_dump(products, default_flow_style=False, indent=2))

if __name__ == '__main__':
    asyncio.run(main())
# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import decimal
import logging
from typing import Generator

import pydantic
from headless.ext.shopify import PublicClient
from headless.ext.shopify import PublicProduct
from headless.ext.shopify import PublicProductVariant


#### TO LIBMOLANO ###
import collections
import re
import statistics


APPLE_MODELS: dict[str, str] = {
    'iPad'              : 'IPA',
    'iPad Pro'          : 'IPAP',
    'iPhone XS'         : 'IPHXS',
    'iPhone XS Max'     : 'IPHXSM',
    'iPhone 11'         : 'IPH11',
    'iPhone 11 Pro'     : 'IPH11P',
    'iPhone 12 mini'    : 'IPH12M',
    'iPhone 12'         : 'IPH12',
    'iPhone 12 Pro'     : 'IPH12P',
    'iPhone 12 Pro Max' : 'IPH12PM',
    'iPhone 13 mini'    : 'IPH13M',
    'iPhone 13'         : 'IPH13',
    'iPhone 13 Pro'     : 'IPH13P',
    'iPhone 13 Pro Max' : 'IPH13PM',
    'iPhone SE 2022'    : 'IPHSE3',
    'iPhone 14'         : 'IPH14',
    'iPhone 14 Plus'    : 'IPH14PL',
    'iPhone 14 Pro'     : 'IPH14P',
    'iPhone 14 Pro Max' : 'IPH14PM',
    'Mac'               : 'MCS',
    'Mac Pro'           : 'MCP',
    'MacBook Pro'       : 'MBP',

    # Custom
    '12 Mini'           : 'IPH12M'
}


APPLE_COLORS: dict[str, str] = {
    'Alpine Green'  : 'ALP',
    'Black'         : 'BLA',
    'Black & Slate' : 'BLS',
    'Blue'          : 'BLU',
    'Coral'         : 'COR',
    'Deep Purple'   : 'DEE',
    'Graphite'      : 'GRA',
    'Green'         : 'GRE',
    'Gold'          : 'GOL',
    'Jet Black'     : 'JET',
    'Lilac'         : 'LIL',
    'Midnight'      : 'MID',
    'Midnight Green': 'MIG',
    'Pink'          : 'PIN',
    'Red'           : 'RED',
    'Rose Gold'     : 'ROS',
    'PRODUCT(RED)'  : 'PRO',
    'Pacific Blue'  : 'PAC',
    'Purple'        : 'PUR',
    'Sierra Blue'   : 'SIE',
    'Silver'        : 'SIL',
    'Space Black'   : 'SPB',
    'Space Gray'    : 'SPA',
    'Space Grey'    : 'SPA',
    'Sky Blue'      : 'SKY',
    'Starlight'     : 'STA',
    'White'         : 'WHI',
    'White & Silver': 'WHS',
    'Yellow'        : 'YEL',

    # NL
    'Blauw'         : 'BLU',
    'Grafiet'       : 'GRA',
    'Geel'          : 'YEL',
    'Groen'         : 'GRE',
    'Goud'          : 'GOL',
    'Middernacht'   : 'MID',
    'Rood'          : 'RED',
    'Roze'          : 'PIN',
    'Paars'         : 'PUR',
    'Ruimte Grijs'  : 'SPA',
    'Sterrenlicht'  : 'STA',
    'Wit'           : 'WHI',
    'Zilver'        : 'SIL',
    'Zwart'         : 'BLA',
}

MEMORY_REGEX: re.Pattern[str] = re.compile(
    r'(:?.+)?(16\s?GB|32\s?GB|64\s?GB|128\s?GB|256\s?GB|512\s?GB|1\s?TB)',
    flags=re.IGNORECASE
)


def parse_color(names: list[str]) -> str | None:
    for name in names:
        for color in sorted(APPLE_COLORS.keys(), key=lambda x: -len(x)):
            if str.lower(color) not in name:
                continue
            break
        else:
            color = None
        if color: break
    else:
        color = None
    return APPLE_COLORS.get(color or '')


def parse_model(names: list[str]) -> dict[str, str | None]:
    params: dict[str, str | None] = {}
    for name in names:
        for model in sorted(APPLE_MODELS.keys(), key=lambda x: -len(x)):
            if str.lower(model) not in name:
                continue
            break
        else:
            continue
        params.update({
            'model': model
        })
        sku = params['base_sku'] = APPLE_MODELS.get(model or '')
        if sku and sku.startswith('IPA'):
            params.update({
                'generation': parse_ipad_generation(names),
                'screen': parse_ipad_screen_size(names)
            })
    return params


def parse_ipad_capability(names: list[str]):
    for name in names:
        if 'cellular' in name:
            cap = 'C'
            break
        if 'wifi' in name:
            cap = 'W'
            break
    else:
        raise NotImplementedError
    return cap


def parse_ipad_generation(names: list[str]) -> str:
    for name in names:
        m = re.match(r'.*[^0-9](([0-9]+)(st|nd|rd|th))', name, flags=re.IGNORECASE)
        if not m:
            continue
        gen = str.zfill(m.group(2), 2)
    else:
        gen = '01'
    return gen


def parse_ipad_screen_size(names: list[str]) -> str:
    for name in names:
        m = re.match(r'.*(10.2|10.9|11|12.9)-inch', name, flags=re.IGNORECASE)
        if m is None:
            assert 'inch' not in name
            continue
        size = str.split(m.group(1), '.')[0]
    else:
        size = '00'
    return size


def parse_memory(names: list[str]) -> str | None:
    for name in names:
        m = MEMORY_REGEX.match(name)
        if m is None:
            continue
        mem = str.upper(re.sub(r'\s', '', m.group(2)))
        break
    else:
        mem = None
    return mem



def parse_product(names: list[str]) -> str | None:
    names = [str.lower(x) for x in names]
    props = [
        parse_model(names),
        parse_color(names),
        parse_memory(names)
    ]
    if any([x is None for x in props]):
        return None
    model, color, memory = props

    assert model is not None
    sku = f'{model}{color}{memory}'
    if model.startswith('IPA'):
        sku += parse_ipad_capability(names)
    return sku




ZAREUR: decimal.Decimal = decimal.Decimal('0.052')



class AppleProduct(pydantic.BaseModel):
    color: str
    generation: str | None = None
    memory: str
    model: str
    price: decimal.Decimal
    price_eur: decimal.Decimal
    screen: str | None = None
    base_sku: str

    @property
    def sku(self) -> str:
        if not str.startswith(self.base_sku, 'IPH'):
            raise NotImplementedError
        return f'{self.base_sku}{self.color}{self.memory}'


class ShopifyProductPriceFinder:
    currency_pair: decimal.Decimal = decimal.Decimal(1)

    def __init__(
        self,
        domain: str | None = None,
        currency_pair: decimal.Decimal | None = None
    ):
        self.currency_pair = currency_pair or self.currency_pair
        self.domain = domain or self.domain

    async def latest(self):
        prices: collections.defaultdict[str, list[decimal.Decimal]] = collections.defaultdict(list)
        async with PublicClient(self.domain) as client:
            async for product in client.listall(PublicProduct):
                for product in self.parse_products(product):
                    prices[product.base_sku + 'MIX' + product.memory].append(product.price_eur)
        return {sku: statistics.median(values) for sku, values in prices.items()}

    def parse_products(self, product: PublicProduct) -> Generator[AppleProduct, None, None]:
        for variant in product.variants:
            names: list[str] = [
                str.lower(product.title),
                str.lower(variant.title)
            ]
            params: dict[str, decimal.Decimal | str | None] = {
                **parse_model(names),
                'color': parse_color(names),
                'memory': parse_memory(names) or self.parse_memory(product, variant),
                'price': variant.price,
                'price_eur': variant.price * self.currency_pair
            }
            if not str.startswith(str(params.get('base_sku') or ''), 'IPH'):
                continue
            try:
                yield AppleProduct.parse_obj(params)
            except pydantic.ValidationError:
                print("Unable to parse", product.title, variant, params)
                continue

    def parse_memory(
        self,
        product: PublicProduct,
        variant: PublicProductVariant
    ) -> str | None:
        return None


class GorillaPhonesPriceFinder(ShopifyProductPriceFinder):
    domain: str = 'gorillaphones.co.za'

    def parse_memory(
        self,
        product: PublicProduct,
        variant: PublicProductVariant
    ) -> str | None:
        if str.startswith(variant.title, variant.option1 or '')\
        and variant.option1 in {'64', '128', '256', '512'}:
            return f'{variant.option1}GB'
        return None
    

async def main():
    logger: logging.Logger = logging.getLogger('headless.client')
    logger.setLevel(logging.INFO)
    finder1: GorillaPhonesPriceFinder = GorillaPhonesPriceFinder(currency_pair=ZAREUR)
    finder2: ShopifyProductPriceFinder = ShopifyProductPriceFinder('macshack.co.za', currency_pair=ZAREUR)
    finder3: ShopifyProductPriceFinder = ShopifyProductPriceFinder('buymolano.com')
    finder4: ShopifyProductPriceFinder = ShopifyProductPriceFinder('refurbcity.nl')
    finder5: ShopifyProductPriceFinder = ShopifyProductPriceFinder('unboxxed.co.za', currency_pair=ZAREUR)
    gorilla = await finder1.latest()
    macshack =await finder2.latest()
    buymolano = await finder3.latest()
    unboxxed = await finder5.latest()
    await finder4.latest()
    for k, v in buymolano.items():
        row: list[str | decimal.Decimal] = [k, v]
        if k in gorilla:
            row.append(gorilla[k] - v)
        else:
            row.append(decimal.Decimal(0))
        if k in macshack:
            row.append(macshack[k] - v)
        else:
            row.append(decimal.Decimal(0))
        if k in unboxxed:
            row.append(unboxxed[k] - v)
        else:
            row.append(decimal.Decimal(0))
        print(row)

    return
    async with PublicClient("gorillaphones.co.za") as client:
        async for product in client.listall(PublicProduct):
            print(product.title)
            for variant in product.variants:
                sku = parse_product([product.title, variant.title])
                #sku = parse_product(product.title)
                #if sku is None or (not sku.startswith('IPA') and not sku.startswith('IPH')):
                #    continue
                print(f' .   {sku}: EUR {variant.price * ZAREUR}', variant.title)


if __name__ == '__main__':
    asyncio.run(main())
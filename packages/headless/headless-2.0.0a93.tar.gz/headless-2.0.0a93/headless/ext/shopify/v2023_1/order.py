# Copyright (C) 2022 Cochise Ruhulessin # type: ignore
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import datetime
import decimal
from typing import Any

from .baseresource import BaseResource
from .clientdetails import ClientDetails
from .customer import Customer
from .customeraddress import CustomerAddress
from .metafield import Metafield
from .metafieldset import MetafieldSet
from .orderdiscountapplication import OrderDiscountApplication
from .orderdiscountcode import OrderDiscountCode
from .orderfinancialstatus import OrderFinancialStatus
from .orderfulfillment import OrderFulfillment
from .orderfulfillmentstatus import OrderFulfillmentStatus
from .orderlineitem import OrderLineItem
from .ordernoteattribute import OrderNoteAttribute
from .orderpaymentdetails import OrderPaymentDetails
from .orderprocessingmethod import OrderProcessingMethod
from .ordershippingline import OrderShippingLine
from .ordertotalamount import OrderTotalAmount
from .ordertax import OrderLineTax


class Order(BaseResource):
    app_id: int
    billing_address: CustomerAddress | None
    browser_ip: str
    buyer_accepts_marketing: bool
    cancel_reason: str | None
    cancelled_at: datetime.datetime | None
    cart_token: str | None
    checkout_token: str | None
    client_details: ClientDetails
    closed_at: datetime.datetime | None
    company: dict[str, Any] | None
    created_at: datetime.datetime
    currency: str
    current_total_discounts: decimal.Decimal
    current_total_discounts_set: OrderTotalAmount | None
    current_total_duties_set: OrderTotalAmount | None
    current_total_price: decimal.Decimal
    current_total_price_set: OrderTotalAmount | None
    current_subtotal_price: decimal.Decimal
    current_subtotal_price_set: OrderTotalAmount | None
    current_total_tax: decimal.Decimal
    current_total_tax_set: OrderTotalAmount | None
    customer: Customer | None
    customer_locale: str | None
    discount_applications: list[OrderDiscountApplication] = []
    discount_codes: list[OrderDiscountCode] = []
    email: str | None
    estimated_taxes: bool
    financial_status: OrderFinancialStatus
    fulfillments: list[OrderFulfillment] = []
    fulfillment_status: OrderFulfillmentStatus | None
    gateway: str | None
    id: int
    landing_site: str | None
    line_items: list[OrderLineItem] = []
    location_id: int | None
    merchant_of_record_app_id: int | None
    name: str
    note: str | None
    note_attributes: list[OrderNoteAttribute]
    number: int
    order_number: int
    original_total_duties_set: OrderTotalAmount | None
    order_status_url: str
    payment_details: OrderPaymentDetails | None = None
    #TODO: payment_terms
    payment_gateway_names: list[str]
    phone: str | None
    presentment_currency: str
    processed_at: datetime.datetime | None
    processing_method: OrderProcessingMethod
    referring_site: str | None
    #TODO: refunds
    shipping_address: CustomerAddress | None
    shipping_lines: list[OrderShippingLine] = []
    source_name: str
    source_identifier: str | None
    source_url: str | None

    # This value is documented as a number but is actually a string
    subtotal_price: decimal.Decimal
    subtotal_price_set: OrderTotalAmount | None
    tags: str
    tax_lines: list[OrderLineTax] = []
    taxes_included: bool
    test: bool
    token: str
    total_discounts: decimal.Decimal
    total_discounts_set: OrderTotalAmount | None
    total_line_items_price: decimal.Decimal
    total_line_items_price_set: OrderTotalAmount | None
    total_outstanding: decimal.Decimal
    total_price: decimal.Decimal
    total_price_set: OrderTotalAmount | None
    total_shipping_price_set: OrderTotalAmount | None
    total_tax: decimal.Decimal
    total_tax_set: OrderTotalAmount | None
    total_tip_received: decimal.Decimal
    total_weight: int
    updated_at: datetime.datetime | None
    user_id: int | None

    @classmethod
    def get_metafields_url(cls, resource_id: int) -> str:
        return f'{cls._meta.base_endpoint}/{resource_id}/metafields.json'

    async def create_metafield(self, key: str, value: Any) -> Metafield:
        params = {'value': value}
        params['namespace'], params['key'] = str.split(key, '.')
        return await self._client.create(Metafield, params, url=self.get_metafields_url(self.id))

    async def get_metafields(self) -> MetafieldSet:
        """Return the metafields defined for this resource."""
        iterator = self._client.listall(
            Metafield,
            params={
                'metafield[owner_resource]': str.lower(type(self).__name__),
                'metafield[owner_id]': self.id
            }
        )
        return MetafieldSet(self._client, self, [x async for x in iterator])

    def get_persist_url(self) -> str:
        return self.get_retrieve_url(self.id)

    def total_ordered_price(self) -> decimal.Decimal:
        return sum([x.price for x in self.line_items])

    class Meta:
        base_endpoint: str = '/2023-01/orders'
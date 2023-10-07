# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pydantic
from canonical import ResourceName


class ProductStock(pydantic.BaseModel):
    idwarehouse: int
    stock: int
    reserved: int
    reservedbackorders: int
    reservedpicklists: int
    reservedallocations: int
    freestock: int

    def get_resource_name(self, domain: str) -> ResourceName:
        return ResourceName(f'//{domain}/warehouses/{self.idwarehouse}')
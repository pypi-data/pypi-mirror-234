# Copyright (C) 2022 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os

from .client import RefurbishedClient


class DefaultRefurbishedClient(RefurbishedClient):

    def __init__(self):
        super().__init__(api_token=os.environ['REFURBISHED_API_KEY'])
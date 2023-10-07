# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import datetime
import urllib.parse
from typing import Any

import pydantic
from canonical import EmailAddress

from .address import Address
from .jsonwebtoken import JSONWebToken


TRUSTED_ISSUERS: set[str] = {
    'https://accounts.google.com'
}

TRUSTED_DOMAINS: dict[str, set[str]] = collections.defaultdict(set, {
    'api.login.yahoo.com': {
        'yahoo.com',
        'yahoomail.com',
        'yahoo.co.in',
        'yahoo.co.uk',
        'yahoo.fr',
        'yahoo.es',
        'rocketmail.com',
    },
    'login.microsoftonline.com': {
        'hotmail.com',
        'live.com',
        'outlook.com',
    }
})


class BaseClaimSet(JSONWebToken):
    name: str | None = pydantic.Field(
        default=None,
        title="Name",
        description=(
            "End-User's full name in displayable form including all name "
            "parts, possibly including titles and suffixes, ordered "
            "according to the End-User's locale and preferences."
        )
    )

    given_name: str | None = pydantic.Field(
        default=None,
        title="Given name",
        description=(
            "Given name(s) or first name(s) of the End-User. Note that in some "
            "cultures, people can have multiple given names; all can be present, "
            "with the names being separated by space characters."
        )
    )

    family_name: str | None = pydantic.Field(
        default=None,
        title="Family name",
        description=(
            "Surname(s) or last name(s) of the End-User. Note that in some cultures, "
            "people can have multiple family names or no family name; all can be "
            "present, with the names being separated by space characters."
        )
    )

    middle_name: str | None = pydantic.Field(
        default=None,
        title="Middle name",
        description=(
            "Middle name(s) of the End-User. Note that in some cultures, people can "
            "have multiple middle names; all can be present, with the names being "
            "separated by space characters. Also note that in some cultures, middle "
            "names are not used."
        )
    )

    nickname: str | None = pydantic.Field(
        default=None,
        title="Nickname",
        description=(
            "Casual name of the End-User that may or may not be the same as "
            "the `given_name`. For instance, a `nickname` value of `Mike` "
            "might be returned alongside a `given_name` value of `Michael`."
        )
    )

    preferred_username: str | None = pydantic.Field(
        default=None,
        title="Preferred username",
        description=(
            "Shorthand name by which the End-User wishes to be referred to "
            "at the RP, such as `janedoe` or `j.doe`. This value MAY be "
            "any valid JSON string including special characters such as "
            "`@`, `/`, or whitespace. The RP MUST NOT rely upon this "
            "value being unique, as discussed in Section 5.7 of the OpenID "
            "Connect Core 1.0 specification."
        )
    )

    profile: str | None = pydantic.Field(
        default=None,
        title="Profile URL",
        description=(
            "URL of the End-User's profile page. The contents "
            "of this Web page SHOULD be about the End-User."
        )
    )

    picture: str | None = pydantic.Field(
        default=None,
        title="Picture",
        description=(
            "URL of the End-User's profile picture. This URL MUST refer "
            "to an image file (for example, a PNG, JPEG, or GIF image "
            "file), rather than to a Web page containing an image. Note "
            "that this URL SHOULD specifically reference a profile photo "
            "of the End-User suitable for displaying when describing the "
            "End-User, rather than an arbitrary photo taken by the End-User."
        )
    )

    website: str | None = pydantic.Field(
        default=None,
        title="Website",
        description=(
            "URL of the End-User's Web page or blog. This Web page SHOULD "
            "contain information published by the End-User or an organization "
            "that the End-User is affiliated with."
        )
    )

    email: EmailAddress | None = pydantic.Field(
        default=None,
        title="Email",
        description=(
            "End-User's preferred e-mail address. Its value MUST conform to the "
            "RFC 5322 addr-spec syntax. The RP MUST NOT rely upon this value being "
            "unique, as discussed in Section 5.7 of the OpenID "
            "Connect Core 1.0 specification."
        )
    )

    email_verified: bool = pydantic.Field(
        default=False,
        title="Email verified?",
        description=(
            "Is `true` if the End-User's e-mail address has been verified; "
            "otherwise `false`. When this Claim Value is `true`, this means "
            "that the OP took affirmative steps to ensure that this e-mail "
            "address was controlled by the End-User at the time the verification "
            "was performed. The means by which an e-mail address is verified "
            "is context-specific, and dependent upon the trust framework or "
            "contractual agreements within which the parties are operating."
        )
    )

    gender: str | None = pydantic.Field(
        default=None,
        title="Gender",
        description=(
            "End-User's gender. Values defined by this specification are "
            "`female` and `male`. Other values MAY be used when neither "
            "of the defined values are applicable."
        )
    )

    birthdate: datetime.date | str | None = pydantic.Field(
        default=None,
        title="Birthdate",
        description=(
            "End-User's birthday, represented as an ISO 8601:2004 `YYYY-MM-DD` "
            "format. The year MAY be `0000`, indicating that it is omitted. "
            "To represent only the year, `YYYY` format is allowed. Note that "
            "depending on the underlying platform's date related function, "
            "providing just year can result in varying month and day, so the "
            "implementers need to take this factor into account to correctly "
            "process the dates."
        )
    )

    zoneinfo: str | None = pydantic.Field(
        default=None,
        title="Timezone",
        description=(
            "String from zoneinfo time zone database representing the "
            "End-User's time zone. For example, `Europe/Paris` or "
            "`America/Los_Angeles`."
        )
    )

    locale: str | None = pydantic.Field(
        default=None,
        title="Locale",
        description=(
            "End-User's locale, represented as a BCP47 language tag. This is "
            "typically an ISO 639-1 Alpha-2 language code in lowercase and "
            "an ISO 3166-1 Alpha-2 country code in uppercase, separated by "
            "a dash. For example, `en-US` or `fr-CA`. As a compatibility "
            "note, some implementations have used an underscore as the "
            "separator rather than a dash, for example, `en_US`; "
            "Relying Parties MAY choose to accept this locale syntax as well."
        )
    )

    phone_number: str | None = pydantic.Field(
        default=None,
        title="Phonenumber",
        description=(
            "End-User's preferred telephone number. E.164 is RECOMMENDED as "
            "the format of this Claim, for example, `+1 (425) 555-1212` "
            "or `+56 (2) 687 2400`. If the phone number contains an extension, "
            "it is RECOMMENDED that the extension be represented using the "
            "RFC 3966 extension syntax, for example, `+1 (604) 555-1234;ext=5678`."
        )
    )

    phone_number_verified: bool = pydantic.Field(
        default=False,
        title="Phonenumber verified?",
        description=(
            "Is `true` if the End-User's phone number has been verified; otherwise "
            "`false`. When this Claim Value is `true`, this means that the OP took "
            "affirmative steps to ensure that this phone number was controlled by "
            "the End-User at the time the verification was performed. The means "
            "by which a phone number is verified is context-specific, and "
            "dependent upon the trust framework or contractual agreements within "
            "which the parties are operating. When `true`, the phone_number Claim "
            "MUST be in E.164 format and any extensions MUST be represented in "
            "RFC 3966 format."
        )
    )

    address: Address | None = pydantic.Field(
        default=None,
        title="Address",
        description=(
            "End-User's preferred postal address. The value of "
            "the address member is a JSON structure containing "
            "some or all of the members defined in Section 5.1.1 "
            "of the OpenID Connect Core 1.0 specification."
        )
    )

    updated_at: int |  None = pydantic.Field(
        default=None,
        title="Updated",
        description=(
            "Time the End-User's information was last updated. Its "
            "value is a JSON number representing the number of "
            "seconds from 1970-01-01T0:0:0Z as measured in UTC "
            "until the date/time."
        )
    )

    # Extension claims
    icg: bool | None = pydantic.Field(
        default=None,
        title="Incognito?",
        description=(
            "Indicates if the End-User used an incognito user-agent "
            "when authorization the request."
        )
    )

    initials: str | None = pydantic.Field(
        default=None,
        title="Initials",
        description=(
            "The initials of the End-User."
        )
    )

    uai: str | None = pydantic.Field(
        default=None,
        title="User Agent ID",
        description=("Identifies the user agent.")
    )

    sct: str | None = pydantic.Field(
        default=None,
        title="Sector",
        description=(
            "The sector identifier of the Subject identity."
        )
    )

    @pydantic.root_validator # type: ignore
    def preprocess(
        cls,
        values: dict[str, Any]
    ) -> dict[str, Any]:
        # TODO: Refactor this into a framework. Now works for Google and
        # Microsoft only.
        email: EmailAddress | None = values.get('email')
        email_verified = values.setdefault('email_verified', False)
        iss: str | None = values.get('iss')
        if email and iss is not None:
            assert isinstance(email, EmailAddress)
            if email_verified:
                values['email_verified'] = iss in TRUSTED_ISSUERS
            else:
                p = urllib.parse.urlparse(str(iss))
                values['email_verified'] = email.domain in TRUSTED_DOMAINS[p.netloc]

        return values

    @pydantic.validator('locale') # type: ignore
    def preprocess_locale(cls, value: str | None) -> str | None:
        if value is not None:
            value = str.replace(value, '_', '-')
        return value
    
    @pydantic.validator('updated_at', pre=True) # type: ignore
    def preprocess_updated_at(
        cls,
        value: int | datetime.datetime | None
    ) -> int | None:
        if isinstance(value, datetime.datetime):
            value = int(value.timestamp())
        return value


class ClaimSet(BaseClaimSet):
    sub: str = pydantic.Field(
        default=...,
        title="Subject",
        description='Subject - Identifier for the End-User at the Issuer.'
    )
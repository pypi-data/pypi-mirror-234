# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import enum


class WebhookType(str, enum.Enum):
    account_deactivated         = "account.deactivated"
    account_deleted             = "account.deleted"
    company_added               = "company.added"
    company_deleted             = "company.deleted"
    company_updated             = "company.updated"
    contact_added               = "contact.added"
    contact_deleted             = "contact.deleted"
    contact_linked              = "contact.linkedToCompany"
    contact_unlinked            = "contact.unlinkedFromCompany"
    contact_updated             = "contact.updated"
    creditnote_booked           = "creditNote.booked"
    creditnote_deleted          = "creditNote.deleted"
    creditnote_sent             = "creditNote.sent"
    creditnote_updated          = "creditNote.updated"
    deal_created                = "deal.created"
    deal_deleted                = "deal.deleted"
    deal_lost                   = "deal.lost"
    deal_moved                  = "deal.moved"
    deal_updated                = "deal.updated"
    deal_won                    = "deal.won"
    invoice_booked              = "invoice.booked"
    invoice_deleted             = "invoice.deleted"
    invoice_drafted             = "invoice.drafted"
    invoice_payment_registered  = "invoice.paymentRegistered"
    invoice_payment_removed     = "invoice.paymentRemoved"
    invoice_sent                = "invoice.sent"
    invoice_updated             = "invoice.updated"
    milestone_created           = "milestone.created"    
    milestone_updated           = "milestone.updated"
    product_added               = "product.added"
    project_created             = "project.created"
    project_deleted             = "project.deleted"
    project_updated             = "project.updated"
    subscription_added          = "subscription.added"
    subscription_deactivated    = "subscription.deactivated"
    subscription_deleted        = "subscription.deleted"
    subscription_updated        = "subscription.updated"
    timetracking_added          = "timeTracking.added"
    timetracking_deleted        = "timeTracking.deleted"
    timetracking_updated        = "timeTracking.updated"
    user_deactivated            = "user.deactivated"
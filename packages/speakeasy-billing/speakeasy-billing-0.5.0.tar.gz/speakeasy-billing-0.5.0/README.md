# billing

<div align="left">
    <a href="https://speakeasyapi.dev/"><img src="https://custom-icon-badges.demolab.com/badge/-Built%20By%20Speakeasy-212015?style=for-the-badge&logoColor=FBE331&logo=speakeasy&labelColor=545454" /></a>
    <a href="https://github.com/speakeasy-sdks/billing-python.git/actions"><img src="https://img.shields.io/github/actions/workflow/status/speakeasy-sdks/bolt-php/speakeasy_sdk_generation.yml?style=for-the-badge" /></a>
    
</div>

<!-- Start SDK Installation -->
## SDK Installation

```bash
pip install speakeasy-billing
```
<!-- End SDK Installation -->

## SDK Example Usage
<!-- Start SDK Example Usage -->
```python
import billing
from billing.models import shared

s = billing.Billing(
    security=shared.Security(
        api_key_auth="",
    ),
)

req = shared.NewCustomer(
    billing_address=shared.NewCustomerBillingAddress(
        country='US',
    ),
    metadata=shared.NewCustomerMetadata(),
    shipping_address=shared.NewCustomerShippingAddress(
        country='US',
    ),
    tax_id=shared.NewCustomerCustomerTaxID(
        country='Latvia',
        type='Configuration Money',
        value='Cambridgeshire grey technology',
    ),
    timezone='Etc/UTC',
)

res = s.customer.create(req)

if res.customer is not None:
    # handle response
```
<!-- End SDK Example Usage -->

<!-- Start SDK Available Operations -->
## Available Resources and Operations


### [availability](docs/sdks/availability/README.md)

* [ping](docs/sdks/availability/README.md#ping) - Check availability

### [coupon](docs/sdks/coupon/README.md)

* [archive](docs/sdks/coupon/README.md#archive) - Archive coupon
* [create](docs/sdks/coupon/README.md#create) - Create coupon
* [fetch](docs/sdks/coupon/README.md#fetch) - Fetch coupon
* [list](docs/sdks/coupon/README.md#list) - List coupons
* [list_subscriptions](docs/sdks/coupon/README.md#list_subscriptions) - List coupon subscriptions

### [credit](docs/sdks/credit/README.md)

* [add_by_external_id](docs/sdks/credit/README.md#add_by_external_id) - Create ledger entry by external ID
* [create](docs/sdks/credit/README.md#create) - Create ledger entry
* [fetch](docs/sdks/credit/README.md#fetch) - Fetch customer credit balance
* [fetch_by_external_id](docs/sdks/credit/README.md#fetch_by_external_id) - Fetch customer credit balance by external customer id
* [fetch_ledger](docs/sdks/credit/README.md#fetch_ledger) - Fetch customer credits ledger
* [fetch_ledger_external_id](docs/sdks/credit/README.md#fetch_ledger_external_id) - Fetch credits ledger by external ID

### [credit_note](docs/sdks/creditnote/README.md)

* [fetch](docs/sdks/creditnote/README.md#fetch) - Fetch credit note
* [list](docs/sdks/creditnote/README.md#list) - List credit notes

### [customer](docs/sdks/customer/README.md)

* [amend](docs/sdks/customer/README.md#amend) - Amend usage
* [amend_by_external_id](docs/sdks/customer/README.md#amend_by_external_id) - Amend usage by external ID
* [create](docs/sdks/customer/README.md#create) - Create customer
* [create_balance_transaction](docs/sdks/customer/README.md#create_balance_transaction) - Create customer balance transaction
* [delete](docs/sdks/customer/README.md#delete) - Delete customer
* [fetch](docs/sdks/customer/README.md#fetch) - Fetch customer
* [fetch_by_external_id](docs/sdks/customer/README.md#fetch_by_external_id) - Fetch customer by external ID
* [fetch_costs](docs/sdks/customer/README.md#fetch_costs) - Fetch customer costs
* [fetch_costs_by_external_id](docs/sdks/customer/README.md#fetch_costs_by_external_id) - Fetch customer costs by external ID
* [fetch_transactions](docs/sdks/customer/README.md#fetch_transactions) - List balance transactions
* [list](docs/sdks/customer/README.md#list) - List customers
* [update_by_external_id](docs/sdks/customer/README.md#update_by_external_id) - Update customer by external ID
* [update_customer](docs/sdks/customer/README.md#update_customer) - Update customer

### [event](docs/sdks/event/README.md)

* [amend](docs/sdks/event/README.md#amend) - Amend event
* [close_backfill](docs/sdks/event/README.md#close_backfill) - Close backfill
* [create](docs/sdks/event/README.md#create) - Create backfill
* [deprecate_event](docs/sdks/event/README.md#deprecate_event) - Deprecate event
* [ingest](docs/sdks/event/README.md#ingest) - Ingest events
* [list_backfills](docs/sdks/event/README.md#list_backfills) - List backfills
* [revert_backfill](docs/sdks/event/README.md#revert_backfill) - Revert backfill
* [search](docs/sdks/event/README.md#search) - Search events

### [invoice](docs/sdks/invoice/README.md)

* [create](docs/sdks/invoice/README.md#create) - Create invoice line item
* [fetch](docs/sdks/invoice/README.md#fetch) - Fetch invoice
* [fetch_upcoming](docs/sdks/invoice/README.md#fetch_upcoming) - Fetch upcoming invoice
* [issue](docs/sdks/invoice/README.md#issue) - Issue an invoice
* [list](docs/sdks/invoice/README.md#list) - List invoices
* [void](docs/sdks/invoice/README.md#void) - Void invoice

### [plan](docs/sdks/plan/README.md)

* [fetch](docs/sdks/plan/README.md#fetch) - Fetch plan
* [get_by_external_id](docs/sdks/plan/README.md#get_by_external_id) - Fetch plan by external ID
* [list](docs/sdks/plan/README.md#list) - List plans

### [subscription](docs/sdks/subscription/README.md)

* [cancel](docs/sdks/subscription/README.md#cancel) - Cancel subscription
* [create](docs/sdks/subscription/README.md#create) - Create subscription
* [fetch](docs/sdks/subscription/README.md#fetch) - Fetch subscription
* [fetch_costs](docs/sdks/subscription/README.md#fetch_costs) - Fetch subscription costs
* [fetch_schedule](docs/sdks/subscription/README.md#fetch_schedule) - Fetch subscription schedule
* [fetch_usage](docs/sdks/subscription/README.md#fetch_usage) - Fetch subscription usage
* [list](docs/sdks/subscription/README.md#list) - List subscriptions
* [schedule_plan_change](docs/sdks/subscription/README.md#schedule_plan_change) - Schedule plan change
* [unschedule_cancellation](docs/sdks/subscription/README.md#unschedule_cancellation) - Unschedule subscription cancellation
* [unschedule_plan_change](docs/sdks/subscription/README.md#unschedule_plan_change) - Unschedule plan change
* [update_fixed_fee_quantity](docs/sdks/subscription/README.md#update_fixed_fee_quantity) - Update price quantity
<!-- End SDK Available Operations -->

<!-- Start Dev Containers -->

<!-- End Dev Containers -->

<!-- Start Pagination -->
# Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
<!-- End Pagination -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release!

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)

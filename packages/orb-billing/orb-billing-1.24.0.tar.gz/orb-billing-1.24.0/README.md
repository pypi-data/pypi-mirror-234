# orb

<!-- Start SDK Installation -->
## SDK Installation

```bash
pip install orb-billing
```
<!-- End SDK Installation -->

## SDK Example Usage
<!-- Start SDK Example Usage -->
```python
import orb
from orb.models import shared

s = orb.Orb(
    security=shared.Security(
        api_key_auth="",
    ),
)


res = s.availability.ping()

if res.ping_response is not None:
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
* [fetch_balance](docs/sdks/credit/README.md#fetch_balance) - Fetch customer credit balance
* [fetch_balance_by_external_id](docs/sdks/credit/README.md#fetch_balance_by_external_id) - Fetch customer credit balance by external customer id
* [fetch_ledger](docs/sdks/credit/README.md#fetch_ledger) - Fetch customer credits ledger
* [fetch_ledger_by_external_id](docs/sdks/credit/README.md#fetch_ledger_by_external_id) - Fetch customer credits ledger by external ID

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
* [list](docs/sdks/customer/README.md#list) - List customers
* [list_balance_transactions](docs/sdks/customer/README.md#list_balance_transactions) - List balance transactions
* [update_by_external_id](docs/sdks/customer/README.md#update_by_external_id) - Update customer by external ID
* [update_customer](docs/sdks/customer/README.md#update_customer) - Update customer

### [event](docs/sdks/event/README.md)

* [amend](docs/sdks/event/README.md#amend) - Amend event
* [close_backfill](docs/sdks/event/README.md#close_backfill) - Close backfill
* [create](docs/sdks/event/README.md#create) - Create backfill
* [deprecate_event](docs/sdks/event/README.md#deprecate_event) - Deprecate event
* [fetch](docs/sdks/event/README.md#fetch) - Fetch backfill
* [ingest](docs/sdks/event/README.md#ingest) - Ingest events
* [list_backfills](docs/sdks/event/README.md#list_backfills) - List backfills
* [revert_backfill](docs/sdks/event/README.md#revert_backfill) - Revert backfill
* [search](docs/sdks/event/README.md#search) - Search events

### [invoice](docs/sdks/invoice/README.md)

* [create](docs/sdks/invoice/README.md#create) - Create a one-off invoice
* [create_line_item](docs/sdks/invoice/README.md#create_line_item) - Create invoice line item
* [fetch](docs/sdks/invoice/README.md#fetch) - Fetch invoice
* [fetch_upcoming](docs/sdks/invoice/README.md#fetch_upcoming) - Fetch upcoming invoice
* [issue](docs/sdks/invoice/README.md#issue) - Issue invoice
* [list](docs/sdks/invoice/README.md#list) - List invoices
* [mark_invoice_as_paid](docs/sdks/invoice/README.md#mark_invoice_as_paid) - Mark invoice as paid
* [void](docs/sdks/invoice/README.md#void) - Void invoice

### [item](docs/sdks/item/README.md)

* [fetch](docs/sdks/item/README.md#fetch) - Fetch item
* [list](docs/sdks/item/README.md#list) - List items

### [metric](docs/sdks/metric/README.md)

* [create](docs/sdks/metric/README.md#create) - Create metric
* [fetch](docs/sdks/metric/README.md#fetch) - Get metric
* [list](docs/sdks/metric/README.md#list) - List metrics

### [plan](docs/sdks/plan/README.md)

* [create](docs/sdks/plan/README.md#create) - Create plan
* [fetch](docs/sdks/plan/README.md#fetch) - Fetch plan
* [fetch_by_external_id](docs/sdks/plan/README.md#fetch_by_external_id) - Fetch plan by external ID
* [list](docs/sdks/plan/README.md#list) - List plans
* [update_plan](docs/sdks/plan/README.md#update_plan) - Update plan by id
* [update_plan_external](docs/sdks/plan/README.md#update_plan_external) - Update plan by external ID

### [price](docs/sdks/price/README.md)

* [create](docs/sdks/price/README.md#create) - Create price
* [fetch](docs/sdks/price/README.md#fetch) - Fetch price
* [fetch_by_external_id](docs/sdks/price/README.md#fetch_by_external_id) - Fetch price by external price id
* [list](docs/sdks/price/README.md#list) - List prices

### [price_interval](docs/sdks/priceinterval/README.md)

* [add_edit_price_intervals](docs/sdks/priceinterval/README.md#add_edit_price_intervals) - Add or edit price intervals

### [subscription](docs/sdks/subscription/README.md)

* [cancel](docs/sdks/subscription/README.md#cancel) - Cancel subscription
* [create](docs/sdks/subscription/README.md#create) - Create subscription
* [fetch](docs/sdks/subscription/README.md#fetch) - Fetch subscription
* [fetch_costs](docs/sdks/subscription/README.md#fetch_costs) - Fetch subscription costs
* [fetch_schedule](docs/sdks/subscription/README.md#fetch_schedule) - Fetch subscription schedule
* [fetch_usage](docs/sdks/subscription/README.md#fetch_usage) - Fetch subscription usage
* [list](docs/sdks/subscription/README.md#list) - List subscriptions
* [schedule_plan_change](docs/sdks/subscription/README.md#schedule_plan_change) - Schedule plan change
* [trigger_phase](docs/sdks/subscription/README.md#trigger_phase) - Trigger phase
* [unschedule_cancellation](docs/sdks/subscription/README.md#unschedule_cancellation) - Unschedule subscription cancellation
* [unschedule_fixed_fee_quantity](docs/sdks/subscription/README.md#unschedule_fixed_fee_quantity) - Unschedule fixed fee quantity updates
* [unschedule_plan_change](docs/sdks/subscription/README.md#unschedule_plan_change) - Unschedule plan change
* [update_fixed_fee_quantity](docs/sdks/subscription/README.md#update_fixed_fee_quantity) - Update price quantity
<!-- End SDK Available Operations -->



<!-- Start Dev Containers -->
# Dev Containers
<div align="left">
    <a href="https://codespaces.new/orbcorp/orb-billing-python-sdk.git/tree/main"><img src="https://github.com/codespaces/badge.svg" /></a>
    
</div>

Experience our SDK in an enhanced sandbox environment. Try it now in **GitHub Codespaces**!

* [Explore Dev Containers](.devcontainer/README.md)
<!-- End Dev Containers -->



<!-- Start Pagination -->
# Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
<!-- End Pagination -->

```python
import orb

# Initialize the SDK.
s = orb.Orb(api_key_auth="my-orb-key")

cursor = None
keep_fetching = True

# We start by attempting to fetch at least one page of results. 
while keep_fetching:
  # The SDK call takes the cursor and any additional arguments to filter the
  # coupon data.
  response = s.coupon.list(cursor=cursor, show_archived=False)
  if response.status_code != 200:
    raise Exception(f"Unexpected status code received from server: {response.status_code}")

  # Ensure the response from the server contains coupon data.
  if response.coupons is None:
    break

  # Check if we received an empty page of results. This is a signal that we
  # should stop requesting more data from the server.
  page = response.coupons.data
  if not page:
    break

  # Capture the cursor for the next loop. If there is no cursor then use that
  # as a signal to stop iteration.
  cursor = response.coupons.pagination_metadata.next_cursor
  keep_fetching = cursor is not None

  # At this point we have a page of coupon entries that we can collect or
  # iterate through as shown below.
  for coupon in page:
    code = coupon.redemption_code
    redeem_count = coupon.times_redeemed
    print(f"Coupon ${code} was redeemed ${redeem_count} times.")
```

<!-- Placeholder for Future Speakeasy SDK Sections -->



### Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

### Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release !

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)

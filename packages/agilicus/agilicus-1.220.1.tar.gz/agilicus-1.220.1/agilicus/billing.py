import datetime
import os
import agilicus
from agilicus import ApiException

import json
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import pop_item_if_none
from .output import output_if_console
from .context import get_apiclient_from_ctx
import operator

from .output.table import (
    column,
    spec_column,
    status_column,
    metadata_column,
    format_table,
    subtable,
)


def delete_billing_account(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.delete_billing_account(billing_account_id, **kwargs)


def delete_subscription(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.delete_subscription(billing_subscription_id, **kwargs)


def get_billing_account(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.get_billing_account(billing_account_id, **kwargs)


def update_subscription(ctx, billing_subscription_id, subscription):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.replace_subscription(
        billing_subscription_id, billing_org_subscription=subscription
    )


def get_billing_subscription(ctx, billing_subscription_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_subscription(billing_subscription_id, **kwargs)


def list_accounts(ctx, **kwargs):
    client = get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.list_billing_accounts(**kwargs)


def list_subscriptions(ctx, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    pop_item_if_none(kwargs)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    else:
        kwargs.pop("org_id")
    return client.billing_api.list_subscriptions(**kwargs)


def format_accounts(
    ctx, accounts, get_subscription_data=False, get_customer_data=False, **kwargs
):
    orgs_column = [column("id"), column("organisation")]
    subscriptions = [
        spec_column("subscription_id"),
        subtable(ctx, "orgs", orgs_column, subobject_name="status"),
    ]
    products_column = [
        column("name", optional=True),
    ]
    columns = [
        metadata_column("id"),
        status_column("product.spec.name", optional=True),
    ]

    def _get_customer_name(record, key):
        status = record.get("status")
        return status.get("customer", {}).get("name")

    if get_customer_data:
        columns.append(
            column(
                "status", newname="customer", getter=_get_customer_name, optional=True
            )
        )
    else:
        columns.append(spec_column("customer_id"))

    if get_subscription_data:
        columns.append(
            subtable(ctx, "products", products_column, subobject_name="status")
        )

    columns.append(subtable(ctx, "orgs", orgs_column, subobject_name="status"))
    columns.append(
        subtable(ctx, "org_subscriptions", subscriptions, subobject_name="status")
    )
    return format_table(ctx, accounts, columns)


def format_subscriptions(ctx, subscriptions):
    orgs_column = [column("id"), column("organisation")]
    columns = [
        metadata_column("id", optional=True),
        spec_column("subscription_id"),
        spec_column("billing_account_id"),
        spec_column("dev_mode"),
        subtable(ctx, "orgs", orgs_column, subobject_name="status"),
        status_column("subscription", optional=True),
    ]
    return format_table(ctx, subscriptions, columns)


def add_billing_account(ctx, customer_id=None, dev_mode=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    spec = agilicus.BillingAccountSpec(customer_id=customer_id)

    if dev_mode is not None:
        spec.dev_mode = dev_mode

    account = agilicus.BillingAccount(spec=spec)

    return client.billing_api.create_billing_account(account)


def add_subscription(
    ctx, billing_account_id, subscription_id=None, dev_mode=None, **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    spec = agilicus.BillingOrgSubscriptionSpec(billing_account_id=billing_account_id)

    if dev_mode is not None:
        spec.dev_mode = dev_mode

    if subscription_id is not None:
        spec.subscription_id = subscription_id

    subscription = agilicus.BillingOrgSubscription(spec=spec)

    return client.billing_api.create_subscription(subscription)


def add_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    billing_org = agilicus.BillingOrg._from_openapi_data(org_id=org_id)
    return client.billing_api.add_org_to_billing_account(
        billing_account_id, billing_org=billing_org
    )


def remove_org(ctx, billing_account_id=None, org_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.remove_org_from_billing_account(billing_account_id, org_id)


def add_org_to_subscription(ctx, billing_subscription_id, org_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    billing_org = agilicus.BillingOrg._from_openapi_data(org_id=org_id)
    return client.billing_api.add_org_to_billing_subscription(
        billing_subscription_id, billing_org=billing_org
    )


def remove_org_from_subscription(ctx, billing_subscription_id, org_id, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.remove_org_from_billing_subscription(
        org_id, billing_subscription_id
    )


def replace_billing_account(
    ctx,
    billing_account_id=None,
    customer_id=None,
    dev_mode=None,
    product_id=None,
    **kwargs,
):
    client = get_apiclient_from_ctx(ctx)

    existing = client.billing_api.get_billing_account(billing_account_id)
    if customer_id is not None:
        existing.spec.customer_id = customer_id
    if dev_mode is not None:
        existing.spec.dev_mode = dev_mode
    if product_id is not None:
        existing.spec.product_id = product_id
    return client.billing_api.replace_billing_account(
        billing_account_id, billing_account=existing
    )


def format_usage_records(ctx, records):
    columns = [
        column("id"),
        column("period"),
        column("total_usage"),
    ]
    return format_table(ctx, records, columns, getter=operator.itemgetter)


def get_usage_records(ctx, billing_account_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_usage_records(billing_account_id)


def _dump_billing_failure(ctx, exception_description, account):
    account_info = {}
    try:
        account_info = account.to_dict()
    except Exception as exc:
        output_if_console(
            ctx,
            f"Failed to dump account info when handling billing failure: {str(exc)}",
        )
    error_message = {
        "time": datetime.datetime.now(datetime.timezone.utc),
        "msg": "error",
        "reason": str(exception_description),
        "account": account_info,
    }
    try:
        print(json.dumps(error_message, default=str))
    except Exception as exc:
        output_if_console(ctx, f"Failed to json.dumps failure info: {str(exc)}")


def run_billing_um_all_accounts(
    ctx, client, dry_run=False, push_to_prometheus_on_success=True, **kwargs
):
    accounts = client.billing_api.list_billing_accounts()
    record = agilicus.CreateBillingUsageRecords(dry_run=dry_run)
    numSuccess = 0
    numSkipped = 0
    numFail = 0

    for account in accounts.billing_accounts:

        if not account.spec.customer_id:
            numSkipped += 1
            continue
        try:

            if len(account.status.orgs) == 0:
                numSkipped += 1
                print(
                    json.dumps(
                        {
                            "skip": True,
                            "billing_account": account.metadata.id,
                            "customer_id": account.spec.customer_id,
                        }
                    )
                )
                continue

            base_result = client.billing_api.add_billing_usage_record(
                account.metadata.id, create_billing_usage_records=record
            )
            success = False
            if base_result:
                result = base_result.to_dict()
                success = True
            else:
                result = {}

            result["billing_account"] = account.metadata.id
            result["customer_id"] = account.spec.customer_id
            result["orgs"] = [
                {"id": org.id, "organisation": org.organisation}
                for org in account.status.orgs
            ]
            if success:
                numSuccess += 1
                result["published"] = True
            else:
                numSkipped += 1
                result["published"] = False
            print(json.dumps(result))
        except ApiException as exc:
            numFail += 1
            _dump_billing_failure(ctx, exc.body, account)
        except Exception as exc:
            numFail += 1
            _dump_billing_failure(ctx, exc, account)

    if push_to_prometheus_on_success:
        try:
            from prometheus_client import (
                CollectorRegistry,
                Gauge,
                push_to_gateway,
            )
        except ModuleNotFoundError:
            output_if_console(ctx, "Not posting success to prometheus_client.")
            output_if_console(
                ctx, "Add the 'billing' option to the install to gain access"
            )
            return

        registry = CollectorRegistry()
        gSuccess = Gauge(
            "billing_usage_records_created_count",
            "number of billing accounts that have created a usage record",
            registry=registry,
        )

        gFail = Gauge(
            "billing_usage_records_failed_count",
            "number of billing accounts that failed to create a usage record",
            registry=registry,
        )
        gSkipped = Gauge(
            "billing_usage_records_skipped_count",
            "number of billing accounts that were skipped",
            registry=registry,
        )

        push_gateway = os.environ.get(
            "PROMETHEUS_PUSH_GATEWAY",
            "push-prometheus-pushgateway.prometheus-pushgateway:9091",
        )
        job_name = os.environ.get("JOB_NAME", "billing_usage_job")
        gSuccess.set(numSuccess)
        gFail.set(numFail)
        gSkipped.set(numSkipped)
        push_to_gateway(push_gateway, job=job_name, registry=registry)


def create_usage_record(
    ctx, billing_account_id=None, all_accounts=None, dry_run=False, **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    record = agilicus.BillingUsageRecord(dry_run=dry_run)
    if billing_account_id is not None:
        records = agilicus.CreateBillingUsageRecords(usage_records=[record])
        result = client.billing_api.add_billing_usage_record(
            billing_account_id, create_billing_usage_records=records
        )
        print(json.dumps(result.to_dict()))
    elif all_accounts is not None:
        run_billing_um_all_accounts(ctx, client, dry_run=dry_run, **kwargs)
    else:
        raise Exception("Need to choose --billing-account-or or --all-accounts")


def list_products(ctx, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    products = client.billing_api.list_products(**kwargs)
    products.products = sorted(products.products, key=lambda d: d["spec"]["label"])
    return products


def format_products(ctx, products_obj):
    products = products_obj.to_dict()

    def get_product_name(record, key):
        return "{0: <20}".format(record["product"]["name"])

    def get_product_nickname(record, key):
        return "{0: <28}".format(record["nickname"])

    def get_product_metric(record, key):
        if "metric" in record["product"]["metadata"]:
            return "{0: <20}".format(record["product"]["metadata"]["metric"])
        else:
            return "{0: <20}".format("")

    def get_unit_amount(record, key):
        if record["unit_amount"]:
            return "{:,.2f}".format(record["unit_amount"] / 100)
        return ""

    product_price_column = [
        column("id", optional=True),
        column("product name", getter=get_product_name, optional=True),
        column("nickname", getter=get_product_nickname, optional=True),
        column("metric", getter=get_product_metric, optional=True),
        column("unit_amount", getter=get_unit_amount, optional=True),
    ]
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("label", optional=True),
        spec_column("description", optional=True),
        spec_column("trial_period", optional=True),
        #        spec_column("dev_mode", optional=True),
        subtable(
            ctx,
            "billing_product_prices",
            product_price_column,
            table_getter=operator.itemgetter,
            subobject_name="status",
            optional=True,
        ),
    ]
    return format_table(
        ctx, products.get("products"), columns, getter=operator.itemgetter
    )


def add_product(
    ctx, name=None, dev_mode=None, trial_period=None, product_price_ids=[], **kwargs
):
    client = get_apiclient_from_ctx(ctx)
    prices = []
    for price_id in product_price_ids:
        prices.append(agilicus.BillingProductPrice(id=price_id))
    spec = agilicus.ProductSpec(name=name, billing_product_prices=prices, **kwargs)

    if dev_mode is not None:
        spec.dev_mode = dev_mode
    if trial_period is not None:
        spec.trial_period = trial_period

    product = agilicus.Product(spec=spec)

    return client.billing_api.create_product(product)


def delete_product(ctx, product_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.delete_product(product_id)


def get_product(ctx, product_id=None, **kwargs):
    client = get_apiclient_from_ctx(ctx)
    return client.billing_api.get_product(product_id)


def update_product(
    ctx,
    product_id=None,
    dev_mode=None,
    name=None,
    product_price_ids=None,
    remove_product_price_ids=None,
    label=None,
    description=None,
    trial_period=None,
    **kwargs,
):
    client = get_apiclient_from_ctx(ctx)

    product = client.billing_api.get_product(product_id)

    if remove_product_price_ids is not None:
        old_prices = product.spec.billing_product_prices
        product.spec.billing_product_prices = []
        for price in old_prices:
            if price.id in remove_product_price_ids:
                # needs to be removed.
                continue
            product.spec.billing_product_prices.append(price)

    if product_price_ids is not None:
        for price_id in product_price_ids:
            product.spec.billing_product_prices.append(
                agilicus.BillingProductPrice(id=price_id)
            )

    if dev_mode is not None:
        product.spec.dev_mode = dev_mode
    if name is not None:
        product.spec.name = name
    if description is not None:
        product.spec.description = description
    if label is not None:
        product.spec.label = label
    if trial_period is not None:
        product.spec.trial_period = trial_period
    return client.billing_api.replace_product(
        product_id,
        product=product,
    )


def _get_subscription(org_subscriptions, subscription_id):
    for org_subscription in org_subscriptions:
        if org_subscription.spec.subscription_id == subscription_id:
            return org_subscription


def _has_org(orgs, org_id):
    for org in orgs:
        if org.id == org_id:
            return True
    return False


def migrate_billing_subscriptions(ctx, billing_account_id=None, commit=False, **kwargs):
    kwargs = {}
    kwargs["get_customer_data"] = True
    kwargs["get_subscription_data"] = True
    kwargs["org_id"] = ""
    if billing_account_id is not None:
        accounts = [get_billing_account(ctx, billing_account_id, **kwargs)]
    else:
        accounts = list_accounts(ctx, **kwargs).billing_accounts
    for account in accounts:
        customer = account.status.customer
        print(f"customer = {customer['name']} - billing account {account.metadata.id}")
        for sub in account.status.subscriptions:
            # check if there is an org sub for this first.
            org_subscription = _get_subscription(
                account.status.org_subscriptions, sub["id"]
            )
            if not org_subscription:
                print(f"  {sub['id']} needs BillingSubscription")
                if not commit:
                    for org in account.status.orgs:
                        print(f"    {org.organisation} needs to be attached")
                    continue
                sub = add_subscription(
                    ctx,
                    account.metadata.id,
                    subscription_id=sub["id"],
                    dev_mode=account.spec.dev_mode,
                )
                print(f"    created billing subscription {sub.metadata.id}")
                for org in account.status.orgs:
                    print(f"    adding org {org.organisation} to billing subscription")
                    val = add_org_to_subscription(ctx, sub.metadata.id, org.id)
                    print(f"    added org {val.id} to billing subscription")
            else:
                print(f"  {sub['id']} already configured {org_subscription.metadata.id}")
                # verify that org is added to subscription
                for org in account.status.orgs:
                    if not _has_org(org_subscription.status.orgs, org.id):
                        print(
                            f"    adding org {org.organisation} to billing subscription"
                        )
                        if not commit:
                            continue
                        val = add_org_to_subscription(
                            ctx, org_subscription.metadata.id, org.id
                        )
                        print(f"    added org {val.id} to billing subscription")
                    else:
                        print(f"    org {org.organisation} already connected")

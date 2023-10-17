import sys

from . import billing


def override_replace(metric, usage_override, usage_min, usage_max, usage_step):
    if usage_override is None:
        usage_override = []
    usage_min = None if usage_min is None else int(usage_min)
    usage_max = None if usage_max is None else int(usage_max)
    usage_step = None if usage_step is None else int(usage_step)
    for idx, x in enumerate(usage_override):
        if x["metric"] == metric:
            usage_override.remove(x)
    if usage_min is not None or usage_max or usage_step is not None:
        rec = {"metric": metric}
        if usage_min is not None:
            rec["min_quantity"] = usage_min
        if usage_max is not None:
            rec["max_quantity"] = usage_max
        if usage_step is not None:
            rec["step_quantity"] = usage_step
        usage_override.append(rec)
    return usage_override


def set_subscription_info(ctx, **kwargs):
    """Update various parameters associated with the subscription.
    e.g. the usage-metrics of min/max/step size."""
    result = billing.list_subscriptions(ctx, org_id=kwargs["org_id"])

    for bi in result.billing_subscriptions:
        billing_account_id = bi.spec.billing_account_id
        for org in bi.status.orgs:
            if org.id == kwargs["org_id"]:
                subscription_id = bi.metadata.id
                break

    if subscription_id is None:
        print(f"ERROR: could not find account info for {kwargs['org_id']}")
        sys.exit(1)

    subscription = billing.get_billing_subscription(
        ctx, billing_subscription_id=subscription_id
    )
    subscription_id = subscription.metadata.id
    usage_override = subscription.spec.usage_override

    usage_override = override_replace(
        "active_users",
        usage_override,
        kwargs["min_user"],
        kwargs["max_user"],
        kwargs["step_user"],
    )
    usage_override = override_replace(
        "active_connectors",
        usage_override,
        kwargs["min_connector"],
        kwargs["max_connector"],
        kwargs["step_connector"],
    )

    subscription.spec.usage_override = usage_override

    billing.update_subscription(
        ctx, billing_subscription_id=subscription_id, subscription=subscription
    )
    res = billing.create_usage_record(ctx, billing_account_id=billing_account_id)
    print(res)

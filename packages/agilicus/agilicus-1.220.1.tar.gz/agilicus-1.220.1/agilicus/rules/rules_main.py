import click
import click_extension

from . import rules
from ..output.table import output_entry


@click.command(name="add-host-prefix-rule")
@click.option("--hostname", required=True)
@click.option("--name", required=True)
@click.option("--action", required=True, multiple=True, type=click.Choice(rules.ACTIONS))
@click.option("--prefix", default=None)
@click.option("--purpose", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_host_prefix_rule(ctx, action, **kwargs):
    output_entry(ctx, rules.add_hostprefix_rule(ctx, actions=action, **kwargs))


@click.command(name="add-standalone-rules-from-file")
@click.option("--rule-json-file", required=True, type=click_extension.JSONFile("r"))
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rules_from_file(ctx, rule_json_file, **kwargs):
    print(rules.add_rules(ctx, rules=rule_json_file, **kwargs))


@click.command(name="list-standalone-rules")
@click.option("--name", default=None)
@click.option("--prefix", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--rule-id", default=None)
@click.pass_context
def cli_command_list_rules(ctx, **kwargs):
    result = rules.list_rules(ctx, **kwargs)
    print(rules.format_rules(ctx, result))


@click.command(name="get-standalone-rule")
@click.option("--rule-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_rule(ctx, **kwargs):
    output_entry(ctx, rules.get_rule(ctx, **kwargs).to_dict())


@click.command(name="delete-standalone-rule")
@click.option("--rule-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rule(ctx, **kwargs):
    rules.delete_rule(ctx, **kwargs)


@click.command(name="update-host-prefix-rule")
@click.option("--rule-id", required=True)
@click.option("--hostname", default=None)
@click.option("--name", default=None)
@click.option("--action", default=None, multiple=True, type=click.Choice(rules.ACTIONS))
@click.option("--prefix", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_replace_host_prefix_rule(ctx, action, **kwargs):
    output_entry(
        ctx, rules.replace_hostprefix_rule(ctx, actions=action, **kwargs).to_dict()
    )


@click.command(name="add-standalone-rule-tree")
@click.option("--name", required=True)
@click.option("--tree-name", default=None, multiple=True)
@click.option("--child-tree-name", default=None, multiple=True)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rule_tree(ctx, tree_name, child_tree_name, **kwargs):
    if len(tree_name) == 0 and len(child_tree_name) == 0:
        raise ValueError("must provide at least one tree-name or child-tree-name")
    output_entry(
        ctx,
        rules.add_rule_tree(ctx, rules=tree_name, children=child_tree_name, **kwargs),
    )


@click.command(name="add-standalone-rule-trees-from-file")
@click.option("--rule-tree-json-file", required=True, type=click_extension.JSONFile("r"))
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rule_trees_from_file(ctx, rule_tree_json_file, **kwargs):
    print(rules.add_trees(ctx, trees=rule_tree_json_file, **kwargs))


@click.command(name="list-standalone-rule-trees")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--rule-tree-id", default=None)
@click.pass_context
def cli_command_list_rule_trees(ctx, **kwargs):
    result = rules.list_rule_trees(ctx, **kwargs)
    print(rules.format_rule_trees(ctx, result))


@click.command(name="get-standalone-rule-tree")
@click.option("--rule-tree-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_rule_tree(ctx, **kwargs):
    output_entry(ctx, rules.get_rule_tree(ctx, **kwargs).to_dict())


@click.command(name="update-standalone-rule-tree")
@click.option("--rule-tree-id", required=True)
@click.option("--name", default=None)
@click.option("--tree-name", default=None, multiple=True)
@click.option("--child-tree-name", default=None, multiple=True)
@click.option("--description", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_update_rule_tree(ctx, tree_name, child_tree_name, **kwargs):
    output_entry(
        ctx,
        rules.replace_rule_tree(
            ctx, rules=tree_name, children=child_tree_name, **kwargs
        ),
    )


@click.command(name="delete-standalone-rule-tree")
@click.option("--rule-tree-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rule_tree(ctx, **kwargs):
    rules.delete_rule_tree(ctx, **kwargs)


@click.command(name="add-standalone-ruleset")
@click.option("--name", required=True)
@click.option("--tree-name", default=None, multiple=True)
@click.option("--label", default=None, multiple=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_ruleset(ctx, tree_name, label, **kwargs):
    output_entry(ctx, rules.add_ruleset(ctx, trees=tree_name, labels=label, **kwargs))


@click.command(name="add-standalone-rulesets-from-file")
@click.option("--ruleset-json-file", required=True, type=click_extension.JSONFile("r"))
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_rulesets_from_file(ctx, ruleset_json_file, **kwargs):
    print(rules.add_rulesets(ctx, rulesets=ruleset_json_file, **kwargs))


@click.command(name="list-standalone-rulesets")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.pass_context
def cli_command_list_rulesets(ctx, **kwargs):
    result = rules.list_rulesets(ctx, **kwargs)
    print(rules.format_rulesets(ctx, result))


@click.command(name="get-standalone-ruleset")
@click.option("--ruleset-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_ruleset(ctx, **kwargs):
    output_entry(ctx, rules.get_ruleset(ctx, **kwargs).to_dict())


@click.command(name="update-standalone-ruleset")
@click.option("--ruleset-id", required=True)
@click.option("--name", default=None)
@click.option("--tree-name", default=None, multiple=True)
@click.option("--label", default=None, multiple=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_update_ruleset(ctx, tree_name, label, **kwargs):
    output_entry(
        ctx, rules.replace_ruleset(ctx, trees=tree_name, labels=label, **kwargs)
    )


@click.command(name="delete-standalone-ruleset")
@click.option("--ruleset-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_ruleset(ctx, **kwargs):
    rules.delete_ruleset(ctx, **kwargs)


@click.command(name="add-standalone-ruleset-label")
@click.argument("label", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_add_host_label(ctx, label, **kwargs):
    for _label in label:
        result = rules.add_label(ctx, label=_label, **kwargs)
        output_entry(ctx, result.to_dict())


@click.command(name="list-standalone-ruleset-labels")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_ruleset_labels(ctx, **kwargs):
    results = rules.list_labels(ctx, **kwargs)
    print(rules.format_labels(ctx, results))


@click.command(name="add-standalone-ruleset-bundle")
@click.option("--name", required=True)
@click.option("--org-id", default=None)
@click.option("--label", default=None)
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.pass_context
def cli_command_add_rulesets_bundle(ctx, **kwargs):
    result = rules.add_bundle(ctx, **kwargs)
    output_entry(ctx, result)


@click.command(name="add-standalone-ruleset-bundle-label")
@click.argument("bundle-id")
@click.argument("label")
@click.option("--label-org-id", default=None)
@click.option("--exclude", is_flag=True, default=None)
@click.option("--priority", type=int, default=0)
@click.pass_context
def cli_command_add_rulesets_bundle_label(ctx, **kwargs):
    result = rules.add_bundle_label(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@click.command(name="delete-standalone-ruleset-bundle")
@click.argument("bundle-id", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_rulesets_bundle(ctx, bundle_id, **kwargs):
    for _bundle_id in bundle_id:
        rules.delete_bundle(ctx, bundle_id=_bundle_id, **kwargs)


@click.command(name="list-standalone-ruleset-bundles")
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_list_rulesets_bundle(ctx, **kwargs):
    results = rules.list_bundles(ctx, **kwargs)
    print(rules.format_bundles(ctx, results))


@click.command(name="get-standalone-ruleset-bundle")
@click.argument("bundle-id")
@click.option("--org-id", default=None)
@click.option("--get-rulesets", is_flag=True, default=None)
@click.option("--standalone-rulesets-etag", default=None)
@click.pass_context
def cli_command_get_rulesets_bundle(ctx, **kwargs):
    result = rules.get_bundle(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])

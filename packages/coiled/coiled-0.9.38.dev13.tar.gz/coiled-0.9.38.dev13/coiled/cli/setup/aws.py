import json
import time
import traceback
from typing import Optional, Tuple, Union

import boto3
import botocore.exceptions
import click
import dask.config
import jsondiff
from rich import print
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt

import coiled

from ...auth import get_local_user
from ..utils import CONTEXT_SETTINGS
from .util import setup_failure

WIDTH = 90


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--region",
    default=None,
    help=(
        "AWS region to use for Coiled. By default, this will use the "
        "default region configured in your AWS profile if one is configured."
    ),
)
@click.option(
    "--profile",
    default=None,
    envvar="AWS_PROFILE",
    help=(
        "AWS profile to use from your local AWS credentials file. "
        "By default, uses your `[default]` profile if one is configured."
    ),
)
@click.option(
    "--account",
    default=None,
    help="Coiled account that will be configured to use the AWS account. By default, uses your default Coiled account.",
)
@click.option(
    "--iam-user",
    default="coiled",
    help="IAM User to create in your AWS account",
)
@click.option(
    "--setup-policy",
    default=None,
    help="Non-default name for the setup IAM Policy, default `{iam-user}-setup`",
)
@click.option(
    "--ongoing-policy",
    default=None,
    help="Non-default name for the ongoing IAM Policy, default `{iam-user}-ongoing`",
)
@click.option(
    "--update-policies",
    default=False,
    is_flag=True,
    help="Only update existing IAM Policies",
)
@click.option(
    "--update-instance-policy",
    default=False,
    is_flag=True,
    help="Update instance policy (not for regular use)",
)
@click.option(
    "--cloudshell-link",
    default=None,
    is_flag=True,
    help="Don't do setup, give instructions for setup using CloudShell",
)
@click.option(
    "--manual-final-setup",
    default=False,
    is_flag=True,
    help="Don't automatically send credentials to Coiled, finish setup manually in the web UI",
)
@click.option(
    "--quotas",
    default=False,
    is_flag=True,
    help="Check and potentially request AWS quota increases for common instance types",
)
@click.option(
    "-y",
    "--yes",
    default=False,
    is_flag=True,
    help="Don't prompt for confirmation, just do it!",
)
@click.option(
    "--accept-delete",
    default=False,
    is_flag=True,
    hidden=True,
    help="use with --yes if you also want to accept deletes",
)
@click.option(
    "--use-legacy-setup/--no-legacy-setup",
    default=False,
    is_flag=True,
    hidden=True,
    help="Use new setup backend",
)
def aws_setup(
    region: Optional[str],
    profile: Optional[str],
    account: Optional[str],
    iam_user: str,
    setup_policy: Optional[str],
    ongoing_policy: Optional[str],
    update_policies: bool,
    update_instance_policy: bool,
    cloudshell_link: Optional[bool],
    manual_final_setup: bool,
    quotas: bool,
    yes: bool,
    accept_delete: bool,
    use_legacy_setup: bool,
):
    accept_delete = yes and accept_delete  # (only accept_delete if --yes is also specified)
    if not do_setup(
        aws_profile=profile,
        slug=iam_user,
        setup_name=setup_policy,
        ongoing_name=ongoing_policy,
        just_update_policies=update_policies,
        just_update_instance_policy=update_instance_policy,
        cloudshell_link=cloudshell_link,
        region=region,
        manual_final_setup=manual_final_setup,
        quotas=quotas,
        yes=yes,
        accept_delete=accept_delete,
        use_shim=not use_legacy_setup,
        coiled_account=account,
    ):
        pass
        # print("[red]The setup process didn't finish.[/red]")


DEFAULT_REGION = "us-east-1"

TAGS = [{"Key": "owner", "Value": "coiled"}]

PROMPTS = {
    "initial": "Proceed with IAM setup?",
    "replace_access_key": (
        "Too many access keys already exist for user "
        "[green]{user_name}[/green]. "
        "\nDelete key [green]{key_id}[/green] and create a new key?"
    ),
    "request_quotas": "Would you like to make any AWS quota increase requests?",
}

SCRIPT_REQUIRED_IAM = [
    "iam:GetPolicy",
    "iam:ListAccessKeys",
    "iam:CreateUser",
    "iam:TagUser",
    "iam:CreatePolicy",
    "iam:CreatePolicyVersion",
    "iam:AttachUserPolicy",
    "iam:GetPolicyVersion",
    "iam:CreateAccessKey",
    "iam:DeleteAccessKey",
]

setup_doc = """{
   "Statement": [
      {
         "Sid": "Setup",
         "Effect": "Allow",
         "Resource": "*",
         "Action": [
            "ec2:AssociateRouteTable",
            "ec2:AttachInternetGateway",
            "ec2:CreateInternetGateway",
            "ec2:CreateRoute",
            "ec2:CreateRouteTable",
            "ec2:CreateSubnet",
            "ec2:CreateVpc",
            "ec2:DeleteInternetGateway",
            "ec2:DeleteRoute",
            "ec2:DeleteRouteTable",
            "ec2:DeleteSubnet",
            "ec2:DeleteVpc",
            "ec2:DescribeInternetGateways",
            "ec2:DetachInternetGateway",
            "ec2:DisassociateRouteTable",
            "ec2:ModifySubnetAttribute",
            "ec2:ModifyVpcAttribute",
            "iam:AddRoleToInstanceProfile",
            "iam:AttachRolePolicy",
            "iam:CreateRole",
            "iam:CreatePolicy",
            "iam:CreateServiceLinkedRole",
            "iam:CreateInstanceProfile",
            "iam:DeleteRole",
            "iam:ListPolicies",
            "iam:ListInstanceProfiles",
            "iam:ListAttachedRolePolicies",
            "iam:TagInstanceProfile",
            "iam:TagPolicy",
            "iam:TagRole"
         ]
      }
   ],
   "Version": "2012-10-17"
}"""

ongoing_doc = """{"Statement": [
      {
         "Sid": "Ongoing",
         "Effect": "Allow",
         "Resource": "*",
         "Action": [
            "ec2:AuthorizeSecurityGroupIngress",
            "ec2:CreateFleet",
            "ec2:CreateLaunchTemplate",
            "ec2:CreateLaunchTemplateVersion",
            "ec2:CreateRoute",
            "ec2:CreateSecurityGroup",
            "ec2:CreateTags",
            "ec2:DeleteFleets",
            "ec2:DeleteLaunchTemplate",
            "ec2:DeleteLaunchTemplateVersions",
            "ec2:DeleteSecurityGroup",
            "ec2:DescribeAvailabilityZones",
            "ec2:DescribeImages",
            "ec2:DescribeInstances",
            "ec2:DescribeInstanceTypeOfferings",
            "ec2:DescribeInstanceTypes",
            "ec2:DescribeInternetGateways",
            "ec2:DescribeLaunchTemplates",
            "ec2:DescribeNatGateways",
            "ec2:DescribeNetworkInterfaces",
            "ec2:DescribeRegions",
            "ec2:DescribeRouteTables",
            "ec2:DescribeSecurityGroups",
            "ec2:DescribeSubnets",
            "ec2:DescribeVpcPeeringConnections",
            "ec2:DescribeVpcs",
            "ec2:RunInstances",
            "ec2:TerminateInstances",
            "ecr:BatchCheckLayerAvailability",
            "ecr:BatchGetImage",
            "ecr:CompleteLayerUpload",
            "ecr:CreateRepository",
            "ecr:DescribeImages",
            "ecr:DescribeRepositories",
            "ecr:GetAuthorizationToken",
            "ecr:GetDownloadUrlForLayer",
            "ecr:GetRepositoryPolicy",
            "ecr:InitiateLayerUpload",
            "ecr:ListImages",
            "ecr:PutImage",
            "ecr:UploadLayerPart",
            "ecr:TagResource",
            "iam:GetInstanceProfile",
            "iam:GetRole",
            "iam:ListAttachedRolePolicies",
            "iam:ListInstanceProfiles",
            "iam:ListPolicies",
            "iam:PassRole",
            "iam:TagRole",
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:DescribeLogGroups",
            "logs:DescribeLogStreams",
            "logs:GetLogEvents",
            "logs:FilterLogEvents",
            "logs:PutLogEvents",
            "logs:PutRetentionPolicy",
            "logs:TagLogGroup",
            "logs:TagResource",
            "sts:GetCallerIdentity"
         ]
      }
   ],
   "Version": "2012-10-17"
}"""


def create_user(iam, name):
    arn = None
    try:
        r = iam.create_user(UserName=name, Tags=TAGS)
        arn = r["User"]["Arn"]
        coiled.add_interaction(action="CreateUser", success=True, arn=arn)
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"user [green]{name}[/green] already exists")
    return arn


def create_or_update_policy(iam, aws_account, name, doc):
    try:
        r = iam.create_policy(PolicyName=name, PolicyDocument=doc)
        arn = r["Policy"]["Arn"]
        coiled.add_interaction(action="CreatePolicy", success=True, arn=arn)
    except iam.exceptions.EntityAlreadyExistsException:
        arn = f"arn:aws:iam::{aws_account}:policy/{name}"
        update_policy(iam, aws_account, name, doc)

    return arn


def get_policy_diff(iam, aws_account, name, doc):
    existing_arn, changes = None, None

    arn = f"arn:aws:iam::{aws_account}:policy/{name}"

    try:
        policy = iam.get_policy(PolicyArn=arn)
        existing_arn = arn
    except iam.exceptions.ClientError as e:
        error_code = e.response["Error"].get("Code")

        if error_code == "NoSuchEntity":
            return existing_arn, changes
        else:
            raise

    policy_version = iam.get_policy_version(PolicyArn=arn, VersionId=policy["Policy"]["DefaultVersionId"])
    existing_doc = policy_version["PolicyVersion"]["Document"]

    doc_diff = jsondiff.diff(existing_doc, json.loads(doc), syntax="symmetric")

    if doc_diff:
        changes = doc_diff

    return existing_arn, changes


def show_policy_diff(doc_diff) -> str:
    diff_lines = []

    if doc_diff:
        if "Statement" in doc_diff and len(doc_diff) == 1:
            if 0 in doc_diff["Statement"] and len(doc_diff["Statement"]) == 1:
                if "Action" in doc_diff["Statement"][0] and len(doc_diff["Statement"][0]) == 1:
                    action_changes = doc_diff["Statement"][0]["Action"]
                    line_changes = []

                    if jsondiff.symbols.insert in action_changes:
                        line_changes.extend([(i, "+", n) for (i, n) in action_changes[jsondiff.symbols.insert]])
                    if jsondiff.symbols.delete in action_changes:
                        line_changes.extend([(i, "-", n) for (i, n) in action_changes[jsondiff.symbols.delete]])

                    for i, change, line in sorted(line_changes):
                        line_color = "red" if change == "-" else "green"
                        diff_lines.append(f" [{line_color}][bold]{change}[/bold] ({i}) {line}")

                    return "\n".join(diff_lines)

        # if we couldn't print the short version, just print the raw diff object
        return f"{doc_diff}"
    else:
        return ""


def update_policy(iam, aws_account, name, doc):
    policy_arn = f"arn:aws:iam::{aws_account}:policy/{name}"
    try:
        r = iam.create_policy_version(PolicyArn=policy_arn, PolicyDocument=doc, SetAsDefault=True)
        coiled.add_interaction(action="CreatePolicyVersion", success=True, arn=policy_arn)
        new_version = r["PolicyVersion"]["VersionId"]
        print(f"Updated Policy [green]{policy_arn}[/green] is [bold]{new_version}[/bold]")
        print()
    except iam.exceptions.LimitExceededException:
        # this is Coiled-specific policy so should be fine to delete old version
        existing_policies = iam.list_policy_versions(PolicyArn=policy_arn)
        to_delete = [
            version["VersionId"] for version in existing_policies["Versions"] if not version["IsDefaultVersion"]
        ][-1]
        print(f"Policy {name} has too many existing versions, deleting {to_delete}")
        iam.delete_policy_version(PolicyArn=policy_arn, VersionId=to_delete)
        update_policy(iam, aws_account, name, doc)
    except Exception as e:
        coiled.add_interaction(
            action="CreatePolicyVersion",
            success=False,
            arn=policy_arn,
            error_message=str(e),
        )
        print("[red]Unable to update existing policy[/red]:")
        print(f"  [red]{e}[/red]")
        print()


def attach_policy(iam, user, policy_arn):
    # idempotent
    iam.attach_user_policy(UserName=user, PolicyArn=policy_arn)
    coiled.add_interaction(action="AttachUserPolicy", success=True, arn=policy_arn)


def make_access_key(iam, user, *, retry=0, accept_delete: bool = False) -> Tuple[Optional[str], Optional[str]]:
    try:
        r = iam.create_access_key(UserName=user)
        coiled.add_interaction(action="CreateAccessKey", success=True, user=user)

        key_id = r["AccessKey"]["AccessKeyId"]
        key_secret = r["AccessKey"]["SecretAccessKey"]

        return key_id, key_secret

    except iam.exceptions.LimitExceededException:
        coiled.add_interaction(
            action="CreateAccessKey",
            success=False,
            user=user,
            error_message="LimitExceededException",
        )
        if retry:
            print("[red]already retried, giving up[/red]")
            return None, None

        # FIXME let user select which key to delete
        # if Confirm.ask(PROMPTS["replace_access_key"].format(user_name=user, key_id=key_id), default=True):
        if delete_access_key(iam, user, accept_delete=accept_delete):
            return make_access_key(iam, user, retry=retry + 1, accept_delete=accept_delete)

    return None, None


def get_user_access_keys(iam, user):
    try:
        r = iam.list_access_keys(UserName=user)
        coiled.add_interaction(action="ListAccessKeys", success=True, user=user)
        return True, r["AccessKeyMetadata"]
    except iam.exceptions.ClientError as e:
        error_code = e.response["Error"].get("Code")

        if error_code == "NoSuchEntity":
            coiled.add_interaction(
                action="ListAccessKeys",
                success=False,
                user=user,
                error_message=str(e),
            )
            return False, []
        else:
            raise


def delete_access_key(iam, user, accept_delete: bool = False):
    r = iam.list_access_keys(UserName=user)
    key_id = r["AccessKeyMetadata"][0]["AccessKeyId"]

    # NOTE: --yes doesn't apply to this since currently
    print()
    if accept_delete or Confirm.ask(
        PROMPTS["replace_access_key"].format(user_name=user, key_id=key_id),
        default=True,
    ):
        coiled.add_interaction(action="prompt:DeleteAccessKey", success=True, user=user)
        iam.delete_access_key(UserName=user, AccessKeyId=key_id)
        coiled.add_interaction(action="DeleteAccessKey", success=True, user=user, key_id=key_id)
        print(f"Deleted access key [green]{key_id}[/green]")
        return True
    else:
        coiled.add_interaction(action="prompt:DeleteAccessKey", success=False, user=user)

    return False


def wait_till_key_works(iam, key, secret):
    print("")
    print("Waiting until access key is ready", end="")
    t0 = time.time()

    while t0 + 10 > time.time():
        try:
            coiled.utils.verify_aws_credentials(key, secret)
            # a little extra wait here also seems to help, otherwise we *still* yet error sometimes when trying to use
            print(".", end="")
            time.sleep(1)
            print()

            return True
        except iam.exceptions.ClientError as e:
            error_code = e.response["Error"].get("Code")
            if error_code == "InvalidClientTokenId":
                print(".", end="")
                time.sleep(1)
                continue

    print("\nAccess key is still not ready. Please manually set up your Coiled account with AWS.")
    return False


def do_intro(sts, iam, region, coiled_account):
    introduction = """
[bold]Introduction[/bold]

This uses your AWS credentials to set up Coiled.

This will do the following ...
1. Create limited IAM roles and grant them to Coiled
2. Check and expand your AWS quota if needed
3. Create initial resources to deploy clusters

This will [bold]not[/bold] ...
1. Create resources that cost money
2. Grant Coiled access to your data
""".strip()
    print(Panel(introduction, width=WIDTH))

    try:
        # get_caller_identity doesn't require any specific IAM rights
        identity = sts.get_caller_identity()
        aws_account = identity.get("Account")
        identity_as = identity.get("Arn").split(":")[-1]

        coiled.add_interaction(
            action="GetCallerIdentity",
            success=True,
            account=aws_account,
            identity_as=identity_as,
        )

        try:
            r = iam.list_account_aliases()
            account_alias = r.get("AccountAliases", [])[0]
            alias_string = f" ({account_alias})"
            coiled.add_interaction(
                action="ListAccountAliases",
                success=True,
                account=aws_account,
                alias=alias_string,
            )
        except Exception:
            # doesn't matter much if we can't get account alias
            alias_string = ""

        account_desc = f"""
[bold]Target AWS Account[/bold]

Current credentials:\t[green]{identity_as}[/green]
Proposed region :\t[green]{region}[/green]
Proposed account:\t[green]{aws_account}[/green]{alias_string}

If this is incorrect then stop and select a different ...
  profile using the [green]coiled setup aws [bold]--profile[/bold][/green] argument
  region using the [green]coiled setup aws [bold]--region[/bold][/green] argument
""".strip()

        print(Panel(account_desc, width=WIDTH))

        return aws_account
    except botocore.exceptions.NoCredentialsError:
        coiled.add_interaction(
            action="GetCallerIdentity",
            success=False,
            error_message="NoCredentialsError",
        )

        print(
            "[red]Missing:[/red] You don't have local AWS credentials.\n"
            "That's ok, you can run setup from AWS CloudShell."
        )
        setup_failure("Getting local aws credentials failed", backend="aws")
        print()
        # is aws cli installed?
        # get_aws_cli_version = subprocess.run(["aws", "--version"], capture_output=True)
        # has_aws_cli = get_aws_cli_version.returncode == 0

        show_cloudshell_instructions(region, coiled_account=coiled_account)

    except Exception as e:
        coiled.add_interaction(action="GetCallerIdentity", success=False, error_message=str(e))
        setup_failure(f"Getting local aws credentials failed {str(e)}", backend="aws")
        print("Error determining your AWS account:")
        print(f"    [red]{e}[/red]")
        print()

        show_cloudshell_instructions(region, coiled_account=coiled_account)

    return None


def show_cloudshell_instructions(region, coiled_account):
    # explain cloudshell
    server_arg = (
        f"--server {dask.config.get('coiled.server', coiled.utils.COILED_SERVER)} \\ "
        if dask.config.get("coiled.server", coiled.utils.COILED_SERVER) != coiled.utils.COILED_SERVER
        else ""
    )

    token = dask.config.get("coiled.token")
    a, b, c = token[:24], token[24:48], token[48:]
    token_args = [
        f"  --token {a} \\",
        f"  --token {b} \\",
        f"  --token {c} && \\",
    ]
    region_arg = f" --region {region}" if region else ""
    account_arg = f"--account {coiled_account} " if coiled_account else ""

    cli_lines = [
        "pip3 install coiled && \\ ",
        f"coiled login {account_arg}\\ ",
    ]
    if server_arg:
        cli_lines.append(server_arg)
    cli_lines.extend(
        [
            *token_args,
            f"coiled setup aws{region_arg}",
        ]
    )
    cli_command = "\n  ".join(cli_lines)

    instruction_text = (
        "Run setup from AWS CloudShell with the following steps:\n\n"
        "1. Go to [link]https://console.aws.amazon.com/cloudshell[/link]\n"
        "2. Sign in to your AWS account\n"
        "   (if you usually switch role or profile, you should do this)\n"
        "3. Run the following command in CloudShell:\n\n"
        f"  [green]{cli_command}[/green]\n"
    )

    # box might be nice but would make copying the command much worse
    print(instruction_text)


def do_coiled_setup(iam, key, secret, region, coiled_account, yes, use_shim) -> bool:
    success = False
    backend_failure = False

    if key and secret:
        coiled.add_interaction(action="prompt:CoiledSetup", success=True)
        # wait on this for a bit till we don't get InvalidClientTokenId error
        if wait_till_key_works(iam, key, secret):
            print("Setting up Coiled to use your AWS account...")
            try:
                coiled.set_backend_options(
                    account=coiled_account,
                    backend="aws",
                    aws_access_key_id=key,
                    aws_secret_access_key=secret,
                    aws_region=region,
                    use_shim=use_shim,
                )
                success = True
                coiled.add_interaction(action="CoiledSetup", success=True)
            except Exception as e:
                backend_failure = True
                error_message = str(e)
                coiled.add_interaction(action="CoiledSetup", success=False, error_message=error_message)
                print()
                print("[red]There was an error setting up Coiled to use your AWS account:\n")
                print(error_message)
        else:
            coiled.add_interaction(action="prompt:CoiledSetup", success=False)

        message = """
[bold]Setup complete 🎉[/bold]

What's next?

  Run a command line application in the cloud with:

    $ [bold]coiled run echo 'Hello, world'[/bold]

  Or create a Dask cluster with:

    $ ipython

    [bold]import coiled
    cluster = coiled.Cluster(
        n_workers=10,
    )
    client = cluster.get_client()[/bold]

  For more examples see [link]https://docs.coiled.io/user_guide/examples/index.html[/link]
""".strip()

        print()
        print()
        print(message)

        if not success and not backend_failure:
            show_manual_setup(key, secret, coiled_account=coiled_account)

    return success


def do_full_setup(
    session,
    iam,
    user_name,
    aws_account,
    region,
    setup_name,
    ongoing_name,
    *,
    coiled_account,
    manual_final_setup,
    yes,
    accept_delete,
    use_shim,
) -> bool:
    # Check for existing user
    user_exists, user_keys = get_user_access_keys(iam, user_name)

    # Check for existing policies
    setup_arn, setup_diff = get_policy_diff(iam, aws_account, setup_name, setup_doc)
    ongoing_arn, ongoing_diff = get_policy_diff(iam, aws_account, ongoing_name, ongoing_doc)

    resource_strings = ["[bold]Proposed AWS Account Changes[/bold]\n"]

    if not user_exists:
        resource_strings.append(f"Create IAM User:\t[green]{user_name}[/green]")
        resource_strings.append("  and create Access Key for this new IAM User")
    else:
        resource_strings.append(f"Create Access Key for [bold]existing[/bold] IAM User:\t[green]{user_name}[/green]")

        existing_key_message = f"  This IAM User already has {len(user_keys)} access keys."
        if len(user_keys) > 1:
            existing_key_message = (
                f"  This IAM User already has {len(user_keys)} access keys. \n"
                "  We'll need to [bold]delete[/bold] an existing access key to create a new access key."
            )
        resource_strings.append(existing_key_message)
        resource_strings.append("")
        resource_strings.append(
            "If you didn't want to configure Coiled with this existing IAM User, "
            "stop now and specify a different IAM User name with the "
            "[green]coiled setup aws [bold]--iam-user[/bold][/green] argument."
        )

    if not setup_arn:
        resource_strings.append("")
        resource_strings.append(f"Create IAM Policy:\t[green]{setup_name}[/green]")
        resource_strings.append(f"  and attach to IAM User [green]{user_name}[/green]")
    if setup_diff:
        resource_strings.append(f"Update IAM Policy:\t[green]{setup_name}[/green]")

    if not ongoing_arn:
        resource_strings.append("")
        resource_strings.append(f"Create IAM Policy:\t[green]{ongoing_name}[/green]")
        resource_strings.append(f"  and attach to IAM User [green]{user_name}[/green]")
    if ongoing_diff:
        resource_strings.append(f"Update IAM Policy:\t[green]{ongoing_name}[/green]")

    if setup_diff:
        resource_strings.append("")
        resource_strings.append(f"Proposed changes to the existing [green]{setup_name}[/green] IAM Policy:")
        resource_strings.append(show_policy_diff(setup_diff))

    if ongoing_diff:
        resource_strings.append("")
        resource_strings.append(f"Proposed changes to the existing [green]{ongoing_name}[/green] IAM Policy:")
        resource_strings.append(show_policy_diff(ongoing_diff))

    if not setup_arn or not ongoing_arn:
        resource_strings.append(
            "\nDocumentation for IAM Policies at "
            "[link]https://docs.coiled.io/user_guide/aws_configure.html#create-iam-policies[/link]"
        )

    resource_desc = "\n".join(resource_strings)
    print(Panel(resource_desc, width=WIDTH))

    if not yes and not Confirm.ask(PROMPTS["initial"], default=True):
        coiled.add_interaction(action="prompt:Setup_AWS", success=False)
        return False

    coiled.add_interaction(action="prompt:Setup_AWS", success=True)

    create_arns = []

    if not user_exists:
        user_arn = create_user(iam, user_name)
        if user_arn:
            create_arns.append(user_arn)

    if not setup_arn:
        setup_arn = create_or_update_policy(iam, aws_account, setup_name, setup_doc)
        create_arns.append(setup_arn)
    elif setup_diff:
        setup_arn = create_or_update_policy(iam, aws_account, setup_name, setup_doc)

    if not ongoing_arn:
        ongoing_arn = create_or_update_policy(iam, aws_account, ongoing_name, ongoing_doc)
        create_arns.append(ongoing_arn)
    elif ongoing_diff:
        ongoing_arn = create_or_update_policy(iam, aws_account, ongoing_name, ongoing_doc)

    attach_policy(iam, user_name, setup_arn)
    attach_policy(iam, user_name, ongoing_arn)

    print()
    if create_arns:
        print("The following resources were created in your AWS account:")
        for arn in create_arns:
            print(f"  {arn}")
    print(f"IAM User [green]{user_name}[/green] is now setup with IAM Policies attached.")
    print()

    check_quotas(session, region=region)

    key, secret = make_access_key(iam, user_name, accept_delete=accept_delete)

    if manual_final_setup:
        return show_manual_setup(key, secret, coiled_account)
    else:
        return do_coiled_setup(
            iam=iam, key=key, secret=secret, region=region, coiled_account=coiled_account, yes=yes, use_shim=use_shim
        )


def show_manual_setup(key, secret, coiled_account):
    if not coiled_account:
        with coiled.Cloud() as cloud:
            coiled_account = cloud.default_account

    setup_url = (
        f"{dask.config.get('coiled.server', coiled.utils.COILED_SERVER)}/"
        f"{coiled_account}/settings/setup/credentials"
    )

    print(
        Panel(
            "You've successfully configured an IAM User for Coiled "
            "in your AWS account. "
            "You can now complete your Coiled account setup by granting "
            "us access to this IAM User:\n"
            "\n"
            f"1. Go to [link]{setup_url}[/link] and select AWS.\n"
            "\n"
            # FIXME adjust instructions once there's better web UI flow
            #  ideally we'd have direct URL to relevant next step (where you'd enter access key)
            '2. Select "Browser Setup".\n'
            "\n"
            "3. Select your desired default AWS region and enter these values where prompted:\n"
            "\n"
            f"\tAWS Access Key ID:\t[green]{key}[/green]\n"
            f"\tAWS Secret Access Key:\t[green]{secret}[/green]\n"
            "\n"
            "4. Continue with the other account setup steps; you'll be able to "
            "choose non-default network or container registry settings as desired.",
            width=WIDTH,
        )
    )

    return True


def do_just_update_policies(iam, aws_account, setup_name, ongoing_name, yes) -> bool:
    # Check for existing policies
    setup_arn, setup_diff = get_policy_diff(iam, aws_account, setup_name, setup_doc)
    ongoing_arn, ongoing_diff = get_policy_diff(iam, aws_account, ongoing_name, ongoing_doc)

    if not setup_arn:
        print(f"[red]WARNING[/red]: No IAM Policy named [green]{setup_name}[/green] found.")
        print("Use `--setup-policy` to specify a different name for the existing setup policy.")
        print()
        return False

    if not ongoing_arn:
        print(f"[red]WARNING[/red]: No IAM Policy named [green]{ongoing_name}[/green] found")
        print("Use `--ongoing-policy` to specify a different name for the existing ongoing policy.")
        print()
        return False

    if setup_diff:
        print(f"Proposed changes to the existing [green]{setup_name}[/green] IAM Policy:")
        show_policy_diff(setup_diff)
        print()

    if ongoing_diff:
        print(f"Proposed changes to the existing [green]{ongoing_name}[/green] IAM Policy:")
        show_policy_diff(ongoing_diff)
        print()

    if setup_arn and ongoing_arn and not setup_diff and not ongoing_diff:
        print("Your AWS IAM Policies are up-to-date")
    elif setup_arn and not setup_diff:
        print("Your [bold]setup[/bold] IAM Policy is up-to-date")
        print("You may need to update your [bold]ongoing[/bold] IAM Policy.")
    elif ongoing_arn and not ongoing_diff:
        print("Your [bold]ongoing[/bold] IAM Policy is up-to-date")
        print("You may need to update your [bold]setup[/bold] IAM Policy.")

    elif not yes and not Confirm.ask(PROMPTS["initial"], default=True):
        return False

    if setup_diff:
        update_policy(iam, aws_account, setup_name, setup_doc)

    if ongoing_diff:
        update_policy(iam, aws_account, ongoing_name, ongoing_doc)

    return True


def get_session(aws_profile: Optional[str], region_name: Optional[str], skip_telemetry: bool = False):
    try:
        session = boto3.Session(profile_name=aws_profile, region_name=region_name)
        if not skip_telemetry:
            coiled.add_interaction(
                action="BotoSession",
                success=True,
                profile=aws_profile,
                region_name=session.region_name,
            )
        return session
    except botocore.exceptions.ProfileNotFound:
        coiled.add_interaction(
            action="BotoSession",
            success=False,
            profile=aws_profile,
            error_message="ProfileNotFound",
        )
        print()
        print(f"[red]The profile `{aws_profile}` is not configured in your local AWS credentials.")
        print(
            "If this isn't the correct AWS identity or account, you can specify a different profile "
            "from your AWS credentials file using the "
            "[green]coiled setup aws [bold]--profile[/bold][/green] argument"
        )
        setup_failure("Requested AWS profile not found", backend="aws")
        return None


def do_setup(
    slug,
    aws_profile=None,
    setup_name=None,
    ongoing_name=None,
    just_update_policies=False,
    just_update_instance_policy=False,
    region=None,
    cloudshell_link=None,
    manual_final_setup=None,
    quotas=None,
    yes=False,
    accept_delete=False,
    use_shim=False,
    coiled_account=None,
) -> bool:
    local_user = get_local_user()

    # this isn't perfect since we aren't checking if token is valid, but it's better than nothing
    is_logged_in = bool(dask.config.get("coiled.token", None))

    # We don't want to require Coiled account if just using `coiled setup aws --quotas`, thus
    # skipping telemetry for `--quotas` if user doesn't already have local Coiled token.
    skip_telemetry = bool(quotas and not is_logged_in)

    if not is_logged_in and not quotas:
        print("To set up your Coiled account, you'll need to authorize this computer to access your Coiled account.")

    if not skip_telemetry:
        # This will trigger auth flow if necessary.
        try:
            coiled.add_interaction(
                action="CliSetupAwsQuotas" if quotas else "CliSetupAws",
                success=True,
                local_user=local_user,
                # use keys that match the cli args
                profile=aws_profile,
                iam_user=slug,
                setup_policy=setup_name,
                ongoing_policy=ongoing_name,
                update_policies=just_update_policies,
                update_instance_policy=just_update_instance_policy,
                region=region,
                cloudshell_link=cloudshell_link,
                manual_final_setup=manual_final_setup,
                yes=yes,
                accept_delete=accept_delete,
                coiled_account=coiled_account,
                quotas=quotas,
            )
        except KeyboardInterrupt:
            if not bool(dask.config.get("coiled.token", None)):
                print("[red]This computer doesn't have access to your Coiled account so setup cannot continue.")
                print("Try running [green]coiled login[/green] to authorize access to your Coiled account.")
                return False
        except ValueError as e:
            if "Authorization failed" in str(e):
                print("[red]This computer doesn't have access to your Coiled account so setup cannot continue.")
                print("Try running [green]coiled login[/green] to authorize access to your Coiled account.")
                return False
            else:
                raise

    if cloudshell_link:
        show_cloudshell_instructions(region, coiled_account=coiled_account)
        return False

    try:
        session = get_session(aws_profile, region_name=region, skip_telemetry=skip_telemetry)
        if session is None:
            print()
            print(
                "If you don't have the AWS credentials locally, another option is to use CloudShell in the AWS Console."
            )
            show_cloudshell_instructions(region=region, coiled_account=coiled_account)
            return False

        region = region or session.region_name or DEFAULT_REGION

        if quotas:
            try:
                # check quotas and give option to request increases
                check_quotas(session, region=region, just_quota_flow=True, skip_telemetry=skip_telemetry)
            except KeyboardInterrupt:
                pass
            except Exception as e:
                raise e
            return False

        try:
            iam = session.client("iam")
        except Exception as e:
            print()
            print("Something went wrong when trying to use your local AWS credentials.")
            print()
            print(f"[red][bold]{type(e).__name__}[/bold]: {e}[/red]")
            print()
            show_cloudshell_instructions(region, coiled_account=coiled_account)
            return False

        sts = session.client("sts")

        user_name = slug
        setup_name = setup_name or f"{slug}-setup"
        ongoing_name = ongoing_name or f"{slug}-ongoing"

        try:
            aws_account = do_intro(sts, iam, region=region, coiled_account=coiled_account)
            if not aws_account:
                return False

            if just_update_instance_policy:
                return update_instance_profile_policy(iam, aws_account, yes=yes)
            elif just_update_policies:
                return do_just_update_policies(iam, aws_account, setup_name, ongoing_name, yes=yes)
            else:
                return do_full_setup(
                    session,
                    iam,
                    user_name,
                    aws_account,
                    region,
                    setup_name,
                    ongoing_name,
                    coiled_account=coiled_account,
                    manual_final_setup=manual_final_setup,
                    yes=yes,
                    accept_delete=accept_delete,
                    use_shim=use_shim,
                )

        except iam.exceptions.ClientError as e:
            error_code = e.response["Error"].get("Code")
            error_msg = e.response["Error"].get("Message")
            error_op = e.operation_name

            coiled.add_interaction(action=error_op, success=False, error_message=error_msg)

            if "assumed-role/AmazonSageMaker-ExecutionRole" in error_msg:
                print()
                print("It appears that you're trying to set up Coiled from inside Amazon SageMaker.")
                print(
                    "SageMaker has restricted permissions on your AWS account. Although you [bold]can use[/bold] "
                    "Coiled from a SageMaker notebook, you [bold]cannot set up[/bold] Coiled from SageMaker."
                )
                print()
                setup_failure("Inside sagemaker", backend="aws")
                show_cloudshell_instructions(region, coiled_account=coiled_account)
                return False

            elif "AccessDenied" in str(e):
                print()
                print(f"Insufficient permissions to [green]{error_op}[/green] using current AWS profile/user.")
                print("You may want to try with a different AWS profile that has different permissions.")
                print()
                print(f"[red]{error_msg}[/red]")
                print()
                print("To run this setup script you'll need the following IAM permissions:")
                for permission in SCRIPT_REQUIRED_IAM:
                    print(f"- {permission}")
                print(
                    "If you don't have access to an AWS profile with these permissions, you may need to ask "
                    "someone with administrative access to your AWS account to help you create the IAM User "
                    "and IAM Policies described in our documentation: "
                    "[link]https://docs.coiled.io/user_guide/aws/manual.html[/link]"
                )
                setup_failure(
                    f"Permission error during for {error_op}. {error_msg}",
                    backend="aws",
                )
                return False
            else:
                print()
                print(f"Something went wrong when trying to [green]{error_op}[/green].")
                print()
                print(f"[red][bold]{error_code}[/bold]: {error_msg}[/red]")
                print()
                setup_failure(
                    f"Error trying {error_op}. {error_msg}",
                    backend="aws",
                )
                return False

    except KeyboardInterrupt as e:
        tb = "\n".join(traceback.format_tb(e.__traceback__))
        coiled.add_interaction(action="KeyboardInterrupt", success=False, error_message=tb)
        raise

    # catch all so we make sure all errors are tracked
    except Exception as e:
        msg = traceback.format_exc()
        coiled.add_interaction(action="Unknown", success=False, error_message=msg)
        # TODO better generic error handling
        print()
        print("[red][bold]ERROR[/bold][/red] Something unexpected happened:")
        print(f"    [red]{e}")
        print("Please reach out to Coiled Support at support@coiled.io if you need help with this issue.")
        setup_failure(
            f"Unhandled exception {msg}",
            backend="aws",
        )
        return False


def check_local_aws_creds():
    session = boto3.Session()
    sts = session.client("sts")
    try:
        # good call to try, since this doesn't require any IAM permissions
        sts.get_caller_identity()
        return True
    except botocore.exceptions.NoCredentialsError:
        return False


def update_instance_profile_policy(iam, aws_account, yes):
    policy_name = "CoiledInstancePolicy"
    policy_doc = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "CoiledEC2Policy",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "cloudwatch:PutMetricData",
                "aps:RemoteWrite"
            ],
            "Resource": "*"
        }
    ]
}"""

    # Check for existing policy
    policy_arn, policy_diff = get_policy_diff(iam, aws_account, policy_name, policy_doc)

    if not policy_arn:
        print(f"[red]WARNING[/red]: No IAM Policy named [green]{policy_name}[/green] found.")
        print()

    if policy_diff:
        print(f"Proposed changes to the existing [green]{policy_name}[/green] IAM Policy:")
        show_policy_diff(policy_diff)
        print()

    if policy_arn and not policy_diff:
        print(f"Your AWS policy document for {policy_name} is up-to-date")

    elif not yes and not Confirm.ask(f"Update {policy_name} policy document?", default=True):
        return False

    if policy_diff:
        update_policy(iam, aws_account, policy_name, policy_doc)

    return True


def check_quotas(session, region: str, just_quota_flow: bool = False, skip_telemetry: bool = False):
    quota_client = session.client("service-quotas", region_name=region)

    quotas = [
        {
            "class": "Standard On-Demand",
            "name": "Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances",
            "code": "L-1216C47A",
            "low": 44,
        },
        {
            "class": "Standard Spot",
            "name": "All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests",
            "code": "L-34B43A08",
            "low": 44,
        },
        {
            "class": "G4dn (NVIDIA T4 GPU) On-Demand",
            "name": "Running On-Demand G and VT instances",
            "code": "L-DB2E81BA",
            "low": -1,
        },
        {
            "class": "G4dn (NVIDIA T4 GPU) Spot",
            "name": "All G and VT Spot Instance Requests",
            "code": "L-3819A6DF",
            "low": -1,
        },
        {
            "class": "P (NVIDIA V100/A100 GPU) On-Demand",
            "name": "Running On-Demand P instances",
            "code": "L-417A185B",
            "low": -1,
        },
        {
            "class": "P (NVIDIA V100/A100 GPU) Spot",
            "name": "All P Spot Instance Requests",
            "code": "L-7212CCBC",
            "low": -1,
        },
    ]

    quota_lines = []

    for quota in quotas:
        quota["link"] = get_quota_link(region, quota["code"])

    error_message = None
    got_quotas = False
    low_quotas = []
    try:
        for quota in quotas:
            quota["value"] = get_quota_value(quota_client, quota["code"])
            if quota.get("low") is not None and quota["value"] <= quota["low"]:
                quota["is_low"] = True
                low_quotas.append(quota)
            got_quotas = True
    except quota_client.exceptions.AccessDeniedException:
        error_message = (
            "[red]Your active AWS account doesn't have permission to read service quotas.[/red]\n\n"
            "You can check the quotas in the AWS Console using the links below."
        )
    except Exception as e:
        error_message = (
            "An unexpected error occurred while trying to read your AWS service quotas:\n\n"
            f"[red]{e}[/red]\n\n"
            "You can check the quotas in the AWS Console using the links below."
        )

    for quota in quotas:
        quota_label = quota["class"]
        if quota.get("value") is not None:
            quota_value_text = f"{quota.get('value'):>6} vCPU"
            if quota.get("is_low"):
                quota_value_text = f"{quota_value_text} (this quota is low, you may wish to request increase)"
        else:
            quota_value_text = f"[link]{quota['link']}[/link]"

        quota_lines.append(f"{quota_label:<36}{quota_value_text}")

    quota_text = "\n".join(quota_lines)

    quota_text = (
        "[bold]Current AWS Quotas[/bold]\n\n"
        f"{quota_text}\n\n"
        "[bold]Standard[/bold] includes:\n"
        "    general purpose [bold]M[/bold] and [bold]T[/bold] families (e.g., M6i, T3),\n"
        "    compute optimized [bold]C[/bold] families (e.g., C6i),\n"
        "    memory optimized [bold]R[/bold] families (e.g., R6i).\n"
        "\n[bold]GPU[/bold] instances have a separate quotas based on GPU type."
    )

    if got_quotas and not just_quota_flow:
        example_cost = "2.46" if region == "us-west-1" else "2.11"
        example_region = region if region in ("us-east-1", "us-east-2", "us-west-1", "us-west-2") else "us-east-1"

        quota_text = (
            f"{quota_text}\n\n"
            "[bold]Example Usage:[/bold]\n"
            "10 VM cluster with m6i.xlarge instances would have 40 vCPUs.\n"
            f"AWS compute cost would be ${example_cost}/hr "
            f"for on-demand instances in {example_region}."
        )

    if error_message:
        quota_text = f"{error_message}\n\n{quota_text}"

    print(Panel(quota_text, width=WIDTH))

    if got_quotas:
        if just_quota_flow:
            # when running explicit quota check (`--quotas`), prompt about each quota
            do_quota_increases(quota_client, region, quotas, skip_telemetry=skip_telemetry)
        elif low_quotas:
            print(
                "Some of your quotas are low. If you'd like to request any increases for these quotas, "
                "we can prompt you for the desired quota value and attempt to submit this request to AWS.\n"
            )
            if Confirm.ask(PROMPTS["request_quotas"], default=True):
                # when running normal setup flow, just prompt about low quotas
                # note that we never consider GPU quotas low ("low" threshold is set to -1)
                do_quota_increases(quota_client, region, low_quotas, skip_telemetry=skip_telemetry)


def get_quota_value(quota_client, quota_code: str) -> int:
    quota = quota_client.get_service_quota(
        ServiceCode="ec2",
        QuotaCode=quota_code,
    )
    return int(quota["Quota"]["Value"])


def do_quota_increases(quota_client, region: str, quotas: list, skip_telemetry: bool):
    for quota in quotas:
        prompt = (
            f"[bold]{quota['class']}[/bold] ({region}) current quota: [bold]{quota['value']}[/bold]\n"
            "Request new quota value? (return to skip):"
        )
        desired_value = IntPrompt.ask(prompt, default=quota["value"])
        if desired_value and desired_value != quota["value"]:
            success, error_message = request_quota_increase(quota_client, region, quota, desired_value=desired_value)

            if not skip_telemetry:
                coiled.add_interaction(
                    action="RequestServiceQuotaIncrease",
                    success=success,
                    quota_name=quota["name"],
                    desired_value=desired_value,
                    current_value=quota["value"],
                    error_message=error_message or None,
                )

            if not success:
                # something failed so stop
                return


def request_quota_increase(
    quota_client, region: str, quota: dict, desired_value: Union[int, float]
) -> Tuple[bool, str]:
    quota_label = quota["class"]
    quota_code = quota["code"]
    try:
        quota_response = quota_client.request_service_quota_increase(
            ServiceCode="ec2",
            QuotaCode=quota_code,
            DesiredValue=float(desired_value),
        )

        request_status = quota_response["RequestedQuota"]["Status"]
        request_case_id = quota_response["RequestedQuota"].get("CaseId")  # might not be in response

        info_text = (
            f"You've submitted a request in increase [bold]{quota_label}[/bold] "
            f"({quota_code}) in {region} to [bold]{desired_value}[/bold]. "
            f"The current status of your request is [bold]{request_status}[/bold]."
        )

        status_text = ""

        if request_status in ("PENDING", "CASE_OPENED"):
            status_text = (
                "Quota requests can take a few days. You can check the status of your request at:\n"
                f"[link]{get_support_case_link(request_case_id)}"
            )
        elif request_status in ("DENIED", "CASE_CLOSED"):
            status_text = (
                "You can find more details about your quota request in the AWS Console:\n"
                f"[link]{get_support_case_link(request_case_id)}"
            )

        if status_text:
            info_text = f"{info_text}\n\n{status_text}"

        print(info_text)

        return True, ""

    except Exception as e:
        error_message = (
            "An error occurred while requesting your quota increase:\n\n"
            f"[red]{e}[/red]\n\n"
            f"You can manually request a quota increase for {quota_label} in the AWS Console at:\n"
            f"[link]{get_quota_link(region, quota_code)}[/link]"
        )
        print(error_message)

        return False, str(e)


def get_support_case_link(case_id: Optional[str]) -> str:
    if case_id:
        return f"https://support.console.aws.amazon.com/support/home#/case/?displayId={case_id}"
    return "https://support.console.aws.amazon.com/support/home#/case/history"


def get_quota_link(region: str, quota_code: str) -> str:
    return f"https://{region}.console.aws.amazon.com/servicequotas/home/services/ec2/quotas/{quota_code}"

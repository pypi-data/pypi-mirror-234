from base64 import b64decode, b64encode
from importlib.machinery import PathFinder
from os import path
from pathlib import Path
import json
import os
import re
import sys
import zlib
from typing import Dict, Any

import boto3
import click
import subprocess
from ..utils import kubeconfig, metaflowconfig
from ..utils.schema import (
    OuterboundsCommandResponse,
    CommandStatus,
    OuterboundsCommandStatus,
)
import requests
from requests.exceptions import HTTPError
import hashlib
import base64
from typing import Callable, List

NO_METAFLOW_INSTALL_MESSAGE = "Resolution of 'metaflow' module succeeded but no Metaflow installation was detected."

EXISTING_METAFLOW_MESSAGE = """It seems that there is an existing Metaflow package on your workstation which conflicts with
the Outerbounds platform.
To remove that package, please try `python -m pip uninstall metaflow -y` or reach out to Outerbounds support.
After uninstalling the Metaflow package, please reinstall the Outerbounds package using `python -m pip
install outerbounds --force`.
As always, please reach out to Outerbounds support for any questions."""

MISSING_EXTENSIONS_MESSAGE = (
    "The Outerbounds Platform extensions for Metaflow was not found."
)

MISSING_KUBECTL_MESSAGE = "No installation for kubectl detected on the user's PATH"

BAD_EXTENSION_MESSAGE = (
    "Mis-installation of the Outerbounds Platform extension package has been detected."
)


class Narrator:
    def __init__(self, verbose):
        self.verbose = verbose

    def announce_section(self, name):
        if not self.verbose:
            click.secho("Validating {}...".format(name), nl=False, err=True)

    def section_ok(self):
        if not self.verbose:
            click.secho("\U0001F600", err=True)

    def section_not_ok(self):
        if not self.verbose:
            click.secho("\U0001F641", err=True)

    def announce_check(self, name):
        if self.verbose:
            click.secho("Checking {}...".format(name), nl=False, err=True)

    def ok(self, force=False):
        if self.verbose or force:
            click.secho("OK", fg="green", err=True)

    def not_ok(self, reason=None, force=False):
        if self.verbose or force:
            if reason is None:
                click.secho("NOT OK", fg="red", err=True)
            else:
                message = click.style("NOT OK", fg="red")
                message = "{} {}".format(
                    message, click.style("(" + reason + ")", fg="white")
                )
                click.secho(message, err=True)

    def warn(self, reason=None, force=False):
        if self.verbose or force:
            if reason is None:
                click.secho("WARNING", fg="yellow", err=True)
            else:
                message = click.style("WARNING", fg="yellow")
                message = "{} {}".format(
                    message, click.style("(" + reason + ")", fg="white")
                )
                click.secho(message, err=True)

    def show_reason_and_mitigation(self, reason, mitigation=""):
        if self.verbose:
            click.echo("", err=True)
            click.secho(reason, err=True)
            if mitigation != "":
                click.secho(mitigation, bold=True, err=True)


def check_ob_metaflow(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("Outerbounds Metaflow package")
    narrator.announce_check("Outerbounds Metaflow package")
    check_status = CommandStatus(
        "ob_metaflow",
        status=OuterboundsCommandStatus.OK,
        reason="ob-metaflow is installed.",
        mitigation="",
    )
    spec = PathFinder.find_spec("metaflow")
    # We can't resolve metaflow module.
    if spec is None or spec.origin is None:
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason="Unable to resolve module 'metaflow'.",
            mitigation="",
        )
        narrator.not_ok()
        return check_status
    # We can resolve the module but we need to
    # make sure we're getting it from the correct
    # package.
    basedir = Path(path.join(path.dirname(spec.origin), ".."))
    # Next, let's check for parallel installations of ob-metaflow
    # and OSS metaflow. This can cause problems because they
    # overwrite each other.
    found = list(basedir.glob("metaflow-*.dist-info"))
    if len(found) > 0:
        # We found an existing OSS Metaflow install.
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason=EXISTING_METAFLOW_MESSAGE,
            mitigation="",
        )
        narrator.not_ok()
        return check_status
    # For completeness, let's verify ob_metaflow is really installed.
    # Should never get here since importing Metaflow's vendored version of click
    # would've failed much earlier on.
    found = list(basedir.glob("ob_metaflow-*.dist-info"))
    if len(found) == 0:
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason=NO_METAFLOW_INSTALL_MESSAGE,
            mitigation="Please reinstall the Outerbounds package using `python -m pip install outerbounds --force`.",
        )
        narrator.not_ok()
    else:
        narrator.ok()
    return check_status


def check_ob_extension(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("Outerbounds Platform extensions package")
    narrator.announce_check("Outerbounds Platform extensions package")
    check_status = CommandStatus(
        "ob_extension",
        status=OuterboundsCommandStatus.OK,
        reason="ob-metaflow-extensions package is installed.",
        mitigation="",
    )

    spec = PathFinder.find_spec("metaflow")

    if spec is None or spec.origin is None:
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason="Unable to resolve module 'metaflow'.",
            mitigation="",
        )
        narrator.not_ok()
        return check_status
    basedir = Path(path.join(path.dirname(spec.origin), ".."))
    # Metaflow install looks fine. Let's verify the correct extensions were installed.
    extensions = Path(basedir, "metaflow_extensions", "outerbounds")
    # Outerbounds extensions not found at all
    if not extensions.exists():
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason=MISSING_EXTENSIONS_MESSAGE,
            mitigation="""Please remove any existing Metaflow installations and reinstall the Outerbounds
            package using `python -m pip install outerbounds --force`.""",
        )
        narrator.not_ok()
        return check_status
    subdirs = [
        d.name
        for d in extensions.glob("*")
        if d.is_dir() and not d.name.startswith("__")
    ]
    subdirs.sort()
    if subdirs != ["config", "plugins", "toplevel"]:
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason=BAD_EXTENSION_MESSAGE,
            mitigation="Please reinstall the Outerbounds package using `python -m pip install outerbounds --force`.",
        )
        narrator.not_ok()
    else:
        narrator.ok()
    return check_status


def check_kubectl_installed(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("kubectl installation")
    narrator.announce_check("kubectl installation")
    check_status = CommandStatus(
        "kubectl",
        status=OuterboundsCommandStatus.OK,
        reason="kubectl is installed.",
        mitigation="",
    )
    try:
        # Check if kubectl can be executed from the command line
        subprocess.run(["kubectl", "--help"], capture_output=True, check=True)
        narrator.ok()
        return check_status
    except:
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason=MISSING_KUBECTL_MESSAGE,
            mitigation="Please install kubectl manually from https://kubernetes.io/docs/tasks/tools/#kubectl",
        )
        narrator.not_ok(reason=MISSING_KUBECTL_MESSAGE)
        return check_status


class ConfigEntrySpec:
    def __init__(self, name, expr, expected=None):
        self.name = name
        self.expr = re.compile(expr)
        self.expected = expected


def get_config_specs():
    return [
        ConfigEntrySpec(
            "METAFLOW_DATASTORE_SYSROOT_S3", "s3://[a-z0-9\-]+/metaflow[/]?"
        ),
        ConfigEntrySpec("METAFLOW_DATATOOLS_S3ROOT", "s3://[a-z0-9\-]+/data[/]?"),
        ConfigEntrySpec("METAFLOW_DEFAULT_AWS_CLIENT_PROVIDER", "obp", expected="obp"),
        ConfigEntrySpec("METAFLOW_DEFAULT_DATASTORE", "s3", expected="s3"),
        ConfigEntrySpec("METAFLOW_DEFAULT_METADATA", "service", expected="service"),
        ConfigEntrySpec(
            "METAFLOW_KUBERNETES_NAMESPACE", "jobs\-default", expected="jobs-default"
        ),
        ConfigEntrySpec("METAFLOW_KUBERNETES_SANDBOX_INIT_SCRIPT", "eval \$\(.*"),
        ConfigEntrySpec("METAFLOW_SERVICE_AUTH_KEY", "[a-zA-Z0-9!_\-\.]+"),
        ConfigEntrySpec("METAFLOW_SERVICE_URL", "https://metadata\..*"),
        ConfigEntrySpec("METAFLOW_UI_URL", "https://ui\..*"),
        ConfigEntrySpec("OBP_AUTH_SERVER", "auth\..*"),
    ]


def check_metaflow_config(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("local Metaflow config")
    check_status = CommandStatus(
        "metaflow_config",
        status=OuterboundsCommandStatus.OK,
        reason="Metaflow config is valid.",
        mitigation="",
    )

    config = metaflowconfig.init_config()
    for spec in get_config_specs():
        narrator.announce_check("config entry " + spec.name)
        if spec.name not in config:
            reason = "Missing"
            if spec.expected is not None:
                reason = "".join([reason, ", expected '{}'".format(spec.expected)])
            narrator.not_ok(reason=reason)
            check_status.update(
                status=OuterboundsCommandStatus.FAIL,
                reason=reason,
                mitigation="Please re-run outerbounds configure using the command on the onboarding page.",
            )
        else:
            v = config[spec.name]
            if spec.expr.fullmatch(v) is None:
                if spec.name.find("AUTH") == -1:
                    reason = "Have '{}'".format(v)
                    if spec.expected is not None:
                        reason += ", expected '{}'".format(spec.expected)
                else:
                    reason = "Bad value"
                narrator.not_ok(reason=reason)
                check_status.update(
                    status=OuterboundsCommandStatus.FAIL,
                    reason=reason,
                    mitigation="Please re-run outerbounds configure using the command on the onboarding page.",
                )
            else:
                narrator.ok()
    return check_status


def check_metaflow_token(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("metaflow token in config")
    narrator.announce_check("metaflow token in config")
    check_status = CommandStatus(
        "metaflow_token",
        status=OuterboundsCommandStatus.OK,
        reason="Metaflow token is valid.",
        mitigation="",
    )

    config = metaflowconfig.init_config()
    try:
        if "OBP_AUTH_SERVER" in config:
            k8s_response = requests.get(
                f"https://{config['OBP_AUTH_SERVER']}/generate/k8s",
                headers={"x-api-key": config["METAFLOW_SERVICE_AUTH_KEY"]},
            )
            try:
                k8s_response.raise_for_status()
                narrator.ok()
                return check_status
            except HTTPError as e:
                if e.response is not None and (
                    e.response.status_code == 401 or e.response.status_code == 403
                ):
                    check_status.update(
                        status=OuterboundsCommandStatus.FAIL,
                        reason="Invalid metaflow auth token",
                        mitigation="Please go to the onboarding page and re-run outerbounds configure.",
                    )
                else:
                    narrator.not_ok(reason="Can't check validity of token")
                    check_status.update(
                        status=OuterboundsCommandStatus.FAIL,
                        reason="Can't check validity of token",
                        mitigation="",
                    )
                return check_status
        else:
            narrator.not_ok(
                reason="Can't check validity of token. Missing OBP_AUTH_SERVER in config."
            )
            check_status.update(
                status=OuterboundsCommandStatus.FAIL,
                reason="Can't check validity of token. Missing OBP_AUTH_SERVER in config.",
                mitigation="",
            )
            return check_status
    except Exception:
        narrator.not_ok(reason="Invalid metaflow auth key")
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason="Encountered an error while validating metaflow token",
            mitigation="",
        )
        return check_status


def check_workstation_api_accessible(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("connectivity with Workstation API")
    narrator.announce_check("connectivity with Workstation API")
    check_status = CommandStatus(
        "api_connectivity",
        status=OuterboundsCommandStatus.OK,
        reason="Workstation api is accessible.",
        mitigation="",
    )

    try:
        config = metaflowconfig.init_config()
        missing_keys = []
        if "METAFLOW_SERVICE_AUTH_KEY" not in config:
            missing_keys.append("METAFLOW_SERVICE_AUTH_KEY")
        if "OBP_API_SERVER" not in config:
            missing_keys.append("OBP_API_SERVER")

        if len(missing_keys) > 0:
            missing_keys_msg = (
                f"Can't check api connectivity. Missing keys: {', '.join(missing_keys)}"
            )
            narrator.not_ok(reason=missing_keys_msg)
            check_status.update(
                status=OuterboundsCommandStatus.FAIL,
                reason=missing_keys_msg,
                mitigation="Re-run outerbounds configure using the command on the onboarding page.",
            )
            return check_status
        k8s_response = requests.get(
            f"https://{config['OBP_API_SERVER']}/v1/workstations",
            headers={"x-api-key": config["METAFLOW_SERVICE_AUTH_KEY"]},
        )
        try:
            k8s_response.raise_for_status()
            narrator.ok()
            return check_status
        except HTTPError as e:
            if e.response != None:
                error_status = e.response.status_code

            error_msg = f"Cannot connect to outerbounds services: Status={error_status}"
            narrator.not_ok(reason=error_msg)
            check_status.update(
                status=OuterboundsCommandStatus.FAIL, reason=error_msg, mitigation=""
            )
            return check_status
    except Exception as e:
        narrator.not_ok(
            reason="Encountered an error while trying to validate workstation api connectivity."
        )
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason="Encountered an error while trying to validate workstation api connectivity.",
            mitigation="",
        )
        return check_status


def check_kubeconfig_valid_for_workstations(narrator: Narrator) -> CommandStatus:
    narrator.announce_section("local kubeconfig")
    narrator.announce_check("local kubeconfig")
    check_status = CommandStatus(
        "kubeconfig",
        status=OuterboundsCommandStatus.OK,
        reason="Kubeconfig is valid to use workstations.",
        mitigation="",
    )

    try:
        config = metaflowconfig.init_config()
        missing_keys = []
        if "METAFLOW_SERVICE_AUTH_KEY" not in config:
            missing_keys.append("METAFLOW_SERVICE_AUTH_KEY")
        if "OBP_AUTH_SERVER" not in config:
            missing_keys.append("OBP_AUTH_SERVER")

        if len(missing_keys) > 0:
            missing_keys_msg = f"Can't check validity of kubeconfig. Missing keys: {', '.join(missing_keys)}"
            narrator.not_ok(reason=missing_keys_msg)
            check_status.update(
                status=OuterboundsCommandStatus.FAIL,
                reason=missing_keys_msg,
                mitigation="Re-run outerbounds configure using the command on the onboarding page.",
            )
            narrator.not_ok()
            return check_status

        k8s_response = requests.get(
            f"https://{config['OBP_AUTH_SERVER']}/generate/k8s",
            headers={"x-api-key": config["METAFLOW_SERVICE_AUTH_KEY"]},
        )
        try:
            k8s_response.raise_for_status()
            k8s_response_json = k8s_response.json()
            current_kubeconfig = kubeconfig.get_kube_config_or_init_default()
            expected_server_url = k8s_response_json["endpoint"]
            token_data = base64.b64decode(
                k8s_response_json["token"].split(".")[1] + "=="
            )

            ws_namespace = "ws-{}".format(
                hashlib.md5(
                    bytes(json.loads(token_data)["username"], "utf-8")
                ).hexdigest()
            )

            if not kubeconfig.validate_kubeconfig_fields_for_workstations(
                expected_server_url, ws_namespace, current_kubeconfig
            ):
                narrator.not_ok(reason="Kubeconfig is not valid to use workstations")
                check_status.update(
                    status=OuterboundsCommandStatus.FAIL,
                    reason="Kubeconfig is not valid to use workstations",
                    mitigation="Run outerbounds configure-cloud-workstation to reset your kubeconfig.",
                )
                return check_status
            else:
                narrator.ok()
                return check_status
        except kubeconfig.KubeconfigError as ke:
            narrator.not_ok(
                reason="Encountered an error while trying to validate kubeconfig. "
                + str(ke)
            )
            check_status.update(
                status=OuterboundsCommandStatus.FAIL,
                reason="Encountered an error while trying to validate kubeconfig. "
                + str(ke),
                mitigation="",
            )
            return check_status
        except HTTPError as e:
            if e.response is not None and (
                e.response.status_code == 401 or e.response.status_code == 403
            ):
                err_msg = f"Cannot connect to outerbounds services: Status={e.response.status_code}"
                narrator.not_ok(reason=err_msg)
                check_status.update(
                    status=OuterboundsCommandStatus.FAIL, reason=err_msg, mitigation=""
                )
            else:
                err_msg = (
                    "Could not contact the outerbounds server to validate kubeconfig."
                )
                narrator.not_ok(reason=err_msg)
                check_status.update(
                    status=OuterboundsCommandStatus.FAIL, reason=err_msg, mitigation=""
                )
            return check_status
    except Exception as e:
        narrator.not_ok(
            reason="Encountered an error while trying to validate kubeconfig."
        )
        check_status.update(
            status=OuterboundsCommandStatus.FAIL,
            reason="Encountered an error while trying to validate kubeconfig.",
            mitigation="",
        )
        return check_status


def execute_checks(
    check_names: List[str], narrator: Narrator
) -> OuterboundsCommandResponse:
    check_name_to_func: Dict[str, Callable[[Narrator], CommandStatus]] = {
        "kubeconfig": check_kubeconfig_valid_for_workstations,
        "api_connectivity": check_workstation_api_accessible,
        "kubectl": check_kubectl_installed,
        "metaflow_token": check_metaflow_token,
        "metaflow_config": check_metaflow_config,
        "ob_metaflow": check_ob_metaflow,
        "ob_extension": check_ob_extension,
    }

    check_response = OuterboundsCommandResponse()

    for check_name in check_names:
        check_status = check_name_to_func[check_name](narrator)
        if check_status.status == OuterboundsCommandStatus.OK:
            narrator.section_ok()
        else:
            if check_status.status == OuterboundsCommandStatus.FAIL:
                narrator.show_reason_and_mitigation(
                    check_status.reason, check_status.mitigation
                )
            narrator.section_not_ok()

        check_response.add_step(check_status)

    return check_response


def read_input(encoded):
    if encoded == "-":
        return "".join(sys.stdin.readlines()).replace("\n", "")
    else:
        return encoded


def to_unicode(x):
    if isinstance(x, bytes):
        return x.decode("utf-8")
    else:
        return str(x)


def serialize(data):
    data_str = json.dumps(data)
    compressed = zlib.compress(data_str.encode("UTF-8"))
    return str(b64encode(compressed), "utf-8")


def deserialize(serialized_data):
    compressed = b64decode(serialized_data)
    uncompressed = zlib.decompress(compressed)
    return json.loads(to_unicode(uncompressed))


class DecodedConfigProcessingError(Exception):
    pass


class ConfigurationWriter:
    def __init__(self, prefixed_encoded_config: str, out_dir, profile):
        self.existing: Dict[str, Any] = dict()
        self.encoded_config = read_input(prefixed_encoded_config)
        # Remove "prefix:" if present. Note our CLI is agnostic to the prefix.
        # Think of it as a human-readable annotation only.
        self.encoded_config = prefixed_encoded_config.split(":", maxsplit=1)[-1]
        self.decoded_config = None
        self.out_dir = out_dir
        self.profile = profile

    def decode(self):
        self.decoded_config = deserialize(self.encoded_config)

    def process_decoded_config(self):
        config_type = self.decoded_config.get("OB_CONFIG_TYPE", "inline")
        if config_type == "inline":
            return
        elif config_type == "aws-secrets-manager":
            try:
                secret_arn = self.decoded_config["AWS_SECRETS_MANAGER_SECRET_ARN"]
                region = self.decoded_config["AWS_SECRETS_MANAGER_REGION"]
            except KeyError as e:
                raise DecodedConfigProcessingError(
                    f"{str(e)} key is required for aws-ref config type"
                )
            try:
                client = boto3.client("secretsmanager", region_name=region)
                response = client.get_secret_value(SecretId=secret_arn)
                self.decoded_config = json.loads(response["SecretBinary"])
            except Exception as e:
                raise DecodedConfigProcessingError(
                    f"Failed to retrieve secret {secret_arn}\n\n{str(e)}"
                )
        else:
            raise DecodedConfigProcessingError(f"Unknown config type: {config_type}")

    def path(self):
        if self.profile == "":
            return path.join(self.out_dir, "config.json")
        else:
            return path.join(self.out_dir, "config_{}.json".format(self.profile))

    def display(self):
        # Create a copy so we can use the real config later, possibly
        display_config = dict()
        for k in self.decoded_config.keys():
            # Replace any auth sensitive bits with placeholder values for security
            if k.find("AUTH_KEY") > -1 or k.find("AUTH_TOKEN") > -1:
                display_config[k] = "*****"
            else:
                display_config[k] = self.decoded_config[k]
        click.echo(json.dumps(display_config, indent=4))

    def confirm_overwrite(self):
        return self.confirm_overwrite_config(self.path())

    def write_config(self):
        config_path = self.path()
        # TODO config contains auth token - restrict file/dir modes
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        self.existing.update(self.decoded_config)
        with open(config_path, "w") as fd:
            json.dump(self.existing, fd, indent=4)

    def confirm_overwrite_config(self, config_path):
        if os.path.exists(config_path):
            if not click.confirm(
                click.style(
                    "We found an existing configuration for your "
                    + "profile. Do you want to replace the existing "
                    + "configuration?",
                    fg="red",
                    bold=True,
                )
            ):
                click.secho(
                    "You can configure a different named profile by using the "
                    "--profile argument. You can activate this profile by setting "
                    "the environment variable METAFLOW_PROFILE to the named "
                    "profile.",
                    fg="yellow",
                )
                return False
        return True


@click.group(help="The Outerbounds Platform CLI", no_args_is_help=True)
def cli(**kwargs):
    pass


@cli.command(help="Check packages and configuration for common errors")
@click.option(
    "-n",
    "--no-config",
    is_flag=True,
    default=False,
    show_default=True,
    help="Skip validating local Metaflow configuration",
)
@click.option(
    "-o",
    "--output",
    default="",
    help="Show output in the specified format.",
    type=click.Choice(["json", ""]),
)
@click.option(
    "-w",
    "--workstation",
    is_flag=True,
    default=False,
    help="Check whether all workstation dependencies are installed correctly.",
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose output")
def check(no_config, verbose, output, workstation=False):
    narrator = Narrator(verbose)

    if not workstation:
        check_names = [
            "ob_metaflow",
            "ob_extension",
            "metaflow_config",
            "metaflow_token",
        ]
    else:
        check_names = [
            "metaflow_config",
            "metaflow_token",
            "kubeconfig",
            "api_connectivity",
            "kubectl",
        ]

    check_response = execute_checks(check_names, narrator)

    if output == "json":
        click.echo(json.dumps(check_response.as_dict(), indent=4))
    if (check_response.status != OuterboundsCommandStatus.OK) and not verbose:
        click.echo("Run 'outerbounds check -v' to see more details.", err=True)
        sys.exit(1)


@cli.command(help="Decode Outerbounds Platform configuration strings")
@click.option(
    "-d",
    "--config-dir",
    default=path.expanduser(os.environ.get("METAFLOW_HOME", "~/.metaflowconfig")),
    help="Path to Metaflow configuration directory",
    show_default=True,
)
@click.option(
    "-p",
    "--profile",
    default="",
    help="Configure a named profile. Activate the profile by setting "
    "`METAFLOW_PROFILE` environment variable.",
)
@click.option(
    "-e",
    "--echo",
    is_flag=True,
    help="Print decoded configuration to stdout",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Force overwrite of existing configuration",
)
@click.argument("encoded_config", required=True)
def configure(
    encoded_config=None, config_dir=None, profile=None, echo=None, force=False
):
    writer = ConfigurationWriter(encoded_config, config_dir, profile)
    try:
        writer.decode()
    except:
        click.secho("Decoding the configuration text failed.", fg="red")
        sys.exit(1)
    try:
        writer.process_decoded_config()
    except DecodedConfigProcessingError as e:
        click.secho(
            "Resolving the configuration from AWS Secrets Manager failed.", fg="red"
        )
        click.secho(str(e), fg="magenta")
        sys.exit(1)
    try:
        if echo == True:
            writer.display()
        if force or writer.confirm_overwrite():
            writer.write_config()
    except Exception as e:
        click.secho("Writing the configuration file '{}' failed.".format(writer.path()))
        click.secho("Error: {}".format(str(e)))

import click
import base64
import json
import os
from os import path
from ..utils import metaflowconfig
from requests.exceptions import HTTPError
from ..utils.schema import (
    OuterboundsCommandResponse,
    CommandStatus,
    OuterboundsCommandStatus,
)
from .workstations_cli import get_all_workstations
from fabric import Connection, Result
from fabric.transfer import Transfer
from typing import List, Tuple, Union
from os.path import expanduser
from tempfile import NamedTemporaryFile
from metaflow_extensions.outerbounds.plugins import ObpAuthProvider
import string
import random


@click.group()
def cli(**kwargs):
    pass


@cli.command(help="Start on-prem workstation", hidden=True)
@click.option(
    "-w",
    "--workstation",
    default="",
    help="The ID of the on-prem workstation to start",
)
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
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "--env-file",
    default=expanduser("~/.metaflowconfig/obp-onprem.env"),
    help="Location of the env file containing the names of the environment variables for the workstation",
)
def start_onprem_workstation(
    workstation=None, config_dir=None, profile=None, env_file=None
):
    on_prem_client = OnPremWorkstationClient(config_dir, profile, env_file=env_file)
    try:
        on_prem_client.ensure_container_running(workstation)
    except Exception as e:
        on_prem_client.command_response._message = str(e)
        click.echo(f"Error starting workstation: {str(e)}", err=True)
    click.echo(json.dumps(on_prem_client.command_response.as_dict(), indent=4))


@cli.command(help="Start on-prem workstation", hidden=True)
@click.option(
    "-w",
    "--workstation",
    required=True,
    help="The ID of the on-prem workstation to start",
)
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
    help="The named metaflow profile in which your workstation exists",
)
def check_onprem_workstation_status(
    workstation=None,
    config_dir=None,
    profile=None,
):
    on_prem_client = OnPremWorkstationClient(config_dir, profile)
    try:
        curr_status = on_prem_client.check_workstation_status(workstation)
        on_prem_client.command_response.add_or_update_data(
            "workstation_status", curr_status
        )
    except Exception as e:
        on_prem_client.command_response._message = str(e)

    click.echo(json.dumps(on_prem_client.command_response.as_dict(), indent=4))


def get_all_onprem_workstations(config_dir, profile, admin_mode=False):
    all_workstations = get_all_workstations(config_dir, profile, admin_mode)[
        "workstations"
    ]

    onprem_workstations = []
    for workstation in all_workstations:
        if workstation["spec"]["on_prem"] == True:
            onprem_workstations.append(workstation)

    return onprem_workstations


class OnPremWorkstationClient:
    def __init__(
        self,
        config_dir=None,
        profile=None,
        verbose=False,
        admin_mode=False,
        init_with_container_status=False,
        env_file=None,
    ):
        self.config_dir = config_dir
        self.profile = profile
        self.command_response = OuterboundsCommandResponse()
        self.verbose = verbose
        self.admin_mode = admin_mode
        self.init_with_container_status = init_with_container_status
        self.env_file_location = env_file

        self.init_onprem_workstations()

    def init_onprem_workstations(self):
        # Init client with the list of existing workstations
        fetch_workstation_spec = CommandStatus(
            "fetch_workstation_spec", OuterboundsCommandStatus.OK, "Fetching succesful"
        )
        try:
            workstations_list = get_all_onprem_workstations(
                self.config_dir, self.profile, self.admin_mode
            )

            self.existing_workstations = {
                ws["instance_id"]: ws for ws in workstations_list
            }

            for workstation_id in self.existing_workstations.keys():
                if self.init_with_container_status:
                    self.existing_workstations[workstation_id]["status"] = {
                        "status_code": self.check_workstation_status(workstation_id)
                    }
                else:
                    self.existing_workstations[workstation_id]["status"] = {
                        "status_code": "Unknown"
                    }

        except Exception as e:
            fetch_workstation_spec.update(OuterboundsCommandStatus.FAIL, str(e), "")
            self.command_response.add_step(fetch_workstation_spec)
            self.existing_workstations = (
                None  # This will forcibly fail all subsequent commands
            )

    def check_workstation_status(self, workstation_id: str):
        """
        Check if the container for the workstation is running
        """

        if workstation_id in self.existing_workstations.keys():
            return convert_container_status_to_workstation_status(
                self.get_container_status(
                    workstation_id,
                    self.existing_workstations[workstation_id]["spec"][
                        "on_prem_settings"
                    ]["remote_server_ip"],
                )
            )

        raise Exception(f"Workstation with ID {workstation_id} does not exist.")

    def ensure_container_running(self, workstation_id: str):
        """
        Ensure that the container for the given workstation is running on the remote system. If it does not exist, create it and run it. If it exists
        but is not running, start it. If it is already running, do nothing.

        :param workstation_id: ID of the workstation to be started.
        """
        for ws in self.existing_workstations.values():
            if ws["instance_id"] == workstation_id and ws["spec"]["on_prem"] == True:
                self.start_container_if_not_running(
                    ws["instance_id"],
                    ws["spec"]["on_prem_settings"]["remote_server_ip"],
                    ws,
                )
                # start_container_if_not_running('ws-1010', "54.188.27.182", ws)
                return

        raise Exception(f"Workstation with ID {workstation_id} does not exist.")

    def exec_remote_command(
        self,
        command_alias: str,
        command: str,
        conn: Connection,
        command_log_override: Union[str, None] = None,
    ) -> Result:
        """
        Execute a command on a remote server over SSH.

        :param command_alias: Alias for the command. This is used for status reporting.
        :param command: Command to be executed on the remote server.
        :param conn: Fabric connection object.
        """
        command_log = (
            command_log_override if command_log_override is not None else command
        )

        exec_step = CommandStatus(
            command_alias,
            OuterboundsCommandStatus.OK,
            "Execute Success: " + command_log,
        )
        res = conn.run(command, hide=not self.verbose)
        if res.exited != 0:
            exec_step.update(
                OuterboundsCommandStatus.FAIL,
                f"Error executing on remote: {command}",
                "",
            )
            self.command_response.add_step(exec_step)
            raise Exception(f"Error executing on remote: {command}")

        self.command_response.add_step(exec_step)
        return res

    def get_container_status(self, workstation_id, hostname) -> str:
        token = metaflowconfig.get_metaflow_token_from_config(
            self.config_dir, self.profile
        )
        with Connection(
            host=hostname,
            user="outerbounds",
            connect_kwargs={"password": token, "look_for_keys": False},
        ) as conn:

            all_containers = self.get_all_containers(conn)
            for container in all_containers:
                if container["Names"] == workstation_id:
                    return container["State"]

        # On top of the existing docker states CREATED, RUNNING, PAUSED, RESTARTING, EXITED, DEAD
        # we will add another state DOES_NOT_EXIST
        return "DOES_NOT_EXIST"

    def start_container_if_not_running(
        self, workstation_id, hostname, workstation_spec
    ):
        """
        Start the container if it is not running already.

        :param workstation_id: ID of the workstation to be started.
        :param hostname: Hostname of the remote system.
        :param workstation_spec: Specification of the workstation to be started.
        """

        token = metaflowconfig.get_metaflow_token_from_config(
            self.config_dir, self.profile
        )
        with Connection(
            host=hostname,
            user="outerbounds",
            connect_kwargs={"password": token, "look_for_keys": False},
        ) as conn:
            # Ensure required resources are present. Disk will be ignored for now.
            self.start_container(conn, workstation_spec)
            container_home = self.get_container_home(conn, workstation_id)

            # Ensure Metaflow Config is copied
            self.copy_to_remote_inside_docker(
                conn,
                os.path.expanduser("~/.metaflowconfig/config.json"),
                "/tmp/config.json",
                "/root/.metaflowconfig",
                workstation_id,
            )

            # Copy gitconfig
            self.copy_to_remote_inside_docker(
                conn,
                os.path.expanduser("~/.gitconfig"),
                "/tmp/.gitconfig",
                f"{container_home}",
                workstation_id,
            )

    def get_container_home(self, conn, container_id) -> Union[str, None]:
        """
        Given a container ID, get the home directory of the container.

        :param conn: Fabric connection object.
        :param container_id: ID of the Docker container on the remote system.
        """

        res = self.exec_remote_command(
            "get_container_home", f"docker exec {container_id} sh -c 'echo $HOME'", conn
        )
        return res.stdout.strip()

    def copy_to_remote_inside_docker(
        self, conn, local_path, remote_temp_path, container_dest_path, container_name
    ):
        """
        Copy a local file to a Docker container on a remote machine using Fabric.

        :param conn: Fabric connection object.
        :param local_path: Path to the local file to be copied.
        :param remote_temp_path: Temporary path on the remote machine (outside the container).
        :param container_dest_path: Destination path inside the Docker container.
        :param container_name: Name or ID of the Docker container on the remote system.
        """

        self.transfer_to_remote(local_path, remote_temp_path, conn)

        # Copy the file from the remote system into the Docker container
        self.exec_remote_command(
            "create_dest_dir",
            f"docker exec {container_name} mkdir -p {container_dest_path}",
            conn,
        )
        self.exec_remote_command(
            "copy_to_container",
            f"docker cp {remote_temp_path} {container_name}:{container_dest_path}",
            conn,
        )

        # Adjust permissions to make the file readable and writable
        self.exec_remote_command(
            "chmod_file",
            f"docker exec {container_name} chmod 644 {container_dest_path}",
            conn,
        )

        # Remove the file from the temporary location
        self.exec_remote_command("rm_temp_file", f"rm {remote_temp_path}", conn)

    def transfer_to_remote(self, local_path, remote_path, conn) -> Result:
        """
        Copy a local file to a remote server.

        :param local_path: Path to the local file to be copied.
        :param remote_path: Temporary path on the remote machine (outside the container).
        :param conn: Fabric connection object.
        """
        try:
            transfer_step = CommandStatus(
                "copy_to_remote", OuterboundsCommandStatus.OK, "Success!"
            )
            transfer = Transfer(conn)
            res = transfer.put(local_path, remote=remote_path)
            self.command_response.add_step(transfer_step)
            return res
        except Exception:
            transfer_step.update(
                OuterboundsCommandStatus.FAIL,
                f"Error copying file from local: {local_path} to remote: {remote_path}",
                "",
            )
            self.command_response.add_step(transfer_step)
            raise Exception(
                f"Error copying file from local: {local_path} to remote: {remote_path}"
            )

    def check_container_exists(self, conn: Connection, container_name: str):
        """
        Given the name of a container, check that it exists on the remote system.

        :param conn: Fabric connection object.
        :param container_name: Name of the Docker container on the remote system.
        """

        containers = self.get_all_containers(conn)
        for container in containers:
            if container["Names"] == container_name:
                return container

        return None

    def get_total_gpus_on_host(self, conn: Connection) -> int:
        """
        Get the total number of GPUs attached to the remote system.

        :param conn: Fabric connection object.
        """

        res = self.exec_remote_command(
            "get_gpu_count",
            "nvidia-smi --query-gpu=count --format=csv,noheader | wc -l",
            conn,
        )
        return int(res.stdout.strip())

    def inspect_container(self, conn: Connection, container_name) -> dict:
        """
        Inspect a Docker container on the remote system.

        :param conn: Fabric connection object.
        :param container_name: Name of the Docker container on the remote system.
        """

        res = self.exec_remote_command(
            "docker_inspect", f"docker inspect {container_name}", conn
        )
        return json.loads(res.stdout.strip())[0]

    def check_available_device_ids(self, conn: Connection):
        """
        Check the GPUs that are not currently being used by any _running_ containers on the remote system.

        :param conn: Fabric connection object.
        """

        num_gpus = self.get_total_gpus_on_host(conn)

        gpu_available = {i: True for i in range(num_gpus)}

        containers = self.get_all_containers(conn)
        for container in containers:
            if container["State"] != "running":
                continue
            inspect_output = self.inspect_container(conn, container["Names"])
            if inspect_output["HostConfig"]["DeviceRequests"] is not None:
                for device_request in inspect_output["HostConfig"]["DeviceRequests"]:
                    for capability in device_request["Capabilities"]:
                        if "gpu" in capability:
                            if device_request["DeviceIds"] is None:
                                return []
                            for gpu_id in device_request["DeviceIds"]:
                                gpu_available[gpu_id] = False

        return [gpu_id for gpu_id in gpu_available if gpu_available[gpu_id]]

    def get_all_containers(self, conn: Connection) -> List[dict]:
        """
        Get all Docker containers on the remote system.

        :param conn: Fabric connection object.
        """

        res = self.exec_remote_command(
            "get_all_containers",
            "docker ps --all --no-trunc --format='{{json .}}'",
            conn,
        )
        return [json.loads(cont_str) for cont_str in res.stdout.split("\n") if cont_str]

    def start_container(self, conn: Connection, workstation: dict):
        existing_container = self.check_container_exists(
            conn, workstation["instance_id"]
        )
        if existing_container is not None and existing_container["State"] == "running":
            return
        elif existing_container is not None:
            self.exec_remote_command(
                "start_existing_container",
                f"docker start {workstation['instance_id']}",
                conn,
            )
        else:
            # Executes docker login if the specified image is not public.
            self.docker_login_if_needed(workstation["spec"]["image"], conn)

            # Prep environment variable file. By principle of immutable containers, we will only
            # copy over the env vars is the Workstation is being created. On resumes - we won't copy
            # over the env vars.

            env_var_dict = get_list_of_env_vars_for_container(self.env_file_location)
            env_file_flags = ""
            if env_var_dict is not None and len(env_var_dict.keys()) > 0:
                env_file_dir = expanduser("~/.metaflowconfig")
                with NamedTemporaryFile(dir=env_file_dir, delete=False, mode="w") as f:
                    f.writelines(
                        [f"{k}={env_var_dict[k]}\n" for k in env_var_dict.keys()]
                    )
                    temp_file_name = f.name
                self.transfer_to_remote(
                    temp_file_name, f"/tmp/{workstation['instance_id']}_env_vars", conn
                )
                env_file_flags = (
                    f" --env-file /tmp/{workstation['instance_id']}_env_vars "
                )
                os.remove(temp_file_name)

            if workstation["spec"]["gpu"] == 0:
                gpu_sub_command = ""
            else:
                reqd_gpus = workstation["spec"]["gpu"]
                available_device_ids = self.check_available_device_ids(conn)
                if len(available_device_ids) < reqd_gpus:
                    raise Exception(
                        f"Requested {reqd_gpus} GPUs but only {len(available_device_ids)} are available."
                    )
                else:
                    gpu_sub_command = f"--gpus '\"device={','.join([str(dev_id) for dev_id in available_device_ids[:reqd_gpus]])}\"'"

            if (
                "volume_mounts" in workstation["spec"]["on_prem_settings"]
                and workstation["spec"]["on_prem_settings"]["volume_mounts"] is not None
                and len(workstation["spec"]["on_prem_settings"]["volume_mounts"]) > 0
            ):
                volume_mounts_command = " ".join(
                    [
                        f"-v {mount}:{mount}"
                        for mount in workstation["spec"]["on_prem_settings"][
                            "volume_mounts"
                        ]
                        if mount != ""
                    ]
                )
            else:
                volume_mounts_command = ""

            container_run_command = f"docker run {env_file_flags} {volume_mounts_command} --name {workstation['instance_id']} -d --cpus='{workstation['spec']['cpu_cores']}' --memory='{workstation['spec']['memory_gb']}g' {gpu_sub_command} {workstation['spec']['image']} sh -c 'tail -f /dev/null'"
            self.exec_remote_command(
                "create_new_container", container_run_command, conn
            )
            self.exec_remote_command(
                "install_outerbounds",
                f"docker exec {workstation['instance_id']} pip install outerbounds",
                conn,
            )

            if env_file_flags != "":
                self.exec_remote_command(
                    "remove_env_file",
                    f"rm /tmp/{workstation['instance_id']}_env_vars",
                    conn,
                )

    def docker_login_if_needed(self, image: str, conn):
        """
        Given the image URL, check if we need to do a `docker login` before pulling the image.
        In the current implementation, this will return True for any image that's hosted on ECR.
        We will do a docker login for the ACCOUNT_ID and AWS_REGION that's in the image URL.
        """

        import re

        ecr_image_pattern = (
            r"(?P<account_id>\d+)\.dkr\.ecr\.(?P<region>[a-z0-9\-]+)\.amazonaws\.com"
        )
        match = re.search(ecr_image_pattern, image)
        if match is None:
            # Image isn't hosted on ECR, we have nothing to do.
            return

        parse_result = match.groupdict()

        ecr_account_id = parse_result["account_id"]
        ecr_region = parse_result["region"]

        username, password = generate_creds_for_docker_login(ecr_account_id, ecr_region)

        self.exec_remote_command(
            "docker_login",
            f"docker login -u {username} -p {password} {ecr_account_id}.dkr.ecr.{ecr_region}.amazonaws.com",
            conn,
            f"docker login -u <SENSITIVE> -p <SENSITIVE> {ecr_account_id}.dkr.ecr.{ecr_region}.amazonaws.com",
        )

    def stop_container_for_workstation(self, workstation_id: str):
        """
        Stop the docker container for the given workstation.
        """

        if workstation_id in self.existing_workstations.keys():
            token = metaflowconfig.get_metaflow_token_from_config(
                self.config_dir, self.profile
            )
            with Connection(
                host=self.existing_workstations[workstation_id]["spec"][
                    "on_prem_settings"
                ]["remote_server_ip"],
                user="outerbounds",
                connect_kwargs={"password": token, "look_for_keys": False},
            ) as conn:
                self.exec_remote_command(
                    "stop_container", f"docker stop {workstation_id}", conn
                )


def generate_creds_for_docker_login(account_id: str, region: str) -> Tuple[str, str]:
    """
    Generate credentials for docker login.

    :param account_id: AWS account ID
    :param region: AWS region

    returns:
        username: AWS account ID
        password: AWS password
    """

    _ = ObpAuthProvider.get_client("sts")
    ecr_role = f'{os.environ["AWS_ROLE_ARN"]}-ecr'
    new_client = ObpAuthProvider.get_client(
        "ecr", role_arn=ecr_role, client_params={"region_name": region}
    )
    token = new_client.get_authorization_token(registryIds=[account_id])

    creds = token["authorizationData"][0]["authorizationToken"]
    creds = base64.b64decode(creds).decode("utf-8")
    creds = creds.split(":")
    return creds[0], creds[1]


@cli.command(help="Hibernate on-prem workstation")
@click.option(
    "-w",
    "--workstation",
    default="",
    help="The ID of the on-prem workstation to start",
)
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
    help="The named metaflow profile in which your workstation exists",
)
def hibernate_onprem_workstation(workstation=None, config_dir=None, profile=None):
    on_prem_client = OnPremWorkstationClient(config_dir, profile)
    try:
        on_prem_client.stop_container_for_workstation(workstation)
    except Exception as e:
        click.echo(
            f"Encountered error while hibernating workstation: {str(e)}", err=True
        )
    click.echo(json.dumps(on_prem_client.command_response.as_dict(), indent=4))


@cli.command(help="List on-prem workstations")
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
    help="The named metaflow profile in which your workstation exists",
)
@click.option(
    "-a",
    "--all",
    default=False,
    help="If set, list all workstations in the cluster. Only available to admins.",
    is_flag=True,
)
@click.option(
    "--filter-by-status",
    default="",
    help="If set, filter workstations by status. If unset, lists all workstations",
    type=click.Choice(["", "Running", "Hibernating"]),
)
@click.option(
    "--use-container-status",
    default=True,
    help="If set, this will actually attempt to check and use the container status",
    is_flag=True,
)
@click.option(
    "--no-use-container-status",
    default=False,
    help="If set, this will skip the container status check and just list workstation specs",
    is_flag=True,
)
def list_onprem_workstations(
    config_dir=None,
    profile=None,
    all=False,
    filter_by_status="",
    use_container_status=True,
    no_use_container_status=False,
):
    """
    Lists all onprem workstations. Supports filtering by status. Deployment admins
    can also use this to list all workstations cluster-wide using the --all flag.

    :param config_dir: Path to Metaflow configuration directory
    :param profile: The named metaflow profile in which your workstation exists
    :param all: If set, list all workstations in the cluster. Only available to admins.
    :param filter_by_status: If set, filter workstations by status. If unset, lists all workstations
    """
    try:
        on_prem_client = OnPremWorkstationClient(
            config_dir,
            profile,
            admin_mode=all,
            init_with_container_status=not no_use_container_status,
        )
        if filter_by_status == "":
            on_prem_client.command_response.add_or_update_data(
                "workstations", list(on_prem_client.existing_workstations.values())
            )
        else:
            filtered_workstations = [
                ws
                for ws in list(on_prem_client.existing_workstations.values())
                if ws["status"]["status_code"].upper() == filter_by_status.upper()
            ]
            on_prem_client.command_response.add_or_update_data(
                "workstations", filtered_workstations
            )
    except Exception as e:
        click.secho("Failed to list workstations", fg="red", err=True)
        click.secho("Error: {}".format(str(e)), err=True)

    click.echo(json.dumps(on_prem_client.command_response.as_dict(), indent=4))


def convert_container_status_to_workstation_status(container_status: str) -> str:
    """
    Convert the container status code from Docker standard to Workstation standard.

    :param container_status: Container status code from Docker

    returns:
        workstation_status: Workstation status code
    """

    docker_status_to_workstation_status = {
        "DOES_NOT_EXIST": "Starting",
        "CREATED": "Starting",
        "RUNNING": "Running",
        "EXITED": "Hibernating",
        "PAUSED": "Hibernating",
        "RESTARTING": "Starting",
        "DEAD": "Error",
    }

    if container_status.upper() in docker_status_to_workstation_status.keys():
        return docker_status_to_workstation_status[container_status.upper()]

    return "Unknown"


def get_list_of_env_vars_for_container(env_file_loc: str) -> dict[str, str]:
    env_vars = {
        "METAFLOW_HOME": "/root/.metaflowconfig",
    }

    # Check if env_file_loc exists and is a file
    if not os.path.isfile(env_file_loc):
        return env_vars

    with open(env_file_loc, "r") as f:
        for line in f.readlines():
            if "=" in line:
                key, value = line.split("=")
                if " " in value.strip():
                    value = f'"{value.strip()}"'
                env_vars[key.strip()] = value
            else:
                key = line.strip()
                if key in os.environ:
                    value = os.environ[key]
                    if " " in value.strip():
                        value = f'"{value.strip()}"'
                    env_vars[key] = value
    return env_vars

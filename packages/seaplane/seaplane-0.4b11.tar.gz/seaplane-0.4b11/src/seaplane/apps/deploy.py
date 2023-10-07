import json
import os
import shutil
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import zipfile

import requests

from ..api.api_http import headers
from ..api.api_object_store import ObjectStorageAPI
from ..api.api_request import provision_req
from ..api.token_api import TokenAPI
from ..configuration import Configuration, config
from ..logging import log
from ..model.secrets import Secret
from ..util import file_md5, unwrap
from .app import App
from .build import PROJECT_TOML, build
from .decorators import context
from .task import Task

ENDPOINTS_STREAM = "_SEAPLANE_ENDPOINT"


def create_http_api_entry_point_docker_file() -> None:
    docker_file = """FROM python:3.10

ENV SEAPLANE_APPS_PRODUCTION True
ENV PORT 5000

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:${PORT} --workers 1 --timeout 300 demo:app
    """

    if not os.path.exists("build/http"):
        os.makedirs("build/http")

    with open("build/http/Dockerfile", "w") as file:
        file.write(docker_file)


def create_endpoints_input_subject(app_id: str) -> str:
    return f"{ENDPOINTS_STREAM}.in.{app_id}.*"


def create_endpoints_output_subject(app_id: str) -> str:
    # The following ${! ... } incantations are Benthos function interpolation
    request_id = '${! meta("_seaplane_request_id") }'
    joined_batch_hierarchy = '${! meta("_seaplane_batch_hierarchy") }'
    return f"{ENDPOINTS_STREAM}.out.{app_id}.{request_id}{joined_batch_hierarchy}"


def create_subject(app_id: str, task_id: str) -> str:
    return f"{app_id}.{task_id}"


def create_carrier_workload_file(
    tenant: str,
    app_id: str,
    task: Task,
    next_tasks: List[str],
    project_url: str,
    is_first_task: bool,
    has_to_save_output: bool,
) -> Dict[str, Any]:
    if is_first_task:
        input = create_endpoints_input_subject(app_id)
    else:
        input = create_subject(app_id, task.id)

    output: Optional[Dict[str, Any]] = None

    if len(next_tasks) > 1:
        output = {
            "broker": {
                "outputs": (
                    {"carrier": {"subject": create_subject(app_id, c_id)}} for c_id in next_tasks
                )
            }
        }
    elif len(next_tasks) == 1:
        output = {
            "carrier": {"subject": create_subject(app_id, next_tasks[0])},
        }
    else:
        if has_to_save_output:
            output = {
                "carrier": {"subject": create_endpoints_output_subject(app_id)},
            }

    max_ack_pending = 2
    if task.replicas:
        max_ack_pending = task.replicas * 2

    workload = {
        "input": {
            "carrier": {
                "subject": input,
                "durable": task.id,
                "queue": task.id,
                "ack_wait": "2m",
                "max_ack_pending": max_ack_pending,
            },
        },
        "processor": {
            "docker": {
                "image": config.runner_image,
                "args": [project_url],
            }
        },
        "output": output,
        "replicas": task.replicas,
    }

    if not os.path.exists(f"build/{task.id}"):
        os.makedirs(f"build/{task.id}")

    with open(f"build/{task.id}/workload.json", "w") as file:
        json.dump(workload, file, indent=2)
        log.debug(f"Created {task.id} workload")

    return workload


def copy_project_into_resource(id: str) -> None:
    source_folder = "."
    destination_folder = f"build/{id}"

    if not os.path.exists(f"build/{id}"):
        os.makedirs(f"build/{id}")

    for item in os.listdir(source_folder):
        if os.path.isdir(item) and item == "build":
            continue  # Skip the "build" folder

        elif os.path.isdir(item):
            destination_path = os.path.join(destination_folder, item)
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)
            shutil.copytree(item, destination_path)
        else:
            destination_path = os.path.join(destination_folder, item)
            shutil.copy2(item, destination_path)


def create_stream(name: str) -> Any:
    log.debug(f"Creating stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"
    req = provision_req(config._token_api)

    payload: Dict[str, Any] = {"ack_timeout": 20}  # should be long enough for OpenAI
    if config.region is not None:
        payload["allow_locations"] = [f"region/{config.region}"]

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=payload,
                headers=headers(access_token),
            )
        )
    )


def delete_stream(name: str) -> Any:
    log.debug(f"Deleting stream: {name}")
    url = f"{config.carrier_endpoint}/stream/{name}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.delete(
                url,
                headers=headers(access_token),
            )
        )
    )


def get_secrets(config: Configuration) -> List[Secret]:
    secrets = []
    for key, value in config._api_keys.items():
        secrets.append(Secret(key, value))

    return secrets


def add_secrets(name: str, secrets: List[Secret]) -> Any:
    url = f"{config.carrier_endpoint}/flow/{name}/secrets"
    req = provision_req(config._token_api)

    flow_secrets = {}
    for secret in secrets:
        flow_secrets[secret.key] = {"destination": "all", "value": secret.value}

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=flow_secrets,
                headers=headers(access_token),
            )
        )
    )


def create_flow(name: str, workload: Dict[str, Any]) -> Any:
    log.debug(f"Creating flow: {name}")
    url = f"{config.carrier_endpoint}/flow/{name}"
    if config.dc_region is not None:
        url += f"?region={config.dc_region}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.put(
                url,
                json=workload,
                headers=headers(access_token),
            )
        )
    )


def delete_flow(name: str) -> Any:
    log.debug(f"Deleting flow: {name}")

    url = f"{config.carrier_endpoint}/flow/{name}"
    if config.dc_region is not None:
        url += f"?region={config.dc_region}"
    req = provision_req(config._token_api)

    return unwrap(
        req(
            lambda access_token: requests.delete(
                url,
                headers=headers(access_token),
            )
        )
    )


def zip_current_directory(tenant: str, project_name: str) -> str:
    current_directory = os.getcwd()
    zip_filename = f"./build/{tenant}.zip"

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(PROJECT_TOML, os.path.relpath(PROJECT_TOML, current_directory))
        if os.path.exists(".env") and not os.path.isdir(".env"):
            zipf.write(".env", os.path.relpath(".env", current_directory))

        for root, _, files in os.walk(f"{current_directory}/{project_name}"):
            for file in files:
                if "__pycache__" in root:
                    continue

                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, current_directory))

    # log.debug(f"Package project for upload: {zip_filename}")
    return zip_filename


def upload_project(project: Dict[str, Any], tenant: str) -> str:
    """
    Pushes a full project into the Seaplane internal datastore, returning a URL
    that our executor image can use to refer back to the project when executing.
    """

    # Step 1: Make sure we have a bucket to dump our project into
    default_bucket_name: str = "seaplane-internal-flows"
    default_bucket_config = {
        "description": "Seaplane bucket used for flow images. Should not be modified directly.",
        "replicas": 3,
        "max_bytes": -1,  # unlimited
        "allow_locations": ["all"],  # TODO: Georestrictions
    }

    obj = ObjectStorageAPI()
    if default_bucket_name not in obj.list_buckets():
        obj.create_bucket(default_bucket_name, default_bucket_config)

    # Step 2: Build the zip file
    project_name: str = project["tool"]["poetry"]["name"]
    project_file = zip_current_directory(tenant, project_name)
    remote_path = project_name + "." + file_md5(project_file) + ".zip"

    # Step 3: Upload & return
    obj.upload_file(default_bucket_name, remote_path, project_file)
    return obj.file_url(default_bucket_name, remote_path)


def register_apps_info(schema: Dict[str, Any]) -> None:
    apps = schema["apps"].keys()

    tenant_api_paths: List[Dict[str, str]] = []

    for app_id in apps:
        entry_point_type = schema["apps"][app_id]["entry_point"]["type"]
        if entry_point_type == "API":
            path = schema["apps"][app_id]["entry_point"]["path"]
            method = schema["apps"][app_id]["entry_point"]["method"]
            tenant_api_paths.append({"path": path, "method": method})


def print_endpoints(schema: Dict[str, Any]) -> None:
    apps = schema["apps"].keys()

    if len(apps) > 0:
        log.info("\nDeployed Endpoints:\n")
    for app_id in apps:
        entry_point_type = schema["apps"][app_id]["entry_point"]["type"]
        if entry_point_type == "API":
            log.info(
                f"🚀 {app_id} Endpoint: POST https://{urlparse(config.carrier_endpoint).netloc}/v1/endpoints/{app_id}/request"  # noqa
            )
            log.info(
                f"🚀 {app_id} CLI Command: plane endpoints request {app_id} <your message here>"
            )

    if len(apps) > 0:
        print("\n")


def deploy_task(
    tenant: str,
    app: App,
    task: Task,
    schema: Dict[str, Any],
    secrets: List[Secret],
    project_url: str,
) -> None:
    delete_flow(task.id)

    is_first_task = schema["apps"][app.id]["io"].get("entry_point", None) == [task.id]

    has_to_save_output = schema["apps"][app.id]["io"].get("returns", None) == task.id

    copy_project_into_resource(task.id)

    next_tasks = schema["apps"][app.id]["io"].get(task.id, None)

    if next_tasks is None:
        next_tasks = []

    workload = create_carrier_workload_file(
        tenant, app.id, task, next_tasks, project_url, is_first_task, has_to_save_output
    )

    create_flow(task.id, workload)
    secrets.append(Secret("TASK_ID", task.id))
    secrets.append(Secret("SAVE_RESULT_TASK", str(has_to_save_output)))
    add_secrets(task.id, secrets)

    log.info(f"Deploy for task {task.id} done")


def deploy(task_id: Optional[str] = None) -> None:
    project = build()
    schema = project["schema"]
    tenant = TokenAPI(config).get_tenant()
    secrets = get_secrets(config)
    project_url = upload_project(project["config"], tenant)

    secrets.append(Secret("SEAPLANE_APPS_PRODUCTION", "true"))

    if task_id is not None and task_id != "entry_point":
        for sm in context.apps:
            for c in sm.tasks:
                if c.id == task_id:
                    deploy_task(tenant, sm, c, schema, secrets[:], project_url)
    elif task_id is not None and task_id == "entry_point":
        log.info("Deploying entry points...")

        copy_project_into_resource("http")
        create_http_api_entry_point_docker_file()
    else:  # deploy everything
        for sm in context.apps:
            delete_stream(sm.id)
            create_stream(sm.id)

            for c in sm.tasks:
                deploy_task(tenant, sm, c, schema, secrets[:], project_url)

    register_apps_info(schema)
    print_endpoints(schema)

    log.info("🚀 Deployment complete")


def destroy() -> None:
    build()

    for sm in context.apps:
        delete_stream(sm.id)

        for c in sm.tasks:
            delete_flow(c.id)

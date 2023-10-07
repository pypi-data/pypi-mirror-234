import asyncio
import functools
from importlib.metadata import version
import json
import os
import sys
import traceback
from typing import Any, List, Optional
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import nats
from seaplane_framework.flow import processor

from ...configuration import config
from ...logging import log
from ...model.errors import SeaplaneError
from ..app import App
from ..build import build
from ..decorators import apps_json, context
from ..deploy import deploy, destroy
from ..task_context import TaskContext

SEAPLANE_APPS_CORS = list(os.getenv("SEAPLANE_APPS_CORS", "http://localhost:3000").split(" "))
AUTH_TOKEN = os.getenv("SEAPLANE_APPS_AUTH_TOKEN")

app = Flask(__name__)

CORS(app, origins=SEAPLANE_APPS_CORS)


if not config.is_production():
    sio = SocketIO(app, cors_allowed_origins=SEAPLANE_APPS_CORS, async_mode="threading")

    @sio.on("message")  # type: ignore
    def handle_message(data: Any) -> None:
        ...

    @sio.on("connect")  # type: ignore
    def on_connect() -> None:
        emit("message", apps_json(context.apps))


def send_something(data: Any) -> None:
    emit("message", data, sid="sp", namespace="", broadcast=True)


def authenticate_token() -> bool:
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        if token == f"Bearer {AUTH_TOKEN}":
            return True

    return False


@app.before_request
def before_request() -> Any:
    if request.path == "/healthz":
        return

    if os.getenv("SEAPLANE_APPS_AUTH_TOKEN") is not None:
        if not authenticate_token():
            return {"message": "Unauthorized"}, 401


def dev_https_api_start() -> Flask:
    log.debug(f"CORS enabled: {SEAPLANE_APPS_CORS}")
    context.set_event(lambda data: send_something(data))

    apps = context.apps

    for myapp in apps:

        def endpoint_func(pipe: App = myapp) -> Any:
            if request.method == "POST" or request.method == "PUT":
                data = request.get_json()
                result = pipe.func(data)
                return result
            elif request.method == "GET":
                return pipe.func("nothing")  # current limitation, it needs to pass something

        endpoint = functools.partial(endpoint_func, pipe=myapp)
        app.add_url_rule(myapp.path, myapp.id, endpoint, methods=[myapp.method])

    def health() -> str:
        emit("message", {"data": "test"}, sid="lol", namespace="", broadcast=True)
        return "Seaplane Apps Demo"

    app.add_url_rule("/", "healthz", health, methods=["GET"])

    if not config.is_production():
        log.info("🚀 Apps DEVELOPMENT MODE")
        sio.run(app, debug=False, port=1337)
    else:
        log.info("🚀 Apps PRODUCTION MODE")

    return app


loop = asyncio.get_event_loop()


async def publish_message(
    stream: str, id: str, message: Any, order: int, tasks: List[str]
) -> None:
    nc = await nats.connect(
        ["nats://148.163.201.1:2003"],
        user_credentials=os.path.abspath("./carrier.creds"),
    )
    js = nc.jetstream()

    nats_message = {"id": id, "input": message, "order": order}

    for task in tasks:
        log.debug(f"Sending to {stream}.{task} task,  message: {nats_message}")
        ack = await js.publish(f"{stream}.{task}", str(json.dumps(nats_message)).encode())
        log.debug(f"ACK: {ack}")

    await nc.close()


def generate_id() -> str:
    random_id = str(uuid.uuid4())
    return random_id


def prod_https_api_start() -> Flask:
    log.debug(f"CORS enabled: {SEAPLANE_APPS_CORS}")

    schema = build()
    context.set_event(lambda data: send_something(data))

    apps = context.apps

    for myapp in apps:

        def endpoint_func(pipe: App = myapp) -> Any:
            if request.method == "POST" or request.method == "PUT":
                body = request.get_json()

                if not ("input" in body):
                    return jsonify({"error": "Invalid JSON"}), 401

                id = generate_id()
                app_first_tasks = schema["apps"][pipe.id]["io"]["entry_point"]
                metadata = body["params"]

                batch = body["input"]

                for idx, content in enumerate(batch):
                    content["_params"] = metadata
                    loop.run_until_complete(
                        publish_message(pipe.id, id, content, idx, app_first_tasks)
                    )

                return jsonify({"id": id, "status": "processing"}), 200
            elif request.method == "GET":
                return pipe.func("nothing")  # current limitation, it needs to pass something

        endpoint = functools.partial(endpoint_func, pipe=myapp)
        app.add_url_rule(myapp.path, myapp.id, endpoint, methods=[myapp.method])

    def health() -> str:
        return "Seaplane Apps Demo"

    app.add_url_rule("/", "healthz", health, methods=["GET"])

    if not config.is_production():
        log.info("🚀 Seaplane Apps DEVELOPMENT MODE")
        sio.run(app, debug=False, port=1337)
    else:
        log.info("🚀 Seaplane Apps PRODUCTION MODE")

    return app


def start_task(task_id: str, save_result: bool) -> None:
    task = context.get_task(task_id)

    if not task:
        raise SeaplaneError(
            f"Task {task_id} not found, \
                            make sure the Task ID is correct."
        )

    processor.start()

    while True:
        log.info(f"Task {task.id} waiting for data...")

        # TODO: A read can fail if the incoming data is using
        #       a newer format than this version of `processor`
        #       understands. This would almost certainly be
        #       our fault, but we should still deadletter the message
        #       rather than crashing.
        message = processor.read()

        if "_seaplane_request_id" not in message.meta:
            # This must be the first task in a smartpipe, so we have to get the
            # Endpoints API generated request ID from the incoming nats_subject.
            request_id = message.meta["nats_subject"].split(".")[
                -1
            ]  # The Endpoints API always adds a request ID as the leaf
            message.meta["_seaplane_request_id"] = request_id

            # Similarly let's initialise the batch hierarchy to start out empty
            message.meta["_seaplane_batch_hierarchy"] = ""

        task_context = TaskContext(message.body, message.meta)

        # TODO: Handle task errors gracefully
        try:
            task.process(task_context)
        except Exception as e:
            # At this point, the SDK user's code has thrown an exception
            # there's nothing we can do but log it and move on.
            # NB: We're not returning here, so any existing batch items
            # will still be written.
            error_str = "\n".join(traceback.format_exception(type(e), e, e.__traceback__))
            log.error(
                f"Error running Task:\
                \n {error_str}"
            )

        # The task may have written messages (by virtue of TaskContext.emit), so we now
        # flush them down the pipe.
        processor.flush()


def start() -> Optional[Flask]:
    log.info(f"\n\n\tSeaplane Apps version {version('seaplane')}\n")

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "build":
            build()
            return None
        elif command == "deploy":
            if len(sys.argv) == 3:
                co_id = sys.argv[2]
                deploy(co_id)
            else:
                deploy()
            return None
        elif command == "destroy":
            destroy()
            return None

    task_id: Optional[str] = os.getenv("TASK_ID")

    if not task_id:
        log.info("Starting API Entry Point...")
        if not config.is_production():
            return dev_https_api_start()
        else:
            return prod_https_api_start()
    else:
        log.info(f"Starting Task {task_id} ...")
        save_result = os.getenv("SAVE_RESULT_TASK", "").lower() == "true"
        start_task(task_id, save_result)
        return None

"""
An integrated test for websocket transmission as used within Geostore and MalardClient.

Here, we create and then start an extremely simple flask server and then send a message to it over a websocket.
Crucially, the message must be larger than 1 MB in order to test the framing properly.

After receiving the message, the flask server will immediately send it back again. We expect to receive it unchanged.

"""
from __future__ import annotations

from multiprocessing import Process
from time import perf_counter, sleep
from typing import Dict

from flask import Flask, request
import numpy as np
import pandas as pd
import pytest
import requests
import simple_websocket

from specklia._websocket_helpers import receive_object_from_websocket, send_object_to_websocket


@pytest.fixture()
def example_dataframe() -> pd.DataFrame:
    np.random.seed(2501)
    return pd.DataFrame({
        'lat': np.random.rand(5000),
        'lon': np.random.rand(5000),
        'timestamp': np.random.randint(1000, 2000, 5000)
    })


def start_api_in_separate_process(flask_app: Flask, api_config: Dict, block_until_api_exits: bool = False) -> Process:
    """Start the API in a separate process.

    Used mainly for testing

    Parameters
    ----------
    flask_app : Flask
        The Flask app containing the API
    api_config : Dict
        The section of the config dictionary under the heading "api"
    block_until_api_exits : bool
        if true, blocks continued execution of geostore until the API kills itself.

    Returns
    -------
    Process
        The separate process running the API.
    """
    # recreate the process just in case it was previously stopped
    server_process = Process(
        target=lambda: flask_app.run(
            host=api_config['test_host_name'], port=api_config['test_port'],
            debug=True, use_reloader=False))

    server_process.start()

    # always block until the server is ready to handle requests
    is_server_ready = False
    while not is_server_ready:
        try:
            requests.get(f"http://localhost:{api_config['test_port']}/", timeout=5)
            is_server_ready = True
        except requests.exceptions.ConnectionError:
            pass

    # if the user has requested it, block until the server kills itself
    if block_until_api_exits:
        while server_process.is_alive():
            sleep(1)

    return server_process


def stop_api_in_separate_process(flask_process: Process) -> None:
    """
    Shutdown the API if it is running in a separate process.

    Parameters
    ----------
    flask_process : Process
        The process in which the API is running.
    """
    flask_process.terminate()
    flask_process.join()


def handle_websocket_message():
    print('handle_websocket_message triggered')
    ws = simple_websocket.Server(request.environ)

    received_data = receive_object_from_websocket(ws, 30)

    print(f'server received a message of type {type(received_data)}')

    send_object_to_websocket(ws, received_data)

    print('server sent the message back to the client')
    ws.close()
    return ''


def crash_while_handling_websocket_message():
    print('crash_while_handling_websocket_message triggered')
    ws = simple_websocket.Server(request.environ)
    receive_object_from_websocket(ws, 30)
    sleep(100)  # simulate a crash in a separate service


def test_websocket_transmission(example_dataframe: pd.DataFrame):
    # create the "bent pipe" - a server that just returns what it receives
    app = Flask('websocket_bent_pipe')
    app.add_url_rule('/endpoint', None, handle_websocket_message, websocket=True)
    api_process = start_api_in_separate_process(
        flask_app=app, api_config={'test_host_name': '127.0.0.1', 'test_port': 9066})
    print('api started')

    try:
        # send a large message to the "bent pipe"
        # give it some structure so we can check the serialisation
        data_to_send = example_dataframe
        data_size_bytes = data_to_send.memory_usage(index=True, deep=True).sum()

        start_time = perf_counter()
        ws_url = 'ws://127.0.0.1:9066/endpoint'
        ws = simple_websocket.Client(ws_url)

        send_object_to_websocket(ws, data_to_send)
        received_data = receive_object_from_websocket(ws, 30)

        end_time = perf_counter()
        pd.testing.assert_frame_equal(data_to_send, received_data)
        print('effective data rate (localhost to localhost): '
              f'{data_size_bytes * 8 / (1024 ** 2) / (end_time-start_time)} Mbps')
    finally:
        stop_api_in_separate_process(api_process)


def test_websocket_transmission_large_files(example_dataframe: pd.DataFrame):
    # create the "bent pipe" - a server that just returns what it receives
    app = Flask('websocket_bent_pipe')
    app.add_url_rule('/endpoint', None, handle_websocket_message, websocket=True)
    api_process = start_api_in_separate_process(
        flask_app=app, api_config={'test_host_name': '127.0.0.1', 'test_port': 9066})
    print('api started')

    try:
        data_to_send = example_dataframe
        original_data_size = data_to_send.memory_usage(index=True, deep=True).sum()
        # transmit 200 MB.
        data_to_send = pd.concat([data_to_send] * int(np.ceil((200 * 1024 ** 2) / original_data_size)))

        ws_url = 'ws://127.0.0.1:9066/endpoint'
        ws = simple_websocket.Client(ws_url)

        send_object_to_websocket(ws, data_to_send)
        received_data = receive_object_from_websocket(ws, 30)

        pd.testing.assert_frame_equal(data_to_send, received_data)
    finally:
        stop_api_in_separate_process(api_process)


def test_broken_websocket_transmission(example_dataframe: pd.DataFrame):
    # create the "bent pipe" - a server that just returns what it receives
    app = Flask('websocket_bent_pipe')
    app.add_url_rule('/broken_endpoint', None, crash_while_handling_websocket_message, websocket=True)
    api_process = start_api_in_separate_process(
        flask_app=app, api_config={'test_host_name': '127.0.0.1', 'test_port': 9066})
    print('api started')

    try:
        # send a large message to the "bent pipe"
        # give it some structure so we can check the serialisation
        data_to_send = example_dataframe
        ws_url = 'ws://127.0.0.1:9066/broken_endpoint'
        ws = simple_websocket.Client(ws_url)

        send_object_to_websocket(ws, data_to_send)
        with pytest.raises(RuntimeError, match="Attempted to receive from a websocket, but nothing was sent."):
            receive_object_from_websocket(ws, 1)
    finally:
        stop_api_in_separate_process(api_process)

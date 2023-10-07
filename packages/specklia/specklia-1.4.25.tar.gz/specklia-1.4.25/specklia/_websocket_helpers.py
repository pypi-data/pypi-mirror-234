"""Utilities for exchanging arbitrary python objects over a websocket."""
import pickle
from typing import Union

import blosc
import simple_websocket


# The blosc library can only compress up to 2 GiB at a time, so we transmit data in chunks of this size.
MAX_BLOSC_COMPRESSION_SIZE = 2147483631
MESSAGE_END_FLAG = b'message_ends'


def receive_object_from_websocket(
        ws: Union[simple_websocket.Server, simple_websocket.Client], timeout: float) -> object:
    """
    Receive an arbitrary python object over a websocket.

    Objects are binary serialised and compressed, then transmitted in MESSAGE_CHUNK_SIZE chunks.

    Works for both the Client and Server objects provided by simple_websocket.

    Parameters
    ----------
    ws : Union[simple_websocket.Server, simple_websocket.Client]
        The Websocket Client or Server.
    timeout : float
        If provided, will raise RuntimeError if no message is recieved within this number of seconds.

    Returns
    -------
    object
        The python object recieved via the websocket.

    Raises
    ------
    RuntimeError
        If the connection times out or is closed without a message being received.
    """
    message = b''
    message_chunk = b''
    while message_chunk != MESSAGE_END_FLAG and message_chunk is not None:
        try:
            if message_chunk is not None:
                message += message_chunk
            compressed_message_chunk = ws.receive(timeout)
            if compressed_message_chunk is None:
                message_chunk = None
            else:
                message_chunk = blosc.decompress(compressed_message_chunk)
        except simple_websocket.ws.ConnectionClosed:
            # we still need to clear the input buffer to guarantee that we have the whole message,
            # and check for early closures
            if len(ws.input_buffer) > 0:
                message_chunk = blosc.decompress(ws.input_buffer.pop(0))

    if len(message) == 0:
        raise RuntimeError("Attempted to receive from a websocket, but nothing was sent.")

    return pickle.loads(message)


def send_object_to_websocket(ws: Union[simple_websocket.Server, simple_websocket.Client], data: object) -> None:
    """
    Send an arbitrary python object over a websocket.

    Objects are binary serialised and compressed, then transmitted in MESSAGE_CHUNK_SIZE chunks.

    Works for both the Client and Server objects provided by simple_websocket.

    Parameters
    ----------
    ws : Union[simple_websocket.Server, simple_websocket.Client]
        The Websocket Client or Server.
    data : object
        The data to be sent over the websocket.

    Raises
    ------
    ConnectionResetError
        If the recipient closed the webscoket.
    """
    message = pickle.dumps(data, protocol=5)
    try:
        for i in range(0, len(message), MAX_BLOSC_COMPRESSION_SIZE):
            ws.send(blosc.compress(message[i:i + MAX_BLOSC_COMPRESSION_SIZE]))
        ws.send(blosc.compress(MESSAGE_END_FLAG))
    except OSError as err:
        if "Bad file descriptor" in str(err):
            raise ConnectionResetError(
                "The recipient closed the websocket before the full message was sent.")

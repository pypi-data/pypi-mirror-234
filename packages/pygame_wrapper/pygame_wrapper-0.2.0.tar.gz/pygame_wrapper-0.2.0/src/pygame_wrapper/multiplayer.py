"""
Contains everything related to multiplayer and sockets in pgw
"""
import socket


def send(msg: str, conn: socket.socket, header: int, encoding: str = "utf-8") -> None:
    """
    A function to easily send messages over sockets
    :param msg: A string of the actual message to send
    :param conn: The socket from which to send the message
    :param header: The integer size of the header
    :param encoding: The encoding type (optional defaults to utf-8)
    :return None: 
    """
    message = msg.encode(encoding)
    msg_length = len(message)
    send_length = str(msg_length).encode(encoding)
    send_length += b' ' * (header - len(send_length))
    conn.send(send_length)
    conn.send(message)


def recv(conn: socket.socket, header: int, encoding: str = "utf-8") -> str:
    """
    A function to easily recv messages over sockets (requires using the send function on both sides)
    :param conn: The socket from which to send the message
    :param header: The integer sixe of the header
    :param encoding: The encoding type (optional defaults to utf-8)
    :return Str:
    """
    length = int(conn.recv(header).decode(encoding).replace(' ', ''))

    return conn.recv(length).decode(encoding)

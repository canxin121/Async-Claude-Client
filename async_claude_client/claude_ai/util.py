from __future__ import annotations

import asyncio
import json
import threading
import urllib.parse
from functools import wraps
from pathlib import Path
from typing import Union


def run_in_loop(loop, func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return loop.run_until_complete(func(*args, **kwargs))
        else:
            return loop.run_in_executor(None, func, *args, **kwargs)

    return wrapper


def run_in_new_thread(func, *args, wait: bool = False):
    t = threading.Thread(target=func(*args))
    t.daemon = True
    t.start()
    if wait:
        t.join()


def parse_proxy_url(url: str):
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme
    hostname = parsed.hostname
    port = parsed.port
    username = parsed.username
    password = parsed.password
    proxy_dict = {}
    if scheme == "http":
        raise Exception(
            "Http proxy not support using curl cffi, since claude.ai use https."
        )
    if username and password:
        if scheme == "https":
            proxy_dict = {scheme: f"http://{username}:{password}@{hostname}:{port}"}
        elif scheme == "socks":
            proxy_dict = {
                "https": f"{scheme}://{username}:{password}@{hostname}:{port}"
            }
    else:
        if scheme == "https" or scheme == "http":
            proxy_dict = {scheme: f"http://{hostname}:{port}"}
        elif scheme == "socks":
            proxy_dict = {"https": f"{scheme}://{hostname}:{port}"}
    if not proxy_dict:
        raise Exception("Wrong proxy url.")
    return proxy_dict


def process_cookie(cookie: str | Path | list[dict]):
    def load_cookie_from_file(path: Union[str, Path]):
        with open(Path(path), "r") as f:
            return json.loads(f.read())

    if isinstance(cookie, (str, Path)):
        try:
            cookie_json = load_cookie_from_file(cookie)
        except Exception:
            try:
                cookie_json = json.loads(cookie)
            except Exception:
                raise ValueError("The cookie is not a valid path or json_schema")
    elif isinstance(cookie, list):
        cookie_json = cookie
    else:
        raise TypeError("The cookie must be a string, a Path, or a list of dicts")

    cookie_str = ""

    for cookie_dict in cookie_json:
        cookie_str += f"{cookie_dict['name']}={cookie_dict['value']};"

    return cookie_str


def get_content_type(file_path):
    file_path = Path(file_path)

    if file_path.suffix == ".pdf":
        return "application/pdf"

    elif file_path.suffix == ".txt":
        return "text/plain"

    elif file_path.suffix == ".csv":
        return "text/csv"

    else:
        return "application/octet-stream"


def build_request(client, question: str, conversation_id: str, attachment: str | Path):
    attachments = []
    if attachment:
        attachment_response = client.upload_attachment(attachment)
        if attachment_response:
            attachments = [attachment_response]
        else:
            return {"Error: Invalid file format. Please try again."}
    if not attachment:
        attachments = []

    return {
        "completion": {
            "prompt": f"{question}",
            "timezone": "Asia/Kolkata",
            "model": "claude-2.1",
        },
        "organization_uuid": f"{client.organization_id}",
        "conversation_uuid": f"{conversation_id}",
        "text": f"{question}",
        "attachments": attachments,
    }

import os
import traceback
from decimal import Decimal

import yaml
from rich.console import Console

DEFAULT_API_ENDPOINT = "https://api.app.predibase.com/v1"
DEFAULT_SERVING_ENDPOINT = "serving.app.predibase.com"

DEBUG = os.environ.get("PREDIBASE_DEBUG") is not None


_console = Console()
_error_console = Console(stderr=True, style="bold red")
_info_console = Console(stderr=True, style="bold blue")


def load_yaml(yaml_fp):
    with open(yaml_fp) as f:
        return yaml.safe_load(f)


def spinner(name):
    def decorator(fn):
        def wrap_fn(*args, **kwargs):
            with _console.status(f"{name}...", spinner="material"):
                try:
                    res = fn(*args, **kwargs)
                    _console.print(f"✅ {name}")
                    return res
                except Exception as e:
                    _console.print(f"💥 {name}")
                    _error_console.print(get_error_message(e))
                    raise

        return wrap_fn

    return decorator


def get_error_message(e: Exception) -> str:
    return f"{type(e).__name__}: {str(e)}" if not DEBUG else traceback.format_exc()


def log_info(v: str):
    _info_console.print(v)


def log_error(v: str):
    _error_console.print(v)


def get_url(session, endpoint: str) -> str:
    if "localhost" in session.url:
        root_url = "http://localhost:8000"
    else:
        url = session.url
        if "api." in url:
            url = url.replace("api.", "").replace("/v1", "")
        root_url = url
    from urllib.parse import urljoin

    return urljoin(root_url, endpoint)


class JSONFloat(float):
    def __repr__(self):
        return format(Decimal(self), "f")


class ConfigEncoder:
    def decimalize(self, val):
        if isinstance(val, dict):
            return {k: self.decimalize(v) for k, v in val.items()}

        if isinstance(val, (list, tuple)):
            return type(val)(self.decimalize(v) for v in val)

        if isinstance(val, float):
            return JSONFloat(val)

        return val

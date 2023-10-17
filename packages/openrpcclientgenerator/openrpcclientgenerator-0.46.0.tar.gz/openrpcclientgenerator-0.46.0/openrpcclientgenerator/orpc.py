"""CLI main entry point."""
import json
from pathlib import Path

from openrpc import OpenRPC, RPCServer
from rpc_cli import cli

from openrpcclientgenerator import generate, Language

rpc = RPCServer(title="OpenRPC Client Generator")


@rpc.method()
def python(api_url: str, out: Path | None = None) -> str:
    """Generate a Python client."""
    openrpc = _get_openrpc()
    out = out or Path.cwd().joinpath("out")
    out.mkdir(exist_ok=True)
    name = generate(openrpc, Language.PYTHON, api_url, out)
    return f"{out.as_posix()}/python/{name}"


@rpc.method()
def typescript(api_url: str, out: Path | None = None) -> str:
    """Generate a TypeScript client."""
    openrpc = _get_openrpc()
    out = out or Path.cwd().joinpath("out")
    out.mkdir(exist_ok=True)
    name = generate(openrpc, Language.TYPESCRIPT, api_url, out)
    return f"{out.as_posix()}/typescript/{name}"


def _get_openrpc() -> OpenRPC:
    return OpenRPC(**json.loads(Path.cwd().joinpath("openrpc.json").read_text()))


def main() -> int:
    """CLI main entry point."""
    exit_code: int = cli(rpc).run()
    return exit_code


if __name__ == "__main__":
    main()

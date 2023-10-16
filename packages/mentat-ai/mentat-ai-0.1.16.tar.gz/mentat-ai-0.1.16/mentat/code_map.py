import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Any, Literal

from .config_manager import CONFIG_MANAGER, ConfigManager
from .git_handler import GIT_ROOT, get_non_gitignored_files
from .llm_api import count_tokens
from .session_stream import SESSION_STREAM
from .utils import run_subprocess_async


async def _get_code_map(
    root: Path, file_path: Path, exclude_signatures: bool = False
) -> str:
    # Create ctags from executable in a subprocess
    ctags_cmd_args = [
        "--extras=-F",
        "--input-encoding=utf-8",
        "--output-format=json",
        "--output-encoding=utf-8",
    ]
    if exclude_signatures:
        ctags_cmd_args.append("--fields=-s")
    else:
        ctags_cmd_args.append("--fields=+S")
    ctags_cmd = ["ctags", *ctags_cmd_args, str(Path(root).joinpath(file_path))]

    output = await run_subprocess_async(*ctags_cmd)
    output_lines = output.splitlines()

    # Extract subprocess stdout into python objects
    ctags = set[tuple[Path, ...]]()
    for output_line in output_lines:
        try:
            tag = json.loads(output_line)
        except json.decoder.JSONDecodeError as err:
            await SESSION_STREAM.get().send(
                f"Error parsing ctags output: {err}\n{repr(output_line)}",
                color="yellow",
            )
            continue

        scope = tag.get("scope")
        kind = tag.get("kind")
        name = tag.get("name")
        signature = tag.get("signature")

        last = name
        if signature:
            last += " " + signature

        res = [file_path]
        if scope:
            res.append(scope)
        res += [kind, last]

        ctags.add(tuple(res))

    if len(ctags) == 0:
        return f"{file_path}\n"

    # Build LLM-readable string representation of ctag objects
    sorted_tags = sorted(ctags)
    output = ""
    last = [None] * len(sorted_tags[0])
    tab = "\t"
    for tag in sorted_tags:
        tag = list(tag)

        num_common = 0
        for i in range(len(last) + 1):
            if i == len(last):
                break
            if last[i] != tag[i]:
                num_common = i
                break

        indent = tab * num_common
        rest = tag[num_common:]

        for item in rest:
            output += indent + str(item) + "\n"
            indent += tab
        last = tag

    return output


def _get_file_map(file_paths: set[Path]) -> str:
    tree = dict[str, Any]()
    for file_path in file_paths:
        parts = file_path.parts
        node = tree
        for part in parts:
            if part not in node:
                node[part] = {}
            node = node[part]

    def tree_to_string(tree: dict[str, Any], indent: int = 0) -> str:
        s = ""
        sorted_keys = sorted(tree.keys())
        for key in sorted_keys:
            s += "\t" * indent + key + "\n"
            s += tree_to_string(tree[key], indent + 1)
        return s

    file_map_tree = tree_to_string(tree)
    return file_map_tree


@dataclass
class CodeMapMessage:
    level: Literal["signatures", "no_signatures", "filenames"]
    content: str


class CodeMap:
    def __init__(self, token_limit: int | None = None):
        self.token_limit = token_limit
        self.ctags_disabled = True
        self.ctags_disabled_reason = ""

    @classmethod
    async def create(cls, token_limit: int | None = None):
        stream = SESSION_STREAM.get()

        self = cls(token_limit)
        await self._check_ctags_executable()
        if self.ctags_disabled:
            ctags_disabled_message = f"""
                There was an error with your universal ctags installation, disabling CodeMap.
                Reason: {self.ctags_disabled_reason}
            """
            ctags_disabled_message = dedent(ctags_disabled_message)
            await stream.send(ctags_disabled_message, color="yellow")

        return self

    async def _check_ctags_executable(self):
        try:
            cmd = ["ctags", "--version"]
            output = await run_subprocess_async(*cmd)
            output = output.lower()

            cmd = " ".join(cmd)
            if "universal ctags" not in output:
                self.ctags_disabled_reason = (
                    f"{cmd} does not claim to be universal ctags"
                )
                return
            if "+json" not in output:
                self.ctags_disabled_reason = f"{cmd} does not list +json support"
                return

            with tempfile.TemporaryDirectory() as tempdir:
                hello_py = Path(tempdir) / "hello.py"
                with open(hello_py, "w", encoding="utf-8") as f:
                    f.write("def hello():\n    print('Hello, world!')\n")
                await _get_code_map(Path(tempdir), hello_py)
        except FileNotFoundError:
            self.ctags_disabled_reason = "ctags executable not found"
            return
        except Exception as e:
            self.ctags_disabled_reason = f"error running universal-ctags: {e}"
            return

        self.ctags_disabled = False

    async def _get_message_from_ctags(
        self,
        config: ConfigManager,
        root: Path,
        file_paths: set[Path],
        exclude_signatures: bool = False,
        token_limit: int | None = None,
    ) -> CodeMapMessage | None:
        token_limit = token_limit or self.token_limit
        code_maps = list[str]()
        code_maps_token_count = 0
        for file_path in file_paths:
            code_map = await _get_code_map(
                root, file_path, exclude_signatures=exclude_signatures
            )
            code_map_token_count = count_tokens(code_map, config.model())

            if token_limit is not None and code_maps_token_count > token_limit:
                if exclude_signatures is True:
                    return
                return await self._get_message_from_ctags(
                    config,
                    root,
                    file_paths,
                    exclude_signatures=True,
                    token_limit=token_limit,
                )

            code_maps.append(code_map)
            code_maps_token_count += code_map_token_count

        message = "Code Map:" + "\n\n" + "\n".join(code_maps)

        message_token_count = count_tokens(message, config.model())
        if token_limit is not None and message_token_count > token_limit:
            if exclude_signatures is True:
                return
            return await self._get_message_from_ctags(
                config, root, file_paths, exclude_signatures=True
            )

        code_map_message = CodeMapMessage(
            level="signatures" if not exclude_signatures else "no_signatures",
            content=message,
        )

        return code_map_message

    def _get_message_from_file_map(
        self,
        config: ConfigManager,
        file_paths: set[Path],
        token_limit: int | None = None,
    ) -> CodeMapMessage | None:
        file_map_tree = _get_file_map(file_paths)
        message = "Code Map:" + "\n\n" + file_map_tree

        message_token_count = count_tokens(message, config.model())
        token_limit = token_limit or self.token_limit
        if token_limit is not None and message_token_count > token_limit:
            return

        code_map_message = CodeMapMessage(level="filenames", content=message)

        return code_map_message

    async def get_message(
        self, token_limit: int | None = None
    ) -> CodeMapMessage | None:
        config = CONFIG_MANAGER.get()
        git_root = GIT_ROOT.get()

        git_file_paths = get_non_gitignored_files(git_root)

        if not self.ctags_disabled:
            code_map_message = await self._get_message_from_ctags(
                config, git_root, git_file_paths, token_limit=token_limit
            )
            if code_map_message is not None:
                return code_map_message

        file_map_message = self._get_message_from_file_map(
            config, git_file_paths, token_limit=token_limit
        )
        if file_map_message is not None:
            return file_map_message

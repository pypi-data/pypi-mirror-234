import asyncio
import shlex

from typing import Tuple

import fipper


class AyiinTools:
    async def bash(self: 'fipper.Client', cmd: str):
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        err = stderr.decode().strip()
        out = stdout.decode().strip()
        return out, err

    async def run_cmd(self: 'fipper.Client', cmd: str) -> Tuple[str, str, int, int]:
        args = shlex.split(cmd)
        process = await asyncio.create_subprocess_exec(
            *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return (
            stdout.decode("utf-8", "replace").strip(),
            stderr.decode("utf-8", "replace").strip(),
            process.returncode,
            process.pid,
        )

    async def aexec(self: 'fipper.Client', code, client, message):
        exec(
            f"async def __aexec(client: fipper.Client, m: fipper.types.Message): "
            + "\n chat = m.chat"
            + "\n from_user = m.from_user"
            + "\n r = m.reply_to_message"
            + "\n c = client"
            + "\n m = message"
            + "\n p = print"
            + "".join(f"\n {l}" for l in code.split("\n"))
        )
        return await locals()["__aexec"](client, message)

import asyncio.subprocess as subprocess


class Zipper:
    def __init__(self, filename):
        self.filename = filename
        self.command = " ".join(
            ["cd", self.filename, "&&", "zip", "-q", "-", "*"]
        )  # quiet, recursive
        self.proc = self.stdout = self.stderr = None

    async def __aenter__(self):
        self.proc = await subprocess.create_subprocess_shell(
            self.command,
            subprocess.PIPE,
            subprocess.PIPE,
        )
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr

    async def read(self, chunk_size=1024):
        if not chunk_size:
            chunk_size = -1  # read until EOF
        return await self.stdout.read(chunk_size)

    async def __aexit__(self, exc_type, exc, traceback):
        await self.proc.wait()

import asyncio.subprocess as subprocess


class Zipper:
    def __init__(self, filename):
        self.filename = filename
        self.command = " ".join(["zip", "-", self.filename])
        self.proc = self.stdout = self.stderr = None

    async def init(self):
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

    async def wait(self):
        await self.proc.wait()

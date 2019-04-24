import asyncio.subprocess as subprocess


class Zipper:
    """compress directory (not file) in subprocess"""

    def __init__(self, dirname):
        self.dirname = dirname
        self.command = " ".join(
            ["cd", self.dirname, "&&", "zip", "-q", "-", "*"]
        )  # quiet, recursive
        self.proc = self.stdout = self.stderr = None

    async def __aenter__(self):
        """run subprocess"""
        self.proc = await subprocess.create_subprocess_shell(
            self.command,
            subprocess.PIPE,
            subprocess.PIPE,
        )
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr

    async def read(self, chunk_size=1024):
        """read part of data from pipe. read all the data if
        chun_size is falsy"""
        if not chunk_size:
            chunk_size = -1  # read until EOF
        return await self.stdout.read(chunk_size)

    async def __aexit__(self, exc_type, exc, traceback):
        """kill subprocess if error happened,
        or gracefully wait while process finished"""
        if exc:
            await self.proc.kill()
        else:
            await self.proc.wait()

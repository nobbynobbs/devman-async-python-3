import asyncio.subprocess as subprocess
import logging


class Zipper:
    """compress directory (not file) in subprocess"""

    def __init__(self, dirname):
        self.dirname = dirname
        self.proc = self.stdout = self.stderr = None

    async def __aenter__(self):
        """run subprocess"""
        logging.debug("enter zipper contextmanager")
        self.proc = await subprocess.create_subprocess_exec(
            "zip", "-", "-rqj", self.dirname,  # recursive, quiet, junk path
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
        self.stdout = self.proc.stdout
        self.stderr = self.proc.stderr

    async def read(self, chunk_size=1024):
        """read part of data from pipe. read all the data if
        chunk_size is falsy"""
        if not chunk_size:
            chunk_size = -1  # read until EOF
        logging.debug("zipper: read the chunk from pipe")
        chunk = await self.stdout.read(chunk_size)
        logging.debug("zipper: return chunk")
        return chunk

    async def __aexit__(self, exc_type, exc, traceback):
        """kill subprocess if error happened, empty read buffers and
        wait while process actually finished"""
        if exc:
            logging.debug("send sigkill to zipper subprocess")
            self.proc.kill()
            await self.proc.communicate()  # flush read buffers
        logging.debug("wait while zipper subprocess finished")
        await self.proc.wait()
        logging.debug("exit zipper contextmanage")

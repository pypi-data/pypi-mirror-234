import pytest
from beni import bfile, bpath

@pytest.mark.asyncio
async def test():
    with bpath.useTempFile() as file:
        content = '...'
        await bfile.writeText(file, content)
        assert await bfile.readText(file) == content
    with bpath.useTempFile() as file:
        content = b'...'
        await bfile.writeBytes(file, content)
        assert await bfile.readBytes(file) == content
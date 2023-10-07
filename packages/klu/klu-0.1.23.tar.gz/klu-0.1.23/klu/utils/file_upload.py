import aiofiles
import aiohttp
from aiohttp import ClientResponse

from klu.context.models import PreSignUrlPostData


async def upload_to_pre_signed_url(
    session: aiohttp.ClientSession,
    pre_signed_url_data: PreSignUrlPostData,
    file_path: str,
) -> ClientResponse:
    pre_signed_url, pre_signed_fields = (
        pre_signed_url_data.url,
        pre_signed_url_data.fields,
    )

    data = aiohttp.FormData()
    for key, value in pre_signed_fields.items():
        data.add_field(key, value)

    async with aiofiles.open(file_path, mode="rb") as file:
        data.add_field("file", await file.read())

    async with session.post(pre_signed_url, data=data) as response:
        response.raise_for_status()
        return response

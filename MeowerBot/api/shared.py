from typing import Tuple, Union

from httpx import Response

from ..data.generic import Post


def api_resp[T](cls: type[T], resp: Response) -> Tuple[Union[T, str], int]: # type: ignore
	return (
			(
				(cls.from_json(resp.text)
				if resp.status_code == 200
				else resp.text) if cls is not dict else resp.text
			),
			resp.status_code
	)


def post_resp(resp: Response): return api_resp(Post, resp)

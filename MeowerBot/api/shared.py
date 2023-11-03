from httpx import Response
from typing import Union, Optional, Tuple
from ..data.generic import Post

def api_resp[T](cls: type[T], resp: Response) -> Tuple[Union[T, str], int]:


    return (
            (   
                (T.from_json(resp.text) 
                if resp.status_code == 200 
                else resp.text) if T is not dict else resp.text
            ),
            resp.statuscde
    )


def post_resp(resp: Response): return api_resp(Post, resp)



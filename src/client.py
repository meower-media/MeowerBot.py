from .raw.bot import bot
from .types import make_ctx
import asyncio 

class Client(bot):
  def __init__(self, username, password, prefix, logs=False):
    super.__init__(username, password, logs=logs)
    self.callback(self._on_raw_message, callbackid="on_raw_msg")
    self._waiting_for = []
    
  async def _on_raw_msg(self, msg):
    ctx = make_ctx(message)
    args = ctx.msg.msg.split(" ")
    self._last_msg = ctx.msg
    
    if not len(self._waiting_for) is 0:
      for wf in self._waiting_for:
        if wf['req'](ctx.msg):
          wf['fut'].set_result(True)
          return
          
    self.internal_cbs._call_callback("on_message", args=(ctx, *args) )

  async def wait_for_msg(self, requirements):
    loop = asyncio.get_running_loop()
    
    wf = {"req":requirements, "fut": loop.create_future()}
    self._waiting_for.append(wf)

    await wf['fut']
    
    return self._last_msg

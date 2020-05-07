class Mock():
  def __init__(self, credentials):
    self.cortex = None

  async def open_connection(self):
    self.cortex = None

  async def close_connection(self):
    self.cortex = None

  async def get_data(self, s):
    record = await record_data(s, self.cortex)
    return record
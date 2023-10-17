class EmailAttachment:
  def __init__(self, path:str, filename:str, filetype:str):
    self.filepath = path
    self.filename = filename
    self.filetype = filetype

  def __eq__(self, obj) -> bool:
    return self.filepath == obj.filepath and self.filetype == obj.filetype \
      and self.filename == obj.filename
  
  def __str__(self) -> str:
    return str(vars(self))

  def __getitem__(self, key:str):
    return self.__getattribute__(key)


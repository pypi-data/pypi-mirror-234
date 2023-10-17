# wtf python

class RainerUtil:
  
  def __init__(self):

    def getBytes(s):
        if isinstance(s, bytes):
            return s
        elif isinstance(s, str):
            return bytes(s, encoding="utf8")
        else:
            return bytes(s)
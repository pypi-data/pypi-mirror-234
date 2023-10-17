import json
import urllib.request as req
import urllib.parse as prs
import base64

from .commit import RainerCommit

class RainerClient:

  def __init__(self, base_uri):
    if not base_uri:
      raise ValueError("base_uri is required")
    self.base_uri = base_uri

  def commit_uri(self, key, version=None):
    """Base URI for a commit key, possibly at a specific version."""
    return self.base_uri + "/" + key + (("/" + str(version)) if version != None else "")

  def list(self, all=False):
    """Get a dict of commit key -> metadata for the most recent versions."""
    rsp = req.urlopen(self.base_uri + ("?all=yes" if all else ""))
    return json.loads(rsp.read())

  def list_full(self, all=False):
    """Get a dict of commit key -> RainerCommit object for the most recent versions."""
    rsp = req.urlopen(self.base_uri + "?payload_base64=yes" + ("&all=yes" if all else ""))
    rsp_json = json.loads(rsp.read())
    for key, value in rsp_json.items():
      rsp_json[key] = RainerCommit(value, base64.b64decode(value['payload_base64']))
    return rsp_json

  def get_commit(self, key, version=None):
    """Get commit object, possibly at a specific version."""
    meta = self.get_metadata(key, version)
    if meta.get("empty", False):
      value = None
    else:
      value = self.get_value(key, meta["version"])
    return RainerCommit(meta, value)

  def get_value(self, key, version=None):
    """Get commit value (a string), possibly at a specific version."""
    rsp = req.urlopen(self.commit_uri(key, version))
    return bytes(rsp.read())

  def get_metadata(self, key, version=None):
    """Get commit metadata (a dict), possibly at a specific version."""
    rsp = req.urlopen(self.commit_uri(key, version) + "/meta")
    return json.loads(rsp.read())

  def post_commit(self, metadata, value):
    """Save a new commit."""
    data = value.encode("utf-8")
    url = self.commit_uri(metadata["key"], metadata["version"])
    headers = {
      "Content-Type"     : "application/octet-stream",
      "X-Rainer-Author"  : metadata["author"],
      "X-Rainer-Comment" : metadata["comment"],
      "X-Rainer-Empty"   : str(metadata.get("empty", "false"))
    }
    
    request = req.Request(url, data, headers)

    # request = req.Request(self.commit_uri(metadata["key"], metadata["version"]), value, {
    #   "Content-Type"     : "application/octet-stream",
    #   "X-Rainer-Author"  : metadata["author"],
    #   "X-Rainer-Comment" : metadata["comment"],
    #   "X-Rainer-Empty"   : bytes(metadata.get("empty", "false"))
    # })
    rsp = req.urlopen(request)
    return json.loads(rsp.read())

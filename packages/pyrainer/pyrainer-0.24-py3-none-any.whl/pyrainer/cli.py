import argparse
import difflib
import errno
import os
import re
import subprocess
import sys
import tempfile
import termcolor
import termios
import urllib.request as req
import yaml

from .commit import RainerCommit
from .http import RainerClient

class RainerCommandLine:

  def __init__(self, client_or_uri):
    if isinstance(client_or_uri, RainerClient):
      self.client = client_or_uri
    else:
      self.client = RainerClient(client_or_uri)

  def action_show(self, key, version=None):
    commit = self.client.get_commit(key, version)
    if commit.value is not None:
      #print (commit.value, end=' ')
      print (commit.value.decode('utf-8'))

  def action_prepare(self, key, version=None):
    commit = self.client.get_commit(key, version)
    next_commit = self.next_commit(commit)
    print (self.prepare_commit(next_commit), end=' ')

  def action_list(self, all=False):
    delimeter = "-"
    data = self.client.list(all)
    for key in sorted(data.keys()):
      version = data[key]['version']
      print (f"{str(version):3}{key:35}\t{self.client.commit_uri(key, version)}")

  def action_commit(self, key):
    print (self.post_prepared_commit(key, sys.stdin.read()))

  def action_commit_value(self, key, version, message):
    if version:
      the_version = version
    else:
      the_version = 1
    print (self.client.post_commit(
      {"key": key, "version": the_version, "author": os.getlogin(), "comment": message},
      sys.stdin.read()
    ))

  def action_log(self, key, version=None):
    """CLI log action."""
    # old_stdout = sys.stdout
    # old = termios.tcgetattr(sys.stdin)
    try:
      # page output
      # pager = subprocess.Popen(['less', '-FRSX'], stdin=subprocess.PIPE, stdout=sys.stdout)
      # sys.stdout = pager.stdin

      q = self.client.get_commit(key, version)
      while int(q.meta["version"]) > 0:
        if int(q.meta["version"]) == 1:
          p = RainerCommit({"version": 0, "key": q.meta["key"]}, "".encode())
        else:
          p = self.client.get_commit(key, int(q.meta["version"]) - 1)

        print (termcolor.colored(f"Commit {q.meta['version']}", "yellow"))
        print (f"Author: {q.meta['author']}")
        print (f"Date:   {q.meta['mtime']}")
        print ()

        if q.meta.get("comment", "") != "":
          for comment_line in q.meta["comment"].split("\n"):
            print ("  {:s}".format(comment_line))
          print ()

        self.__printdiff(
          p.value.decode() if p.value is not None else "",
          q.value.decode() if q.value is not None else "",
          "{:s} {:d}".format(p.meta["key"], p.meta["version"]),
          "{:s} {:d}".format(q.meta["key"], q.meta["version"]),
        )

        if int(q.meta["version"]) > 0:
          print ()
          print ()

        # sys.stdout.flush()

        q = p

      # pager.stdin.close()
      # pager.wait()

    finally:
      # sys.stdout = old_stdout
      # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old)
      print("End of Log")

  def action_uncommit(self, key, version=None, yes=False):
    """CLI uncommit action."""
    commit = self.client.get_commit(key, version)
    next_commit = self.next_commit(commit)
    next_commit.meta["empty"] = True
    next_commit.value = ""
    if yes:
      self.post_prepared_commit(key, self.prepare_commit(next_commit))
    else:
      self.interactive_confirm_and_post(key, commit, self.prepare_commit(next_commit))

  def action_edit(self, key, version=None):
    """CLI edit action."""
    try:
      commit = self.client.get_commit(key, version)
    except req.HTTPError as e:
      if e.code == 404:
        # Commit not found. Make some stuff up.
        commit = RainerCommit({"key": key, "version": 0}, "")
      else:
        raise

    with tempfile.NamedTemporaryFile(delete=False, suffix=".yaml") as tmp:
      editor         = os.environ.get("EDITOR", "vi")
      prepared       = self.prepare_commit(self.next_commit(commit))
      tmp.write(prepared)

    try:
      # open EDITOR on the temp file
      ecode  = subprocess.call([editor + " " + re.escape(tmp.name)], shell=True)
      if ecode != 0:
        raise Exception("Editor %s exited with code %d" % (editor, ecode))

      # read what the editor wrote
      with open(tmp.name, 'r') as tmp:
        newprepared = tmp.read()

      if self.interactive_confirm_and_post(key, commit, newprepared):
        # all successful - remove tmp file
        os.unlink(tmp.name)
      else:
        print ("Your work is saved in: " + tmp.name)

    except:
      print ("An error was encountered. Your work is saved in: " + tmp.name)
      raise

  def interactive_confirm_and_post(self, key, old_commit, new_prepared):
    """Display a diff, ask for confirmation on the terminal, and then post (maybe). Returns True if a post occurred."""
    written = False
    if old_commit.meta["key"] != key:
      raise ValueError("Expected key '%s', got '%s'" % (key, old_commit.meta["key"]))

    # extract value for comparison and diffing
    new_prepared_split = self.__splitprepared(new_prepared)

    if old_commit.value != new_prepared_split[1]:
      # show diff
      self.__printdiff(
        old_commit.value if old_commit.value is not None else "",
        new_prepared_split[1],
        "{:s} (current)".format(key),
        "{:s} (new)".format(key)
      )

      # ask for confirmation
      usersaid = input("Commit to %s (yes/no)? " % self.client.commit_uri(key))

      while usersaid != "yes" and usersaid != "no":
        usersaid = input("Please type 'yes' or 'no': ")

      if usersaid == "yes":
        print (self.post_prepared_commit(key, new_prepared))
        written = True
      else:
        print ("OK, not commiting.")

    else:
      print ("No change, not commiting.")

    return written

  def next_commit(self, commit):
    """Return a commit like this one, but representing the next commit in the series."""
    return RainerCommit(
      {"version" : int(commit.meta["version"]) + 1,
       "author"  : os.getlogin(),
       "comment" : ""},
      commit.value if commit.value is not None else ""
    )

  def prepare_commit(self, commit):
    """Prepare a commit for editing in an editor (convert metadata + value into text form). Returns a string."""
    header = yaml.dump(commit.meta, default_flow_style=False)
    header += "---\n"
    if commit.value is None:
      return bytes(header, encoding='utf8')
    else:
      return bytes(header, encoding='utf8') + bytes(commit.value)

  def post_prepared_commit(self, key, prepared):
    """Post a prepared commit back to the API."""
    docs           = self.__splitprepared(prepared)
    docs[0]["key"] = key
    return self.client.post_commit(docs[0], docs[1])

  def __splitprepared(self, prepared):
    # We can't use yaml.load_all since we want to pass the second document straight through. It might not even be
    # a valid yaml document (gasp!)
    docs = prepared.split("\n---\n")
    docs[0] = yaml.full_load(docs[0])
    return docs

  def __printdiff(self, oldtext, newtext, oldname, newname):
    oldlines = [line + "\n" for line in str(oldtext).split("\n")]
    newlines = [line + "\n" for line in str(newtext).split("\n")]

    for line in difflib.unified_diff(oldlines, newlines, str(oldname), str(newname)):
      if line.startswith("---") or line.startswith("+++"):
        sys.stdout.write(termcolor.colored(str(line), "white", attrs=["bold"]))
      elif line.startswith("-"):
        sys.stdout.write(termcolor.colored(str(line), "red"))
      elif line.startswith("+"):
        sys.stdout.write(termcolor.colored(str(line), "green"))
      else:
        sys.stdout.write(str(line))

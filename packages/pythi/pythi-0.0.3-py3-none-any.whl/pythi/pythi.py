import os

def unify_cwd():
  """
  cd into the project root folder (containing the .git subfolder)

  :return: None
  """
  cwd = os.getcwd()
  while(not os.path.exists(os.path.join(cwd, '.git'))):
    cwd = os.path.dirname(cwd)

  # change cwd to this directory
  os.chdir(cwd)
  
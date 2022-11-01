import os
import shutil
import subprocess

from pysd_package.restartfile import Restartfile, Coordfile

SD_PATH = os.getenv("SD_PATH", "/home/jp/UppASD/bin/sd.gfortran")

class Result:
  def __init__(self, config, cmdres, restartfile, coordfile):
    self.config = config
    self.cmdres = cmdres
    self.restartfile = restartfile
    self.coordfile = coordfile

class SDLauncher:
  def __init__(self):
    pass

  def run(self, config, config_dir):
    shutil.rmtree(config_dir, ignore_errors=True)
    os.makedirs(config_dir, exist_ok=True)
    config.save_all_configs(config_dir)
    p = subprocess.run(SD_PATH, cwd=config_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0 or len(p.stderr) > 0 or 'ERROR' in str(p.stdout):
      return Result(config, p, None, None)
    restartfile = Restartfile(os.path.join(config_dir, config.restartfile_fname()))
    if config.do_prnstruct == 1:
      coordfile = Coordfile(os.path.join(config_dir, config.coordfile_fname()))
    else:
      coordfile = Coordfile()
    return Result(config, p, restartfile, coordfile)
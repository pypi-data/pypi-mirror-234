# -*- coding: utf-8 -*-
HELP= """ IO



"""
import os, glob, sys, math, string, time, json, logging, functools, random, yaml, operator, gc
from pathlib import Path; from collections import defaultdict, OrderedDict
from box import Box


#################################################################
from utilmy.utilmy_base import log, log2

def help():
    """function help"""
    from utilmy import help_create
    ss = help_create(__file__)
    print(ss)



#####################################################################################
def test_all():
  test_screenshot()

  

def test_screenshot():
  import utilmy as uu

  _, dirtmp = uu.dir_testinfo()
  output_filename = "test_screenshot.png"

  log("\n#######", screenshot)
  screenshot(dirtmp + output_filename)
  assert uu.os_file_check(dirtmp + output_filename), "FAILED -> screenshot()"



#####################################################################################
def screenshot(output='fullscreen.png'):
  """ take screenshot from python and save on disk
  Docs::

      output_filename = "test_screenshot.png"
      log("\n#######", screenshot)
      screenshot(dirtmp + output_filename)
      assert uu.os_file_check(dirtmp + output_filename), "FAILED -> screenshot()"



  """
  import mss  

  with mss.mss() as mss_instance:
    mss_instance.shot(output=output)




#####################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



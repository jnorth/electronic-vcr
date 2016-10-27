import os
import re
import sys
import json
import time
import argparse
from subprocess import call
from datetime import timedelta

# Parse arguments

parser = argparse.ArgumentParser(
  description='Online video archiver, powered by youtube-dl.'
)

parser.add_argument(
  '--script-path',
  help='path to a json script file',
  default=os.path.join(os.getcwd(), 'vcr.json')
)

parser.add_argument(
  '--data-path',
  help='path to download files to',
  default=os.getcwd()
)

parser.add_argument(
  '--interval',
  help='run the script on a schedule (e.g. 2h0m0s)',
  default=False
)

args = parser.parse_args()

# Functions

duration_regex = re.compile(
  r'(?P<hours>\d+?)h'
  r'(?P<minutes>\d+?)m'
  r'(?P<seconds>\d+?)s$'
)

def parse_time(time_str):
  parts = duration_regex.match(time_str)
  if not parts: return

  parts = parts.groupdict()

  time_params = {}
  for name, param in parts.items():
    if param:
      time_params[name] = int(param)

  return timedelta(**time_params)

def parse_option(option, value):
  if value == False:
    return []
  elif value == True:
    return [option]
  else:
    return [option, value]

def vcr(path, url, options=[]):
  os.makedirs(path, exist_ok=True)
  args = ["youtube-dl"]

  for option in options:
    args = args + parse_option(option, options[option])

  args.append(url)
  print("VCR: {}".format(" ".join(args)), flush=True)
  call(args, cwd=path)

def load_vcr_script(script_path, data_path):
  try:
    with open(script_path, 'r') as script_file:
      script = json.load(script_file)
  except IOError as e:
    print("VCR: No script file found at {}".format(script_path), flush=True)
    return

  default_options = script.get("default-options", {})
  items = script.get("items", [])

  for item in items:
    options = default_options.copy()
    options.update(item.get("options", {}))
    path = os.path.join(data_path, item.get("path", ""))
    url = item.get("url", "")
    vcr(path, url, options)

while True:
  try:
    load_vcr_script(args.script_path, args.data_path)
  except Exception as e:
    print("VCR: {}".format(e), flush=True)

  if (args.interval):
    interval = parse_time(args.interval)
    print("VCR: Sleeping for {}".format(interval), flush=True)
    time.sleep(interval.total_seconds())
  else:
    break

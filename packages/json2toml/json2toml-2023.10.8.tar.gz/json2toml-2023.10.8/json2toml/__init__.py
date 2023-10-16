#! coding: utf-8
"""
    json2toml
    ~~~~~~~~~~
    
    :copyright: © 2023 by the NicoNing(dodoru@foxmail.com)
    :license: MIT, see LICENSE for more details.
"""

import argparse

__version__ = '2023.10.08'

PROG = "json2toml"
LONG_USAGE = f"""

## shell command toolkit :: convert json to toml
    
    json2toml ({__version__})

eg:
  [0] json2toml --help                                  ; show help
  [1] json2toml input.json output.toml                  ; json to tmol
  [2] json2toml input.toml output.json                  ; toml to json   
  [3] json2toml --stdin '{{"name":"jsonfile"}}'         ; stdin:json to stdout:toml
  [4] json2toml --stdin 'name = "jsonfile"' --mode=2    ; stdin:toml to stdout:json
"""


def get_sys_args():
    tip_usage = LONG_USAGE
    sys_parser = argparse.ArgumentParser(usage=tip_usage, prog=PROG)
    # tip_usage = tip_help
    # sys_parser = argparse.ArgumentParser(usage=tip_usage, prog=PROG)
    sys_parser.add_argument("-v", "--version", help="show versions", action="store_true")
    sys_parser.add_argument("-i", "--stdin", help="stdin::text", action="store_true")
    sys_parser.add_argument("-d", "--dry_run", help="debug only, 不运行，只打印调试参数", action="store_true")
    sys_parser.add_argument("--force_redo", help="force overwrite", action="store_true")
    sys_parser.add_argument("--indent", help="output json/toml file", default=2)
    sys_parser.add_argument("--mode", help="0-auto; 1-json2toml; 2-toml2json; ", default=0)
    sys_parser.add_argument("--input_file", help="input json/toml file", default="")
    sys_parser.add_argument("--output_file", help="output json/toml file", default="")
    return sys_parser


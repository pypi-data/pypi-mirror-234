#!python3


import os
import sys
import json
import rtoml

from pprint import pformat

_curdir = os.path.abspath(os.path.dirname(__file__))
_srcdir = os.path.dirname(_curdir)
if _srcdir not in sys.path:
    sys.path.insert(0, _srcdir)


# pprint(sys.path, indent=2)
import json2toml

def cli_main():
    """
    --help              ; 显示参数列表
    --version           ; 获取版本号
    """
    # print(json2toml.__file__, _srcdir)
    sys_parser = json2toml.get_sys_args()
    sys_args, _unknown_argv = sys_parser.parse_known_args()
    if sys_args.version:
        # print(f"version: {json2toml.__version__}", sys_args.version)
        print(f"version: {json2toml.__version__} ({__file__})")
        return 0

    raw_text = ""
    if sys_args.stdin:
        raw_text = " ".join(_unknown_argv)

    else:
        if not sys_args.input_file:
            if len(_unknown_argv) > 0:
                sys_args.input_file = _unknown_argv[0]

        if not sys_args.output_file:
            if len(_unknown_argv) > 1:
                sys_args.output_file = _unknown_argv[1]

    if sys_args.dry_run:
        print("##; DryRun:: ", pformat(sys_args, indent=2))
        print("##; _execute_file:", os.path.dirname(__file__))
        if sys_args.stdin:
            print("##; _raw_stdin:\n", raw_text)
        else:
            print("##; _unknown_argv:", len(_unknown_argv), pformat(_unknown_argv, indent=2))
        return 0

    mode = int(sys_args.mode)
    ## 0: json -> toml
    ## 1: toml -> json
    if sys_args.stdin:
        if not raw_text:
            print("##; @stdin: expect stdin(json/toml)")
            return -1

    else:
        if not os.path.isfile(sys_args.input_file):
            print(f"##; @input_file: expect json/toml file, but recieve:({sys_args.input_file})")
            return -1

        with open(sys_args.input_file, "r") as fr:
            raw_text = fr.read()

    if sys_args.output_file.endswith("json"):
        mode = 2

    if os.path.exists(sys_args.output_file) and not sys_args.force_redo:
        print(f"##; @output_file:({sys_args.output_file}) is already existed, and force_redo=({sys_args.force_redo})")
        return -2

    if mode == 2:
        raw_object = rtoml.loads(raw_text)
        raw_result = json.dumps(raw_object, indent=sys_args.indent, ensure_ascii=False)
    else:
        try:
            raw_object = json.loads(raw_text)
        except Exception as e:
            try:
                import json5
                raw_object = json5.loads(raw_text)
            except Exception as e2:
                print(raw_text)
                print("##;json parse failed:", pformat(e2, indent=2))
                return -2
        raw_result = rtoml.dumps(raw_object, pretty=True)

    if not sys_args.output_file:
        print(raw_result)
    else:
        with open(sys_args.output_file, "w") as fw:
            fw.write(raw_result)
            fw.write(os.linesep)
    return 0


def main():
    st = cli_main()
    if st != 0:
        PROG = json2toml.PROG
        if sys.argv[0].startswith("."):
            PROG = sys.argv[0]
        tip_help = f"## 如需帮助，请运行: {PROG} --help"
        print(tip_help)
        print("## Error!")
    return st


if __name__ == '__main__':
    main()

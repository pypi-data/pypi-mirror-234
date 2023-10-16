import os
import os.path
import subprocess
from typing import List

from pymultigit.configs import ConfigSubprocess, ConfigOutput


def check_call_ve(orig_args: List[str]) -> None:
    if not os.path.isdir(".venv/default"):
        if ConfigOutput.print_not:
            print("not a make venv folder (.venv/default is not there)")
        return
    # we call 'venv-run' with absolute path since it may change folder
    args = [
        "venv-run",
        "--venv",
        os.path.abspath(".venv/default"),
        "--",
    ]
    args.extend(orig_args)
    if ConfigSubprocess.print_command:
        print(f"running {args}")
    if ConfigSubprocess.quiet:
        subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.check_call(args)

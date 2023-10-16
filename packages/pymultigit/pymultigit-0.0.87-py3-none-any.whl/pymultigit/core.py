import glob
import os
import os.path
import subprocess
import sys
from typing import Union, Generator, Tuple

import git

from pymultigit.configs import ConfigOutput, ConfigDebug, ConfigGrep, ConfigPull, ConfigMain
from pymultigit.utils.subprocess import check_call_ve


DISABLE = ".build.disable"


def projects() -> Generator[str, None, None]:
    """
    the method yields all project folders [project_dir]
    """
    if ConfigMain.use_glob:
        if os.path.isdir(".git"):
            repos_list = [os.getcwd()]
        else:
            repos_list = [os.path.dirname(x) for x in glob.glob("*/.git")]
            if not repos_list:
                repos_list = [os.path.dirname(x) for x in glob.glob("*/**/.git")]
    else:
        repos_list = ConfigMain.folders
    if ConfigMain.sort:
        repos_list.sort()
    yield from repos_list


def run(args, do_exit=True) -> Tuple[str, str, int]:
    with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
        (res_out_b, res_err_b) = p.communicate()
        res_out = res_out_b.decode()
        res_err = res_err_b.decode()
        if p.returncode:
            print(f"errors while running [{args}]...")
            print(res_out, end="", file=sys.stderr)
            print(res_err, end="", file=sys.stderr)
            if do_exit:
                sys.exit(p.returncode)
    return res_out, res_err, p.returncode


def do_count(fnc, attr_name, not_attr_name, attr_plural, print_attr, print_not_attr) -> None:
    count = 0
    count_attr = 0
    for project_dir in projects():
        count += 1
        repo = git.Repo(project_dir)
        attr = fnc(repo)
        if attr:
            count_attr += 1
        if attr:
            if print_attr:
                if ConfigOutput.terse:
                    print(project_dir)
                else:
                    print(f"project [{project_dir}] {attr_name}")
        else:
            if print_not_attr:
                if ConfigOutput.terse:
                    print(project_dir)
                else:
                    print(f"project [{project_dir}] {not_attr_name}")
    if ConfigOutput.stats:
        print(f"scanned [{count}] projects")
        print(f"[{count_attr}] projects {attr_plural}")


def do_for_all_projects(fnc) -> None:
    orig_dir = os.getcwd()
    for project_dir in projects():
        if ConfigOutput.output:
            print(f"[{project_dir}]...")
        os.chdir(project_dir)
        # pylint: disable=bare-except
        try:
            fnc()
        except:  # noqa: E722
            if ConfigMain.stop:
                raise
        os.chdir(orig_dir)


def is_git_folder(directory: str) -> bool:
    return os.path.isdir(directory) and os.path.isdir(os.path.join(directory, ".git"))


def print_projects_that_return_data(fnc) -> None:
    """
    In this function we are sure that the directories we get a real git folders
    since we get them from the `projects` function. There is no need to check this.
    """
    orig_dir = os.getcwd()
    have_projects = False
    for project_dir in projects():
        have_projects = True
        os.chdir(project_dir)
        data = fnc()
        if data is not None:
            if ConfigOutput.terse:
                print(project_dir)
            else:
                print(f"project [{project_dir}]...")
                print(data, end="")
        os.chdir(orig_dir)
    if ConfigMain.print_no_projects and not have_projects:
        print("no projects found")


def is_dirty(repo) -> bool:
    return repo.is_dirty()


def has_untracked_files(repo) -> bool:
    return len(repo.untracked_files) > 0


def non_synchronized_with_upstream(_repo: str) -> bool:
    return False


def disable():
    if os.path.isfile(DISABLE):
        if ConfigOutput.print_not:
            print(f"build is disabled with file [{DISABLE}]")
        return True
    return False


def check_pydmt():
    if not os.path.isfile(".pydmt.config"):
        if ConfigOutput.print_not:
            print("not a pydmt folder (.pydmt.config not there)")
        return True
    return False


def do_build_bootstrap() -> None:
    if disable():
        return
    if not os.path.isfile("bootstrap"):
        if ConfigOutput.print_not:
            print("not a boostrap folder (bootstrap not there)")
        return
    subprocess.check_call(["./bootstrap"])


def do_build_pydmt() -> None:
    if disable():
        return
    if check_pydmt():
        return
    subprocess.check_call([
        "pydmt",
        "build",
    ])


def do_build_venv_pydmt() -> None:
    if disable():
        return
    if check_pydmt():
        return
    check_call_ve([
        "pydmt",
        "build",
    ])


def do_build_pydmt_build_venv() -> None:
    if disable():
        return
    if not os.path.isfile(".pydmt.config"):
        if ConfigOutput.print_not:
            print("not a pydmt folder (.pydmt.config not there)")
        return
    args = ["pydmt", "build_venv"]
    subprocess.check_call(args)


def do_build_venv_make() -> None:
    if disable():
        return
    if not os.path.isfile("Makefile") or not os.path.isdir(".venv/default"):
        if ConfigOutput.print_not:
            print("not a make venv folder (either Makefile or .venv/default is not there)")
        return
    check_call_ve([
        "make",
    ])


def do_build_make() -> None:
    if disable():
        return
    if not os.path.isfile("Makefile"):
        if ConfigOutput.print_not:
            print("not a make folder (Makefile not there)")
        return
    subprocess.check_call(["make"])


def do_pull() -> int:
    args = ["git", "pull"]
    if ConfigDebug.git_verbose:
        args.append("--verbose")
    if ConfigPull.pull_quiet:
        args.append("--quiet")
    return subprocess.check_call(args)


def do_check_workflow_exists_for_makefile() -> bool:
    return os.path.isfile("Makefile") and os.path.isfile(".github/workflows/build.yml")


def do_grep() -> None:
    project_dir = os.path.basename(os.getcwd())
    args = ["git", "grep"]
    if ConfigDebug.git_verbose:
        args.append("--verbose")
    if ConfigDebug.git_quiet:
        args.append("--quiet")
    args.append(ConfigGrep.regexp)
    if ConfigGrep.files is not None:
        args.extend([
            "--",
            ConfigGrep.files
        ])
    with subprocess.Popen(
        args,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as pipe:
        for line in pipe.stdout:  # type: ignore[union-attr]
            try:
                print(f"{project_dir}/{line.decode()}", end="")
            except UnicodeDecodeError:
                print(f"{project_dir}/-- line cant be decoded --", end="")
        if pipe.returncode:
            raise subprocess.CalledProcessError(
                returncode=pipe.returncode,
                cmd=" ".join(args),
            )


def do_local_branch() -> None:
    args = ["git", "branch", "--show-current"]
    if ConfigDebug.git_verbose:
        args.append("--verbose")
    if ConfigDebug.git_quiet:
        args.append("--quiet")
    subprocess.check_call(args)


def do_remote_branch() -> None:
    args = ["git", "branch", "--remotes", "--show-current"]
    if ConfigDebug.git_verbose:
        args.append("--verbose")
    if ConfigDebug.git_quiet:
        args.append("--quiet")
    subprocess.check_call(args)


def do_github_branch() -> str:
    """
    https://stackoverflow.com/questions/28666357/git-how-to-get-default-branch
    """
    args = ["gh", "repo", "view", "--json", "defaultBranchRef", "--jq", ".defaultBranchRef.name",]
    return subprocess.check_output(args).decode().strip()


def do_clean() -> int:
    args = ["git", "clean", "-qffxd"]
    # if ConfigDebug.git_verbose:
    #     args.append("--verbose")
    # if ConfigDebug.git_quiet:
    #     args.append("--quiet")
    return subprocess.check_call(args)


def do_status() -> Union[None, str]:
    (res_out, res_err, _) = run([
        "git",
        "status",
        # porcelain is guaranteed to have parsable output and not
        # change across git versions
        "--porcelain",
        # when using --porcelain branch information is not shown,
        # this flag makes it not so, the problem with it is that
        # it produces output which should be parsed and that is
        # why we do not used it and use the "git rev-list" that follows...
        # "--branch"
        # "--short",
    ])
    if res_out != "" or res_err != "":
        return res_out + res_err
    (res_out, res_err, _) = run([
        "git",
        "rev-list",
        "--left-only",
        "--count",
        "@...@{upstream}",
    ])
    if res_out != "0\n" or res_err != "":
        return res_out + res_err
    return None


def do_dirty() -> Union[None, str]:
    args = ["git", "status", "--porcelain"]
    if ConfigDebug.git_verbose:
        args.append("--verbose")
    if ConfigDebug.git_quiet:
        args.append("--quiet")
    output = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode()
    if output != "":
        return output
    return None

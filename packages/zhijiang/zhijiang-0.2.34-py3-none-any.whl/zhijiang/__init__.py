try:
    from zhijiang.scripts.zhijiang_useful_func import *
except:
    pass


def main():
    import os
    import subprocess
    from termcolor import cprint
    import fire
    import zhijiang as pkg
    pkg_installed_path = pkg.__path__[0]
    def setup_rc_files(dry_run=True, restore_rc=False):
        assert isinstance(
            dry_run, bool
        ), "dry_run should be a boolean, so its value can only by True or False"
        if dry_run:
            cprint(
                "you are in dry run mode, use '--dry_run=False' to disable dry run", "red"
            )

        rc_files_path = os.path.join(pkg_installed_path, "data/rc_files")
        for root, _, files in os.walk(rc_files_path):
            for f in files:
                rc_file = os.path.join(root, f)
                if f not in ["bashrc", "alias"] and ".sw" not in f:
                    if ".sw" in f:
                        continue
                    if f != "htoprc":
                        dst = f"~/.{f}"
                    else:
                        dst = "~/.config/htop/htoprc"
                    backup = f"{dst}.bk"
                    # backup the file if backup file is not existed
                    if not os.path.exists(os.path.expanduser(backup)):
                        # when user is root, then the rc file is not existed
                        if not os.path.exists(os.path.expanduser(dst)):
                            os.system(f"mkdir -p `basename {dst}` && touch {dst}")
                        os.system(f"cp {dst} {backup}")

                    cmd = f"cp {backup} {dst}"
                    if not restore_rc:
                        # restore to backup file first, then do the changes
                        cmd = f"{cmd} && cp {rc_file} {dst}"
                    print(cmd)

                    if not dry_run:
                        os.system(cmd)
                else:
                    dst = "~/.bashrc"
                    backup = f"{dst}.bk"
                    # backup the file if backup file is not existed
                    if not os.path.exists(os.path.expanduser(backup)):
                        # when user is root, then the rc file is not existed
                        if not os.path.exists(os.path.expanduser(dst)):
                            os.system(f"mkdir -p `basename {dst}` &&  touch {dst}")
                        # if file is alias then just backup related is not need
                        if f != "alias":
                            os.system(f"cp {dst} {backup}")

                    cmd = "echo -n"  # noop
                    if f == "bashrc":
                        cmd = f"cp {backup} {dst}"
                    if not restore_rc:
                        cmd = f"{cmd} && cat {rc_file} >> {dst}"
                    print(cmd)

                    if not dry_run:
                        os.system(cmd)


    def install_useful_tools():
        """
        install usefule shell commands and python pkg, e.g. profiling tools, debugging tools;
        """
        script_path = os.path.join(pkg_installed_path, "scripts/install_useful_tools.sh")
        subprocess.run(f"bash {script_path}".split(), check=True)


    def enhance_python():
        """
        add useful functions to python site.py, so you can call them like built-in functions, they are prefixed with zhijxu
        """
        script_path = os.path.join(pkg_installed_path, "scripts/enhance_python.sh")
        subprocess.run(f"bash {script_path}".split(), check=True)


    def info():
        """
        print help info;
        """
        zip_file = os.path.join(pkg_installed_path, "zhijiang.7z")
        cmd = f"7z x {zip_file} -o{pkg_installed_path.rstrip('zhijiang')}"
        cprint(f"1. unzip file with the follwoing command fisrt \n'   {cmd}  \n 7z is from p7zip-full '", "red")
        cprint(f"2. you can modify the file before executing them, they are put at {pkg_installed_path}", "red")
        cprint("3. added python function or bash command are all prefixed with zhijiang- ", "red")


    def all():
        """
            run all subcommands
        """
        setup_rc_files(dry_run=False)
        install_useful_tools()
        enhance_python()
        os.system("zhijiang -- --completion > ~/.zhijiang; echo source  ~/.zhijiang >> ~/.bashrc")
        # if install_useful_tools.sh need to modify bashrc, then do it here, as the script will not be executed again
        os.system("echo source ~/.git-completion.bash >> ~/.bashrc")
        os.system("echo 'echo -------------bashrc done-------------------' >> ~/.bashrc")
        cprint("remember to source ~/.bashrc to make the changes take effect", "red")



    fire.Fire(
        {
            "info": info,
            "all": all,
            "setup_rc_files": setup_rc_files,
            "install_useful_tools": install_useful_tools,
            "enhance_python": enhance_python,
        }
    )


if __name__ == "__main__":
    main()

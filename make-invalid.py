#!/usr/bin/env python

import click
import os
import subprocess
import sys


@click.command()
@click.option("--location", required=True, help="Location to create demo repository")
def main(location):
    if not os.path.exists(location):
        print("Repository not found")
        sys.exit(1)

    current_dir = os.getcwd()

    keys_dir = os.path.join(current_dir, "keys")

    os.chdir(location)

    result = subprocess.run(["git", "config", "--local", "user.name", "Aditya Sirish"])
    if result.returncode != 0:
        print("Unable to set Git config")
        sys.exit(1)

    result = subprocess.run(
        ["git", "config", "--local", "user.email", "aditya@saky.in"]
    )
    if result.returncode != 0:
        print("Unable to set Git config")
        sys.exit(1)

    result = subprocess.run(["git", "config", "--local", "gpg.format", "ssh"])
    if result.returncode != 0:
        print("Unable to set Git config")
        sys.exit(1)

    result = subprocess.run(
        [
            "git",
            "config",
            "--local",
            "user.signingkey",
            f"{os.path.join(keys_dir, 'ossna-1')}",
        ]
    )
    if result.returncode != 0:
        print("Unable to set Git config")
        sys.exit(1)

    result = subprocess.run(["gittuf", "verify-ref", "main"])
    if result.returncode != 0:
        print("Repository is already in invalid state")
        sys.exit(1)

    result = subprocess.run(["git", "checkout", "main"])
    if result.returncode != 0:
        print("Unable to checkout main branch")
        sys.exit(1)

    with open("README.md", "w+") as fp:
        fp.write("yolo")

    subprocess.run(["git", "add", "README.md"])
    result = subprocess.run(["git", "commit", "-S", "-m", "YOLO"])
    if result.returncode != 0:
        print("Unable to create bad commit")
        sys.exit(1)

    result = subprocess.run(["gittuf", "rsl", "record", "main"])
    if result.returncode != 0:
        print("Unable to create bad RSL entry")
        sys.exit(1)


if __name__ == "__main__":
    main()

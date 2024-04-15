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

    result = subprocess.run(["git", "config", "--local", "user.name", "Billy Lynch"])
    if result.returncode != 0:
        print("Unable to set Git config")
        sys.exit(1)

    result = subprocess.run(
        ["git", "config", "--local", "user.email", "billy@chainguard.dev"]
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
            f"{os.path.join(keys_dir, 'ossna-2')}",
        ]
    )
    if result.returncode != 0:
        print("Unable to set Git config")
        sys.exit(1)

    result = subprocess.run(["gittuf", "verify-ref", "main"])
    if result.returncode == 0:
        print("Repository is in valid state")
        sys.exit(1)

    result = subprocess.run(
        ["git", "rev-parse", "refs/gittuf/reference-state-log"], capture_output=True
    )
    if result.returncode != 0:
        print("Unable to read invalid entry in RSL")
        sys.exit(1)
    bad_entry = result.stdout.decode("utf-8").strip()

    result = subprocess.run(
        ["gittuf", "rsl", "annotate", "--skip", "-m", "No yolo!", bad_entry]
    )
    if result.returncode != 0:
        print("Unable to revoke bad RSL entry")
        sys.exit(1)

    result = subprocess.run(["git", "revert", "-S", "--no-edit", "HEAD"])
    if result.returncode != 0:
        print("Unable to revert bad commit")
        sys.exit(1)

    result = subprocess.run(["gittuf", "rsl", "record", "main"])
    if result.returncode != 0:
        print("Unable to create fix RSL entry")
        sys.exit(1)

    result = subprocess.run(["gittuf", "verify-ref", "main", "--verbose"])
    if result.returncode != 0:
        print("Verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

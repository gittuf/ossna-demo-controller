#!/usr/bin/env python

import click
import os
import pathlib
import subprocess
import sys


@click.command()
@click.option("--location", required=True, help="Location to create demo repository")
def main(location):
    os.environ["GITTUF_DEV"] = "1"

    with open("verify-workflow.yml") as fp:
        workflow = fp.read()

    current_dir = os.getcwd()

    keys_dir = os.path.join(current_dir, "keys")

    if os.path.exists(location):
        print("Target location exists")
        sys.exit(1)

    os.mkdir(location)
    os.chdir(location)

    result = subprocess.run(["git", "init", "-b", "main"])
    if result.returncode != 0:
        print("Unable to create Git repository in specified location")
        sys.exit(1)

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

    result = subprocess.run(
        ["gittuf", "trust", "init", "-k", f"{os.path.join(keys_dir, 'root')}"]
    )
    if result.returncode != 0:
        print("Unable to initialize gittuf root of trust")
        sys.exit(1)

    result = subprocess.run(
        [
            "gittuf",
            "trust",
            "add-policy-key",
            "-k",
            f"{os.path.join(keys_dir, 'root')}",
            "--policy-key",
            f"{os.path.join(keys_dir, 'targets.pub')}",
        ]
    )
    if result.returncode != 0:
        print("Unable to add policy key to gittuf root of trust")
        sys.exit(1)

    result = subprocess.run(
        ["gittuf", "policy", "init", "-k", f"{os.path.join(keys_dir, 'targets')}"]
    )
    if result.returncode != 0:
        print("Unable to initialize gittuf policy")
        sys.exit(1)

    result = subprocess.run(
        [
            "gittuf",
            "policy",
            "add-rule",
            "-k",
            f"{os.path.join(keys_dir, 'targets')}",
            "--rule-name",
            "protect-main-branch",
            "--rule-pattern",
            "git:refs/heads/main",
            "--authorize-key",
            f"{os.path.join(keys_dir, 'ossna-1.pem')}",
            "--authorize-key",
            f"{os.path.join(keys_dir, 'ossna-2.pem')}",
            "--threshold",
            "2",
        ]
    )
    if result.returncode != 0:
        print("Unable to add main branch protection rule")
        sys.exit(1)

    result = subprocess.run(["git", "checkout", "-b", "feature"])
    if result.returncode != 0:
        print("Unable to checkout feature branch")
        sys.exit(1)

    with open("README.md", "w+") as fp:
        fp.write("Hello, open source summit!\n")

    pathlib.Path(".github/workflows").mkdir(parents=True, exist_ok=True)
    with open(".github/workflows/verify.yml", "w+") as fp:
        fp.write(workflow)

    subprocess.run(["git", "add", "README.md"])
    subprocess.run(["git", "add", ".github"])
    result = subprocess.run(["git", "commit", "-S", "-m", "Initial commit"])
    if result.returncode != 0:
        print("Unable to create initial commit")
        sys.exit(1)

    result = subprocess.run(["gittuf", "rsl", "record", "feature"])
    if result.returncode != 0:
        print("Unable to create RSL entry")
        sys.exit(1)

    result = subprocess.run(
        [
            "gittuf",
            "dev",
            "authorize",
            "--from-ref",
            "refs/heads/feature",
            "--signing-key",
            f"{os.path.join(keys_dir, 'ossna-2')}",
            "refs/heads/main",
        ]
    )
    if result.returncode != 0:
        print("Unable to approve merging feature into main")
        sys.exit(1)

    result = subprocess.run(["git", "checkout", "-b", "main"])
    if result.returncode != 0:
        print("Unable to checkout main branch")
        sys.exit(1)

    result = subprocess.run(["gittuf", "rsl", "record", "main"])
    if result.returncode != 0:
        print("Unable to create RSL entry")
        sys.exit(1)

    result = subprocess.run(["gittuf", "verify-ref", "main", "--verbose"])
    if result.returncode != 0:
        print("gittuf verification failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
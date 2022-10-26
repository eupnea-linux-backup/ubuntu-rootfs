#!/usr/bin/env python3
import argparse
import os

from functions import *


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", dest="ubuntu_version", type=float, nargs=1, help="Set Ubuntu version to boostrap")
    return parser.parse_args()


if __name__ == "__main__":
    set_verbose(True)
    args = process_args()
    ubuntu_version = args.ubuntu_version[0]

    versions_codenames = {
        18.04: "bionic",
        20.04: "focal",
        22.04: "jammy",
        22.10: "kinetic"
    }

    print_status("Making directory")
    mkdir(f"/tmp/{ubuntu_version}")

    print_status(f"Bootstrapping Ubuntu version {ubuntu_version}")
    bash(f"debootstrap --components=main,restricted,universe,multiverse {versions_codenames[ubuntu_version]} "
         f"/tmp/{ubuntu_version} http://archive.ubuntu.com/ubuntu")

    print_status("Compressing rootfs")
    os.chdir(f"/tmp/{ubuntu_version}")
    bash(f"tar -cv -I 'xz -9 -T0' -f ../ubuntu-rootfs-{ubuntu_version}.tar.xz ./")

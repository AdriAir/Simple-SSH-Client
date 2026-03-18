#!/usr/bin/env python3
import subprocess
import sys
from profiles_menu import load_profiles, pick_profile


def ssh_connect(profile):
    cmd = ["ssh", "-p", str(profile["port"])]
    if profile.get("private_key"):
        cmd += ["-i", profile["private_key"]]
    cmd.append(f"{profile['user']}@{profile['host']}")
    print(f"  > {' '.join(cmd)}\n")
    subprocess.run(cmd)


if __name__ == "__main__":
    profiles = load_profiles()
    if not profiles:
        print("  No hay perfiles en profiles.json")
        sys.exit(1)

    while True:
        profile = pick_profile(profiles)
        if profile is None:
            break
        ssh_connect(profile)
        print()  # linea en blanco antes de volver al menu

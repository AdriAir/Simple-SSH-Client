#!/usr/bin/env python3
import subprocess
import sys
from profiles_menu import load_profiles, pick_profile


def scp_transfer(profile, origin, dest):
    user_host = f"{profile['usuario']}@{profile['host']}"
    if ":" not in origin and ":" not in dest:
        dest = f"{user_host}:{dest}"
    else:
        if origin.startswith(":"):
            origin = f"{user_host}{origin}"
        if dest.startswith(":"):
            dest = f"{user_host}{dest}"

    cmd = ["scp", "-P", str(profile["puerto"]), origin, dest]
    print(f"  > {' '.join(cmd)}\n")
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("  Uso: python scp.py <pathOrigen> <pathDestino>")
        print()
        print("  Paths locales se escriben normal:  ./archivo.txt")
        print("  Paths remotos empiezan con ':' :   :/ruta/remota/")
        print("  Si ninguno lleva ':', el destino se trata como remoto.")
        print()
        print("  Ejemplos:")
        print("    python scp.py ./local.txt :/home/user/remote.txt")
        print("    python scp.py :/var/log/app.log ./logs/")
        print("    python scp.py ./deploy.sh /opt/scripts/")
        sys.exit(1)

    origin = sys.argv[1]
    dest = sys.argv[2]

    profiles = load_profiles()
    if not profiles:
        print("  No hay perfiles en profiles.json")
        sys.exit(1)
    profile = pick_profile(profiles)
    scp_transfer(profile, origin, dest)

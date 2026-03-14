#!/usr/bin/env python3
"""Selector interactivo de perfiles SSH con flechas de teclado."""
import json
import sys
import os

PROFILES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "profiles/profiles.json")

# --- Lectura de teclas multiplataforma ---

if os.name == "nt":
    import msvcrt

    def read_key():
        key = msvcrt.getch()
        if key in (b"\x00", b"\xe0"):  # tecla especial (flechas, etc.)
            key = msvcrt.getch()
            if key == b"H":
                return "up"
            if key == b"P":
                return "down"
            return None
        if key in (b"\r", b"\n"):
            return "enter"
        if key == b"\x1b":
            return "esc"
        if key in (b"q", b"Q"):
            return "quit"
        return None
else:
    import tty
    import termios

    def read_key():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == "\x1b":
                seq = sys.stdin.read(2)
                if seq == "[A":
                    return "up"
                if seq == "[B":
                    return "down"
                return "esc"
            if ch in ("\r", "\n"):
                return "enter"
            if ch in ("q", "Q"):
                return "quit"
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return None

# --- Funciones de perfiles ---

def load_profiles():
    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def format_profile(p):
    return f"{p['nombre']}  —  {p['usuario']}@{p['host']}:{p['puerto']}"


def pick_profile(profiles):
    selected = 0
    total = len(profiles)
    # lineas totales: 1 titulo + 1 vacia + total perfiles + 1 vacia + 1 leyenda = total + 4
    lines = total + 4

    sys.stdout.write("\033[?25l")  # ocultar cursor
    sys.stdout.flush()

    def render():
        if render.drawn:
            # Subir al inicio del bloque
            sys.stdout.write(f"\033[{lines}A")
        # Titulo + linea vacia
        sys.stdout.write("\033[2K  Perfiles SSH disponibles:\n")
        sys.stdout.write("\033[2K\n")
        # Perfiles
        for i, p in enumerate(profiles):
            sys.stdout.write("\033[2K")  # limpiar linea entera
            if i == selected:
                sys.stdout.write(f"  \033[7m > {format_profile(p)} \033[0m\n")
            else:
                sys.stdout.write(f"    {format_profile(p)}\n")
        # Leyenda de controles
        sys.stdout.write("\033[2K\n")
        sys.stdout.write("\033[2K  \033[2m[↑↓] Mover   [Enter] Conectar   [Q] Salir\033[0m\n")
        sys.stdout.flush()
        render.drawn = True

    render.drawn = False

    def cleanup(extra=""):
        sys.stdout.write(f"\033[?25h{extra}")
        sys.stdout.flush()

    try:
        render()
        while True:
            key = read_key()
            if key == "up" and selected > 0:
                selected -= 1
                render()
            elif key == "down" and selected < total - 1:
                selected += 1
                render()
            elif key == "enter":
                break
            elif key in ("esc", "quit"):
                cleanup("\n")
                return None
    except (KeyboardInterrupt, EOFError):
        cleanup("\n")
        sys.exit(0)

    cleanup("\n")
    return profiles[selected]

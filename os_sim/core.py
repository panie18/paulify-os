import os
import time
from .commands import handle_command, handle_music_commands, handle_recovery


def intro_tour():
    cat = r"""
        |\---/|
        | o_o |
         \_^_/
    Hi, ich bin Kitty, dein Guide! 🐱

    Ich zeige dir kurz, was du hier tun kannst:
    - 'help' für alle Befehle
    - 'tictactoe' zum Spielen
    - 'fortune', 'cow', 'guess' für Spaß
    - 'play', 'pause', 'stop' für Musik
    - 'login', 'resetpass' für Benutzerkonten
    - 'calc', 'translate', 'define', 'learn' zum Lernen
    - 'todo', 'notes' und 'calendar' für Alltag
    - 'shutdown' und 'log' für System
    - und vieles mehr!

    Viel Spaß mit Paulify OS 😺
    """
    print(cat)


def run_shell():
    cwd = "/"
    history = []
    user = {"name": "guest", "root": False}
    start_time = time.time()
    print("Welcome to Paulify OS!")
    intro_tour()
    while True:
        try:
            cmd = input(f"{user['name']}:{cwd}$ ").strip()
            if not cmd:
                continue
            if cmd == "exit":
                break
            history.append(cmd)

            output = handle_music_commands(cmd)
            if output: print(output); continue
            output = handle_recovery(cmd, user)
            if output: print(output); continue
            output = handle_command(cmd, cwd, history, user, start_time)
            if output: print(output)
            continue
                print(output)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")

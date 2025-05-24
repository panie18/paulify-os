import os
import time
import random

VIRTUAL_FILES = {"/hello.txt": "Welcome to Paulify OS!"}
USERS = {"guest": {"password": "", "root": False}, "root": {"password": "toor", "root": True}}
TRASH = {}
LANG = "en"

I18N = {
    "en": {"hello": "Welcome to Paulify OS!", "invalid": "Invalid command.", "deleted": "File moved to trash.", "restored": "File restored.", "notrash": "No such file in trash.", "trash_empty": "Trash is empty."},
    "de": {"hello": "Willkommen bei Paulify OS!", "invalid": "Ungültiger Befehl.", "deleted": "Datei in Papierkorb verschoben.", "restored": "Datei wiederhergestellt.", "notrash": "Keine solche Datei im Papierkorb.", "trash_empty": "Papierkorb ist leer."}
}

FORTUNES = [
    "You will write bug-free code... someday.",
    "Keep calm and code Python.",
    "Beware of infinite loops.",
    "Did you try turning it off and on again?",
    "SyntaxError: Unexpected wisdom."
]

COW_TEMPLATE = r"""
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||
{msg}
"""

TICTAC_BOARD = [" "] * 9

def draw_board():
    return f"""
 {TICTAC_BOARD[0]} | {TICTAC_BOARD[1]} | {TICTAC_BOARD[2]}
---+---+---
 {TICTAC_BOARD[3]} | {TICTAC_BOARD[4]} | {TICTAC_BOARD[5]}
---+---+---
 {TICTAC_BOARD[6]} | {TICTAC_BOARD[7]} | {TICTAC_BOARD[8]}
"""

def check_win(player):
    wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    return any(all(TICTAC_BOARD[i] == player for i in combo) for combo in wins)

def tictac_move(pos, player):
    if TICTAC_BOARD[pos] != " ":
        return "Position already taken."
    TICTAC_BOARD[pos] = player
    return None

def translate(key):
    return I18N.get(LANG, I18N["en"]).get(key, key)

def handle_fun_commands(cmd):
    parts = cmd.split()
    base = parts[0]

    if base == "cow":
        msg = " ".join(parts[1:]) if len(parts) > 1 else "Moo!"
        return COW_TEMPLATE.format(msg=msg)
    elif base == "fortune":
        return random.choice(FORTUNES)
    elif base == "hack":
        return "\n".join(["[*] Accessing mainframe...", "[*] Bypassing firewall...", "[*] Injecting shellcode...", "[*] Root access granted. 😈", "Just kidding. You're still in Paulify OS."])
    elif base == "tictactoe":
        if len(parts) == 1:
            return draw_board() + "\nUse: tictactoe MOVE (0-8)"
        try:
            move = int(parts[1])
            if move < 0 or move > 8:
                return "Invalid move (0–8)."
            err = tictac_move(move, "X")
            if err: return err
            if check_win("X"): return draw_board() + "\nYou win!"
            for i in range(9):
                if TICTAC_BOARD[i] == " ":
                    TICTAC_BOARD[i] = "O"
                    break
            if check_win("O"): return draw_board() + "\nBot wins!"
            return draw_board()
        except:
            return "Usage: tictactoe MOVE (0-8)"
    return None

def handle_extra_commands(cmd):
    parts = cmd.split()
    base = parts[0]

    global LANG
    if base == "lang":
        if len(parts) < 2: return "Usage: lang [en|de]"
        if parts[1] in I18N:
            LANG = parts[1]
            return f"Language set to {parts[1]}"
        else:
            return "Unsupported language"
    elif base == "calc":
        try:
            expr = " ".join(parts[1:])
            return str(eval(expr, {}, {}))
        except:
            return "Calculation error."
    elif base == "trash":
        if not TRASH: return translate("trash_empty")
        return "\n".join(TRASH.keys())
    elif base == "restore":
        if len(parts) < 2: return "Usage: restore FILE"
        for path in list(TRASH):
            if path.endswith(parts[1]):
                VIRTUAL_FILES[path] = TRASH.pop(path)
                return translate("restored")
        return translate("notrash")
    elif base == "guess":
        target = random.randint(1, 10)
        guess = input("Guess a number (1-10): ")
        try:
            guess = int(guess)
            if guess == target:
                return "Correct!"
            else:
                return f"Wrong. It was {target}."
        except:
            return "Invalid input."
    return None

def handle_command(cmd, cwd, history, user, start_time):
    fun_result = handle_fun_commands(cmd)
    if fun_result: return fun_result
    extra = handle_extra_commands(cmd)
    if extra: return extra

    parts = cmd.split()
    base = parts[0]

    if base == "echo":
        return " ".join(parts[1:])
    elif base == "cat":
        if len(parts) < 2: return "Usage: cat FILE"
        path = os.path.join(cwd, parts[1])
        return VIRTUAL_FILES.get(path, "No such file")
    elif base == "touch":
        if len(parts) < 2: return "Usage: touch FILE"
        path = os.path.join(cwd, parts[1])
        VIRTUAL_FILES[path] = ""
        return f"{parts[1]} created."
    elif base == "rm":
        if len(parts) < 2: return "Usage: rm FILE"
        path = os.path.join(cwd, parts[1]).replace("\\", "/")
        if path in VIRTUAL_FILES:
            TRASH[path] = VIRTUAL_FILES.pop(path)
            return translate("deleted")
        return "No such file"
    elif base == "help":
        return "Commands: echo, cat, touch, rm, fortune, cow, hack, tictactoe, trash, restore, guess, calc, lang"
    else:
        return translate("invalid")

import getpass

PASSWORDS = {"guest": "", "root": "toor"}

def handle_music_commands(cmd):
    parts = cmd.split()
    if parts[0] == "play":
        if len(parts) < 2:
            return "Usage: play SONG_NAME"
        return f"🎵 Now playing: {' '.join(parts[1:])} (simulated)"
    elif parts[0] == "pause":
        return "⏸️ Music paused (simulated)"
    elif parts[0] == "stop":
        return "⏹️ Music stopped (simulated)"
    return None

def handle_recovery(cmd, user):
    parts = cmd.split()
    if parts[0] == "resetpass":
        if not user.get("root"):
            return "Only root can reset passwords."
        if len(parts) < 3:
            return "Usage: resetpass USER NEWPASSWORD"
        target = parts[1]
        newpass = parts[2]
        if target in USERS:
            USERS[target]["password"] = newpass
            return f"Password for {target} reset."
        return "No such user."
    elif parts[0] == "login":
        if len(parts) < 2:
            return "Usage: login USER"
        uname = parts[1]
        if uname not in USERS:
            return "No such user."
        password = getpass.getpass("Password: ")
        if password == USERS[uname]["password"]:
            user["name"] = uname
            user["root"] = USERS[uname]["root"]
            return f"Logged in as {uname}"
        return "Incorrect password."
    return None


def handle_command(cmd, cwd, history, user, start_time):
    fun_result = handle_fun_commands(cmd)
    if fun_result: return fun_result
    extra = handle_extra_commands(cmd)
    if extra: return extra
    misc = {
        "define": "Definition: A simulated definition.",
        "translate": "Übersetzung: Translation.",
        "fetch": f"System: Paulify OS\nUser: {user['name']}",
        "calendar": "📅 Calendar: Today is a good day.",
        "todo": "You have 3 tasks. All pending.",
        "notes": "Note 1: Build Paulify OS!",
        "passwd": "Password changed (simulated).",
        "shutdown": "System is shutting down (simulated).",
        "asciiart": "(\__/)
( •_•)
/ >🌯 ASCII bunny!",
        "quiz": "Q: What is 2+2? A: 4",
        "learn": "Lesson: Python uses indentation.",
        "history": "\n".join(history),
        "uptime": f"Uptime: {round(time.time() - start_time)} seconds",
        "whoami": f"You are {user['name']}"
    }
    if cmd in misc:
        return misc[cmd]
    parts = cmd.split()
    if parts and parts[0] in misc:
        return misc[parts[0]]
    return translate("invalid")

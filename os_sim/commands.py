import os

def get_prompt(cwd):
    return f"user@paulify:{cwd}$ "

VIRTUAL_FS = {'/': []}

def handle_command(cmd, cwd):
    parts = cmd.split()
    base = parts[0]

    if base == "help":
        return "\n".join([
            "Available commands:",
            "  help      - Show this help message",
            "  ls        - List directory",
            "  cd DIR    - Change directory",
            "  mkdir DIR - Make directory",
            "  echo TEXT - Print text",
            "  clear     - Clear screen",
            "  exit      - Exit shell"
        ])

    elif base == "ls":
        return "\n".join(VIRTUAL_FS.get(cwd, [])) or "(empty)"

    elif base == "mkdir":
        if len(parts) < 2:
            return "Usage: mkdir DIR"
        new_dir = parts[1]
        path = os.path.join(cwd, new_dir).replace("\\", "/")
        if path in VIRTUAL_FS:
            return f"Directory already exists: {new_dir}"
        VIRTUAL_FS[path] = []
        VIRTUAL_FS[cwd].append(new_dir)
        return f"Created directory: {new_dir}"

    elif base == "cd":
        if len(parts) < 2:
            return "Usage: cd DIR"
        dest = parts[1]
        new_path = os.path.normpath(os.path.join(cwd, dest)).replace("\\", "/")
        if new_path not in VIRTUAL_FS:
            return f"No such directory: {dest}"
        return (new_path, None)

    elif base == "echo":
        return " ".join(parts[1:])

    elif base == "clear":
        os.system("cls" if os.name == "nt" else "clear")
        return ""

    elif base == "exit":
        print("Goodbye.")
        exit(0)

    else:
        return f"Unknown command: {base}"

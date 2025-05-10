import os
from os_sim.commands import handle_command, get_prompt

def run_shell():
    print("Paulify OS Simulation Shell v1.1")
    print("Type 'help' to see available commands. Type 'exit' to quit.\n")

    cwd = "/"
    while True:
        try:
            cmd = input(get_prompt(cwd))
            if not cmd.strip():
                continue
            result = handle_command(cmd.strip(), cwd)
            if isinstance(result, tuple):
                cwd, output = result
                if output:
                    print(output)
            else:
                print(result)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting Paulify OS.")
            break

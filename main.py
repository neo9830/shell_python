import sys
import os
import subprocess

def locate_executable(command):
    path = os.environ.get("PATH", "")

    for directory in path.split(":"):
        file_path = os.path.join(directory, command)

        if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return file_path



def main():
    #Initalizing the valid commands list as empty
    valid_commands = ["exit", "echo", "type", "pwd", "cd"]
    PATH = os.environ.get("PATH")
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_command = input()
        if user_command.startswith("exit"):
            break
        elif user_command.startswith("echo"):
            print(user_command[len("echo "):])
            continue
        elif user_command.startswith("type"):
            command_to_check = user_command[len("type "):]
            command_path = None
            paths = PATH.split(":")
            for path in paths:
                if os.path.isfile(f"{path}/{command_to_check}"):
                    command_path = f"{path}/{command_to_check}"
            if command_to_check in valid_commands:
                print(f"{command_to_check} is a shell builtin")
                continue
            elif command_path:
                print(f"{command_to_check} is {command_path}")
                continue
            else:
                print(f"{command_to_check}: not found")
                continue
        elif user_command == "pwd":
            print(os.getcwd())
            continue
        #CD command for absolute paths
        elif user_command.startswith("cd "):
            target_path = user_command[len("cd "):].strip()

            #Handle '~' for the home directory
            if target_path == "~" or target_path.startswith("~/"):
                home_dir = os.environ.get("HOME",os.path.expanduser("~"))
                target_path = os.path.join(home_dir, target_path[2:]) if target_path.startswith("~/") else home_dir
            target_path = os.path.abspath(os.path.join(os.getcwd(), target_path))

            #Check if the path is absolute
            #if not target_path.startswith("/"):
                #Converting relative path to absolute path
                #target path can be ./ or ../, this abspath removes the . and .. it combines path into canonical form
                #target_path = os.path.abspath(os.path.join(os.getcwd(), target_path))
                #print(f"cd: {target_path}: only absolute paths are supported in this stage")

            # Change directory
            if os.path.exists(target_path) and os.path.isdir(target_path): #verifies that the specfied path exists ins filesystem and also if the existing path is a directory
                try:
                    os.chdir(target_path)
                except Exception as e:
                    print(f"cd: {target_path}: {e}")
            else:
                print(f"cd: {target_path}: No such file or directory")
            continue

        command_parts = user_command.split()
        if not command_parts:
            continue
        command = command_parts[0]
        args = command_parts[1:]
        executable = locate_executable(command)
        if executable:
            try:
                result = subprocess.run([executable, *args], capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
                if result.stderr:
                    print(result.stderr, end="")
            except Exception as e:
                print(f"Error executing command: {e}")
            continue
            
        if user_command not in valid_commands:
            print(f"{user_command}: command not found")
            continue
        

if __name__ == "__main__":
    main()

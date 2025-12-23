import os
import subprocess

def list_conda_envs():
    """Return a list of conda environments by calling 'conda env list'."""
    result = subprocess.run(["conda", "env", "list"], capture_output=True, text=True)
    envs = []
    for line in result.stdout.splitlines():
        if line.strip() and not line.startswith("#"):
            parts = line.split()
            envs.append(parts[0])  # environment name
    return envs

def list_folders(drive):
    """List all folders in the root of the chosen drive."""
    path = f"{drive}:\\"
    try:
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return folders
    except Exception as e:
        print(f"Error accessing {path}: {e}")
        return []

def go_to_env():
    # Step 1: Ask for drive
    drive = input("Which drive do you want to go to? (C/D/E): ").upper()
    if drive not in ["C", "D", "E"]:
        print("Invalid drive choice.")
        return

    # Step 2: Show folders in that drive
    folders = list_folders(drive)
    print(f"\nFolders in {drive}:\\")
    for i, f in enumerate(folders, 1):
        print(f"{i}. {f}")

    # Step 3: Ask which folder
    folder_choice = input("\nEnter folder name (or leave blank for root): ").strip()
    full_path = f"{drive}:\\{folder_choice}" if folder_choice else f"{drive}:\\"

    # Step 4: Show available environments
    envs = list_conda_envs()
    print("\nAvailable Conda environments:")
    for i, env in enumerate(envs, 1):
        print(f"{i}. {env}")

    # Step 5: Ask which env to activate
    choice = input("Enter environment name to activate: ").strip()
    if choice not in envs:
        print("Invalid environment name.")
        return

    # Step 6: Launch new terminal in that folder with env activated
    subprocess.run([
        "cmd", "/K",
        f"cd /d {full_path} && conda activate {choice}"
    ])

if __name__ == "__main__":
    go_to_env()
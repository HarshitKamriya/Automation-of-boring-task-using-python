import os
import shutil
import subprocess

def list_folders(drive):
    """List all folders in the root of the chosen drive."""
    path = f"{drive}:\\"
    try:
        folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
        return folders
    except Exception as e:
        print(f"Error accessing {path}: {e}")
        return []

def choose_paths():
    # Step 1: Ask for drive
    drive = input("Which drive do you want to go to? (C/D/E): ").upper()
    if drive not in ["C", "D", "E"]:
        print("Invalid drive choice.")
        return None, None

    # Step 2: Show folders in that drive
    folders = list_folders(drive)
    print(f"\nFolders in {drive}:\\")
    for i, f in enumerate(folders, 1):
        print(f"{i}. {f}")

    # Step 3: Ask which folder
    source_folder = input("\nEnter source folder name (or leave blank for root): ").strip()
    source_full_path = f"{drive}:\\{source_folder}" if source_folder else f"{drive}:\\"

    return source_full_path, drive

def is_git_repo(path):
    """Check if a folder is a Git repo using subprocess."""
    try:
        subprocess.run(
            ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False

def remove_git_dirs():
    source_folder, drive = choose_paths()
    if not source_folder:
        return

    print(f"\nScanning recursively for Git repositories inside: {source_folder}\n")

    removed = []
    for root, dirs, files in os.walk(source_folder):
        if '.git' in dirs:
            git_path = os.path.join(root, '.git')
            if is_git_repo(root):  # safer check
                try:
                    shutil.rmtree(git_path)
                    removed.append(git_path)
                    print(f"Removed Git repo: {git_path}")
                    dirs.remove('.git')  # prevent descending into deleted folder
                except Exception as e:
                    print(f"Error removing {git_path}: {e}")

    if removed:
        print("\n✅ Cleanup complete. Removed the following Git repos:")
        for path in removed:
            print(f" - {path}")
    else:
        print("\nNo Git repos found in the selected path.")

if __name__ == "__main__":
    remove_git_dirs()
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
    


def seperate_pdf():
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
    source_folder = input("\nEnter source folder name (or leave blank for root): ").strip()
    destination_folder = input("\nEnter destination folder name (or leave blank for root): ").strip()

    source_full_path = f"{drive}:\\{source_folder}" if source_folder else f"{drive}:\\"
    destination_full_path = f"{drive}:\\{destination_folder}" if destination_folder else f"{drive}:\\"
    return source_full_path,destination_full_path


def separate_pdfs():
    # Create destination folder if it doesn't exist
    source_folder,destination_folder = seperate_pdf()
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Walk through all subfolders
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            if file_name.lower().endswith(".pdf"):
                source_path = os.path.join(root, file_name)
                destination_path = os.path.join(destination_folder, file_name)

                shutil.copy2(source_path, destination_path)
                print(f"Copied: {source_path} -> {destination_path}")

    print(" All PDFs have been separated!")

if __name__ == "__main__":

    separate_pdfs()
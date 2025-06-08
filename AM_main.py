# MIT License
#
# Copyright (c) 2024 Filip Pawłowski(kotlecikmud)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
import threading
import subprocess
from colorama import Fore, Style
from tqdm import tqdm

__version__ = "01.02.00.00"  # code untested ! beyond com port seeker


# --- ampy wrapper ---
def run_ampy_command(
    com_port: str,
    ampy_args: list[str],
    capture_output: bool = True,
    check_errors: bool = True,
) -> tuple[bool, str, str]:
    cmd = ["ampy", "-p", "COM" + com_port] + ampy_args
    try:
        # Universal newlines handles different line endings, text=True decodes output
        process = subprocess.run(
            cmd, text=True, capture_output=capture_output, check=False
        )

        if check_errors and process.returncode != 0:
            print(f"{Fore.RED}Ampy command failed: {' '.join(cmd)}{Style.RESET_ALL}")
            if process.stderr:
                print(f"{Fore.RED}Error: {process.stderr.strip()}{Style.RESET_ALL}")
            return (
                False,
                process.stdout.strip() if process.stdout else "",
                process.stderr.strip() if process.stderr else "",
            )

        return (
            True,
            process.stdout.strip() if process.stdout else "",
            process.stderr.strip() if process.stderr else "",
        )
    except FileNotFoundError:
        print(
            f"{Fore.RED}Error: 'ampy' command not found. Make sure it is installed and in your PATH.{Style.RESET_ALL}"
        )
        return False, "", ""
    except Exception as e:
        print(
            f"{Fore.RED}An unexpected error occurred with ampy command {' '.join(cmd)}: {e}{Style.RESET_ALL}"
        )
        return False, "", ""


# --- Helper Functions ---
SEPARATOR = "-" * 30
INPUT_SIGN = ">>>"
ROOT_DIR = "/"
HELP_DOC = f"""
--- ABOUT ---

Script Name:    AM_main.py
Version:        {__version__}
Author:         Filip Pawłowski
Contact:        filippawlowski2012@gmail.com

--- DESCRIPTION ---

The `ampy_manager.py` script is a utility for managing files on any ampy compatibile device such as:
Raspberry Pi, ESP8266 or ESP32 device using 'ampy' (Adafruit MicroPython tool).
It provides various options to display file content, upload and download files, delete files, and more.

--- MAIN OPTIONS ---

1. **Display File Content:**
    - Display the content of a file on the device.
    - Usage: Select option 1 -> Enter destination path of the file on the device.

2. **Upload Single File:**
    - Upload a single file to the device.
    - Usage: Select option 2 -> Enter source path for the local file -> Enter destination path on the device.

3. **Upload Multiple Files:**
    - Upload multiple files from a local directory to the device.
    - Usage: Select option 3 -> Enter the source directory path for the files.

4. **Download Single File:**
    - Download a single file from the device to the local machine.
    - Usage: Select option 4 -> Enter the path of the file on the device -> Enter the target directory for the
      downloaded file.

5. **Download Multiple Files:**
    - Download multiple files from the device to a local directory.
    - Usage: Select option 5 -> Enter the remote file paths to download (separated by comma) -> Enter the local
      directory to save downloaded files.

6. **Delete Single File:**
    - Delete a single file from the device.
    - Usage: Select option 6 -> Enter the file name to delete from the device.

7. **Delete Files by Extension:**
    - Delete all files with a specific extension from the device.
    - Usage: Select option 7 -> Enter the file extension to delete (e.g., txt, py).

8. **Delete Everything:**
    - Delete all files from the device.

9. **Rescan COM Ports:**
    - Rescan available COM ports to select a different one.

10. **Exit:**
    - Exit the script.

11. **Help:**
    - Display the help documentation.
    - Usage: Type 'help' when prompted for an option.

--- CONTACT ---

For any queries or assistance, please contact the author:
Author: Filip Pawłowski
Contact: filippawlowski2012@gmail.com

"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_file_content(selected_com, selected_file):
    print("Fetching file content...")
    success, output, error = run_ampy_command(
        selected_com, ["get", selected_file], capture_output=True
    )
    if success:
        if (
            output
        ):  # ampy get stdout can be empty if file is empty or an error occurred that ampy didn't report via exit code
            print(SEPARATOR)
            print(output)  # This is the file content
            print(SEPARATOR)
            print("File content displayed.")
        elif (
            error
        ):  # Sometimes ampy 'get' writes to stderr on success (e.g. "Couldn't access '/nonexistentfile'") but still exits 0
            print(
                f"{Fore.YELLOW}Could not retrieve file. Ampy reported: {error}{Style.RESET_ALL}"
            )
        else:  # Success but no output and no error, could be an empty file
            print(SEPARATOR)
            print("(File is empty or no content to display)")
            print(SEPARATOR)
            print("File content displayed (possibly empty).")

    else:
        print(f"{Fore.RED}Failed to display file content.{Style.RESET_ALL}")


def upload_single(com_port, local_file, remote_file):
    print(f"Uploading {local_file} to {remote_file}...")
    success, _, _ = run_ampy_command(
        com_port, ["put", local_file, remote_file], capture_output=False
    )  # Output not usually needed for put
    return success


def upload_from_dir(selected_com, local_dir_id):
    if not os.path.exists(local_dir_id):
        print("Source directory does not exist.")
    else:
        # Get a list of files in the local directory
        files_to_upload = [
            f
            for f in os.listdir(local_dir_id)
            if os.path.isfile(os.path.join(local_dir_id, f))
        ]

        if not files_to_upload:
            print("No files found in the source directory.")

        else:
            for file_name in tqdm(files_to_upload, desc="Uploading files", unit="file"):
                local_file = os.path.join(local_dir_id, file_name)
                remote_file = ROOT_DIR + file_name  # Upload to root directory
                if upload_single(
                    selected_com, local_file, remote_file
                ):  # selected_com is now a parameter
                    # Tqdm will show progress, specific print might be too verbose
                    pass  # print(f"Successfully uploaded {file_name}")
                else:
                    # Error is printed by run_ampy_command, tqdm will continue
                    print(f"{Fore.RED}Failed to upload {file_name}{Style.RESET_ALL}")


def download_single(com_port, remote_file, local_file):
    print(f"Downloading {remote_file} to {local_file}...")
    success, file_content, error_message = run_ampy_command(
        com_port, ["get", remote_file], capture_output=True
    )
    if success:
        if file_content is not None:  # Ensure content is not None before writing
            try:
                with open(local_file, "w") as f:  # ampy get usually returns text
                    f.write(file_content)
                # Success message handled by caller or in main loop
            except IOError as e:
                print(
                    f"{Fore.RED}Error writing downloaded file {local_file}: {e}{Style.RESET_ALL}"
                )
                success = False  # Mark as failed if file write fails
        # If ampy get "succeeds" (exit 0) but gives error (e.g. file not found), file_content might be empty and error_message populated
        elif error_message:
            print(
                f"{Fore.YELLOW}Could not retrieve file for download. Ampy reported: {error_message}{Style.RESET_ALL}"
            )
            success = False  # Mark as failed
        else:  # No content and no error_message, could be an empty file
            try:
                with open(local_file, "w") as f:  # Create empty file
                    f.write("")
            except IOError as e:
                print(
                    f"{Fore.RED}Error writing empty downloaded file {local_file}: {e}{Style.RESET_ALL}"
                )
                success = False
    return success  # Return success status


def download_multiple(selected_com, remote_files_id, local_dir_id):
    if not os.path.exists(local_dir_id):
        os.makedirs(local_dir_id)

    remote_file_list = [f.strip() for f in remote_files_id.split(",")]

    for remote_file in tqdm(remote_file_list, desc="Downloading files", unit="file"):
        local_file_path = os.path.join(local_dir_id, os.path.basename(remote_file))
        # The print inside download_single is already quite informative
        if download_single(
            selected_com, remote_file, local_file_path
        ):  # selected_com is now a parameter
            # tqdm shows progress, specific print might be too verbose here
            pass  # print(f"Successfully downloaded {os.path.basename(remote_file)} to {local_file_path}")
        else:
            # Error is printed by run_ampy_command or download_single's file write error
            print(
                f"{Fore.RED}Failed to download {os.path.basename(remote_file)}{Style.RESET_ALL}"
            )


def delete_by_extension(selected_com, extension_to_delete):
    confirm = input(
        f"Are you sure you want to delete all '{extension_to_delete}' files from the device? (y/n): "
    )

    if confirm.lower() == "y":
        success_ls, files_output, _ = run_ampy_command(
            selected_com, ["ls"], capture_output=True
        )
        if not success_ls:
            print(f"{Fore.RED}Could not list files for deletion.{Style.RESET_ALL}")
            return  # Exit function

        files = [line.strip() for line in files_output.splitlines() if line.strip()]
        if not files:
            print("No files found on device.")
            return

        deleted_count = 0
        for file_name in files:
            if file_name.endswith(extension_to_delete):
                print(f"Attempting to delete: {file_name}...")
                # For 'rm', we don't need to capture output unless debugging.
                success_rm, _, _ = run_ampy_command(
                    selected_com, ["rm", file_name], capture_output=False
                )
                if success_rm:
                    print(f"Successfully deleted {file_name}.")
                    deleted_count += 1
                # else: run_ampy_command will print the error

        if deleted_count > 0:
            print(
                f"All '{extension_to_delete}' files processed. {deleted_count} file(s) deleted."
            )
        else:
            print(f"No files with extension '{extension_to_delete}' found to delete.")
    else:
        print(f"Delete '{extension_to_delete}' files operation canceled.")


def delete_everything(selected_com):
    choice_1 = input(f"Do you want to delete all files from the device? (y/n): ")
    choice_2 = input(
        f"{Fore.RED}Are you sure you want to delete ALL files from the device? (double-check) (y/n): {Style.RESET_ALL}"
    )

    if choice_1.lower() == "y" and choice_2.lower() == "y":
        success_ls, files_output, _ = run_ampy_command(
            selected_com, ["ls"], capture_output=True
        )
        if not success_ls:
            print(f"{Fore.RED}Could not list files for deletion.{Style.RESET_ALL}")
            return

        files = [line.strip() for line in files_output.splitlines() if line.strip()]
        if not files:
            print("No files found on device to delete.")
            return

        deleted_count = 0
        for file_name in files:
            print(f"Attempting to delete: {file_name}...")
            success_rm, _, _ = run_ampy_command(
                selected_com, ["rm", file_name], capture_output=False
            )
            if success_rm:
                print(f"Successfully deleted {file_name}.")
                deleted_count += 1
            # else: run_ampy_command will print the error

        if deleted_count > 0:
            print(f"All files processed. {deleted_count} file(s) deleted.")
        elif not files:  # Should be caught earlier
            print("No files found on device.")
        else:
            print(
                "No files were deleted (possibly due to errors during deletion attempts)."
            )
    else:
        print(f"Operation canceled.")


def find_COM():
    clear_screen()
    # print("Waiting for COM port...") # Moved
    # loading_animation.start() # Removed

    while True:
        print("Scanning for COM ports...")
        com_ports = []  # declare/clean port list

        # Find available COM ports
        output = subprocess.check_output("mode", shell=True).decode("utf-8")

        for line in output.splitlines():
            if "COM" in line:
                com_port = line.split("COM")[1].strip()
                if com_port != "1:":  # append every found COM port ignoring COM1
                    com_ports.append(com_port.replace(":", ""))

        if com_ports:  # if found any COM ports except 1:
            # loading_animation.stop() # Removed

            while True:
                clear_screen()

                if not len(com_ports) == 1:
                    print(f"Available COM Ports:\n{', '.join(com_ports)}")
                    com_choice = input(
                        f"Type number or 'r' for 'refresh'.\nEnter your choice: "
                    )

                    if com_choice.isdigit():
                        if com_choice.replace(":", "") in com_ports:
                            print(f"Selected COM Port: {com_choice}")
                            return com_choice

                        else:
                            print("Invalid COM Port. Please try again.")

                    elif com_choice == "r" or com_choice == "refresh":
                        clear_screen()
                        # print("Waiting for COM port...") # Moved to the beginning of the outer loop
                        # loading_animation.start() # Removed
                        break

                    else:
                        print("Invalid choice. Please try again.")

                else:
                    return com_ports[0].replace(":", "")
        else:
            print("No COM ports found. Retrying...")
            time.sleep(1)  # Add a small delay before retrying


def display_content(selected_com):
    print("Storage on device:")
    print("Fetching directory listing...")
    success, output, _ = run_ampy_command(selected_com, ["ls"], capture_output=True)
    if success:
        if output:
            print(output)
        else:
            print("(No files found or directory is empty)")
        print("Directory listing displayed.")
    else:
        print(f"{Fore.RED}Failed to fetch directory listing.{Style.RESET_ALL}")


if __name__ == "__main__":
    selected_com = find_COM()

    # Menu
    while True:
        clear_screen()

        print(
            f"Ampy Manager {Fore.CYAN}{Style.BRIGHT}v{__version__}{Style.RESET_ALL}\nselected port: {Fore.LIGHTRED_EX}{Style.BRIGHT}COM{selected_com}{Style.RESET_ALL}"
        )

        print(SEPARATOR)

        display_content(selected_com)  # Pass selected_com

        print(SEPARATOR)

        options = {
            1: "Display file content",
            2: "Upload single file",
            3: "Upload multiple files",
            4: "Download single file",
            5: "Download multiple files",
            6: "Delete single file",
            7: "Delete by extension",
            8: "Delete everything",
            9: "Rescan COM ports",
            10: "Exit",
        }

        print("Options:")
        for key, value in options.items():
            print(f"{str(key).ljust(2)} {value.ljust(30)}")

        print(SEPARATOR)

        choice = input(f"Choose an option {INPUT_SIGN} ")

        # Display file content
        if choice == "1":
            selected_file_path = input(
                "Enter destination path of the file on the device: "
            ).strip()
            display_file_content(
                selected_com, selected_file_path
            )  # selected_com is global

        # Upload single file
        elif choice == "2":
            local_file_path = input(
                "Enter the source path for the local file: "
            ).strip()
            remote_file_path = input(
                "Enter destination path of the file on the device: "
            ).strip()
            if upload_single(
                selected_com, local_file_path, remote_file_path
            ):  # selected_com is global
                print("File uploaded successfully to the device.")
            else:
                print(
                    "File upload failed."
                )  # More specific error printed by run_ampy_command

        # Upload multiple files
        elif choice == "3":
            local_dir = input("Enter the source directory path for the files: ").strip()
            upload_from_dir(selected_com, local_dir)

        # Download single file
        elif choice == "4":
            remote_file_path = input(
                "Enter the path of the file on the device: "
            ).strip()
            target_dir_path = input(
                "Enter the target directory for the downloaded file: "
            ).strip()

            if not os.path.exists(target_dir_path):
                os.makedirs(target_dir_path)

            # Construct full local path for the file
            local_file_full_path = os.path.join(
                target_dir_path, os.path.basename(remote_file_path)
            )

            if download_single(
                selected_com, remote_file_path, local_file_full_path
            ):  # selected_com is global
                print(
                    f"File {remote_file_path} downloaded successfully to {local_file_full_path}."
                )
            else:
                print(
                    f"Failed to download {remote_file_path}."
                )  # More specific error printed by run_ampy_command or download_single

        # Download multiple files
        elif choice == "5":
            remote_files = input(
                "Enter the remote file paths to download (separated by comma): "
            ).strip()
            local_dir = input(
                "Enter the local directory to save downloaded files: "
            ).strip()
            download_multiple(selected_com, remote_files, local_dir)

        # Delete single file
        elif choice == "6":
            file_name_to_delete = input(
                "Enter the file name to delete from the device: "
            ).strip()
            confirm = input(
                f"Are you sure you want to delete '{file_name_to_delete}' from the device? (y/n): "
            ).strip()
            if confirm.lower() == "y":
                print(
                    f"Attempting to delete '{file_name_to_delete}' from the device..."
                )
                success, _, _ = run_ampy_command(
                    selected_com, ["rm", file_name_to_delete], capture_output=False
                )  # selected_com global
                if success:
                    print(f"File '{file_name_to_delete}' deleted from the device.")
                else:
                    print(
                        f"Failed to delete '{file_name_to_delete}'. Check error messages above."
                    )
            else:
                print(f"Deletion of '{file_name_to_delete}' canceled.")

        # Delete by extension
        elif choice == "7":
            extension_to_delete = input(
                "Enter the file extension to delete (e.g., txt, py): "
            )
            delete_by_extension(
                selected_com, extension_to_delete
            )  # selected_com is global

        # Delete everything
        elif choice == "8":
            delete_everything(selected_com)  # selected_com is global

        # Rescan COM ports
        elif choice == "9":
            selected_com = find_COM()

        # Exit
        elif choice == "10":
            print("Script terminated.")
            break

        elif choice == "help":
            print(HELP_DOC)

        else:
            print("Invalid choice. Choose an option from 1 to 9 or type e to exit.")

        input(INPUT_SIGN)

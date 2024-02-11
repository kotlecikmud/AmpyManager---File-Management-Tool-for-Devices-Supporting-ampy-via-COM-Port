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

__version__ = '01.01.21.00'
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


class LoadingAnimation:
    def __init__(self):
        self.animation_signs = ['|....', '.|...', '..|..', '...|.', '....|', '...|.', '..|..', '.|...']
        self.sign_index = 0
        self.finished = False

    def start(self):
        self.finished = False
        self._animate_thread = threading.Thread(target=self._animate)
        self._animate_thread.start()

    def stop(self):
        self.finished = True
        self._animate_thread.join()

    def _animate(self):
        while not self.finished:
            print(self.animation_signs[self.sign_index % len(self.animation_signs)], end='\r')
            time.sleep(0.1)
            self.sign_index += 1


# Instantiate LoadingAnimation class
loading_animation = LoadingAnimation()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def display_file_content(selected_com, selected_file):
    loading_animation.start()

    print(SEPARATOR)
    print("\n\n\n")
    subprocess.run(["ampy", "-p", "COM" + selected_com, "get", selected_file])
    print(SEPARATOR)

    loading_animation.stop()


def upload_single(com_port, local_file, remote_file):
    loading_animation.start()
    cmd = ["ampy", "-p", "COM" + com_port, "put", local_file, remote_file]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stderr:
        if b"Transfer complete" in line:
            break
    loading_animation.stop()


def upload_from_dir(local_dir_id):
    if not os.path.exists(local_dir_id):
        print("Source directory does not exist.")
    else:
        # Get a list of files in the local directory
        files_to_upload = [f for f in os.listdir(local_dir_id) if os.path.isfile(os.path.join(local_dir_id, f))]

        if not files_to_upload:
            print("No files found in the source directory.")

        else:
            for file_name in files_to_upload:
                print(f"uploading: {file_name}")

                local_file = os.path.join(local_dir_id, file_name)
                remote_file = ROOT_DIR + file_name  # Upload to root directory
                upload_single(selected_com, local_file, remote_file)

                print("DONE  ")  # space present to cover loading animation in the same line


def download_single(com_port, remote_file, local_file):
    cmd = ["ampy", "-p", "COM" + com_port, "get", remote_file, local_file]
    loading_animation.start()

    try:
        # Start the download process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()  # Wait for the subprocess to finish

        # Check if the process completed successfully
        if process.returncode == 0:
            loading_animation.stop()

        else:
            loading_animation.stop()
            print("Error downloading the file from the device.")

    except subprocess.CalledProcessError as e:
        loading_animation.stop()
        print("Error executing the 'ampy' command:", e)


def download_multiple(remote_files_id, local_dir_id):
    if not os.path.exists(local_dir_id):
        os.makedirs(local_dir_id)

    remote_file_list = [f.strip() for f in remote_files_id.split(',')]

    for remote_file in remote_file_list:
        loading_animation.start()

        local_file = os.path.join(local_dir_id, os.path.basename(remote_file))
        print(f"downloading: '{remote_file}' as '{local_file}'")
        download_single(selected_com, remote_file, local_file)

        loading_animation.stop()

        print("DONE  ")


def delete_by_extension(extension_to_delete):
    confirm = input(
        f"Are you sure you want to delete all '{extension_to_delete}' files from the device? (y/n): ")

    if confirm.lower() == "y":
        output = subprocess.check_output(["ampy", "-p", "COM" + selected_com, "ls"]).decode("utf-8")
        files = [line.strip() for line in output.splitlines() if line.strip()]

        for file_name in files:
            if file_name.endswith(extension_to_delete):
                loading_animation.start()

                print(f"deleting: {file_name}")
                subprocess.run(["ampy", "-p", "COM" + selected_com, "rm", file_name])

                loading_animation.stop()

                print("DONE  ")

        print(f"All '{extension_to_delete}' files deleted from the device.")

    else:
        print(f"Delete '{extension_to_delete}' files operation canceled.")


def delete_everything():
    choice_1 = input(f"Do you want to delete all files from the device? (y/n): ")
    choice_2 = input(
        f"{Fore.RED}Are you sure you want to delete ALL files from the device? (double-check) (y/n): {Style.RESET_ALL}")

    if choice_1.lower() == "y" and choice_2.lower() == "y":
        output = subprocess.check_output(["ampy", "-p", "COM" + selected_com, "ls"]).decode("utf-8")
        files = [line.strip() for line in output.splitlines() if line.strip()]

        for file_name in files:
            print(f"deleting: {file_name}")

            loading_animation.start()
            subprocess.run(["ampy", "-p", "COM" + selected_com, "rm", file_name])
            loading_animation.stop()

            print("DONE  ")

        print(f"All files deleted from the device.")

    else:
        print(f"Operation canceled.")


def find_COM():
    clear_screen()
    print("Waiting for COM port...")
    loading_animation.start()

    while True:
        com_ports = []  # declare/clean port list

        # Find available COM ports
        output = subprocess.check_output("mode", shell=True).decode("utf-8")

        for line in output.splitlines():
            if "COM" in line:
                com_port = line.split("COM")[1].strip()
                if com_port != "1:":  # append every found COM port ignoring COM1
                    com_ports.append(com_port.replace(':', ''))

        if com_ports:  # if found any COM ports except 1:
            loading_animation.stop()

            while True:
                clear_screen()

                if not len(com_ports) == 1:
                    print(f"Available COM Ports:\n{', '.join(com_ports)}")
                    com_choice = input(f"Type number or 'r' for 'refresh'.\nEnter your choice: ")

                    if com_choice.isdigit():

                        if com_choice.replace(':', '') in com_ports:
                            print(f"Selected COM Port: {com_choice}")
                            return com_choice

                        else:
                            print("Invalid COM Port. Please try again.")

                    elif com_choice == "r" or com_choice == "refresh":
                        clear_screen()
                        print("Waiting for COM port...")
                        loading_animation.start()
                        break

                    else:
                        print("Invalid choice. Please try again.")

                else:
                    return com_ports[0].replace(':', '')


def display_content():
    print("Storage on device:")

    loading_animation.start()
    subprocess.run(["ampy", "-p", "COM" + selected_com, "ls"])
    loading_animation.stop()


if __name__ == '__main__':
    selected_com = find_COM()

    # Menu
    while True:
        clear_screen()

        print(
            f"Ampy Manager {Fore.CYAN}{Style.BRIGHT}v{__version__}{Style.RESET_ALL}\nselected port: {Fore.LIGHTRED_EX}{Style.BRIGHT}COM{selected_com}{Style.RESET_ALL}")

        print(SEPARATOR)

        display_content()

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
            10: "Exit"
        }

        print("Options:")
        for key, value in options.items():
            print(f"{str(key).ljust(2)} {value.ljust(30)}")

        print(SEPARATOR)

        choice = input(f"Choose an option {INPUT_SIGN} ")

        # Display file content
        if choice == "1":
            selected_file = input("Enter destination path of the file on the device: ").strip()
            display_file_content(selected_com, selected_file)

        # Upload single file
        elif choice == "2":
            local_file = input("Enter the source path for the local file: ").strip()
            remote_file = input("Enter destination path of the file on the device: ").strip()
            upload_single(selected_com, local_file, remote_file)
            print("File uploaded to the device.")

        # Upload multiple files
        elif choice == "3":
            local_dir = input("Enter the source directory path for the files: ").strip()
            upload_from_dir(local_dir)

        # Download single file
        elif choice == "4":
            remote_file = input("Enter the path of the file on the device: ").strip()
            local_file = input("Enter the target directory for the downloaded file: ").strip()

            if not os.path.exists(local_file):
                os.makedirs(local_file)

            download_single(selected_com, remote_file, os.path.join(local_file, os.path.basename(remote_file)))
            print(f"File {remote_file} downloaded from the device.")

        # Download multiple files
        elif choice == "5":
            remote_files = input("Enter the remote file paths to download (separated by comma): ").strip()
            local_dir = input("Enter the local directory to save downloaded files: ").strip()
            download_multiple(remote_files, local_dir)

        # Delete single file
        elif choice == "6":
            file_name_to_delete = input("Enter the file name to delete from the device: ").strip()
            confirm = input(f"Are you sure you want to delete '{file_name_to_delete}' from the device? (y/n): ").strip()
            if confirm.lower() == "y":
                subprocess.run(["ampy", "-p", "COM" + selected_com, "rm", file_name_to_delete])
                print(f"File '{file_name_to_delete}' deleted from the device.")
            else:
                print(f"Deletion of '{file_name_to_delete}' canceled.")

        # Delete by extension
        elif choice == "7":
            extension_to_delete = input("Enter the file extension to delete (e.g., txt, py): ")
            delete_by_extension(extension_to_delete)

        # Delete everything
        elif choice == "8":
            delete_everything()

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

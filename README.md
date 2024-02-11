# Ampy Manager

## About

- **Script Name:** AM_main.py
- **Author:** Filip Pawłowski
- **Contact:** [filippawlowski2012@gmail.com](mailto:filippawlowski2012@gmail.com)
- **Version:** 01.01.21.00

## Description

`AM_main.py` is a versatile utility script designed to streamline file management tasks on Ampy-compatible devices,
including popular platforms such as Raspberry Pi, ESP8266, and ESP32, leveraging the capabilities of the 'ampy' tool (
Adafruit MicroPython tool).

This script operates as a console-based manager, offering an array of functionalities for seamless interaction with
devices connected through a COM port using the Ampy tool. Its comprehensive features include displaying file content,
uploading and downloading files, and performing file deletions. The script aims to enhance the user experience by
providing a user-friendly interface for efficient file management on MicroPython-based devices.

## Menu Options

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

## Initialization

- Checks if the script is the main module.
- Calls `find_COM()` to determine the selected COM port.

## `find_COM()` Function Description

The `find_COM()` function is responsible for searching and selecting available COM ports on the computer. Below is a
description of how this function operates:

1. **Initialization:**
    - The function begins by clearing the screen for better readability.

2. **Waiting for COM Port Message:**
    - Displays a message informing the user that the function is in the process of searching for available COM ports.

3. **Start Loading Animation:**
    - Initiates a loading animation to keep the user informed about the status of the search process.

4. **Searching for Available COM Ports:**
    - The function uses the system command `mode` to obtain information about available COM ports.
    - Analyzes the command's output, identifying COM ports available on the computer.

5. **User Selection of COM Port:**
    - If more than one COM port is found (excluding COM1), it presents the user with a list of available ports.
    - The user is prompted to enter the number of the chosen port or choose the refresh option (`r` or `refresh`).
    - In case of an invalid number or option, the user is informed of the error and asked to re-enter.

6. **Stop Loading Animation:**
    - Once the user makes a valid selection, it stops the loading animation.

7. **Return the Selected COM Port:**
    - The function returns the chosen COM port number, which can be used in other parts of the program.

This function provides users with the flexibility to choose a COM port, essential when dealing with different devices
connected to the computer.

## Display

- Shows version and selected COM port.
- Lists options for file management operations.

## User Input and Options

- Takes user input for desired operation (`choice`).
- Executes different actions based on the user's choice.

### Actions

1. Display file content
2. Upload single file
3. Upload multiple files from a directory
4. Download single file
5. Download multiple files
6. Delete single file
7. Delete files by extension
8. Delete all files
9. Rescan COM ports
10. Exit

## Documentation

- Typing "help" displays additional documentation (`HELP_DOC`).

## Contact

For any queries or assistance, please contact the author:

- **Author:** Filip Pawłowski
- **Contact:** [filippawlowski2012@gmail.com](mailto:filippawlowski2012@gmail.com)

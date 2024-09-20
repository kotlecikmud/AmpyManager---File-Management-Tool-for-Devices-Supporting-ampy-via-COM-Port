### **AmpyManager**

#### **Program Information**

- **Script Name:** `AM_main.py`
- **Author:** *Filip Pawłowski*
- **Contact:** [filippawlowski2012@gmail.com](mailto:filippawlowski2012@gmail.com)
- **Version:** `01.01.21.00`

---

#### **Description**

The `ampy_manager.py` script is a tool for managing files on devices compatible with **ampy**, such as the **Raspberry Pi Pico** with the **MicroPython** firmware installed. It allows performing the following operations:

- **Viewing file contents** (does not decode binary data – displays raw data)
- **Uploading and downloading files**
- **Deleting files**
- And other file management functions on the device.

*Note*: The script has only been tested with the Raspberry Pi Pico.

---

#### **Usage Instructions**

The script is run from the command line using the command:

    python ampy_manager.py

After launching, a menu with the following options will appear on the screen:

- **View file content:** Displays the content of a selected file on the device (raw data, no decoding).
- **Upload a single file:** Uploads a single file from the local computer to the device.
- **Upload multiple files:** Uploads multiple files from a local directory to the device.
- **Download a single file:** Downloads a selected file from the device to the local computer.
- **Download multiple files:** Downloads all files from a selected directory on the device to a local directory.
- **Delete a single file:** Deletes a selected file from the device.
- **Delete files by extension:** Deletes all files with a specified extension (e.g., .txt, .py) from the device.
- **Delete all:** Deletes all files from the device.
- **Scan COM ports:** Scans available COM ports, allowing you to select a different port to connect to the device.
- **Exit:** Closes the script.
- **Help:** Displays detailed documentation and help regarding the use of the script.

**Contact**  
For any questions or issues, please contact:

- **Author:** Filip Pawłowski
- **Email:** filippawlowski2012@gmail.com

---
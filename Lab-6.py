import requests
import hashlib
import subprocess
import os

def main():
    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer
    if not installer_ok(installer_data, expected_sha256):
        print("Installer integrity check failed. Aborting.")
        return

    # Save the downloaded VLC installer to disk
    installer_path = save_installer(installer_data)

    # Silently run the VLC installer
    run_installer(installer_path)

    # Delete the VLC installer from disk
    delete_installer(installer_path)

def get_expected_sha256():
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/"
    response = requests.get(url)

    # Extract the SHA-256 hash value from the response message body
    expected_hash = None
    if response.status_code == 200:
        hash_lines = response.text.splitlines()
        for line in hash_lines:
            if "vlc-3.0.18-win64.exe" in line:
                expected_hash = line.split()[0]
                break

    return expected_hash

def download_installer():
    url = "http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.17.4-win64.exe"
    response = requests.get(url)
    return response.content

def installer_ok(installer_data, expected_sha256):
    # Calculate the SHA-256 hash value of the downloaded installer file
    installer_hash = hashlib.sha256(installer_data).hexdigest()

    # Compare the computed hash with the expected hash
    return installer_hash == expected_sha256

def save_installer(installer_data):
    # Save the installer to the system's temporary folder
    temp_folder = os.getenv('TEMP')
    installer_path = os.path.join(temp_folder, "vlc-3.0.18-win64.exe")
    with open(installer_path, 'wb') as f:
        f.write(installer_data)
    return installer_path

def run_installer(installer_path):
    # Run the installer silently, suppressing any output to the console
    command = [installer_path, "/S"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def delete_installer(installer_path):
    # Delete the installer file
    os.remove(installer_path)

if __name__ == '__main__':
    main()
        
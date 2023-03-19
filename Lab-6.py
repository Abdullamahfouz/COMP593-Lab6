import requests
import hashlib
import os
import subprocess

def main():
    version = '3.0.17.4'

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256(version)

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer(version)

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data, version)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256(version):
    hash_url = f'http://download.videolan.org/pub/videolan/vlc/{version}/win64/vlc-{version}-win64.txt'
    resp_msg = requests.get(hash_url)
    if resp_msg.status_code == requests.codes.ok:
        hash_content = resp_msg.text
        return hash_content.split()[0]
    return None

def download_installer(version):
    installer_url = f'http://download.videolan.org/pub/videolan/vlc/{version}/win64/vlc-{version}-win64.exe'
    resp_msg = requests.get(installer_url)
    if resp_msg.status_code == requests.codes.ok:
        return resp_msg.content
    return None

def installer_ok(installer_data, expected_sha256):
    installer_hash = hashlib.sha256(installer_data).hexdigest()
    return installer_hash == expected_sha256

def save_installer(installer_data, version):
    temp_folder = os.getenv('TEMP')
    installer_path = os.path.join(temp_folder, f'vlc-{version}-win64.exe')
    with open(installer_path, 'wb') as file:
        file.write(installer_data)
    return installer_path

def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'])

def delete_installer(installer_path):
    os.remove(installer_path)

if __name__ == '__main__':
    main()

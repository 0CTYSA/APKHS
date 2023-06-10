import os
import shutil
import zipfile
import tldextract
import hashlib
from androguard.core.bytecodes.apk import APK


def generate_apktemplate():
    apk_folder_path = os.path.join(os.path.dirname(__file__), "apk")
    apk_files = [f for f in os.listdir(apk_folder_path) if f.endswith(".apk")]

    if not apk_files:
        print("No se encontraron archivos APK en la carpeta 'apk'.")
        return

    with open(os.path.join(os.path.dirname(__file__), "template.txt"), "w") as file:
        file.truncate()  # Clear the contents of the file template.txt

        for apk_filename in apk_files:
            apk_file_path = os.path.join(apk_folder_path, apk_filename)
            apk_basename = os.path.basename(apk_file_path)

            # Calculate MD5 and SHA-256 hashes
            with open(apk_file_path, "rb") as f:
                md5_hash = hashlib.md5(f.read()).hexdigest()
                f.seek(0)
                sha256_hash = hashlib.sha256(f.read()).hexdigest()

            # Extract version using androguard
            apk = APK(apk_file_path)
            version = apk.get_androidversion_name()

            # Construct template
            template = """Greetings.

The DTP Teams has been detected an Unauthorized Mobile App Against your organization:

Unauthorized App Information:
App Store: {app_store}
Download: {download_url}
Filename: {apk_filename}
Version: {version}
SO: Android
MD5: {md5_hash}
SHA256: {sha256_hash}


Sincerely,
DTP SOC Team.
"""

            download_url = input(
                f"Ingrese la URL de descarga de la aplicación '{apk_basename}': ")

            # Extract domain from URL and add "https://" before it
            app_store = "https://" + \
                tldextract.extract(download_url).registered_domain

            # Replace placeholders with actual values
            template = template.replace("{app_store}", app_store)
            template = template.replace("{download_url}", download_url)
            template = template.replace("{apk_filename}", apk_filename)
            template = template.replace("{version}", version)
            template = template.replace("{md5_hash}", md5_hash)
            template = template.replace("{sha256_hash}", sha256_hash)

            separator = "-" * 50

            final_template = f"{separator}\n{template.strip()}\n{separator}"

            file.write(final_template)  # Write the template in the file

    # Ask user if they want to delete the APK, XAPK, and ZIP files
    delete_files = input(
        "¿Desea eliminar los archivos APK, XAPK y ZIP de la carpeta 'apk'? (s/n): ")
    while delete_files.lower() not in ["s", "n"]:
        delete_files = input("Por favor, ingrese 's' para sí o 'n' para no: ")

    if delete_files.lower() == "s":
        for apk_filename in apk_files:
            apk_file_path = os.path.join(apk_folder_path, apk_filename)
            os.remove(apk_file_path)

        xapk_folder_path = "APKHS/ApphashT/apk"

        for root, dirs, files in os.walk(xapk_folder_path):
            for file in files:
                if file.endswith(".xapk") or file.endswith(".zip"):
                    os.remove(os.path.join(root, file))

        delete_msg = "Los archivos APK, XAPK y ZIP han sido eliminados"
    else:
        delete_msg = "Los archivos APK, XAPK y ZIP no han sido eliminados"

    print(delete_msg, "y los templates han sido generados exitosamente.")


def extract_apks_from_archive(folder_path, archive_extension):
    for filename in os.listdir(folder_path):
        file_path = os.path.abspath(os.path.join(folder_path, filename))
        if filename.endswith(archive_extension):
            try:
                with zipfile.ZipFile(file_path) as archive:
                    extracted_apk_path = None
                    for entry in archive.namelist():
                        if entry.endswith(".apk") and "config." not in entry:
                            apk_file = archive.open(entry)
                            extracted_apk_path = os.path.join(
                                folder_path, os.path.split(entry)[-1])
                            with open(extracted_apk_path, "wb") as f:
                                f.write(apk_file.read())
                            apk_file.close()

                    if extracted_apk_path is not None:
                        apk_destination = os.path.join(
                            folder_path, os.path.split(extracted_apk_path)[-1])
                        shutil.move(extracted_apk_path, apk_destination)

            except zipfile.BadZipFile:
                print(f"Error: {file_path} is not a valid archive.")


def extract_apks_from_xapk():
    xapk_folder_path = "APKHS/ApphashT/apk"
    extract_apks_from_archive(xapk_folder_path, ".xapk")

    zip_folder_path = "APKHS/ApphashT/apk"
    extract_apks_from_archive(zip_folder_path, ".zip")


extract_apks_from_xapk()
generate_apktemplate()

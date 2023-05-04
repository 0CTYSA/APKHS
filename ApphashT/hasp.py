import os
import tldextract
import hashlib  # pip install hashlib
from androguard.core.bytecodes.apk import APK  # pip install androguard

apk_folder_path = os.path.join(os.path.dirname(__file__), "apk")

apk_files = os.listdir(apk_folder_path)

apk_files = [f for f in apk_files if f.endswith(".apk")]

if not apk_files:
    print("No se encontraron archivos APK en la carpeta 'apk'.")
else:
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

            # Ask user if they want to delete APK files
            delete_apks = input(
                "¿Desea eliminar los archivos APK de la carpeta 'apk'? (s/n)")

            if delete_apks.lower() == "s":
                for apk_filename in apk_files:
                    apk_file_path = os.path.join(apk_folder_path, apk_filename)
                    os.remove(apk_file_path)

    print("Los templates han sido generados exitosamente.")

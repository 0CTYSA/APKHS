import os
import tldextract
import hashlib  # pip install hashlib
from androguard.core.bytecodes.apk import APK  # pip install androguard
import shutil
import zipfile


def generate_apktemplate():
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

                # Ask user if they want to delete the APK and XAPK files
                delete_apks = input(
                    "¿Desea eliminar los archivos APK y XAPK  de la carpeta 'apk'? (s/n)")
                while delete_apks.lower() not in ["s", "n"]:
                    delete_apks = input(
                        "Por favor, ingrese 's' para sí o 'n' para no: ")

                if delete_apks.lower() == "s":
                    for apk_filename in apk_files:
                        apk_file_path = os.path.join(
                            apk_folder_path, apk_filename)
                        os.remove(apk_file_path)
                        delete_msg = "Los archivos APK y XAPK han sido eliminados"
                else:
                    delete_msg = "Los archivos APK y XAPK no han sido eliminados"

        print(delete_msg, "y los templates han sido generados exitosamente.")


def extract_apks_from_xapk():
    # Ruta de la carpeta que contiene los archivos .xapk
    ruta_carpeta_xapk = "APKHS/ApphashT/apk"

    # Crear la subcarpeta "apks_extraidos" si no existe
    ruta_apks_extraidos = os.path.join(ruta_carpeta_xapk)
    if not os.path.exists(ruta_apks_extraidos):
        os.makedirs(ruta_apks_extraidos)

    # Extraer los archivos APK de todos los archivos .xapk en la carpeta
    for nombre_archivo_xapk in os.listdir(ruta_carpeta_xapk):
        ruta_archivo_xapk = os.path.abspath(
            os.path.join(ruta_carpeta_xapk, nombre_archivo_xapk))
        if nombre_archivo_xapk.endswith(".xapk"):
            # Crear un objeto ZipFile
            archivo_xapk = zipfile.ZipFile(ruta_archivo_xapk)

            # Extraer los archivos APK en una subcarpeta con el mismo nombre que el archivo XAPK
            nombre_carpeta_apk = os.path.splitext(nombre_archivo_xapk)[0]
            ruta_apks_extraidos_xapk = os.path.join(
                ruta_apks_extraidos, nombre_carpeta_apk)
            if not os.path.exists(ruta_apks_extraidos_xapk):
                os.makedirs(ruta_apks_extraidos_xapk)

            for nombre_archivo in archivo_xapk.namelist():
                if nombre_archivo.endswith(".apk") and "config." not in nombre_archivo:
                    archivo_apk = archivo_xapk.open(nombre_archivo)
                    nombre_archivo_sin_carpeta = os.path.split(
                        nombre_archivo)[-1]
                    ruta_extraido = os.path.join(
                        ruta_apks_extraidos_xapk, nombre_archivo_sin_carpeta)
                    with open(ruta_extraido, "wb") as f:
                        f.write(archivo_apk.read())
                    archivo_apk.close()

            archivo_xapk.close()

            # Mover el archivo APK fuera de la carpeta y eliminar la carpeta vacía
            ruta_apk_original = os.path.join(
                ruta_apks_extraidos_xapk, nombre_archivo_sin_carpeta)
            ruta_apk_destino = os.path.join(
                ruta_apks_extraidos, nombre_archivo_sin_carpeta)
            shutil.move(ruta_apk_original, ruta_apk_destino)
            os.rmdir(ruta_apks_extraidos_xapk)


extract_apks_from_xapk()
generate_apktemplate()

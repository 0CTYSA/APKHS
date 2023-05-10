import os
import shutil
import zipfile

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
                nombre_archivo_sin_carpeta = os.path.split(nombre_archivo)[-1]
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

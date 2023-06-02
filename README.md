# APKHS

## Usage

The provided code serves the following purposes:

### Generating APK Template

1. Place the APK files in a folder named "apk" located in the same directory as the script.
2. Run the script to generate an APK template.
3. The script will search for APK files in the "apk" folder.
4. If APK files are found, a file named "template.txt" will be created.
5. For each APK file, the script performs the following steps:
   - Calculates the MD5 and SHA-256 hashes of the APK file.
   - Extracts the version information using the Androguard library.
   - Prompts the user to input the download URL of the application.
   - Constructs a template with placeholders for various details.
   - Replaces the placeholders in the template with the actual values.
   - Writes the filled template to the "template.txt" file.
6. After generating the template, the script prompts the user whether to delete the APK, XAPK, and ZIP files.

### Extracting APKs from XAPK

1. Ensure that the XAPK files are located in the "APKHS/ApphashT/apk" folder.
2. Run the script to extract APKs from XAPK files.
3. The script will create a subfolder named "apks_extraidos" within the "APKHS/ApphashT/apk" folder (if not already present).
4. For each XAPK file in the folder, the script performs the following steps:
   - Opens the XAPK file as a ZipFile object.
   - Creates a subfolder with the same name as the XAPK file within the "apks_extraidos" folder.
   - Extracts APK files from the XAPK file and saves them to the subfolder.
   - Moves the extracted APK file out of the subfolder and deletes the empty subfolder.

### Extracting APKs from Archives

1. Modify the folder path and archive extension in the script according to your requirements.
2. Run the script to extract APKs from archive files.
3. The script will search for files with the specified archive extension in the specified folder.
4. For each archive file, the script performs the following steps:
   - Opens the archive file as a ZipFile object.
   - Searches for APK files within the archive and extracts them to the folder.
   - Moves the extracted APK file to the folder and deletes the archive file if successful.

### Extracting APKs from XAPK and ZIP

1. Run the script to extract APKs from both XAPK and ZIP files.
2. The script will call the "extract_apks_from_archive" function twice, specifying the folder paths and extensions for each type.

## Note

- Make sure to install the required dependencies before running the script.
- Adjust the file paths and names as per your specific setup.
- This explanation serves as a guide to understand the functionality and usage of the code. Please adapt it according to your specific requirements and context.

Feel free to adjust the formatting and structure of the explanation according to your specific requirements for the README file.

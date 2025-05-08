import os
import shutil
import argparse

if len(os.sys.argv) != 3:
    print("Usage: python extractPak.py <input_pak> <output_directory>")
    exit()

# Get the pak file and output directory from the command line arguments
pakPath = os.sys.argv[1]
outputPath = os.sys.argv[2]

# Open the file
f = open(pakPath, "rb")

# Check signature
signature = f.read(16)
if signature != b'HMMSYS PackFile\n':
    print("Invalid Pak signature")
    exit()

# Unknown header part
unknown = f.read(16)

# Read number of stored files
filesN = int.from_bytes(f.read(4), byteorder='little')

# Unknown value
unknown2 = int.from_bytes(f.read(4), byteorder='little')

# Read the files
files = []
for i in range(filesN):

    # Get file name size TODO: this needs to be understood better!
    a = int.from_bytes(f.read(1), byteorder='little')
    b = int.from_bytes(f.read(1), byteorder='little')
    pathLenght = a-b

    path = f.read(pathLenght)

    # Read the position of the file
    fileLocation = int.from_bytes(f.read(4), byteorder='little')

    # Read the size of the file
    fileSize = int.from_bytes(f.read(4), byteorder='little')

    # Create a dict and add it to files
    el = {
        "path" : path.decode('utf-8'),
        "location" : fileLocation,
        "size" : fileSize
    }
    files.append(el)

# Create the output folder
os.makedirs(outputPath, exist_ok=True)

# Clean the output folder
for item in os.listdir(outputPath):
    item_path = os.path.join(outputPath, item)

    if os.path.isfile(item_path) or os.path.islink(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)

# Extract the files
for el in files:

    # Split the path
    pathSplit = el["path"].split("\\")

    # Remove the filename to maintain only the folders tree
    folders = pathSplit[:-1]

    # Extract the file name
    fileName = pathSplit[-1]

    # Navigate to the file location
    f.seek(el["location"])

    # Read the file
    fileData = f.read(el["size"])

    # Create folder structure
    full_path = os.path.join(outputPath, *folders)
    os.makedirs(full_path, exist_ok=True)

    # Write the file
    with open(os.path.join(full_path, fileName), "wb") as outFile:
        outFile.write(fileData)
        print(f'Extracted: {fileName}')

f.close()

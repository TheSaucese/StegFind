import os
from subprocess import Popen, PIPE

def extract_with_optional_passphrase(img, passphrase=None):
    img = os.path.abspath(img)
    original_dir = os.getcwd()
    img_dir = os.path.dirname(img) or original_dir
    os.chdir(img_dir)

    # Get the list of files before extraction
    files_before = set(os.listdir(img_dir))
    print(img_dir)
    print(files_before)

    process = Popen(["steghide.exe", "extract", "-sf", os.path.basename(img)], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    output, error = process.communicate()

    passphrase_needed = "Enter passphrase" in output or "Enter passphrase" in error
    extraction_failed = "could not extract" in output or "could not extract" in error

    if passphrase_needed and passphrase:
        process = Popen(["steghide.exe", "extract", "-sf", os.path.basename(img), "-p", passphrase], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        output, error = process.communicate()
        extraction_failed = "could not extract" in output or "could not extract" in error

    if extraction_failed:
        os.chdir(original_dir)
        return None, "Extraction failed or wrong passphrase."

    if passphrase_needed and not passphrase:
        os.chdir(original_dir)
        return None, "Passphrase required but not provided."

    # Get the list of files after extraction
    files_after = set(os.listdir(img_dir))
    print("FILES AFTER",files_after)

    # Determine the new file(s)
    new_files = files_after
    new_files.discard(os.path.basename(img))
    new_files.discard('view')
    print(new_files)
    if new_files:
        os.chdir(original_dir)
        # Return the first new file found; modify as needed if multiple files can be extracted
        return os.path.join(img_dir, new_files.pop()), None
    else:
        os.chdir(original_dir)
        return None, "No new file was extracted."

# Usage example:
#result, error = extract_with_optional_passphrase('C:/Users/Elfar/stuff/StegFind/static/uploads/02a8894423864fb4c02e86c24fa38305/file.jpeg', 'ju5tfindm3')

#print(result)
#print(error)
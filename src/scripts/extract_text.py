import os
from src.extractors import get_extractor
from src.extractors.file_types import FileType

FILES_DIR = "files/raw"
EXTRACTED_DIR = "files/extracted"

# If pdf to image conversion is enabled, extract to this directory instead
EXTRACTED_PDF_TO_IMAGE_DIR = "files/extracted_pdf_to_image"

def get_new_filename(file):
    return file + ".txt"

def extract(convert_pdf_to_image=False):
    """Loops through each subdirectory in files and extracts text from each file.
    Saves the extracted text in a new files_extracted directory.
    """
    output_dir = EXTRACTED_PDF_TO_IMAGE_DIR if convert_pdf_to_image else EXTRACTED_DIR

    # Create extracted directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Loop through each directory
    category_directories = os.listdir(FILES_DIR)
    for dir in category_directories:
        # Skip if non-directory
        if not os.path.isdir(os.path.join(FILES_DIR, dir)):
            continue

        # Create sub-directory in extracted directory
        subdir = os.path.join(output_dir, dir)
        os.makedirs(subdir, exist_ok=True)

        # Extract text for each file
        files = os.listdir(os.path.join(FILES_DIR, dir))
        for file in files:
            # Skip unsupported files and sub directories
            extension = file.split(".")[-1]
            if extension not in FileType:
                continue

            file_path = os.path.join(FILES_DIR, dir, file)
            extractor = get_extractor(file_path, convert_pdf_to_image=convert_pdf_to_image)
            text = extractor.extract()

            new_filename = get_new_filename(file)
            with open(os.path.join(subdir, new_filename), "w") as f:
                f.write(text)

if __name__ == "__main__":
    extract()

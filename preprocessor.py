
import os
import time

from pathlib import Path
from pprint import pprint
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType

from converters import pdf_converter, extract_metadata, metadata, save_docs_to_jsonl

# ------------------------------------------------------------------------------ 

# A naughty global used on line 71 (for batch loading).
# Set it to False if you don't need (want) to use OCR.

OCR = True

# ------------------------------------------------------------------------------ 


def format_files(directory, verbose=False):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            formatted_filename = format_filename(filename)
            new_file_path = os.path.join(directory, formatted_filename)
            os.rename(file_path, new_file_path)
            if verbose:
                print(f"Renamed '{filename}' to '{formatted_filename}'")


def batch_load(file_path, ocr):
    loader = DoclingLoader(
        converter=pdf_converter(ocr),
        file_path=file_path,
        export_type=ExportType.DOC_CHUNKS
    )
    loaded_documents = loader.load()
    documents = extract_metadata(loaded_documents)
    return documents
    

def batch_convert(data_dir):
    print(f"\nNote: a message saying 'Token indices sequence length is longer than "
          f"the specified maximum sequence length...' can be ignored in this case"
          f"\nDetails: https://github.com/docling-project/docling-core/issues/119"
          f"#issuecomment-2577418826\n")

    converted_documents = []

    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)

        if os.path.isfile(file_path):
            output_dir = Path("./jsondata")
            output_dir.mkdir(parents=True, exist_ok=True)
            stem, _ = os.path.splitext(file)
            json_file_name = stem+".jsonl"
            json_file_path = os.path.join(output_dir, json_file_name)

            if os.path.isfile(json_file_path):
                print(f"{json_file_path} already exists.")
                continue

            print(f"Processing {file}")
            start_time = time.time()
            documents = batch_load(file_path, OCR)
            save_docs_to_jsonl(documents, json_file_path)
            converted_documents.append(documents)
            end_time = time.time() - start_time
            print(f"Document {file} converted in {end_time:.2f} seconds.")

    return converted_documents


if __name__ == "__main__":

    DATA_DIR = Path("./data")

    converted_documents = batch_convert(data_dir=DATA_DIR)

    print("\nFinished.\n")



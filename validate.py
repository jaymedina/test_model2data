#!/usr/bin/env python3

import glob
import json
import os
import zipfile
import argparse

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Validate prediction files against a gold standard.")
    parser.add_argument('-p', '--predictions_file', required=True, help="Path to the predictions file (or zip containing predictions)")
    parser.add_argument('-g', '--goldstandard_folder', required=True, help="Folder containing the gold standard file")
    parser.add_argument('-o', '--output', required=True, help="Output file name for the validation results")

    # Parsing command line arguments
    args = parser.parse_args()
    predictions_path = args.predictions_file
    goldstandard_path = args.goldstandard_folder
    results_filename = args.output

    invalid_reasons = []
    if "INVALID" in predictions_path:
        prediction_status = "INVALID"
        with open(predictions_path, "r") as file:
            invalid_reasons.append(file.read())
    else:
        # Unzipping the predictions and extracting the files in the current working directory
        if ".zip" in os.path.basename(predictions_path):
            with zipfile.ZipFile(predictions_path, "r") as zip_ref:
                for zip_info in zip_ref.infolist():
                    if zip_info.is_dir():
                        continue
                    # Extract the file ignoring directory structure it was zipped in
                    zip_info.filename = os.path.basename(zip_info.filename)
                    zip_ref.extract(zip_info, os.getcwd())

        # Grabbing the extracted predictions files
        predictions_files = glob.glob(os.path.join(os.getcwd(), "*.csv"))

        # Grabbing the gold standard file
        gs_file = glob.glob(os.path.join(goldstandard_path, "*"))[0]

        # Validating file contents
        with open(gs_file, "r") as sub_file:
            message = sub_file.read()

        # Validating predictions files
        for file in predictions_files:
            with open(file, "r") as sub_file:
                message = sub_file.read()
            prediction_status = "VALIDATED"
            if message is None:
                prediction_status = "INVALID"
                invalid_reasons.append("At least one predictions file is empty")
    
    result = {
        "validation_status": prediction_status,
        "validation_errors": ";".join(invalid_reasons),
    }

    # Writing results to the output file
    with open(results_filename, "w") as o:
        o.write(json.dumps(result))
    print(prediction_status)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import glob
import json
import os
import zipfile
import argparse
import typing


INVALID = "INVALID"
SCORED = "SCORED"


def score_submission(predictions_path: str, status: str) -> typing.Tuple[str, dict]:
    """Determine the score of a submission. This is a placeholder function.
    Args:
        predictions_path (str): path to the predictions file
        status (str): current submission status
    Returns:
        result (dict): dictionary containing score, status and errors
    """

    if status == INVALID:
        score_status = INVALID
        score1, score2, score3 = None, None, None
        message = f"Submission was not scored due to {INVALID} status"
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

        # Checking if there are any files
        if len(predictions_files) == 0:
            score_status = INVALID
            message = "No predictions files found"
            score1, score2, score3 = None, None, None

        # Placeholder file reading
        for file in predictions_files:
            with open(file, "r") as sub_file:
                predictions_contents = sub_file.read()

        try:
            # Placeholder scoring
            score1 = 1 + 1
            score2 = score1 * 2
            score3 = score1 * 3
            score_status = SCORED
            message = ""
        except Exception as e:
            message = f"Error {e} occurred while scoring"
            score1, score2, score3 = None, None, None
            score_status = INVALID

    result = {
        "score1": score1,
        "score2": score2,
        "score3": score3,
        "score_status": score_status,
        "score_errors": message,
    }

    return score_status, result


def update_json(results_path: str, result: dict) -> None:
    """Update the results.json file with the current score and status
    Args:
        results_path (str): path to the results.json file
        result (dict): dictionary containing score, status and errors
    """
    file_size = os.path.getsize(results_path)
    with open(results_path, "r") as o:
        data = json.load(o) if file_size else {}
    data.update(result)
    with open(results_path, "w") as o:
        o.write(json.dumps(data))


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Score predictions file and update the results JSON.")
    parser.add_argument('-p', '--predictions_file', required=True, help="Path to the predictions file (or zip containing predictions)")
    parser.add_argument('-g', '--goldstandard', required=True, help="Path to the gold standard file or folder (not used here but included for consistency)")
    parser.add_argument('-o', '--output', required=True, help="Output file path for the validation results JSON")

    # Parsing command line arguments
    args = parser.parse_args()
    predictions_path = args.predictions_file
    result_path = args.output

    # Read validation status from the results JSON
    with open(result_path, encoding="utf-8") as out:
        res = json.load(out)

    status = res.get("validation_status")

    # Score the submission and update the JSON output
    score_status, result = score_submission(predictions_path, status)
    update_json(result_path, result)
    print(score_status)


if __name__ == "__main__":
    main()

import json
import os
import time
import traceback
from datetime import datetime
from enum import Enum
from typing import Optional

import requests

from korbit.constant import (
    KORBIT_CODE_ANALYSIS_CHECK,
    KORBIT_CODE_ANALYSIS_PULL_REQUEST_CHECK,
    KORBIT_CODE_ANALYSIS_SERVICE,
    KORBIT_LOCAL_FOLDER,
    KORBIT_SCAN_REPORT_URL,
)
from korbit.interface import (
    INTERFACE_SCAN_REPORT_ISSUES_COUNT_MSG,
    INTERFACE_SCAN_WAITING_REPORT_MSG,
    INTERFACE_SCAN_WAITING_START_MSG,
    INTERFACE_SLEEPING_REFRESH,
    console_print_message,
    construct_file_tree,
    create_console,
    create_progress_bar,
    generate_category_table,
)
from korbit.login import authenticate_request
from korbit.models.issue import IssueFilterThresholds
from korbit.models.report import Report, ReportCategory
from korbit.telemetry import send_telemetry


class ProgressStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PROGRESS = "PROGRESS"


def display_scan_status(scan_id: int, headless=False):
    """
    Display the progress of the scan status.
    If it's headless mode, the messages will be prompt only once.
    """
    console = create_console(headless)
    previous_progress = -1
    while True:
        response = authenticate_request(requests.get, url=f"{KORBIT_CODE_ANALYSIS_SERVICE}/{scan_id}/progress")
        try:
            data = response.json()
            status = data.get("status")
            if not status:
                console_print_message(console, INTERFACE_SCAN_WAITING_START_MSG, only_once=headless)
                time.sleep(INTERFACE_SLEEPING_REFRESH)
                continue
            if status == ProgressStatus.SUCCESS.value:
                console_print_message(console, INTERFACE_SCAN_WAITING_REPORT_MSG, only_once=headless)
                break

            progress = data.get("progress", 0.0)

            title = data.get("title", "File(s) status")

            file_tree_data = data.get("files", [])
            tree = construct_file_tree(title, file_tree_data)

            progress_bar = create_progress_bar(console, f"Analyzing files ({len(file_tree_data)})...", progress)
            if headless and previous_progress == progress:
                continue
            console.clear()
            console.print(tree)
            console.print(progress_bar)

        except Exception as e:
            send_telemetry([""], f"display_scan_status: {traceback.format_exc()}", error=True)
            console.print(f"Error processing response: {e}")

        time.sleep(INTERFACE_SLEEPING_REFRESH)


def download_report(scan_id: int) -> dict:
    response = authenticate_request(
        requests.get, url=f"{KORBIT_SCAN_REPORT_URL}/{scan_id}/issues?format=json&output_concept_embedding=false"
    )

    now = datetime.now()
    datetime_format = "%Y-%m-%dT%H-%M-%S"
    report_path = os.path.join(KORBIT_LOCAL_FOLDER, f"{scan_id}_{now.strftime(datetime_format)}_report")
    os.makedirs(KORBIT_LOCAL_FOLDER, exist_ok=True)
    html_report_path = f"{report_path}.html"
    json_report_path = f"{report_path}.json"

    with open(os.path.abspath(json_report_path), "w+") as json_file:
        issues = response.content.decode()
        json_file.write(issues)
        all_issues = json.loads(issues)

    final_issues = {"issues": all_issues, "scan_id": scan_id, "report_path": html_report_path}

    return final_issues


def filter_issues_by_threshold(report: Report, thresholds: IssueFilterThresholds) -> Report:
    if not thresholds:
        return report
    filtered_categories = []
    for category, issues in report.categories_iterator():
        filtered_categories.append(ReportCategory(category, thresholds.apply(issues)))

    report.categories = filtered_categories
    return report


def display_report(report: Report, headless=False) -> tuple[int, int]:
    console = create_console(headless)
    total_issues, selected_issues, ignored_issues = report.get_issues_stats()
    for i, category_issues in enumerate(report.categories):
        if not category_issues.get_total_selected_issues():
            continue

        generate_category_table(console, category_issues.category, category_issues.issues)

        if i != len(report.categories) - 1:
            console.print("\n")
            console.print("\n")

    console.print(
        INTERFACE_SCAN_REPORT_ISSUES_COUNT_MSG.format(
            total_issues=total_issues, selected_issues=selected_issues, ignored_issues=ignored_issues
        )
    )

    with open(report.report_path, "a+", encoding="utf-8") as report_file:
        report_file.write(console.export_html())

    return total_issues, selected_issues


def upload_file(zip_file_path: str, is_pr_scan: bool = False) -> Optional[int]:
    check_url = KORBIT_CODE_ANALYSIS_CHECK
    if is_pr_scan:
        check_url = KORBIT_CODE_ANALYSIS_PULL_REQUEST_CHECK
    with open(zip_file_path, "rb") as file:
        response = authenticate_request(requests.post, url=check_url, files={"repository": file})
        if response.status_code == 200:
            return response.json()
        else:
            return None

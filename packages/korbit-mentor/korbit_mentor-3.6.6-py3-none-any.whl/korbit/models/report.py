from dataclasses import dataclass
from typing import Iterator

from korbit.models.issue import Issue


@dataclass
class ReportCategory:
    category: str
    issues: list[Issue]

    @classmethod
    def from_json(cls, json_data):
        issues = [Issue.from_json(issue) for issue in json_data["files"]]
        return cls(
            category=json_data["category"],
            issues=issues,
        )

    def get_total_ignored_issues(self) -> int:
        return sum(len(issue.ignored_issue_files) for issue in self.issues)

    def get_total_selected_issues(self) -> int:
        return sum(len(issue.issue_files) for issue in self.issues)


@dataclass
class Report:
    scan_id: int
    report_path: str
    categories: list[ReportCategory]

    @classmethod
    def from_json(cls, json_data):
        computed_categories = {}

        for entry in json_data["issues"]:
            category = entry["files"][0]["category"]
            if category not in computed_categories:
                computed_categories[category] = []
            computed_categories[category].append(entry)

        return cls(
            scan_id=json_data["scan_id"],
            report_path=json_data["report_path"],
            categories=[
                ReportCategory.from_json({"category": category, "files": files})
                for category, files in computed_categories.items()
            ],
        )

    def categories_iterator(self) -> Iterator[tuple[str, list[Issue]]]:
        for category in self.categories:
            yield category.category, category.issues

    def get_issues_stats(self) -> tuple[int, int, int]:
        "Return the issues count, selected issues and ignored issues"
        total_issues = 0
        selected_issues = 0
        ignored_issues = 0
        for category_issues in self.categories:
            ignored_issues += category_issues.get_total_ignored_issues()
            selected_issues += category_issues.get_total_selected_issues()
        total_issues += selected_issues + ignored_issues
        return total_issues, selected_issues, ignored_issues

    def is_successful(self) -> bool:
        _, selected_issues, _ = self.get_issues_stats()
        return selected_issues == 0

from dataclasses import dataclass, field


@dataclass
class IssueFile:
    """
    This class represents a file where an issue was found.

    Attributes:
    confidence: Confidence level of the issue found in the file.
    priority: Priority level of the issue found in the file.
    path: Path to the file.
    line_start: Line where the issue starts.
    line_end: Line where the issue ends.
    """

    confidence: int
    priority: int
    path: str
    line_start: int
    line_end: int

    @classmethod
    def from_json(cls, json_data):
        return cls(
            confidence=json_data["confidence"],
            priority=json_data["priority"],
            path=json_data["path"],
            line_start=json_data["line_start"],
            line_end=json_data["line_end"],
        )

    def get_line_number(self):
        if self.line_start == self.line_end:
            return self.line_start
        return f"{self.line_start}:{self.line_end}"


@dataclass
class Issue:
    """
    This class represents an issue found in one or more files.

    Attributes:
    description: Description of the issue.
    issue_files: List of files where the issue was found.
    """

    description: str
    code_suggestion: str
    issue_files: list[IssueFile]
    ignored_issue_files: list[IssueFile] = field(default_factory=list)

    @classmethod
    def from_json(cls, json_data):
        return cls(
            description=json_data["description"],
            issue_files=[IssueFile.from_json(file) for file in json_data["files"]],
            code_suggestion=json_data.get("code_suggestion", ""),
        )

    @property
    def language(self) -> str:
        file_path = self.issue_files[0].path
        return file_path.split(".")[-1] if "." in file_path else ""


@dataclass
class IssueFilterThresholds:
    """
    This class represents the thresholds for filtering issues.

    Attributes:
    confidence: Confidence threshold (scale 0-10).
    priority: Priority threshold (scale 0-10).
    """

    confidence: int
    priority: int

    def apply(self, issues: list[Issue]) -> list[Issue]:
        filtered_issues = []
        for issue in issues:
            selected_issue_files = []
            ignored_issue_files = []
            for issue_file in issue.issue_files:
                if issue_file.confidence >= self.confidence and issue_file.priority >= self.priority:
                    selected_issue_files.append(issue_file)
                else:
                    ignored_issue_files.append(issue_file)

            filtered_issues.append(
                Issue(
                    description=issue.description,
                    issue_files=selected_issue_files,
                    ignored_issue_files=ignored_issue_files,
                    code_suggestion=issue.code_suggestion,
                )
            )
        return filtered_issues

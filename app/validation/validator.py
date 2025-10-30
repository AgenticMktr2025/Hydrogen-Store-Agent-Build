import reflex as rx
import re
from typing import TypedDict


class ValidationIssue(TypedDict):
    line: int
    message: str
    type: str


class CodeValidator:
    def validate_file(self, path: str, content: str) -> list[ValidationIssue]:
        issues = []
        lines = content.splitlines()
        backtick = chr(96)
        if content.strip().startswith(f"{backtick * 3}") and content.strip().endswith(
            f"{backtick * 3}"
        ):
            issues.append(
                {
                    "line": 1,
                    "message": "File contains markdown code fences.",
                    "type": "error",
                }
            )
        is_component = "app/components/" in path or "app/routes/" in path
        if is_component and (
            not re.search(
                "from ['\\\"]@shopify/hydrogen|from ['\\\"]@shopify/remix-oxygen|from ['\\\"]@shopify/hydrogen-react",
                content,
            )
        ):
            issues.append(
                {
                    "line": 1,
                    "message": "File may be missing key Shopify Hydrogen imports.",
                    "type": "warning",
                }
            )
        is_route = "app/routes/" in path
        if is_route:
            if "export async function loader" not in content:
                issues.append(
                    {
                        "line": 1,
                        "message": "Route is missing 'loader' export.",
                        "type": "warning",
                    }
                )
            if "export function meta" not in content:
                issues.append(
                    {
                        "line": 1,
                        "message": "Route is missing 'meta' export.",
                        "type": "warning",
                    }
                )
        return issues
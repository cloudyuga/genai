import pandas as pd
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from typing import Optional


# Initialize FastMCP server
mcp = FastMCP("hr")

HR_FOLDER = Path("hrdataset")
SURVEY_FILE = HR_FOLDER / "surveys" / "Employee_Culture_Survey_Responses.csv"

def read_markdown_file(file_path: Path) -> str:
    """Reads and returns content of a markdown file."""
    if not file_path.exists():
        return f"File {file_path.name} not found."
    return file_path.read_text(encoding="utf-8")

def find_employee_file(employee_name: str) -> Optional[Path]:
    """Search for an employee file based on their name (case-insensitive)."""
    employee_dir = HR_FOLDER / "employees"
    pattern = f"*{employee_name.replace(' ', '_')}*.md"
    matches = list(employee_dir.glob(pattern))
    if matches:
        return matches[0]
    # Try more flexible matching (lowercase, remove underscores)
    for path in employee_dir.glob("*.md"):
        if employee_name.replace(" ", "") in path.stem.replace("_", ""):
            return path
    return None

@mcp.tool()
async def get_employee_profile(employee_name: str) -> str:
    """Get the profile of a specific employee by name."""
    file_path = find_employee_file(employee_name)
    if not file_path:
        return f"Profile for '{employee_name}' not found."
    return read_markdown_file(file_path)

@mcp.tool()
async def get_employee_benefits() -> str:
    """Get the employee benefits information."""
    return read_markdown_file(HR_FOLDER / "policies" / "employee_benefits.md")

@mcp.tool()
async def get_leave_policies() -> str:
    """Get the company's leave policies."""
    return read_markdown_file(HR_FOLDER / "policies" / "leave_policies.md")

@mcp.tool()
async def get_training_and_development() -> str:
    """Get training and development resources."""
    return read_markdown_file(HR_FOLDER / "policies"  / "training_and_development.md")

@mcp.tool()
async def get_holiday_calendar() -> str:
    """Get the company's holiday calendar."""
    return read_markdown_file(HR_FOLDER / "policies" / "holiday_calendar.md")

@mcp.tool()
async def get_events_calendar() -> str:
    """Get the company's events calendar."""
    return read_markdown_file(HR_FOLDER / "policies" / "events_calendar.md")

@mcp.tool()
async def summarize_culture_survey() -> str:
    """Summarize the Employee Culture Survey (CSV)"""
    if not SURVEY_FILE.exists():
        return "Survey file not found."
    
    try:
        df = pd.read_csv(SURVEY_FILE)
        summary = df.describe(include="all").transpose()
        return summary.to_string()
    except Exception as e:
        return f"Error reading survey file: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from nooa import Agent
from nooa.unifiedllm.registry import get_llm_client
from pydantic import BaseModel


load_dotenv()


llm = get_llm_client(
    "openrouter/auto"
)


ALLOWED_FOLDERS = {
    "documents",
    "images",
    "code",
    "data",
    "notes",
}


class OrganizeReport(BaseModel):
    actions_taken: list[str]
    summary: str


class WorkspaceOrganizerAgent(Agent, llm=llm):
    """
    Organize files in a simulated workspace.

    Inspect the workspace, understand what each file is,
    move files into appropriate folders, and verify the
    final workspace state.

    Do not invent files or folders.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._workspace = {
            "annual_report.pdf": {
                "content": "Company annual financial report",
                "location": "unfiled",
            },
            "vacation_photo.png": {
                "content": "Photo taken during a beach vacation",
                "location": "unfiled",
            },
            "analysis.py": {
                "content": "Python script for analysing sales data",
                "location": "unfiled",
            },
            "sales_2026.csv": {
                "content": "Monthly sales figures for 2026",
                "location": "unfiled",
            },
            "project_ideas.md": {
                "content": "Notes containing ideas for future projects",
                "location": "unfiled",
            },
        }

    def list_files(self) -> list[str]:
        """Return every file currently in the workspace."""

        return list(self._workspace.keys())

    def inspect_file(
        self,
        filename: str,
    ) -> dict:
        """Return information about a file."""

        if filename not in self._workspace:
            return {
                "error": "File does not exist."
            }

        file = self._workspace[filename]

        return {
            "filename": filename,
            "extension": Path(filename).suffix,
            "content": file["content"],
            "location": file["location"],
        }

    def move_file(
        self,
        filename: str,
        destination: str,
    ) -> str:
        """Move a file into one of the allowed folders."""

        if filename not in self._workspace:
            return f"{filename} does not exist."

        if destination not in ALLOWED_FOLDERS:
            return (
                f"{destination} is not valid. "
                f"Allowed folders: {sorted(ALLOWED_FOLDERS)}"
            )

        old_location = self._workspace[
            filename
        ]["location"]

        self._workspace[
            filename
        ]["location"] = destination

        return (
            f"Moved {filename} from "
            f"{old_location} to {destination}."
        )

    def get_workspace_state(
        self,
    ) -> dict[str, list[str]]:
        """Return the current files grouped by folder."""

        state = {
            "unfiled": [],
            "documents": [],
            "images": [],
            "code": [],
            "data": [],
            "notes": [],
        }

        for filename, info in self._workspace.items():
            state[
                info["location"]
            ].append(filename)

        return state

    async def organize_workspace(
        self,
    ) -> OrganizeReport:
        """
        Organize the workspace autonomously.

        First call list_files().

        Inspect the files when needed using inspect_file().

        Move every unfiled file into the most appropriate
        folder using move_file().

        Available destination folders are:

        - documents
        - images
        - code
        - data
        - notes

        After moving the files, call get_workspace_state()
        to verify that no files remain unfiled.

        Return a short report describing the actions taken.
        """
        ...


async def main():
    agent = WorkspaceOrganizerAgent()

    print("BEFORE")
    print(
        json.dumps(
            agent.get_workspace_state(),
            indent=2,
        )
    )

    print("\nNOOA AGENT RUNNING...\n")

    report = await agent.organize_workspace()

    print("AGENT REPORT")
    print(
        report.model_dump_json(
            indent=2
        )
    )

    print("\nAFTER - ACTUAL PYTHON STATE")
    print(
        json.dumps(
            agent.get_workspace_state(),
            indent=2,
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
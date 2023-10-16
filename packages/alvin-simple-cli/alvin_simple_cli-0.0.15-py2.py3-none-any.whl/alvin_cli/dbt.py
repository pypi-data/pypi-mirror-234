import json
import logging
import os
import shutil
from typing import Dict
from typing import List

import requests
import typer
from git import Repo

from alvin_cli.config import settings
from alvin_cli.utils.common_arguments import ARTIFACTS_PATH
from alvin_cli.utils.common_arguments import DBT_PROJECT_NAME
from alvin_cli.utils.common_arguments import DBT_USER_EMAIL
from alvin_cli.utils.common_arguments import DW_PLATFORM_ID
from alvin_cli.utils.common_arguments import PLATFORM_ID
from alvin_cli.utils.helper_functions import console
from alvin_cli.utils.helper_functions import typer_secho_raise

app = typer.Typer(add_completion=False)


def __setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)


def list_json_artifacts(target_path: str) -> List[str]:
    try:
        items = os.listdir(target_path)
        items = [item for item in items if item.endswith(".json")]
        return items
    except FileNotFoundError:
        typer_secho_raise(f"`{target_path}` folder not found.", "RED")
        exit(1)


def get_invocation_id(target_path: str) -> str:
    with open(os.path.join(target_path, "manifest.json"), "r") as file:
        contents = json.load(file)
        return contents["metadata"]["invocation_id"]


def collect_zip(
    invocation_id: str,
    dbt_platform_id: str,
    bq_platform_id: str,
) -> None:
    files = [
        (
            "artifacts",
            ("artifacts.zip", open("artifacts.zip", "rb"), "application/zip"),
        )
    ]
    headers = {"X-API-Key": settings.alvin_api_token}
    upload_payload = {
        "platform_id": dbt_platform_id,
        "dw_platform_id": bq_platform_id,
        "invocation_id": invocation_id,
    }

    try:
        console.print("Sending artifacts to Alvin dbt API")
        response = requests.request(
            "POST",
            f"{settings.alvin_dbt_api_url}/upload",
            headers=headers,
            data=upload_payload,
            files=files,
        )
    except Exception as e:
        raise Exception(f"Error processing artifacts! {str(e)}")

    if response.status_code != 200:
        raise Exception(f"Error processing artifacts! {response.text=}")
    console.print("Artifacts processed successfully!")


def save_alvin_metadata(artifacts_path: str, meta: Dict) -> None:
    with open(os.path.join(artifacts_path, "alvin_metadata.json"), "w") as file:
        file.write(json.dumps(meta, default=str))


@app.command()
def process_artifacts(
    platform_id: str = PLATFORM_ID,
    dw_platform_id: str = DW_PLATFORM_ID,
    artifacts_path: str = ARTIFACTS_PATH,
    project_name: str = DBT_PROJECT_NAME,
    user_email: str = DBT_USER_EMAIL,
) -> None:
    """Process artifacts generated on dbt run commands"""

    json_artifacts = list_json_artifacts(artifacts_path)

    alvin_metadata = {
        "platform_id": platform_id,
        "project_name": project_name,
        "dw_platform_id": dw_platform_id,
        "user_email": user_email,
    }

    alvin_metadata.update(get_git_metadata())

    if len(json_artifacts) == 0 or "manifest.json" not in json_artifacts:
        typer_secho_raise("Can't process metadata", "RED")
        exit(1)

    invocation_id = get_invocation_id(artifacts_path)
    alvin_metadata["invocation_id"] = invocation_id
    save_alvin_metadata(artifacts_path, alvin_metadata)

    try:
        console.print(f"Processing artifacts ({invocation_id=})")
        shutil.make_archive("artifacts", "zip", artifacts_path)

        collect_zip(invocation_id, platform_id, dw_platform_id)
        console.print("Cleaning up")
        os.remove("artifacts.zip")
        console.print("Done")
    except Exception as e:
        typer_secho_raise(str(e), "RED")
        if "artifacts.zip" in os.listdir("."):
            os.remove("artifacts.zip")


def get_git_metadata() -> Dict:
    git_branch = None
    git_commit_sha = None
    git_commit_message = None
    git_commit_email = None
    try:
        repo = Repo(search_parent_directories=True)
        git_branch = repo.active_branch.name
        last_git_object = repo.head.object
        git_commit_sha = last_git_object.hexsha
        git_commit_message = last_git_object.message
        git_commit_email = last_git_object.committer.email
    except:
        if settings.alvin_verbose_log:
            logging.exception("Unable to fetch git metadata", exc_info=True)
    git_payload = {
        "git_branch": git_branch,
        "git_commit_sha": git_commit_sha,
        "git_commit_message": git_commit_message,
        "git_commit_email": git_commit_email,
    }
    return git_payload

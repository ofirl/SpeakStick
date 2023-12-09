from git.repo import Repo
import requests
import datetime
import logging
import re

import common.system_utils
import common.config_utils
from monitoring.logs_config import logFilesFolder


def runUpgrade(version=""):
    return common.system_utils.runCommandBackground(
        f"/opt/SpeakStick/upgrade-script.sh {version} >> {logFilesFolder}/upgrade.log"
    )


def isUpgradeRunning():
    return common.system_utils.is_process_running("upgrade-script")


def version_key(tag):
    # Split the tag into components: major, minor, patch, pre-release, and build
    match = re.match(r"v(\d+)\.(\d+)\.(\d+)(-(rc\d+))?(\+.+)?", tag)

    if match:
        major, minor, patch, pre_release, build = match.groups()

        # Convert major, minor, and patch to integers
        version_numbers = tuple(map(int, (major, minor, patch)))

        # Pre-release tags should come before actual releases
        # If there is a pre-release tag, add it to the tuple for sorting
        if pre_release:
            return version_numbers, pre_release
        else:
            return version_numbers, ()

    # If the tag doesn't match the expected pattern, return a high value
    return (float("inf"),)


def get_versions():
    try:
        development_builds = False
        configs = common.config_utils.get_configs(
            advanced=1, key="ENABLE_DEVELOPMENT_BUILDS"
        )
        if configs != None and len(configs) > 0:
            development_builds = configs[0].get("value") == "1"

        repo = Repo("/opt/SpeakStick")
        tags = [str(tag) for tag in repo.tags]

        if not development_builds:
            tags = [tag for tag in tags if "rc" not in tag and "dev" not in tag]

        tags.reverse()
        logging.info("tags", extra={"repo.tags": repo.tags, "tags": tags})
        # return tags
        return sorted(tags, reverse=True, key=version_key)

    except Exception as e:
        logging.exception(f"Error getting versions")
        return None


def get_current_version():
    try:
        repo = Repo("/opt/SpeakStick")
        return repo.git.describe(tags=True)

    except Exception as e:
        logging.exception(f"Error getting current version")
        return None


def update_available_versions():
    try:
        repo = Repo("/opt/SpeakStick")
        repo.git.fetch()
        return True

    except Exception as e:
        logging.exception(f"Error updating available versions")
        return None


def get_github_releases():
    try:
        repo = Repo("/opt/SpeakStick")

        # Extract owner and repo name from the remote URL
        remote_url_parts = repo.remotes.origin.url.split("/")
        owner = remote_url_parts[-2]
        repo_name = remote_url_parts[-1].replace(".git", "")

        # Send a GET request to the GitHub API
        response = requests.get(
            url=f"https://api.github.com/repos/{owner}/{repo_name}/releases"
        )

        # Check if the request was successful
        if response.status_code == 200:
            releases = response.json()

            # Extract title and description for each release
            release_info = []
            for release in releases:
                release_title = release.get("name", "N/A")
                release_description = release.get("body", "N/A")
                release_info.append(
                    {"title": release_title, "description": release_description}
                )

            return release_info, None
        else:
            error = None
            logging.error(
                f"Failed to retrieve releases. Status code: {response.status_code}"
            )
            if response.status_code == 403:
                timestamp = response.headers.get("x-ratelimit-reset")
                if timestamp is not None:
                    date = datetime.datetime.fromtimestamp(float(timestamp))
                    formatted_date = date.strftime("%Y-%m-%d %H:%M:%S")
                    error = (
                        f"Rate limit reached, limit will be reset at {formatted_date}"
                    )

            return None, error

    except requests.exceptions.RequestException as e:
        logging.exception(f"Error getting github release")
        return None, e.strerror

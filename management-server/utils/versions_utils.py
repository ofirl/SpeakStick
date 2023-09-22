from git.repo import Repo
import requests
import datetime

import utils.system_utils
import utils.db_utils


def runUpgrade(version=""):
    return utils.system_utils.runCommandBackground(
        f"/opt/SpeakStick/upgrade-script.sh {version}"
    )


def isUpgradeRunning():
    return utils.system_utils.is_process_running("upgrade-script.sh")


def get_versions():
    try:
        development_builds = False
        configs = utils.db_utils.get_configs(
            advanced=True, key="ENABLE_DEVELOPMENT_BUILDS"
        )
        if configs != None and len(configs) > 0:
            _, value, _, _ = configs[0]
            development_builds = value == 1

        repo = Repo("/opt/SpeakStick")
        tags = [str(tag) for tag in repo.tags]

        if not development_builds:
            tags = [tag for tag in tags if "rc" not in tag and "dev" not in tag]

        return sorted(tags, reverse=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_current_version():
    try:
        repo = Repo("/opt/SpeakStick")
        return repo.git.describe(tags=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def update_available_versions():
    try:
        repo = Repo("/opt/SpeakStick")
        repo.git.fetch()
        return True

    except Exception as e:
        print(f"An error occurred: {e}")
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
            print(f"Failed to retrieve releases. Status code: {response.status_code}")
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
        print(f"An error occurred: {e}")
        return None, e.strerror

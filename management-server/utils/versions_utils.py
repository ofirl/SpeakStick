from git.repo import Repo
import requests

import utils.system_utils


def switch_version(version):
    try:
        pid, err = utils.system_utils.runUpgrade(version)
        if err is not None or pid is None:
            raise BaseException("Error running upgrade script")

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_versions():
    try:
        repo = Repo("/opt/SpeakStick")
        tags = [str(tag) for tag in repo.tags]
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

            return release_info
        else:
            # Handle errors, e.g., repository not found
            print(f"Failed to retrieve releases. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

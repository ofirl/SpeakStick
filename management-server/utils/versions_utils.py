from git.repo import Repo

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

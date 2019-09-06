import subprocess


def message_variable(func):
    """
    Decorator which marks a function as being safe to use as a message variable.
    """
    func.is_message_variable = True
    return func


@message_variable
def git_branch():
    return subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, encoding="utf8"
    ).stdout.strip()


@message_variable
def git_commit_subject():
    return subprocess.run(
        ["git", "log", "-1", "--pretty=%s"], capture_output=True, encoding="utf8"
    ).stdout.strip()


@message_variable
def git_commit_author():
    return subprocess.run(
        ["git", "log", "-1", "--pretty=%an"], capture_output=True, encoding="utf8"
    ).stdout.strip()


@message_variable
def git_repository():
    repository_url = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"], capture_output=True, encoding="utf8"
    ).stdout.strip()
    return repository_url.rpartition("/")[2].partition(".")[0]

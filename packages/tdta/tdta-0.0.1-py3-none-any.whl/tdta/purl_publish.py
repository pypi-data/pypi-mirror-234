import os
import requests
import shutil
import subprocess
import logging

from typing import Optional

GITHUB_TOKEN_ENV = 'GITHUB_AUTH_TOKEN'
GITHUB_USER_ENV = 'GITHUB_USER'
GITHUB_EMAIL_ENV = 'GITHUB_EMAIL'

PURL_TAXONOMY_FOLDER_URL = 'https://github.com/brain-bican/purl.brain-bican.org/tree/main/config/taxonomy/'
PURL_REPO_NAME = 'purl.brain-bican.org'
PURL_REPO = 'brain-bican/{}'.format(PURL_REPO_NAME)

BRANCH_NAME_FORMAT = "{user_name}-taxonomy-{taxonomy_name}"

TOKEN_FILE = "mytoken.txt"


def publish_to_purl(file_path: str, taxonomy_name: str, user_name: str) -> str:
    """
    Publishes the given taxonomy to the purl system. First checks if PURL system already has a config for the given
    taxonomy. If not, makes a pull request to create a config.
    :param file_path: path to the project root folder
    :param taxonomy_name: name of the taxonomy
    :param user_name: authenticated GitHub username
    :return: url of the created pull request or the url of the existing PURL configuration.
    """
    work_dir = os.path.abspath(file_path)
    purl_folder = os.path.join(work_dir, "purl")

    if not os.environ.get(GITHUB_TOKEN_ENV):
        report_problem("'{}' environment variable is not declared. Please follow https://brain-bican.github.io/taxonomy-development-tools/Build/ to setup.".format(GITHUB_TOKEN_ENV), purl_folder)
    elif not os.environ.get(GITHUB_USER_ENV):
        report_problem("'{}' environment variable is not declared. Please follow https://brain-bican.github.io/taxonomy-development-tools/Build/ to setup.".format(GITHUB_USER_ENV), purl_folder)
    elif not os.environ.get(GITHUB_EMAIL_ENV):
        report_problem("'{}' environment variable is not declared. Please follow https://brain-bican.github.io/taxonomy-development-tools/Build/ to setup.".format(GITHUB_EMAIL_ENV), purl_folder)

    user_name = os.environ.get(GITHUB_USER_ENV)
    runcmd("git config --global user.name \"{}\"".format(user_name))
    runcmd("git config --global user.email \"{}\"".format(os.environ.get(GITHUB_EMAIL_ENV)))

    files = [f for f in os.listdir(purl_folder) if str(f).endswith(".yml")]
    if len(files) == 0:
        report_problem("PURL config file couldn't be found at project '/purl' folder.", purl_folder)
    else:
        purl_config_name = files[0]

    response = requests.get(PURL_TAXONOMY_FOLDER_URL + purl_config_name)
    if response.status_code == 200:
        print('PURL already exists: ' + (PURL_TAXONOMY_FOLDER_URL + purl_config_name))
    else:
        # create purl publishing request
        create_purl_request(purl_folder, os.path.join(purl_folder, purl_config_name), taxonomy_name, user_name)

    cleanup(purl_folder)
    return "DONE"


def report_problem(msg: str, purl_folder: str):
    """
    Logs the problem and raises an exception.
    :param msg: error message
    :param purl_folder: folder where temp files are created inside
    """
    print(msg)
    cleanup(purl_folder)
    raise Exception(msg)


def create_purl_request(purl_folder: str, file_path: str, taxonomy_name: str, user_name: str):
    """
    Creates a purl publishing request at the purl repository.
    :param purl_folder: path of the purl folder
    :param file_path: purl config file path
    :param taxonomy_name: name of the taxonomy
    :param user_name: github user name
    """
    gh_login(purl_folder)

    response = requests.get('https://github.com/{user}/purl.brain-bican.org'.format(user=user_name))
    if response.status_code == 200:
        report_problem('purl.brain-bican fork (https://github.com/{user}/purl.brain-bican.org) already exists. Aborting operation. Please delete the fork and retry.'.format(user=user_name), purl_folder)
    else:
        existing_pr = check_pr_existence(user_name, taxonomy_name)
        if existing_pr is not None:
            report_problem("Already have a related pull request: " + existing_pr, purl_folder)
        else:
            cleanup(purl_folder)
            clone_folder = clone_project(purl_folder, user_name)
            branch_name = create_branch(clone_folder, taxonomy_name, user_name)
            push_new_config(branch_name, file_path, clone_folder, taxonomy_name)
            create_pull_request(clone_folder, taxonomy_name)


def cleanup(purl_folder):
    """
    Cleanups all intermediate file/folders.
    :param purl_folder: path of the purl folder where intermediate files are added
    """
    delete_project(os.path.join(purl_folder, PURL_REPO_NAME))
    token_file = os.path.join(purl_folder, TOKEN_FILE)
    if os.path.exists(token_file):
        os.remove(token_file)


def gh_login(purl_folder):
    github_token = os.environ.get(GITHUB_TOKEN_ENV)
    token_file = os.path.join(purl_folder, TOKEN_FILE)
    with open(token_file, 'w') as f:
        f.write(github_token)

    runcmd("git config --global credential.helper store")
    runcmd("gh auth login --with-token < {}".format(token_file))
    runcmd("gh auth setup-git")

    return token_file


def check_pr_existence(user_name: str, taxonomy_name: str) -> Optional[str]:
    """
    Check if user already made a PR
    :param user_name: name of the user
    :param taxonomy_name: name of the taxonomy
    :return: url of the pull request if a PR already exists. Otherwise, returns None.
    """
    branch_name = BRANCH_NAME_FORMAT.format(user_name=user_name, taxonomy_name=taxonomy_name)
    my_prs = runcmd("gh pr list --author \"@me\" --repo {repo} --json title --json url --json headRefName".format(repo=PURL_REPO))
    for pr in my_prs:
        if "headRefName" in pr and pr["headRefName"] == branch_name:
            return pr["url"]
    return None


def delete_project(clone_folder):
    """
    Deletes the project folder and its content.
    :param clone_folder: path to the project folder
    """
    if os.path.exists(clone_folder):
        shutil.rmtree(clone_folder)


def create_pull_request(clone_folder, taxonomy_name):
    """
    Creates a Pull Request at the PURL repo.
    :param clone_folder: PURL project cloned folder
    :param taxonomy_name: name of the taxonomy
    """
    title = "{} taxonomy configuration".format(taxonomy_name)
    description = "New taxonomy configuration added for {}.".format(taxonomy_name)
    pr_url = runcmd(
        "cd {dir} && gh pr create --title \"{title}\" --body \"{body}\" --repo {repo}".format(dir=clone_folder,
                                                                                              title=title,
                                                                                              body=description,
                                                                                              repo=PURL_REPO))
    print("PURL creation Pull Request successfully created: " + pr_url)


def push_new_config(branch_name, file_path, clone_folder, taxonomy_name):
    """
    Adds the new taxonomy config to the PURL project and pushes to the branch.
    :param branch_name: name of the current working branch
    :param file_path: path to the config file
    :param clone_folder: PURL project clone folder
    :param taxonomy_name: name of the taxonomy
    """
    taxon_configs_folder = os.path.join(clone_folder, "config/taxonomy")
    config_name = os.path.basename(file_path)
    new_file = shutil.copyfile(file_path, os.path.join(taxon_configs_folder, config_name))
    runcmd("cd {dir} && git add {new_file}".format(dir=clone_folder, new_file=new_file))
    runcmd("cd {dir} && gh auth setup-git && git commit -m \"New taxonomy config for {taxonomy_name}\".".format(dir=clone_folder,
                                                                                           taxonomy_name=taxonomy_name))
    runcmd("cd {dir} && git push -u origin {branch_name}".format(dir=clone_folder, branch_name=branch_name))


def create_branch(clone_folder, taxonomy_name, user_name):
    """
    Creates a branch and starts working on it.
    :param clone_folder: PURL project cloned folder
    :param taxonomy_name: name of the taxonomy
    :param user_name: name of the user
    :return: name of the created branch
    """
    branch_name = BRANCH_NAME_FORMAT.format(user_name=user_name, taxonomy_name=taxonomy_name)
    runcmd("cd {dir} && gh auth setup-git && git branch {branch_name} && git checkout {branch_name}".format(
        dir=clone_folder, branch_name=branch_name))
    # runcmd(
    #     "cd {dir} && git remote remove origin && git remote add origin https://{user_name}:{gh_token}@github.com/{user_name}/{repo_name}.git".format(
    #         dir=clone_folder, gh_token=os.environ.get('GH_TOKEN'), user_name=user_name, repo_name=PURL_REPO_NAME))
    runcmd(
        "cd {dir} && git remote set-url origin https://{gh_token}@github.com/{user_name}/{repo_name}.git".format(
            dir=clone_folder, gh_token=os.environ.get('GH_TOKEN'), user_name=user_name, repo_name=PURL_REPO_NAME))
    runcmd("cd {dir} && git remote remove origin && git remote add origin https://{gh_token}@github.com/{user_name}/{repo_name}.git".format(dir=clone_folder, gh_token=os.environ.get('GH_TOKEN'), user_name=user_name, repo_name=PURL_REPO_NAME))

    return branch_name


def clone_project(purl_folder, user_name):
    """
    Forks and clones the PURL repository.
    :param purl_folder: folder to clone project into
    :param user_name: git username
    :return: PURL project clone path
    """
    runcmd("cd {dir} && gh repo fork {repo} --clone=true --remote=true --default-branch-only=true"
           .format(dir=purl_folder, repo=PURL_REPO))
    # runcmd("cd {dir} && gh repo clone {repo}".format(dir=purl_folder, repo=PURL_REPO))

    return os.path.join(purl_folder, PURL_REPO_NAME)


def runcmd(cmd):
    """
    Runs the given command in the command line.
    :param cmd: command to run
    :return: output of the command
    """
    logging.info("RUNNING: {}".format(cmd))
    p = subprocess.Popen([cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    (out, err) = p.communicate()
    logging.info('OUT: {}'.format(out))
    if err:
        logging.error(err)
    if p.returncode != 0:
        raise Exception('Failed: {}'.format(cmd))
    return out


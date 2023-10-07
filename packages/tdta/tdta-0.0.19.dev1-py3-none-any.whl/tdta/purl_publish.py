import os
import requests
import shutil
import subprocess
import logging

from typing import Optional


PURL_TAXONOMY_FOLDER_URL = 'https://github.com/brain-bican/purl.brain-bican.org/tree/main/config/taxonomy/'
PURL_REPO_NAME = 'purl.brain-bican.org'
PURL_REPO = 'brain-bican/{}'.format(PURL_REPO_NAME)
# PURL_TAXONOMY_FOLDER_URL = 'https://github.com/hkir-dev/purl.brain-bican.org/tree/main/config/taxonomy/'
# PURL_REPO_LOCAL = 'hkir-dev/purl.brain-bican.org'

BRANCH_NAME_FORMAT = "{user_name}-taxonomy-{taxonomy_name}"


def publish_to_purl(file_path: str, taxonomy_name: str, user_name: str) -> str:
    """
    Publishes the given taxonomy to the purl system. First checks if PURL system already has a config for the given
    taxonomy. If not, makes a pull request to create a config.
    :param file_path: path to the project root folder
    :param taxonomy_name: name of the taxonomy
    :param user_name: authenticated GitHub username
    :return: url of the created pull request or the url of the existing PURL configuration.
    """
    print("In PURL action 19.")
    # TODO delete
    # print(runcmd("git config --global user.name \"{}\"".format(user_name)))
    if not os.environ.get('GH_TOKEN'):
        raise Exception("'GH_TOKEN' environment variable is not declared. Please follow https://brain-bican.github.io/taxonomy-development-tools/Build/ to setup.")
    else:
        # TODO delete
        print(os.environ.get('GH_TOKEN'))
        print(runcmd("gh --version"))
        print(runcmd("gh auth status"))
        print(runcmd("gh auth setup-git"))
        print(runcmd("git --version"))
        print(runcmd("git config --list"))
        print(user_name)
        # print(runcmd("git config user.name"))

    work_dir = os.path.abspath(file_path)
    purl_folder = os.path.join(work_dir, "purl")
    files = [f for f in os.listdir(purl_folder) if str(f).endswith(".yml")]
    if len(files) == 0:
        raise Exception("PURL config file couldn't be found at project '/purl' folder.")
    else:
        purl_config_name = files[0]

    response = requests.get(PURL_TAXONOMY_FOLDER_URL + purl_config_name)
    if response.status_code == 200:
        print('PURL already exists: ' + (PURL_TAXONOMY_FOLDER_URL + purl_config_name))
    else:
        # create purl publishing request
        create_purl_request(purl_folder, os.path.join(purl_folder, purl_config_name), taxonomy_name, user_name)

    return "DONE"


def create_purl_request(purl_folder: str, file_path: str, taxonomy_name: str, user_name: str):
    """
    Creates a purl publishing request at the purl repository.
    :param purl_folder: path of the purl folder
    :param file_path: purl config file path
    :param taxonomy_name: name of the taxonomy
    :param user_name: github user name
    """
    # user_name = str(runcmd("gh auth setup-git && git config user.name")).strip()
    runcmd("gh auth setup-git")

    response = requests.get('https://github.com/{user}/purl.brain-bican.org'.format(user=user_name))
    if response.status_code == 200:
        raise Exception('purl.brain-bican fork (https://github.com/{user}/purl.brain-bican.org) already exists. Aborting operation. Please delete the fork and retry.'.format(user=user_name))
    else:
        existing_pr = check_pr_existence(user_name, taxonomy_name)
        if existing_pr is not None:
            raise Exception("Already have a related pull request: " + existing_pr)
        else:
            # TODO delete folder if exists
            clone_folder = clone_project(purl_folder, user_name)
            branch_name = create_branch(clone_folder, taxonomy_name, user_name)
            push_new_config(branch_name, file_path, clone_folder, taxonomy_name)
            create_pull_request(clone_folder, taxonomy_name)
            delete_project(clone_folder)


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
    print(branch_name)
    runcmd("cd {dir} && gh auth setup-git && git branch {branch_name} && git checkout {branch_name}".format(
        dir=clone_folder, branch_name=branch_name))
    runcmd(
        "cd {dir} && git remote remove origin && git remote add origin https://{user_name}:{gh_token}@github.com/{user_name}/{repo_name}.git".format(
            dir=clone_folder, gh_token=os.environ.get('GH_TOKEN'), user_name=user_name, repo_name=PURL_REPO_NAME))
    return branch_name


def clone_project(purl_folder, user_name):
    """
    Forks and clones the PURL repository.
    :param purl_folder: folder to clone project into
    :param user_name: git username
    :return: PURL project clone path
    """
    runcmd("cd {dir} && gh repo fork {repo} --clone=true --default-branch-only=true".format(dir=purl_folder,
                                                                                            repo=PURL_REPO))
    # runcmd("cd {dir} && gh repo clone {repo}".format(dir=purl_folder, repo=PURL_REPO))

    clone_path = os.path.join(purl_folder, PURL_REPO_NAME)
    runcmd("cd {dir} && git remote remove origin && git remote add origin https://{user_name}:{gh_token}@github.com/{user_name}/{repo_name}.git".format(dir=clone_path, gh_token=os.environ.get('GH_TOKEN'), user_name=user_name, repo_name=PURL_REPO_NAME))
    return clone_path


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


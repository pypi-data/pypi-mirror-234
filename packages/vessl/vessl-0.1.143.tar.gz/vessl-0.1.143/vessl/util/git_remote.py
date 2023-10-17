import os
import pathlib
import subprocess
import tempfile
from typing import List

from openapi_client import ResponseCodeRefsV2, ResponseGitHubCodeRef
from vessl import logger
from vessl.util.downloader import Downloader


def clone_codes(code_refs: List[ResponseGitHubCodeRef]):
    for code_ref in code_refs:
        if code_ref.git_provider == "github":
            prefix = "x-access-token"
            git_provider_domain = "github.com"
        elif code_ref.git_provider == "gitlab":
            prefix = "oauth2"
            git_provider_domain = "gitlab.com"
        else:
            prefix = "x-token-auth"
            git_provider_domain = "bitbucket.org"

        if code_ref.git_provider_custom_domain is not None:
            git_provider_domain = code_ref.git_provider_custom_domain

        if code_ref.token is None or code_ref.token == "":
            git_url = f"https://{git_provider_domain}/{code_ref.git_owner}/{code_ref.git_repo}.git"
        else:
            git_url = f"https://{prefix}:{code_ref.token}@{git_provider_domain}/{code_ref.git_owner}/{code_ref.git_repo}.git"
        if code_ref.mount_path:
            dirname = code_ref.mount_path
        else:
            dirname = code_ref.git_repo

        try:
            subprocess.run(["git", "clone", git_url, dirname])
        except subprocess.CalledProcessError:
            dirname = f"vessl-{code_ref.git_repo}"
            logger.info(f"Falling back to '{dirname}'...")
            subprocess.run(["git", "clone", git_url, dirname])

        if code_ref.git_ref:
            subprocess.run(["/bin/sh", "-c", f"cd {dirname}; git reset --hard {code_ref.git_ref}"])

        if code_ref.git_diff_file:
            diff_file_path = f"/tmp/{code_ref.git_repo}.diff"
            Downloader.download(
                code_ref.git_diff_file.path, diff_file_path, code_ref.git_diff_file, quiet=False
            )
            subprocess.run(["/bin/sh", "-c", f"cd {dirname}; git apply {diff_file_path}"])


def clone_codes_v2(code_refs: List[ResponseCodeRefsV2]):
    for code_ref in code_refs:
        mount_path = pathlib.Path(code_ref.mount_path)
        fallback = False
        if mount_path.exists():
            if mount_path.is_file():
                print(f"path {code_ref.mount_path} is a file.")
                fallback = True
            elif any(mount_path.iterdir()):
                print(f"path {code_ref.mount_path} is not empty.")
                fallback = True
        if fallback:
            print(f"Warning: cannot clone into {mount_path}")
            dirname = mount_path.parent
            subdir = f"vessl-{mount_path.name}"
            mount_path = dirname / subdir
            print(f"Alternatively trying to clone into f{dirname}/{subdir}...")
            print(f"This might affect the automated code execution")
        if code_ref.protocol == "http":
            url = code_ref.ref_http.url
            subprocess.run(["git", "clone", url, str(mount_path)]).check_returncode()
        elif code_ref.protocol == "ssh":
            if code_ref.ref_ssh.private_key:
                with tempfile.TemporaryFile() as key:
                    key.write(code_ref.ref_ssh.private_key)
                    os.chmod(key.name, 0o400)
                    subprocess.run(
                        ["git", "clone", code_ref.ref_ssh.host, str(mount_path)],
                        env={
                            "GIT_SSH_COMMAND": f"ssh -i {key.name}",
                        },
                    ).check_returncode()
            else:
                subprocess.run(
                    ["git", "clone", code_ref.ref_ssh.host, str(mount_path)]
                ).check_returncode()

        if code_ref.git_ref:
            subprocess.run(
                ["git", "checkout", code_ref.git_ref], cwd=str(mount_path)
            ).check_returncode()

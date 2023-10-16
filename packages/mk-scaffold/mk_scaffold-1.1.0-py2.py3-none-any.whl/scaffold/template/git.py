import atexit
import os
import shutil
import subprocess
import sys
import tempfile

from . import directory


def git_clone(url):
    git = shutil.which("git")
    if git is None:
        sys.exit("error: git executable was not found")

    # Create a temporary folder to be deleted at exit
    tmpdir = tempfile.mkdtemp(prefix="scaffold")

    def remove_tmpdir():
        shutil.rmtree(tmpdir)

    atexit.register(remove_tmpdir)
    try:
        git = shutil.which("git")
        subprocess.run([git, "clone", url, "repository", "--depth", "1"], cwd=tmpdir, check=True)

        template_dir = os.path.join(tmpdir, "repository")
        return directory.find(template_dir)
    except subprocess.CalledProcessError:
        sys.exit(f'error: failed to clone remote repository "{url}"')


def find(path):
    # Clone the repository
    #
    # TODO: We should not rely on the existance of git,
    # but rather detect, in order, from the url path if
    # it fits common sites (github.com, gitlab.com), if
    # it's prefixed such as git+http[s]://
    #

    return git_clone(path)

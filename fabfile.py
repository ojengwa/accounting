"""Summary."""

from fabric.api import local, task

from accounting import __version__


@task
def install(version=""):
    """Install project artifacts.

    Args:
        version (str, optional): Description
    """
    local("pip install -r requirements.txt")
    local("pip install -r test-requirements.txt")


@task
def clean():
    """Remove all the .pyc files."""
    local("find . -name '*.pyc' -print0|xargs -0 rm", capture=False)
    # Remove the dist folder
    local("rm -rf ./dist && rm -rf accounting.egg-info")
    local("rm -rf **__pycache__* && rm -rf coverage*")
    local("rm -rf ./temp && rm -rf ./build")


@task
def push(msg):
    """Push to github.

    Args:
        msg (str, required): Description
    """
    clean()
    local("git add . && git commit -m '{}'".format(msg))
    local("git push")


@task
def publish(msg="checkpoint: publish package"):
    """Deploy the app to PYPI.

    Args:
        msg (str, optional): Description
    """
    test = check()
    if test.succeeded:
        # clean()
        # push(msg)
        sdist = local("python setup.py sdist")
        if sdist.succeeded:
            build = local(
                'python setup.py build && python setup.py bdist_egg')
            if build.succeeded:
                upload = local("twine upload dist/*")
                if upload.succeeded:
                    tag()


@task
def check():
    """Test project."""
    test = local(
        "coverage erase && nosetests  --with-coverage "
        "--cover-package=accounting/"
    )



@task
def tag(version=__version__):
    """Deploy a version tag."""
    build = local("git tag {0}".format(version))
    if build.succeeded:
        local("git push --tags")

# roxbot



---

**Documentation**: [https://roxautomation.gitlab.io/roxbot](https://roxautomation.gitlab.io/roxbot)

**Source Code**: [https://gitlab.com/roxautomation/roxbot](https://gitlab.com/roxautomation/roxbot)


---

KISS robootics framework


## Development

**Please develop inside the container**, this will ensure all the required checks (`pylint` & `mypy`) as well as formatting (`black`)

If you are not familiar with devcontainers, read [Developing inside a Container](https://code.visualstudio.com/docs/devcontainers/containers) first

1. Clone this repository
2. open dir in *VS Code* `vscode .`
3. rebuild and reopen in container (you'll need `Dev Containers` extension)

**note**: if a container with `devcontainer` name already exists, an error will occur. You can remove it with
`docker container prune -f`


### What goes where

* `gitlab-ci.yml` - gitlab ci script
* `.devcontainer/requirements.txt` packages required for development
* `setup.py` - main packge setup file (cli scripts, dependencies etc.)
* `docs` - documentation, uses mkdocs
* `install` - scripts for preparing host system

### Version control

use `bumpversion major/minor/patch` to update version number.

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code.

run `serve_docs.sh` from inside the container to build and serve documentation.

**note:** `pyreverse` creates images of packages and classes in `docs/uml/..`

### Pre-commit

optional. Add `precommit install` to `init_container.sh` if required.

This project was forked from [cookiecutter template](https://gitlab.com/sjev/python-template) template.

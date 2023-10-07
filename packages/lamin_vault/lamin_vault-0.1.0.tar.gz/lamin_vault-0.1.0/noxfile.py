from typing import Mapping, Optional

import nox
from laminci.nox import run_pre_commit, run_pytest
from nox import Session

# we'd like to aggregate coverage information across sessions
# and for this the code needs to be located in the same
# directory in every github action runner
# this also allows to break out an installation section
nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session()
def build(session):
    session.run(*"pip install -e .[dev]".split())
    login_lnci(session)
    run_pytest(session)
    # build_docs(session, strict=True)


def login_lnci(session: Session, env: Optional[Mapping] = None):
    login_laminapp_admin = "lamin login ci@lamin.ai --password m7HuXoCPc2V76mWn"  # noqa
    session.run(*(login_laminapp_admin.split(" ")), external=True, env=env)

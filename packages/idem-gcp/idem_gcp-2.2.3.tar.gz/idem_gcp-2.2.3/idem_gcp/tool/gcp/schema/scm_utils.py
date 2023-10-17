import json
import os
import shutil
import subprocess
import tempfile

script_template = """
cd "{clone_dir}"
git clone "{official_repo_url}"
cd "{work_dir}"
git checkout --quiet {rev}
python -m venv venv
source "{work_dir}"/venv/bin/activate
pip uninstall -q -y --disable-pip-version-check --require-virtualenv idem-gcp
pip install -q --disable-pip-version-check --require-virtualenv -e .
idem doc states.gcp --output=json > "{out_file}"
"""


def get_idem_doc(idem_cli, doc_path):
    return idem_cli("doc", doc_path).json


def fetch_current_states_schema(hub, idem_cli):
    return get_idem_doc(idem_cli, "states.gcp")


def fetch_current_exec_schema(hub, idem_cli):
    return get_idem_doc(idem_cli, "exec.gcp")


# !!! important - currently you can't fetch schemas from other than the latest changeset in forked repos
def fetch_states_schema_from_official_repo(hub, official_repo_url: str, rev: str):
    tmp_dir = tempfile.mkdtemp()
    try:
        return json.loads(_fetch_schema_for_rev(official_repo_url, rev, tmp_dir))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _fetch_schema_for_rev(official_repo_url: str, rev: str, clone_dir: str):
    out_file = os.path.abspath(os.path.join(clone_dir, f"{rev}.json"))
    work_dir = os.path.join(
        clone_dir, os.path.splitext(os.path.basename(official_repo_url))[0]
    )

    script_file = f"schema-{rev}.sh"
    command = ["/bin/bash", script_file]

    with open(os.path.join(clone_dir, script_file), "w") as f:
        script = script_template.format(
            **{
                "clone_dir": clone_dir,
                "official_repo_url": official_repo_url,
                "rev": rev,
                "out_file": out_file,
                "work_dir": work_dir,
            }
        )
        f.write(script)

    print(f"Fetching schema for commit/tag {rev}")

    ret = subprocess.run(
        command,
        cwd=clone_dir,
        capture_output=True,
    )

    if not ret or ret.returncode != 0:
        print(f"Error fetching schema: {str(ret.stderr, 'utf-8')}")
        return None

    with open(os.path.join(work_dir, out_file)) as f:
        result = f.read()

    if result:
        end_mark = result.rfind("}")
        if end_mark != -1:
            result = result[: end_mark + 1]

    return result

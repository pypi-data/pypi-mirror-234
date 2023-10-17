import os
import pathlib

import git
import jinja2
import pkg_resources

package = __name__.split(".")[0]
templates_dir = pathlib.Path(pkg_resources.resource_filename(package, "templates"))
loader = jinja2.FileSystemLoader(searchpath=templates_dir)
env = jinja2.Environment(loader=loader, keep_trailing_newline=True)


def render_templates(project_path: pathlib.Path, commit_changes: bool = True):
    makefile(project_path)
    goreleaser(project_path)
    github_workflows_ci(project_path)
    github_workflows_release(project_path)
    create_gitingore(project_path)
    commit_boilerplate_files(project_path, commit_changes)


def create_gitingore(_dir: pathlib.Path):
    gitignore = _dir / ".gitignore"
    gitignore.touch()

    # Check if 'dist/' is already in .gitignore
    if "dist/" not in gitignore.read_text():
        # Append 'dist/' to .gitignore
        with gitignore.open(mode="a") as f:
            f.write("\ndist/\n")


def goreleaser(path: pathlib.Path):
    template = env.get_template("goreleaser.yaml.j2")
    out_path = pathlib.Path(".goreleaser.yaml")

    data = {
        "new_app_name": pathlib.Path(path).name,
    }
    out = template.render(data=data)
    out_path.write_text(out)


def makefile(path: pathlib.Path):
    makefiles = [
        {"tpl": "Makefile.j2", "out": "Makefile"},
        {"tpl": "Makefile2.j2", "out": "Makefile2"},
    ]

    for makefile in makefiles:
        template = env.get_template(makefile["tpl"])
        out_path = pathlib.Path(makefile["out"])

        data = {
            "new_app_name": pathlib.Path(path).name,
        }
        out = template.render(data=data)
        out_path.write_text(out)


def github_workflows_ci(path: pathlib.Path):
    template = env.get_template("github_ci.yml")
    out_path = pathlib.Path.cwd() / ".github/workflows/ci.yml"
    out_path.parent.mkdir(exist_ok=True, parents=True)

    data = {
        "new_app_name": pathlib.Path(path).name,
    }
    out = template.render(data=data)
    out_path.write_text(out)


def github_workflows_release(path: pathlib.Path):
    template = env.get_template("github_release.yml")
    out_path = pathlib.Path.cwd() / ".github/workflows/release.yml"
    out_path.parent.mkdir(exist_ok=True, parents=True)

    data = {
        "new_app_name": pathlib.Path(path).name,
    }
    out = template.render(data=data)
    out_path.write_text(out)


def commit_boilerplate_files(project_path: pathlib.Path, commit_changes: bool):
    if not commit_changes:
        print(f"There are no changes to commit in {pathlib.Path.cwd()}, exitting.")
        return

    git_dir = project_path / ".git"
    if not os.path.isdir(git_dir):
        print(f"Dir {git_dir} does not exist. The new files have not been committed.")
        return

    repo = git.Repo(project_path)
    boilerplate_files = [
        ".gitignore",
        ".goreleaser.yaml",
        "Makefile",
        ".github/workflows/ci.yml",
        ".github/workflows/release.yml",
    ]

    # Add boilerplate files to git
    for file in boilerplate_files:
        repo.git.add(file)

    # Commit boilerplate files
    repo.index.commit("Boilerplate")

import subprocess
import typing

import semver


def get_latest_git_tag(
        default_or_error: typing.Literal["default", "error"] = "default",
        default: str = "0.0.0"
) -> str:
    try:
        process_output = subprocess.check_output("git describe --tags --abbrev=0")
        tag = process_output.strip().decode()
    except subprocess.CalledProcessError:
        if default_or_error == "default":
            print(f"No git tag found. Using default git tag {default}.")
            tag = default
        elif default_or_error == "error":
            raise AssertionError("git describe --tags --abbrev=0 failed to return a tag.")
        else:
            raise ValueError("default_or_error should be 'default' or 'error'")
    return tag


def get_poetry_project_version(
        default_or_error: typing.Literal["default", "error"] = "default",
        default: str = "0.0.0"
) -> str:
    import tomllib
    with open("pyproject.toml", "rb") as fp:
        version = tomllib.load(fp).get("tool", {}).get("poetry", {}).get("version")
    if version is None:
        print(f"No poetry project version found.")
        if default_or_error == "default":
            print(f"Using default poetry project version {default}.")
            version = default
        elif default_or_error == "error":
            raise
        else:
            raise ValueError("default_or_error should be 'default' or 'error'")
    return version


def main():
    tag_version = get_latest_git_tag()
    tag_version = semver.Version.parse(tag_version)
    project_version = get_poetry_project_version()
    project_version = semver.Version.parse(project_version)
    if project_version <= tag_version:
        print(f"Should bump project version. Poetry project version: {project_version} <= Git tag version: {tag_version}.")
        next_version = tag_version.next_version(part="patch")
        subprocess.run(f"poetry version {next_version}")
    else:
        print(f"Shouldn't bump project version. Poetry project version: {project_version} > Git tag version: {tag_version}")


if __name__ == '__main__':
    raise SystemExit(main())

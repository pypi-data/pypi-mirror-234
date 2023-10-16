# pre-commit-hook-poetry-auto-semver
A pre-commit hook to auto-increment the poetry project's version when source code changes.

## Using pre-commit-hook-poetry-auto-semver

Add this to your `.pre-commit-config.yaml`
```yaml
-   repo: https://github.com/ipear3/pre-commit-hook-poetry-auto-semver
    rev: '0.0.1'
    hooks:
    -   id: poetry-auto-semver
```

## Hooks available
### `poetry-auto-semver`

Check whether the poetry project's version is greater than the current git tag version.
If the poetry project's version is less than or equal to the current git tag version, increment the project's patch version.
If the poetry project's version is greater than the current git tag version, the developer has already incremented the project's version.

Pre-configured to run on `push` affecting `files: src.*|.*py|poetry.lock|pyproject.toml`.

## Development

1. `poetry install`
2. `pre-commit install`

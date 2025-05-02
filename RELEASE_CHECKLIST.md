# Release Workflow Checklist

## Pre-Release Checks

- [ ] All tests passing locally
- [ ] All pre-commit hooks passing
- [ ] Documentation is up to date
- [ ] CHANGELOG.md is updated

## Version Update

- [ ] Update version in `src/chimera/__init__.py`
- [ ] Update version in `setup.py`
- [ ] Update version in `Dockerfile.test`

## Build and Test Locally

- [ ] Clean previous builds: `rm -rf build/ dist/`
- [ ] Build package: `python -m build`
- [ ] Build macOS executable: `./build_executables.sh`
- [ ] Build Linux executable: `docker build -t chimera-build -f Dockerfile.build .`
- [ ] Extract Linux executable: `docker cp $(docker create chimera-build):/app/dist/chimera-stack-cli ./releases/chimera-stack-cli-linux`
- [ ] Test macOS executable: `./releases/chimera-stack-cli --version`
- [ ] Test Linux executable in Docker: `docker run --rm -v $(pwd)/releases:/test ubuntu /test/chimera-stack-cli-linux --version`

## Git Operations

- [ ] Create git tag: `git tag v{version}`
- [ ] Push tag: `git push origin v{version}`
- [ ] Push all changes: `git push origin main`

## PyPI Deployment

- [ ] Upload to PyPI: `python -m twine upload dist/*`
- [ ] Verify package on PyPI: https://pypi.org/project/chimera-stack-cli/
- [ ] Test installation: `pipx install chimera-stack-cli=={version} --force`

## GitHub Release

- [ ] Create new release on GitHub
- [ ] Upload macOS executable
- [ ] Upload Linux executable
- [ ] Add release notes from CHANGELOG.md

## Post-Release

- [ ] Verify installation works on macOS: `pipx install chimera-stack-cli`
- [ ] Verify installation works on Linux (using Docker)
- [ ] Update documentation if needed
- [ ] Close related issues and PRs

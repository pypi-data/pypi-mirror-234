# Make a release

GeoVisio uses [semantic versioning](https://semver.org/) for its release numbers.

__ℹ️ Note__ : make sure that versions are in-sync with other GeoVisio components. Each component can have different `PATCH` versions, but compatibility __must__ be ensured between `MAJOR.MINOR` versions.

⚠️ This is particularly true for __web viewer__: as API [default templates](../geovisio/templates/) embed web viewer based on `MAJOR.MINOR` version, viewer __must be__ released before API to avoid issues.

Run these commands in order to issue a new release:

```bash
git checkout develop

vim ./geovisio/setup.cfg		# Change metadata.version
vim ./geovisio/__init__.py	# Change __version__

vim CHANGELOG.md	# Replace unreleased to version number

git add *
git commit -m "Release x.x.x"
git tag -a x.x.x -m "Release x.x.x"
git push origin develop
git checkout main
git merge develop
git push origin main --tags
```

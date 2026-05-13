# Contributing to jules

This repository uses `changie`-managed release notes and a tag-driven GitHub release workflow.

See `README.md` for repository-specific setup, tooling, and local development commands.

## Pull request workflow

1. Create a branch from the repository default branch
2. Make the change and run the local checks documented in `README.md`
3. Add a `changie` fragment for any change that should appear in release notes
4. Open a pull request and merge it to the default branch

## Changie workflow

Install `changie` locally — see the [official installation guide](https://changie.dev/guide/installation) for all available methods.

Add one unreleased fragment per logical change:

```bash
changie new --interactive=false --kind Added --body 'New `jules` change description'
```

Valid kinds are:

- `Added`
- `Changed`
- `Deprecated`
- `Removed`
- `Fixed`
- `Security`

Fragments are written to `.changes/unreleased/`.

## Release flow

Releases are driven by pushing a semantic version tag like `v0.1.0`.

### 1. Prepare the release notes

Batch unreleased fragments into a versioned release file:

```bash
changie batch 0.1.0
```

> Do not include the `v` prefix in `changie batch`.
> `changie batch v0.1.0` creates the wrong filename.

Merge the versioned release notes into `CHANGELOG.md`:

```bash
changie merge
```

### 2. Commit and merge the release changes

Commit the generated files, then make sure that commit is merged to the repository default branch before tagging.

### 3. Tag the merged release commit

Create and push the release tag:

```bash
git tag v0.1.0
git push origin refs/tags/v0.1.0
```

## What the release workflow does

When a `v*` tag is pushed, GitHub Actions will:

1. Verify the tag points to a commit on the repository default branch
2. Verify `.changes/<version>.md` exists
3. Publish the GitHub release using the changie release notes

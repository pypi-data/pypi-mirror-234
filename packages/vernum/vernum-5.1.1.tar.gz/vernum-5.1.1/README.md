# VerNum


Version numbering for project releases

<a href="https://www.flaticon.com/free-icons/rat" title="rat icons">Rat icons created by Freepik - Flaticon</a>

## Warning: Breaking Changes

Starting in VerNum v4.0.0:

- No longer generates a `.version` file - file generation is the responsibility of an outer script
- Includes `alpha` and `beta` increments
- Supports the `--set-current` option to receive the current version number from a source other than Git tags
- Requires an increment - `patch` is no longer the default
- No longer checks Git status before proceeding
- No longer provides the option to automatically update the Git tag, and no longer supports the `dry-run` option

## Default functionality

- Read the Git tags in the current branch that match the pattern e.g. "v5.6.1" and pick the highest value
- Increment the version number for major, minor, patch, alpha, or beta releases
- Return the new version for later use

## Installation

Requires Python 3 to run the command; your project can be anything.

```
pip3 install vernum
```


## Usage (CLI)

Requirements:

- CD to the root of the project before running it
- Be on the branch that you use for releases (i.e. `master`)
- Be fully up-to-date in git (i.e. merged, committed, and pushed)

Then run the command, specifying the increment to trigger the change:

- `major` change e.g. 5.6.2 to 6.0.0
- `minor` change e.g. 5.6.2 to 5.7.0
- `patch` change e.g. 5.6.2 to 5.6.3
- `beta` change e.g. 5.7.beta3 to 5.7.beta4
- `alpha` change e.g. 5.7.alpha8 to 5.7.alpha9
- Leave it out for no change, just to view the current version

## Source of truth

The default behaviour assumes that the source of truth for the current version comes from the highest valued Git tag in the current branch (based on a regular expression match) but VerNum does not actually update the Git tag. Note that a "v" at the beginning of the input version number is optional; it's not included in the output.

Alternatively, use the `--set-current` option to define a different current version to reference rather than a Git tag. The override is useful for:

- Bootstrapping a repo that has previous versions
- Using a downstream system as the source of truth for version numbers (such as an artifact repository)
- Fixing errors in the Git tag history

To update the Git tag, try something like:

```bash
vernum patch
git tag -a "cat $(.version)" -m "cat $(.version)"
git push origin "cat $(.version)"
```

## Usage (GitLab CI/CD)

VerNum is designed for use withing GitLab CI/CD, and includes a CI/CD configuration template to support the most common use cases.

Use the provided `vernum.gitlab-ci.yml` to use it in GitLab. Here's an example:

```yaml
include:
  - project: 'vernum/vernum'
    ref: stable
    file: 'vernum.gitlab-ci.yml'

stages:
  - Build
  - Test
  - Pre-release
  - Release
  - Post-release

deliver:
    stage: Post-release
    script:
        - echo "Edit this script to deploy or distribute v$(cat .version)"
```

The CI/CD template will provide a set of manual jobs following the rules:

- Numbered version increments (patch, minor, major) only on the default branch
- Alpha and beta increments only on branches that start with `next-`

Usage:

1. Go to the pipeline view in GitLab for the project and choose the latest pipeline on the appropriate branch
2. Confirm the pipeline represents the commit you intend to release
3. Go into the "Latest version info" when it's done, and confirm that the latest version number is accurate
4. Click the "play" button on the appropriate release job (major, minor, alpha, etc.)
5. **After the release job is complete** play the "Increment Version" job - it will fail if played too soon
6. When the "Mark Release in GitLab" job is complete, go into it to confirm the new version


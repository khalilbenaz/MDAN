# How to: update and release channels

## Regular update

```bash
npx mdan-method@latest update
```

Re-installs with the options recorded from your original install (language, modules, IDEs, user, scale) — you don't repeat `--lang`/`--modules`/etc unless you want to change them. `mdan update --lang en` changes just that key.

## How conflicts are handled

Every installed file is hash-tracked in `_mdan/_config/files-manifest.csv`. On update:

- A file you never touched (hash unchanged since install) is silently updated to the new version.
- A file you edited is **never overwritten** — the incoming version is written next to it as `<file>.mdan-new` so you can diff and merge by hand.
- `--force` overwrites your edits with the incoming version (careful — this discards your changes for tracked files).

In `config.yaml` files, only the managed keys (`user_name`, `communication_language`, `project_name`, `project_scale`) are updated; anything else you added there is left alone.

`_mdan/custom/` (your [agent customizations](customize-agents.md)) is never touched by install or update.

## Release channels

```bash
npx mdan-method update --channel latest     # the current npm "latest" dist-tag
npx mdan-method update --channel next       # a pre-release / next dist-tag, if published
npx mdan-method update --channel 4.1.0      # an exact pinned version
```

`--channel` works on both `install` and `update`. Under the hood it delegates to `npx -y mdan-method@<channel> install|update` — i.e. it downloads and runs that exact published version's installer against your project, so the channel governs which installer logic runs, not just which content is copied.

## Checking what's installed

```bash
mdan status                          # workflow/agent progress
cat _mdan/_config/manifest.yaml      # installed version, modules, IDEs, install/update dates
```

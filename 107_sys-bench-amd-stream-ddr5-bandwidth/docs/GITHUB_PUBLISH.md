# Publishing this workload repository to GitHub

This generated workload is designed to be published as its own independent GitHub repository.

GitHub repository name = the `Repo Name` field in `benchmark_specification.json` (for example `gpu-bench-amd-babelstream-hbm-bandwidth`). The local folder may still be `115_<Repo Name>`. Keep the workload number in the local folder and in the GitHub **description**; do not put it in the GitHub slug unless you deliberately choose to.

## Pre-publish check

Copy the generated workload to a publish tree (do not destroy the only generation copy), then:

```bash
bash scripts/prepare_github_publish.sh --dry-run
bash scripts/prepare_github_publish.sh --apply --github-owner=YOUR_GITHUB_USER
bash scripts/check_github_publish_ready.sh --published
```

`prepare_github_publish.sh` removes generator leftovers (nested copies, template-only docs, generation-only scripts and schemas), converts CRLF to LF, replaces `<org>` clone URLs, and makes GitHub Actions clone-safe. It does not commit or push. If you must clean the generation tree itself, pass `--in-place`.

The `--published` readiness check verifies leftover files are gone, README relative links resolve, ignore rules are present, and host-safe syntax checks pass.

## Initialize and publish

Create the remote repository on GitHub using the `Repo Name` value, then run locally:

```bash
git init
git branch -M main
git add .
git status
git commit -m "Initial benchmark workload"
git remote add origin https://github.com/GaryMichaelBass/<REPOSITORY>.git
git push -u origin main
```

Suggested GitHub description: `Workload <number>: <Repo Name>`. Add topics such as `amd`, `rocm`, `benchmark`, and the workload family (`perf`, `hipmemcpy`, `babelstream`, and so on).

Before committing, review `git status` carefully. The nested `TEMPLATE_*_copy/` generation workspace, runtime results, virtual environments, downloaded weights, logs, and credentials are intentionally excluded by `.gitignore` and must not be published.

## GitHub Actions

- `.github/workflows/ci.yml` performs host-safe linting, schema validation, structural validation, and publication-readiness checks on GitHub-hosted runners. It does not install GPU software or execute the benchmark.
- `.github/workflows/nightly.yml` is intended for a self-hosted runner labeled `gpu`. It is manual-only by default; add a schedule only after attaching an appropriate GPU runner and reviewing workload costs/dependencies.

## Required legal files

Keep the root `LICENSE` and `legal/NOTICE` with the repository.

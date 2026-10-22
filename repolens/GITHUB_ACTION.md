# GitHub Action

`.github/workflows/repolens.yml` runs ReproLens on pull requests and uploads the generated report as an artifact.

The current workflow is intentionally read-only: it audits the repository and uploads `repolens-report/`. A follow-up version can add PR comments and suggested patches after the core benchmark is stable.

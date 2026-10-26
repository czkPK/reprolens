# Security Policy

## Supported scope

ReproLens is a static audit tool. It does not execute untrusted repository code by default.

## Safety rules

- The web interface accepts public `https://github.com/owner/repo` URLs only.
- Repository files are treated as untrusted text.
- `--execute` is disabled in the web interface.
- AutoFix writes only to an isolated staging copy.
- API keys and access tokens must never be committed or written into reports.
- Third-party repository source and staging copies must not be included in release archives.

## Reporting a vulnerability

Please open a private security advisory or contact the maintainer through the GitHub repository. Do not publish exploit details before a fix is available.

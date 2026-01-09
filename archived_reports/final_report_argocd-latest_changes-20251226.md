## Overview of Argo CD latest changes (as of 2025-12-26)

The Argo CD project has released multiple updates in the 3.x line, including release candidates, and announced end-of-life for the 2.14.x line. This report compiles release notes, changelog references, upgrade guidance, and security advisories up to the stated date. Citations reference official release notes, upgrade documentation, and security advisories.

### Release activity and notes

- Argo CD v3.3.0-rc3 released on 2025-12-19. The release page includes a full changelog and links to the complete changelog; see https://github.com/argoproj/argo-cd/releases/tag/v3.3.0-rc3 [2].
- Argo CD v3.3.0-rc2 released on 2025-12-17; RC2 includes its own changelog entries and links to the release notes [3].
- Argo CD v3.2.3 released on 2025-12-24; the page includes a "Release Notes Blog Post" and assets; see https://github.com/argoproj/argo-cd/releases/tag/v3.2.3 [4].
- End-of-Life: Argo CD v2.14.21 released on 2025-11-04; final release in the 2.14.x line; upgrade to a supported 3.x version is recommended [5].

- The overall Argo CD releases index is available at https://github.com/argoproj/argo-cd/releases [1].

### Upgrade guidance and deprecations

- Upgrade guidance and breaking-change handling are documented in the Upgrading Overview page. It outlines upgrade steps for moving across minor/major versions and the recommended approaches for non-HA and HA deployments: https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/ [13].
- Notable deprecations are tied to the 2.14.x end-of-life signal; there are no widely documented explicit 3.x deprecations in the RC-era notes referenced here, but upgrading across versions should always review the specific release notes for any deprecations when moving across minor versions [5].

### Security advisories and CVEs

- Security advisories overview page: https://github.com/argoproj/argo-cd/security/advisories [6].
- Specific advisories:
  - GHSA-786q-9hcg-v9ff (Credential exposure; unauthenticated remote DoS): https://github.com/argoproj/argo-cd/security/advisories/GHSA-786q-9hcg-v9ff [7].
  - GHSA-gpx4-37g2-c8pv (Unauthenticated DoS via malformed Azure DevOps webhook): https://github.com/argoproj/argo-cd/security/advisories/GHSA-gpx4-37g2-c8pv [8].
  - GHSA-f9gq-prrc-hrhc (Unauthenticated DoS via malformed Bitbucket-Server webhook): https://github.com/argoproj/argo-cd/security/advisories/GHSA-f9gq-prrc-hrhc [9].

- CVE-2025-55190 (Credential exposure):
  - Advisory: ASEC CVE-2025-55190: https://asec.ahnlab.com/en/90101/ [10].
  - Independent coverage: ZeroPath CVE-2025-55190 info disclosure: https://zeropath.com/blog/argo-cd-cve-2025-55190-info-disclosure-summary [11].
  - Security overview: Codefresh Argo CD security overview: https://codefresh.io/learn/argo-cd/argo-security/ [12].

### Upgrade path, patching, and best practices

- Upgrading guidance: The primary upgrade reference when moving across minor/major versions is the Upgrading Overview (docs). It provides recommended upgrade flow and notes on breaking changes: https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/ [13].
- The End-of-Life signal for 2.14.x means upgrading to a supported 3.x version is recommended; verify release notes for any deprecations or breaking changes during the upgrade [5].

### How to use this information

- If planning an upgrade, start with the Upgrading Overview to map a path (e.g., from 2.x/3.0/3.1 up to 3.2 or 3.3 series). Then consult specific release notes for breaking changes or upgrade steps, and finally review security advisories to apply patches and mitigate CVEs [13].

### Notable considerations

- End-of-Life deprecation signals are most explicit for 2.14.x; no explicit 3.x deprecations are highlighted in the RC-era notes referenced here; always verify the specific release notes when upgrading across minor versions [5].

### Conclusion

The latest publicly visible changes in Argo CD as of 2025-12-26 include RC and patch releases in the 3.x line, ongoing security advisories with several high-severity issues, and a clear upgrade path via the official upgrading guidance. The 2.14.x line has reached end-of-life, so prioritizing a move to a supported 3.x release is advisable for security and feature support.

### Sources
[1] GitHub Releases - Argo CD: https://github.com/argoproj/argo-cd/releases
[2] Argo CD v3.3.0-rc3 release page: https://github.com/argoproj/argo-cd/releases/tag/v3.3.0-rc3
[3] Argo CD v3.3.0-rc2 release page: https://github.com/argoproj/argo-cd/releases/tag/v3.3.0-rc2
[4] Argo CD v3.2.3 release page: https://github.com/argoproj/argo-cd/releases/tag/v3.2.3
[5] Argo CD v2.14.21 release page (End-of-Life): https://github.com/argoproj/argo-cd/releases/tag/v2.14.21
[6] Argo CD Security Advisories (general): https://github.com/argoproj/argo-cd/security/advisories
[7] GHSA-786q-9hcg-v9ff advisory: https://github.com/argoproj/argo-cd/security/advisories/GHSA-786q-9hcg-v9ff
[8] GHSA-gpx4-37g2-c8pv advisory: https://github.com/argoproj/argo-cd/security/advisories/GHSA-gpx4-37g2-c8pv
[9] GHSA-f9gq-prrc-hrhc advisory: https://github.com/argoproj/argo-cd/security/advisories/GHSA-f9gq-prrc-hrhc
[10] ASEC CVE-2025-55190 advisory: https://asec.ahnlab.com/en/90101/
[11] ZeroPath CVE-2025-55190 information: https://zeropath.com/blog/argo-cd-cve-2025-55190-info-disclosure-summary
[12] Codefresh Argo CD security overview: https://codefresh.io/learn/argo-cd/argo-security/
[13] Argo CD Upgrading Overview (docs): https://argo-cd.readthedocs.io/en/stable/operator-manual/upgrading/overview/
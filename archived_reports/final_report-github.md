## Overview of latest features and changes in GitHub Actions (as of 2025-12-26)

GitHub Actions has continued to evolve toward greater automation, security, and scalability. The most notable developments through late 2025 include expanded capabilities for reusable workflows, broader and more capable runner options, security posture improvements, and ongoing sunset/migration efforts for older runtimes and artifacts. The information summarized here draws on the GitHub Changelog entries published in early and late 2025, including notable posts on November 6, 2025, February 12, 2025, and January 15, 2025, which collectively describe new features, deprecations, and roadmap-oriented previews. Citations are provided inline where specific changes are described. [1][2][3]

## 1) New features and enhancements (2025 updates)

- Reusable workflows and orchestration
  - Nested reusable workflows expanded to 10 levels, with up to 50 total workflow calls in a single workflow run. This is a significant upgrade from the prior limit of 4 nesting and 20 calls, enabling more complex cross-repo automation and reuse without duplicating workflow logic [1].
  - Impact: greatly improves modularization and scalability of CI/CD pipelines in large codebases and organizations [1].

- Runners and OS support
  - Apple Silicon (M2) macOS runners are generally available, with new labels and configurations to leverage improved performance and GPU acceleration on ARM-based hardware (e.g., macos-latest-xlarge, macos-15-xlarge, macos-14-xlarge, macos-13-xlarge) [1].
  - The Ubuntu 20.04 hosted runner image is being sunset with planned brownouts and a migration path to newer images (e.g., Ubuntu 22.04/24.04) [3].
  - These changes signal a shift toward newer, more capable runners and a multi-OS strategy to support diverse workloads [1][3].

- Security and automation enhancements
  - Immutable actions migration has entered public preview, with guidance for updating allow lists and addressing new domains used for immutable actions resolution. This is part of a broader move toward stronger security and reliability in hosted runner executions [2].
  - GitHub has introduced additional OIDC token claims and related security improvements in the 2025 changelogs, reflecting ongoing hardening of credentials and permissions within workflows [1].
  - Copilot integration for AI-assisted coding can operate without requiring organization-wide Actions enablement, enabling AI-assisted automation within workflows more flexibly [1].

- Other ecosystem updates
  - GitHub has highlighted REST API updates, Windows Server-related changes, and ongoing exploratory previews as part of the expanding Actions ecosystem, with a cadence of monthly changelogs that reflect roadmap and preview activities [1].
  - Public previews and previews of immutable actions, as well as broader ecosystem improvements, are recurring themes in late-2025 changelog entries [1].

## 2) Deprecations and sunsetting plans (2025 outlook)

- Check Run status modification deprecation
  - The ability to modify the conclusion and status of a check run created from a workflow using the GitHub token will be removed, with the change effective around March 31, 2025. This deprecation is part of a broader shift in how check results can be updated through API calls and workflow events [2].

- Immutable actions migration (public preview)
  - The public preview of immutable actions continues, prompting organizations to update allow lists and consider the new action resolution model. This migration is designed to improve security and stability but requires changes to existing workflows and runner configurations [2].

- Ubuntu 20 image sunset and related changes
  - The Ubuntu 20 runner image is sunset, with full retirement targeted for April 15, 2025 and brownouts in March–April 2025 to raise awareness. This migration is accompanied by related changes to artifact actions and caching implementations (e.g., actions/cache v1-v2, and the toolkit cache package) [3].
  - These changes require migration to newer Ubuntu images (22.04/24.04) to avoid workflow failures due to missing or deprecated infrastructure [3].

- Additional migration guidance
  - The February 12, 2025 changelog post outlines further deprecations and breaking changes affecting check runs, self-hosted runner network allow lists, and security-related changes. It remains important to monitor changelogs for updated timelines and migration guidance [2].

## 3) Runners, OS support, and usage patterns (2025 context)

- macOS runners and hardware acceleration
  - GA of M2-powered macOS runners provides improved performance for macOS CI workloads, with expanded labeling options to target Apple Silicon environments [1].

- Ubuntu runner images and general OS strategy
  - The sunset of Ubuntu 20.04 hosted runners pushes users toward newer images such as 22.04/24.04, with brownouts intended to encourage migration and reduce legacy infrastructure usage [3].

- Concurrency and usage limits
  - The key documented change in usage limits for 2025 centers on reusable workflows; the enhanced nesting and calls enable more scalable architectures but may require rethinking of workflow architectures to stay within new quotas [1].

## 4) Notable announcements and previews (2025 highlights)

- Copilot and AI-enabled automation
  - Copilot integration within workflows can be used without enabling Actions for the organization, broadening the applicability of AI-assisted coding within automation pipelines [1].

- Immutable actions and security previews
  - Public previews of immutable actions reflect GitHub's strategy to reduce variability and improve security in action execution across hosted and self-hosted runners; organizations should plan migrations accordingly [2].

- Roadmap signals and API updates
  - Ongoing REST API updates and Windows Server adjustments are part of the broader roadmap and preview cycles, signaling continued investments in the Actions platform and ecosystem [1].

## 5) Conclusion

GitHub Actions continues to invest in scalability, security, and cross-organization automation. The 2025 updates emphasize stronger modularity through expanded reusable workflows, a broader and more capable runner ecosystem (including M2 macOS runners), and a deliberate migration plan away from legacy Ubuntu 20 images and older caching mechanisms. Organizations should plan for migration windows tied to the published sunsetting milestones, adjust workflow architectures to leverage higher reusable workflow quotas, and monitor ongoing changelogs for incremental previews, API updates, and security improvements [1][2][3].

### Sources
[1] New releases for GitHub Actions – November 2025. https://github.blog/changelog/2025-11-06-new-releases-for-github-actions-november-2025/
[2] Notice of upcoming deprecations and breaking changes for GitHub Actions. https://github.blog/changelog/2025-02-12-notice-of-upcoming-deprecations-and-breaking-changes-for-github-actions/
[3] GitHub Actions: Ubuntu 20 runner image brownout dates and other breaking changes. https://github.blog/changelog/2025-01-15-github-actions-ubuntu-20-runner-image-brownout-dates-and-other-breaking-changes/

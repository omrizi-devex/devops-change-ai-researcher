## Introduction
This report consolidates the latest Terragrunt release notes and deprecations identified to date, focusing on the most recent release tag available in the official Terragrunt releases index. It highlights deprecations, breaking changes, and migration guidance to help operators adapt to the evolving toolchain. The findings rely on the official release notes for the RC tag v0.97.0-rc2025121901 and the general releases index, with corroborating notes from release aggregators where appropriate.

## Latest Terragrunt release overview
- Latest release tag (as of this report): v0.97.0-rc2025121901 (release candidate). Release date listed: December 19, 2025.
- Source of truth: Terragrunt releases page and the specific RC tag notes; a releases index provides the canonical list of published releases.
- Primary references:
  - Release tag with notes: https://github.com/gruntwork-io/terragrunt/releases/tag/v0.97.0-rc2025121901 [1]
  - Releases index: https://github.com/gruntwork-io/terragrunt/releases [2]
  - Release Bot notes (aggregate context): https://releasebot.io/updates/gruntwork/terragrunt [3]

## Deprecations introduced in the latest release
- The --queue-strict-include flag is deprecated and is not functional in this release; it will not be removed before Terragrunt 2.0 [1].
- The --units-that-include flag is deprecated; it is described as an alias for the reading= attribute filter and is effectively superseded by filter-based targeting [1].
- Run report generation and related filtering behavior have adjustments, including changes related to reporting exclusions (e.g., --queue-exclude-dir no longer appears as a reason for exclusion) as part of the updated filtering system [1].

## Breaking changes affecting configuration or usage
- The release formalizes a shift from legacy --queue flags to a filter-based approach. The --filter flag is now generally available and can replace several legacy queue/flag combinations; a new --filters-file facility allows applying multiple filters from a file [1].
- Changes to how filtering and queueing are evaluated, including the expansion of filter capabilities to support Git-based filtering, are described in the release notes [1].
- A broader migration path is outlined, urging users to migrate to the filter-based workflow and to phase out root terragrunt.hcl usage where feasible to favor more modular configurations [1].

## Migration guidance and practical steps
- Core migration direction: migrate from legacy queue flags to the new filter-based targeting, using --filter expressions or a --filters-file for complex criteria [1].
- Practical steps you can start now:
  1) Replace legacy queue flags with filter expressions that capture the same scope (e.g., path or reading-based filters) as described in the release notes [1].
  2) When multiple filters are needed, use --filters-file to consolidate expressions in a file rather than stacking flags [1].
  3) Update automation and CI/CD scripts to stop relying on deprecated queue flags and instead rely on the filter-based approach [1].
  4) Consider refactoring root terragrunt.hcl usage toward modular configurations to reduce root-hcl dependencies [1].
  5) After migrating, re-run a representative subset of runs to confirm that filtering behavior and outputs align with expectations [1].
- Migration examples (illustrative):
  - Before: terragrunt apply --queue-strict-include=env-dev
  - After: terragrunt apply --filter 'path=env-dev'  (or use a filters file with a line like: path=env-dev)
  Notes: The exact syntax for filter expressions is defined in the Terragrunt filter feature documentation accompanying the release; refer to the release notes for specifics [1].

## Additional context and considerations
- This RC represents a significant step in enabling a filter-based workflow; final releases after this RC may introduce further refinements or deprecations. It is advisable to monitor the official releases page for updates and to perform a staged rollout in non-production environments before broad adoption [2].
- For a consolidated history of changes and official changelogs, consult the release notes linked above [1].

### Sources
[1] Release v0.97.0-rc2025121901 - gruntwork-io/terragrunt: https://github.com/gruntwork-io/terragrunt/releases/tag/v0.97.0-rc2025121901
[2] Releases - gruntwork-io/terragrunt: https://github.com/gruntwork-io/terragrunt/releases
[3] Gruntwork Release Notes (Release Bot): https://releasebot.io/updates/gruntwork/terragrunt

## Introduction

This report consolidates the deprecations and new features introduced in Kubernetes releases 1.33, 1.34, and 1.35, with a particular focus on implications for upgrading from v1.33 to v1.35. It highlights API deprecations and migrations, changes to core components and runtimes, networking and ingress considerations, scheduling and resource management enhancements, and observability improvements. The goal is to provide operators with actionable guidance to plan and execute a smooth upgrade path while minimizing disruption to workloads and integrations.

## Overview of Kubernetes v1.33

- Deprecations and migrations
  - Endpoints API deprecation began in v1.33, with a continued transition toward EndpointSlices. Tools and controllers that read or manipulate Endpoints should migrate to EndpointSlices to avoid warnings and future removals [1][2]. The official deprecation guidance and migration resources provide the authoritative path for updating manifests and clients [4].
  - The upgrade guidance emphasizes auto-detection of the container runtime cgroup driver and discourages static kubelet.config cgroup-driver settings, aligning with a longer-term move away from kubelet-config based cgroup management [2].

- New features and improvements affecting upgrade planning
  - In-place Pod Resize reached beta status, enabling non-disruptive vertical scaling of container resources for running Pods [1].
  - Image Volumes (CSI-driven) progressed toward beta, expanding support for image-backed volume capabilities [1].
  - HorizontalPodAutoscaler Configurable Tolerance became usable in more scenarios, allowing finer autoscale control at the workload level [1].
  - Mutable CSINode Allocatable counts were introduced to improve accounting for CSI resources on nodes, aiding scheduling decisions [1].
  - Dynamic Resource Allocation (DRA) improvements signaled stronger support for dynamic resource management in workloads [1].

- API and migration focus
  - The Endpoints deprecation and EndpointSlices migration represent the primary API-level migration in this release cycle; developers and operators should audit code and manifests for Endpoints usage and plan substitutions where appropriate [2][4].

- Migration considerations
  - A staged upgrade path (often 1.33 → 1.34 → 1.35) is commonly recommended to align with the deprecation timeline and to validate changes in a controlled fashion before moving to the next minor version [1][4].

- Quick actions for operators
  - Inventory all Endpoints usage and related automation; begin migration to EndpointSlices in test environments and update client tooling and controllers accordingly [2], [4].
  - Begin testing in-place pod resize and DRA features in non-production to validate behavior and upgrade readiness [1].

## Overview of Kubernetes v1.34

- Deprecations and migrations
  - v1.34 continued the trend toward auto-detection of container runtimes and a shift away from manual cgroup driver configuration; ensure compatibility with CRI auto-detection across all nodes [5].
  - The release notes highlight evolving traffic routing semantics and naming conventions around traffic distribution, encouraging migration to newer policies and ensuring alignment with EndpointSlice-based routing in the longer term [5].
  - Additional hardening changes tighten authentication/authorization flows around endpoints and resources; review access controls and RBAC implications for new subresources and streaming behaviors [5].

- Notable new features and stability improvements
  - Pod-level resources support (beta) for per-Pod CPU/memory requests and limits, simplifying budgeting for multi-container Pods and easing autoscaler interactions [5].
  - DRA enhancements and better exposure of resource health through kubelet integration improve observability and scheduling decisions [5].
  - CSI improvements and volume modification capabilities (on-line) provide more flexible storage operations [5].
  - Improved streaming responses, watch cache stability, and list encoding mitigate API-server load in large clusters and improve scalability [5].
  - Topology-related features and the Downward API groundwork for topology awareness begin to mature toward broader GA in the 1.35 window [2].

- API changes and migration guidance
  - Expect continued emphasis on EndpointSlices and the migration away from Endpoints, as well as the broader Deprecation Migration Guide for safe, version-agnostic upgrade planning [4].

- Upgrade considerations
  - Plans to upgrade through 1.34 as a stepping stone help in managing deprecations and validating workloads against EndpointSlices and other changes before confronting 1.35 changes [1][4].

## Overview of Kubernetes v1.35

- Deprecations and removals
  - The most significant operational change is the removal of cgroup v1 support in favor of cgroup v2; nodes that run on cgroup v1 must be upgraded to runtimes/kernel configurations that support cgroup v2, or kubelet startup will fail after upgrade [6].
  - IPVS-based kube-proxy is deprecated; plan to migrate to nftables and adjust networking policies accordingly; this is part of an evolving networking landscape with future removal timelines [6].
  - Containerd v1.x support ends; for upgrades beyond v1.35, containerd should be upgraded to 2.x+ to avoid compatibility issues with newer Kubernetes versions [6].
  - WebSocket-based operations (exec/attach/port-forward) RBAC implications tighten permissions, requiring create access to pods/exec subresources; update RBAC policies accordingly [6].

- New features and improvements (GA/Beta/Matured) affecting upgrade planning
  - In-place Pod Resource Resize (GA) allows modifying Pod-level resources for running containers without restart, a major productivity enhancement for many workloads [6].
  - Node Declared Features (Alpha) and related scheduling enhancements enable safer handling of mixed-version clusters and feature girding for topology-aware scheduling [6].
  - Pod metadata.generation stability and status.observedGeneration become reliable signals for operators to understand when a Pod spec change has been observed by the kubelet, improving upgrade testing and rollout observability [6].
  - CSI driver tokens in secrets and mutable CSINode allocatable counts (beta) provide more secure secret handling and improved capacity awareness for storage workloads [6].
  - Gateway API adoption and enhanced traffic routing controls (trafficDistribution and related policies) give operators more explicit routing choices and integration options for ingress traffic, aligning with modern service mesh and gateway controllers [6].
  - Gang scheduling (alpha) and opportunistic batching (beta) advance scheduling capabilities for large-scale batch and AI/ML workloads; these require enabling feature gates on the API server and scheduler in test environments [6].
  - Storage version migration support moves toward GA in 1.35, enabling in-tree storage version updates; validate driver compatibility and test upgrade paths for persistent data schemas [6].

- API changes to watch for during upgrade
  - Pod-level resource fields, metadata.generation signals, and watch streaming changes require downstream tooling and controllers to adapt patch/update logic to the new semantics [6].
  - The Downward API topology exposure becomes more robust, enabling topology-aware scheduling and app behavior, which may influence workload manifests and config maps for topology hints [2].
  - CSI driver version and token management changes require compatibility checks with storage drivers and authentication flows [6].

- Upgrade guidance and practical steps
  - Confirm kernel and runtime support for cgroup v2 on all nodes; plan OS and runtime upgrades as necessary before 1.35 to avoid kubelet startup failures [6].
  - Plan containerd upgrade to 2.x+ and validate compatibility with your workloads and cluster components; ensure drivers support new containerd interfaces [6].
  - Transition networking from IPVS to nftables and adopt Gateway API-based traffic routing for ingress to reduce dependency on deprecated APIs and controllers [6].
  - Enable and validate new features in a staged manner (canary clusters) to observe scheduling and observability impacts; prepare for changes in RBAC, API semantics, and logging/metrics collection [6].

- Post-upgrade considerations
  - Remove any remaining references to cgroup v1; update node configurations and management tooling accordingly [6].
  - Review upgrade success signals (PodGeneration, observedGeneration, rollout tracking) and adjust monitoring dashboards to reflect the new observability signals [6].
  - Update CI/CD pipelines, monitoring, and admission controllers to align with new APIs and feature gates [6].

## Detailed comparison and practical upgrade path

- Endpoints vs EndpointSlices
  - 1.33 introduced deprecation of Endpoints in favor of EndpointSlices; by 1.34/1.35 the EndpointSlices API has matured and should be the primary interface for service endpoints; update automation, controllers, and tooling to query EndpointSlice resources rather than Endpoints [1][2][4].

- Cgroup and container runtimes
  - 1.33–1.34 begin de-emphasizing kubelet.config cgroup-driver in favor of CRI auto-detection; 1.35 requires cgroup v2 support and ends v1 support, necessitating OS/runtime upgrades or host feature changes across clusters [2][6].

- Networking and ingress
  - IPVS deprecation in 1.35 points to nftables as the preferred implementation, and the Ingress NGINX path is in maintenance mode; plan Gateway API migrations or alternative ingress controllers to avoid future friction [6].

- Scheduling and resource management
  - Pod-level resource resizing (1.34/1.35) and DRA improvements enable more dynamic workloads with less disruption; Gang Scheduling (alpha) and advanced tolerations alter how batch/workload pods are scheduled [1][3][6].

- Observability and API stability
  - Streaming list responses and watch-cache stability reduce API server memory pressure and improve scalability for large clusters; there is greater emphasis on metadata.generation and observedGeneration signaling for upgrade validation [1][6].

## Upgrade planning recommendations (practical steps)

1) Pre-upgrade assessment
- Inventory Endpoints usage and audit all tooling and manifests for Endpoints usage; plan migration to EndpointSlices [1][2][4].
- Check container runtimes and ensure CRI auto-detection; plan cgroup v2 readiness for all nodes [2][6].
- Review networking architecture and prepare Gateway API or alternative controllers for ingress traffic management; plan to migrate away from Ingress NGINX where feasible [6].

2) Staged upgrade path
- Upgrade to v1.34 in a staging cluster to validate new features and deprecations; verify Pod-level resource settings, DRA behavior, and Topology exposure groundwork [5][1].
- Validate EndpointSlice-based workloads and adjust automation; update role-based access controls for exec/attach subresources if upgrading RBAC behavior [5].
- Proceed to v1.35 after confirming stability in 1.34; validate containerd upgrades, cgroup v2 readiness, and networking changes; enable GA features like in-place resize and ensure scheduling changes align with workloads [6].

3) Validation and go-live
- Run end-to-end tests and performance/load tests to ensure no regressions in service discovery and DNS resolution; monitor watch-cache and streaming API behaviors [5][6].
- Verify upgrade health signals (metadata.generation, observedGeneration) and adjust monitoring dashboards for new signals [6].
- Update runbooks, CI pipelines, and external tooling to reflect new APIs and features; document any deprecations that require upcoming removals (cgroup v1, IPVS, Ingress NGINX) [6].

4) Post-upgrade
- Complete migration away from Endpoints to EndpointSlices and remove residual Endpoints objects where applicable [2].
- Ensure CSI drivers are compatible with mutable CSINode allocatable counts and storage version migration; verify data integrity after storage version upgrades [6].
- Continuously monitor cluster stability and adjust resource management policies in line with new features and tolerances [1][6].

### Sources

[1] Kubernetes v1.33 release notes and deprecations: https://kubernetes.io/blog/2025/04/23/kubernetes-v1-33-release/
[2] Endpoints deprecation and EndpointSlices migration: https://kubernetes.io/blog/2025/04/24/endpoints-deprecation/
[3] Kubernetes v1.33 upcoming changes: https://kubernetes.io/blog/2025/03/26/kubernetes-v1-33-upcoming-changes/
[4] Deprecated API Migration Guide: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
[5] Kubernetes v1.34 release: https://kubernetes.io/blog/2025/08/27/kubernetes-v1-34-release/
[6] Kubernetes v1.35 release: https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/
[7] Kubernetes 1.35 Upgrade Guide: https://scaleops.com/blog/kubernetes-1-35-release-overview/
[8] InfoQ coverage of v1.35: https://www.infoq.com/news/2025/12/kubernetes-1-35/
[9] Kubermatic discussion on v1.35: https://www.kubermatic.com/blog/another-growth-ring-on-the-world-tree-kubernetes-v1-35-timbernetes/

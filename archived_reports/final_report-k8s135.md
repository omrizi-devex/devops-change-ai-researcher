Kubernetes v1.35 Release – New Features and Deprecations (Timbernetes)

Introduction
Kubernetes v1.35, released in December 2025, introduces a broad set of new features across GA, beta, and alpha, alongside notable deprecations and removals. The release emphasizes improvements in pod resource management, topology awareness, storage/migration workflows, scheduling efficiency, and operational posture, while pruning legacy components to accelerate modernization. The official materials frame this as the World Tree release (Timbernetes), with a mix of stable and evolving capabilities and explicit migration guidance for administrators. Key sources include the official release blog, the kubelet configuration drop-in directory GA post, and the official release notes page [1][2][3].

New features and enhancements (GA/Stable)
- In-place update of Pod resources (CPU/memory)
  - Description: Pods can adjust CPU and memory requests/limits in-place without restarting, enabling nondisruptive vertical scaling. This feature is GA/Stable [1].
- Metadata.generation for Pods (observedGeneration)
  - Description: Pod API exposes metadata.generation and status.observedGeneration to reliably reflect kubelet processing of the latest Pod spec changes. Now GA/Stable in v1.35 [1].
- Job API: new external-management capability (managed-by)
  - Description: A new managed-by field allows an external controller (e.g., cross-cluster workflows) to synchronize Job status; graduates to Stable [1].
- Topology and NUMA enhancements
  - MaxAllowableNUMANodes for Topology Manager: Configurable limit to support systems with many NUMA nodes; now Stable [1].
  - Rationale: Builds on prior beta/config support and stabilizes for higher-NUMA hardware [1].
- Traffic and networking refinements
  - trafficDistribution with PreferSameNode: Introduces a field to prefer local-node endpoints for traffic distribution; part of stable networking improvements [1].
  - PreferSameZone rename: PreferClose was renamed to PreferSameZone to clarify zonal routing semantics [1].
- Node topology exposure via Downward API (Beta)
  - Description: Node topology labels (topology.kubernetes.io/zone/region) can be exposed to Pods through the Downward API, enabling topology-aware workloads inside pods [1].
- Storage version migration (native in-tree support)
  - Description: Storage version migration gains native in-tree support and is enabled by default in the core control plane, simplifying migration workflows [1].
- Mutable CSINode allocatable count
  - Description: CSINode.spec.drivers[*].allocatable.count becomes mutable with automatic refresh behavior via CSIDriver; default-enabled in this release (beta previously) [1].
- Scheduling improvements: opportunistic batching
  - Description: Scheduling optimization that batches compatible Pods to reuse filtering/scoring work, reducing scheduling overhead on large clusters [1].
- StatefulSet updates: maxUnavailable
  - Description: The maxUnavailable field for StatefulSets (stable since earlier releases) remains usable to control unavailable Pods during updates alongside Parallel pod management [1].
- Kubernetes YAML enhancements (KYAML)
  - Description: KYAML transitions to beta and is enabled by default, with a disable option (KUBECTL_KYAML) [1].
- HPA tolerance configurability
  - Description: Tolerance for HorizontalPodAutoscaler (HPA) scaling is configurable per resource (beta) for finer control [1].
- User namespaces in Pods
  - Description: Support for user namespaces in Pods (id-mapped namespaces) to improve container isolation [1].
- OCI artifacts for images and related security improvements
  - Description: OCI artifact/image volume support matures and is default-enabled in v1.35; kubelet credential verification for cached images is now beta, enhancing security posture [1].
- CSI driver tokens in NodePublishVolume secrets
  - Description: CSI drivers can opt-in to receive ServiceAccount tokens via the secrets field in NodePublishVolume to minimize leakage in logs [1].
- Fine-grained container restart policies
  - Description: Per-container restart behavior controls recovery semantics within a Pod (beta) [1].
- Deployment status: terminatingReplicas (beta)
  - Description: Terminating replicas are reported in Deployment status to improve rollout observability [1].
- Native gang scheduling (alpha)
  - Description: Workload API and PodGroup provide all-or-nothing scheduling for interdependent Pods (alpha) for AI/batch workloads [1].
- Constrained impersonation (alpha)
  - Description: Fine-grained impersonation authorization for RBAC (alpha) [1].
- HTTP endpoints for component configuration/status (flagz/statusz) (alpha)
  - Description: Exposes /flagz and /statusz endpoints for machine-readable configuration/status (alpha) [1].

Deprecations, removals, and major changes
- Ingress NGINX retirement; Gateway API migration recommended
  - Description: Ingress NGINX is retired with best-effort maintenance through March 2026; migration to Gateway API is recommended [1].
- Removal of cgroup v1 support
  - Description: Cgroup v1 support is removed; nodes must run with cgroup v2 to avoid kubelet startup failures [1].
- Deprecation of kube-proxy IPVS mode
  - Description: IPVS mode is deprecated; kube-proxy will warn on startup if IPVS is used, with guidance to migrate toward nftables on Linux [1].
- End of life for containerd v1.x support
  - Description: v1.35 is the last Kubernetes release to support containerd v1.x; upgrade to containerd v2.x before moving to newer Kubernetes versions [1].
- Other notable deprecations and modernization moves
  - Description: Broader modernization efforts include ongoing protobuf and infrastructure changes; major removals center on cgroup v1, Ingress NGINX, and containerd v1.x [1].

API removals / transitions
- Storage version migration is native (beta) within core APIs
  - Description: Migration capability is integrated into the core control plane, reducing external tooling dependencies [1].
- API evolution around stable features (e.g., metadata.generation on Pods, Job managed-by semantics)
  - Description: Various API evolutions accompany stability/GA status for several features [1].

Changes to components and operational improvements
- Cloud provider route controller reconciliation moved to watch-based informers
  - Description: Reduces API calls and increases responsiveness in route management [1].
- CSI token handling and security posture improvements
  - Description: Token handling changes for CSI drivers via secrets in NodePublishVolume reduce credential leakage risk [1].
- Node topology exposure in workloads via Downward API (Beta)
  - Description: Workloads can safely access topology information without additional API server queries [1].
- Gang scheduling (alpha) and Workload API enhancements
  - Description: Native support for all-or-nothing scheduling of interdependent Pods [1].
- KYAML, HPA tuning, and per-resource autoscaling refinements
  - Description: YAML tooling advances and autoscaling tuning improvements [1].

Migration guidance for administrators
- Plan Kubernetes and container runtime upgrades in concert
  - Guidance: Upgrade containerd to v2.x given v1.x end-of-life; verify node runtime compatibility before cluster upgrades beyond v1.35 [1].
- Node OS and cgroup considerations
  - Guidance: Ensure Linux nodes are using cgroup v2 to avoid kubelet startup failures; plan OS upgrades if necessary [1].
- Ingress and gateway planning
  - Guidance: Begin migrating Ingress-based workflows to Gateway API-based approaches; prepare for maintenance windows and deprecation timelines [1].
- Feature gates and testing
  - Guidance: Many features are beta/alpha; enable with feature gates and validate workloads in staging clusters prior to production rollout [1].

Notable announcements and context
- Release theme and ecosystem direction
  - Description: The World Tree metaphor signals ongoing API evolution and ecosystem modernization [1].
- Release cadence and migration emphasis
  - Description: Emphasis on upgrading container runtimes and host configurations in step with new capabilities and deprecations [3].

Conclusion
Kubernetes v1.35 delivers substantial feature breadth across pod resource management, topology awareness, storage migration, and scheduling, while driving modernization through key deprecations such as cgroup v1, Ingress NGINX, and containerd v1.x support. Administrators should plan targeted migrations, test beta/alpha capabilities in staging environments, and ensure runtime and host configurations align with new requirements to realize the full value of the release.

Sources
[1] Kubernetes v1.35 Release: Timbernetes (The World Tree Release): https://kubernetes.io/blog/2025/12/17/kubernetes-v1-35-release/
[2] Kubernetes v1.35: Kubelet Configuration Drop-in Directory Graduates to GA: https://kubernetes.io/blog/2025/12/22/kubernetes-v1-35-kubelet-config-drop-in-directory-ga/
[3] Release Notes (Notes for v1.35): https://kubernetes.io/releases/notes/

Would you like me to tailor this report for a specific cluster context (e.g., large multi-tenant clusters, GPU workloads, or edge deployments) or export a version of this as a structured /final_report.md file in your repo after confirming the exact wording you prefer?
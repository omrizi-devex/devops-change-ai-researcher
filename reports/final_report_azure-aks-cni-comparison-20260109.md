## Introduction
This report provides a comprehensive comparison of Azure Kubernetes Service (AKS) networking options, focusing on Azure CNI (including standard and overlay variants) versus Kubenet. The goal is to help operators, architects, and decision-makers understand how pod IP addressing, VNet integration, security policies, private networking, outbound egress, and scalability differ between these networking models, and to offer guidance for common deployment patterns such as dual-stack IPv4/IPv6, private clusters, and large-scale environments. The analysis draws on official Microsoft documentation and Azure community resources to reflect current guidance and best practices. Inline citations reference a single set of sources for consistency across the discussion.

## Overview of Topic A: AKS CNI (Azure CNI)
Azure CNI refers to the networking model in which pods receive IP addresses from the Azure Virtual Network (VNet) IP space and participate in VNet routing. There are several variants and evolutions under the AKS umbrella, including the standard Azure CNI integration and the Overlay approach, which decouples pod IP space from the VNet while preserving integration with Azure networking features such as Network Security Groups (NSGs), Private Link, and private endpoints. This section presents the architecture, IP addressing modes, dual-stack capabilities, security and policy integration, and typical deployment patterns for AKS CNI.

- Architecture and IP addressing: In the classic Azure CNI (Standard) model, pods obtain IPs directly from the VNet subnet, enabling direct pod-to-VNet communication without mandatory NAT for intra-cluster traffic. This tight integration allows straightforward access to other VNet resources, and supports Azure-native network policies and ACLs when combined with appropriate CNI plugins or built-in controls. Overlay variants decouple pod IPs from the underlying VNet space, using an overlay network (e.g., VXLAN) to carry pod traffic while still enabling NSGs and other Azure services to operate in concert with your policies [1][3], [7].

- Dual-stack IPv4/IPv6 support: AKS can operate in dual-stack mode with a dual-stack VNet. Nodes receive both IPv4 and IPv6 addresses, and pods can be assigned both families from a separate pod CIDR. Services can also be dual-stack. This arrangement requires Kubernetes version support and careful configuration of ipFamilies, podCIDR, and service CIDR ranges [2].

- NSG integration and security: Pods on the AKS CNI model reside on routable IPs within the VNet (or in the overlay in overlay mode), enabling direct application of Network Security Groups and other Azure network controls. In the Overlay variants, NSG applicability is preserved, and when combined with policy layers such as Cilium, security observability can be enhanced [3], [7].

- Outbound traffic and private endpoints: Pod egress to the internet is typically NATed to an outbound IP. For predictable outbound behavior, NAT Gateway and user-defined routes (UDRs) backed by Azure Firewall or equivalent can be employed. Private clusters and private DNS zones enable private API access and internal name resolution with Private Link/Private DNS zones as part of standard production deployments [5][6][7].

- Private clusters and DNS: Private AKS clusters keep the API server private, accessible from your private network or via VPN/ExpressRoute, with Private DNS zones used to resolve private endpoints and service names. This pattern is common for regulated workloads and enterprise deployments [4].

- Scaling, IP exhaustion, and best practices: For large-scale clusters, Overlay networking with dynamic IP allocation, and IPv6 dual-stack designs, help mitigate IP space constraints while preserving Azure policy and NSG integration. It is generally recommended to evaluate the Overlay/dual-stack path for future-proofing and scale [1][2][3], [7].

- Representative patterns and ingress: For modern ingress, Application Gateway with Gateway API (AGIC) is preferred, while HTTP Application Routing has been retired in favor of gateway-based approaches. Private endpoints and Private DNS zones continue to serve internal access needs [7][4].

### Sources for Topic A
[1] Announcing Azure CNI Overlay in Azure Kubernetes Service (GA) - Azure Blog: https://azure.microsoft.com/en-us/blog/announcing-the-general-availability-of-azure-cni-overlay-in-azure-kubernetes-service/
[2] Use dual-stack networking in Azure Kubernetes Service (AKS): https://learn.microsoft.com/en-us/azure/aks/configure-dual-stack
[3] Choosing the right networking model for Azure Kubernetes Service (AKS) - Azure CNI vs Kubenet: https://techcommunity.microsoft.com/blog/startupsatmicrosoftblog/choosing-the-right-networking-model-for-azure-kubernetes-service-aks-azure-cni-v/4351872
[4] Create a private Azure Kubernetes Service (AKS) cluster: https://learn.microsoft.com/en-us/azure/aks/private-clusters
[5] AKS NAT AGIC and private endpoints: https://github.com/Azure-Samples/aks-nat-agic
[6] AKS Egress Traffic Demystified: https://argonsys.com/microsoft-cloud/library/aks-egress-traffic-demystified/
[7] AKS networking made easy: Your comprehensive guide: https://techcommunity.microsoft.com/blog/startupsatmicrosoftblog/aks-networking-made-easy-your-comprehensive-guide/4398603

## Overview of Topic B: Kubenet
Kubenet is a simpler, NAT-based networking model that historically served AKS clusters before Azure CNI matured to support large-scale deployments. Pods in Kubenet get IP addresses from an overlay range and traffic to external resources is NATed through the node. Kubenet relies less on direct VNet integration and has a different set of policy, scalability, and operational implications. Microsoft guidance indicates Kubenet retirement in favor of Azure CNI variants, with migration recommended for long-term workloads [3][4][7].

- Architecture and IP addressing: Kubenet uses a NAT-based approach where pod IPs and node IPs are decoupled; pod traffic to other VNets or Azure resources can be NATed, with less direct pod-to-VNet routing. This model reduces pressure on VNet IP space but at the cost of reduced native VNets integration and higher NAT overhead [3].

- Security and policy: With Kubenet, security policy enforcement relies more on Kubernetes Network Policies and potential external tooling, as direct NSG integration with pod IPs is limited compared to Azure CNI. This makes detailed policy enforcement more challenging in some topologies [3], [7].

- Outbound/NAT and private endpoints: Because traffic is NATed, outbound control and IP stability can be more complex in Kubenet deployments. The guidance emphasizes moving toward Azure CNI variants for improved egress control and integration with NAT Gateways and Firewall-based patterns [3], [7].

- Private clusters and DNS: Kubenet-based deployments can still use Private DNS and private endpoints, but strategies are usually aligned with the broader NAT-based connectivity design and may require additional configuration for private access to resources [4].

- Scaling and IP exhaustion: Kubenet typically uses less VNets IP space pressure than direct VNet IP assignment, but the NAT model can limit large-scale efficiency and direct access features. Microsoft notes Kubenet retirement and recommends migrating to Azure CNI overlays for scalable, future-proof deployments [4][7].

### Sources for Topic B
[3] Choosing the right networking model for Azure Kubernetes Service (AKS) - Azure CNI vs Kubenet: https://techcommunity.microsoft.com/blog/startupsatmicrosoftblog/choosing-the-right-networking-model-for-azure-kubernetes-service-aks-azure-cni-v/4351872
[4] Create a private Azure Kubernetes Service (AKS) cluster: https://learn.microsoft.com/en-us/azure/aks/private-clusters
[7] AKS networking made easy: Your comprehensive guide: https://techcommunity.microsoft.com/blog/startupsatmicrosoftblog/aks-networking-made-easy-your-comprehensive-guide/4398603

## Detailed comparison
- IP addressing and VNet integration:
  - AKS CNI (Standard) provides direct IPs from the VNet, enabling access to VNets and services without mandatory NAT for intra-cluster routing; Overlay variants decouple pod IPs from the VNet yet retain Azure policy and NSG support [3], [7].
  - Kubenet uses NAT-based pod networking with a separate addressing space, reducing direct VNet IP pressure but requiring NAT for egress and cross-VNet access, and offering less direct integration with VNet resources [3].

- Security and policy:
  - AKS CNI enables NSG integration on pod IPs and supports Kubernetes Network Policies, with enhanced security visibility in Cilium-backed overlays; Kubenet offers basic policy capabilities and relies more on Kubernetes-level controls and external tooling for advanced observability [3], [7].

- Dual-stack and IPv6:
  - AKS CNI supports dual-stack (IPv4/IPv6) within a dual-stack VNet; pods can receive IPv6 addresses in a decoupled or integrated model depending on configuration. Dual-stack support in AKS requires careful configuration of ipFamilies, podCIDRs, and service CIDRs [2]. Kubenet guidance generally aligns with AKS dual-stack readiness but specifics depend on the chosen CNI variant and cluster version [3].

- Outbound and private networking:
  - AKS CNI benefits from native outbound controls via NAT Gateway and private endpoints; Private DNS zones help internal resolution; Kubenet requires NAT-based egress handling and may be more complex to achieve deterministic outbound IPs in practice [5][6][7].

- Scale and future readiness:
  - For large-scale deployments, AKS CNI Overlay with dynamic IP allocation and IPv6 dual-stack is favored to prevent IP exhaustion while maintaining policy continuity; Kubenet is considered legacy for new deployments and is on a retirement trajectory [1][4][7].

- Ingress patterns:
  - AKS CNI can leverage Gateway API-based ingress (AGIC) for scalable, policy-driven routing; Kubenet remains compatible with Kubernetes-native and external ingress options but lacks some integrations with modern gateway architectures [7].

### Quick-start patterns and migration guidance
- Dual-stack AKS with private cluster and NAT: Deploy a dual-stack VNet, configure ipFamilies, assign IPv4/IPv6 CIDRs, enable Overlay as needed, and attach a NAT Gateway for predictable outbound IPs [2][7].
- Private cluster with private DNS: Create a private AKS cluster and configure Private DNS zones for internal access to API endpoints and services [4][5].
- Ingress modernization: Prefer AGIC and Gateway API for AKS networking, and plan transitions away from HTTP Application Routing to gateway-based ingress [4][7].

### Conclusion
AKS CNI (including Overlay and dual-stack configurations) offers direct VNet integration, robust policy and security options, and scalable IP management for large clusters. Kubenet provides a simpler, NAT-based networking approach with lower initial IP pressure but limited direct VNet integration and a clear retirement trajectory. For most new deployments, especially those requiring large scale, private networking, and strong policy enforcement, AKS CNI with Overlay or standard configurations is the recommended path. For smaller or ephemeral clusters, Kubenet can still be suitable in the short term, but migration planning is encouraged to preserve long-term support and capabilities.

### Sources
[1] Announcing Azure CNI Overlay in Azure Kubernetes Service (GA) - Azure Blog: https://azure.microsoft.com/en-us/blog/announcing-the-general-availability-of-azure-cni-overlay-in-azure-kubernetes-service/
[2] Use dual-stack networking in Azure Kubernetes Service (AKS): https://learn.microsoft.com/en-us/azure/aks/configure-dual-stack
[3] Choosing the right networking model for Azure Kubernetes Service (AKS) - Azure CNI vs Kubenet: https://techcommunity.microsoft.com/blog/startupsatmicrosoftblog/choosing-the-right-networking-model-for-azure-kubernetes-service-aks-azure-cni-v/4351872
[4] Create a private Azure Kubernetes Service (AKS) cluster: https://learn.microsoft.com/en-us/azure/aks/private-clusters
[5] AKS NAT AGIC and private endpoints: https://github.com/Azure-Samples/aks-nat-agic
[6] AKS Egress Traffic Demystified: https://argonsys.com/microsoft-cloud/library/aks-egress-traffic-demystified/
[7] AKS networking made easy: Your comprehensive guide: https://techcommunity.microsoft.com/blog/startupsatmicrosoftblog/aks-networking-made-easy-your-comprehensive-guide/4398603
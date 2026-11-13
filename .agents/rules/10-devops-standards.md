# DevOps & Platform Engineering Standards

This rule governs continuous integration, continuous delivery, Infrastructure as Code (IaC), containerization, and deployment automation.

## 1. Infrastructure as Code (IaC)
- All cloud and hosting infrastructure (networks, clusters, storage, databases, IAM) must be defined as code (Terraform, OpenTofu, Pulumi, Kubernetes manifests, or CloudFormation).
- Manual cloud console modifications ("clickops") are prohibited for production infrastructure.
- IaC definitions must be version-controlled, linted, and security-scanned (e.g., tfsec, checkov) prior to deployment.

## 2. CI/CD Pipeline Determinism
- Builds must be deterministic, reproducible, and isolated.
- Pipelines must execute quality gate checks automatically before merging to main branches.
- Pipeline definition files (e.g., `.github/workflows/`) must not use unpinned actions or insecure curl-to-bash scripts.

## 3. Container Standards
- Container images must be based on minimal, audited base images (e.g., Alpine, Distroless).
- Containers must never run as root (`USER nonroot`).
- Container images must be scanned for CVEs and signed before admission into production registries.

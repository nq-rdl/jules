## Instructions

Implement the appropriate infrastructure-as-code solution for the issue above.

Focus on Ansible, Terraform or OpenTofu, ArgoCD, platform automation,
validation tooling, and adjacent operator documentation as needed.

Constraints and validation:
- Jules does not have direct access to libvirt, hypervisors, QEMU hosts,
  running Kubernetes clusters, or ArgoCD.
- Do not claim live infrastructure verification or end-to-end platform testing.
- Validate with repository-local checks only: pre-commit hooks,
  `ansible-lint`, `yamllint`, syntax checks, `terraform fmt` /
  `terraform validate`, Helm or Argo lint, and similar static or dry-run checks
  available in the repo.
- If important validation tooling is missing, add the minimal tooling or
  configuration needed and include it in the pull request.

Implementation expectations:
- Prefer minimal, reviewable, idempotent changes.
- Keep bootstrap concerns in Terraform or OpenTofu, continuous delivery
  concerns in ArgoCD, and host or VM lifecycle concerns in Ansible.
- Use secure defaults, explicit configuration, and least privilege.
- Update related docs or examples when the operator workflow changes.

Open a pull request with your changes when complete.

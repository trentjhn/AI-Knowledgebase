# AI Governance

Emerging standards, tools, and best practices for governing AI-generated code in teams and regulated environments.

## Topics

- **[AI Code Attribution](ai-code-attribution.md)** — Disclosure spectrum, attribution methods, industry standards (LLVM, Ghostty, Fedora), compliance (HIPAA, SOC2, FedRAMP), tools (git-ai, Entire CLI)

## Key Concepts

- **AI Code Halflife** = 3.33 years (time before significant modification needed)
- **Disclosure spectrum** = 4 levels from none → minimal → standard → full provenance
- **Attribution methods** = Co-Authored-By, ASSIST tags, git-ai checkpoints, SBOM attestation

## When to Use

- **Personal projects**: No attribution needed
- **Open-source**: Use Co-Authored-By in commit messages
- **Teams/internal**: Document AI usage, add to PR descriptions
- **Regulated (HIPAA/SOC2)**: Use Entire CLI for full audit trails
- **Enterprise**: SBOM + approval workflows with git-ai

Last updated: 2026-03-08

# Team GitHub Workflow & Collaboration Guidelines

## 1. Overview
This document defines the team collaboration workflow, branching strategy, commit message standards, code review rules, and issue tracking guidelines for **Sem 5 — Sprint 1 (Squad 85, Team 04, Chitkara Campus)**.

### Project Problem Statement:
> *"Customer support teams manage ticket categories, escalation records, and resolution times, but unresolved complaints are never connected to cancellation behaviour, making churn prevention reactive instead of proactive."*

### Business Objective:
Establish a collaborative engineering workflow to build an end-to-end Data Product that connects customer support complaint data with cancellation behavior to enable proactive churn prevention.

---

## 2. Branching Strategy

Our team adheres to a structured branching model to ensure `main` remains stable, deployable, and reliable at all times.

### Key Rules:
1. **Protected `main` Branch**: 
   - The `main` branch contains production-ready, verified code.
   - **Direct commits to `main` are strictly prohibited.**
2. **Branch Naming Conventions**:
   - Feature branches: `feature/[short-description]` (e.g., `feature/data-ingestion`, `feature/churn-risk-scoring`)
   - Bug fix branches: `fix/[short-description]` (e.g., `fix/missing-value-imputation`)
   - Documentation branches: `docs/[short-description]` (e.g., `docs/data-dictionary`)
   - Refactoring branches: `refactor/[short-description]` (e.g., `refactor/sql-aggregation-queries`)
   - Chore/Maintenance branches: `chore/[short-description]` (e.g., `chore/dependencies-update`)
3. **Lifecycle of a Branch**:
   - Create a branch from an updated `main` branch: `git checkout -b feature/<task-name>`
   - Work locally, commit changes following Conventional Commits, and push to GitHub.
   - Open a Pull Request (PR) to `main`.
   - Once reviewed and merged, **delete the feature branch** on GitHub and locally (`git branch -d feature/<task-name>`) to prevent clutter.

---

## 3. Commit Message Conventions

We enforce the **Conventional Commits** standard (`[type]: [description]`). This creates an explicit commit history, communicates developer intent, and enables automated changelog generation.

### Supported Types:
- `feat`: A new feature or analytical capability added to the codebase.
- `fix`: A bug fix or correction in logic/data pipelines.
- `docs`: Documentation updates only (e.g., `README.md`, `WORKFLOW.md`, Data Dictionary).
- `refactor`: Code restructures that neither fix a bug nor add a feature.
- `test`: Adding missing unit tests or validating data schemas.
- `chore`: Project maintenance (updating dependencies, `.gitignore`, build config).

### Structure:
```text
[type]: [short summary in present tense]

[optional detailed body explaining WHY the change was made]
[optional footer referencing issue numbers, e.g. Closes #12]
```

### Examples:
- `feat: add data validation function for support tickets dataset`
- `fix: correct null percentage calculation in customer profiler`
- `docs: document team github workflow and conventions`
- `chore: update requirements.txt with pandas and streamlit libraries`

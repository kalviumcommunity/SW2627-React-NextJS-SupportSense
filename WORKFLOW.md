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

---

## 4. Pull Request & Code Review Process

Pull Requests (PRs) serve as mandatory safety gates before code enters `main`.

### PR Guidelines:
1. **Title Standard**: Must be action-oriented and descriptive (e.g., `feat: setup team GitHub workflow and branching guidelines`).
2. **Issue Association**: Every PR must link to its corresponding GitHub issue in the description using GitHub keywords (e.g., `Closes #1`, `Fixes #3`).
3. **Code Review Criteria**:
   - **Correctness & Logic**: Does the pipeline execute without errors?
   - **Data Integrity**: Are null values, schemas, and data types validated?
   - **Clarity & Maintainability**: Are functions modular and readable?
   - **Commit Quality**: Do commit messages adhere to Conventional Commits?
4. **Approval Requirement**: At least **one teammate approval** is required before merging into `main`.
5. **Merge Strategy**: Use **Squash and Merge** or standard Merge Commit to preserve clean linear history, then delete the source branch.

---

## 5. GitHub Issue Tracking Approach

All team tasks originate as trackable GitHub Issues to establish ownership, context, and sprint progress.

### Issue Requirements:
1. **Action-Oriented Title**: Clear statement of work (e.g., `Ingest customer support ticket dataset into processing pipeline`).
2. **Detailed Description**: Contains background/context, business objective, and acceptance criteria (Definition of Done).
3. **Categorization Labels**: Assigned appropriate GitHub labels (`feature`, `bug`, `documentation`, `data-pipeline`).
4. **Assignee**: Exactly one team member assigned for clear accountability.
5. **Automatic Closing**: Closing keyword (`Closes #ID`) included in PR description to close the issue automatically upon merging PR into `main`.

---

## 6. Emergency Rollback & Incident Management Policy

If a bug or broken pipeline logic reaches `main`:
1. **Never Force Push (`git push --force`) to `main`**: Force pushing destroys team commit history.
2. **Use Surgical Reverts**:
   ```bash
   git checkout main
   git pull origin main
   git revert <bad-commit-hash>
   git push origin main
   ```
3. **Create Hotfix Issue & Post-Mortem**: Document why the failure bypassed review and add validation tests to prevent recurrence.

---

## 7. Merge Conflict Resolution Protocol

When `main` has advanced while you were working on your feature branch:
1. Fetch latest changes from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-branch-name
   ```
2. Rebase feature branch onto `main` (or merge `main` into feature branch):
   ```bash
   git rebase main
   ```
3. Resolve conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) in affected files manually.
4. Stage resolved files and continue rebase:
   ```bash
   git add <resolved-file>
   git rebase --continue
   ```

---

## 8. Data & Credentials Security Guidelines

To maintain repository security and prevent data leakage:
1. **No Credentials in Git**: Never commit `.env` files, API keys, passwords, or database URIs.
2. **Strict `.gitignore`**: All raw confidential datasets, local virtual environments (`venv/`), temporary outputs, and credentials must be listed in `.gitignore`.
3. **Automated Secret Scanning**: Use GitHub secret scanning to prevent accidental key exposure.

---

## 9. Onboarding Checklist for New Contributors

When a new developer joins the repository, they must follow these exact steps to contribute without breaking `main`:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kalviumcommunity/SW2627-React-NextJS-SupportSense.git
   cd SW2627-React-NextJS-SupportSense
   ```
2. **Pull Latest Main**:
   ```bash
   git checkout main
   git pull origin main
   ```
3. **Check GitHub Issues**: Pick an assigned open issue (e.g., Issue #1).
4. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Develop & Commit**: Make atomic, focused commits with Conventional Commit format:
   ```bash
   git commit -m "feat: add customer ticket validation parser"
   ```
6. **Push & Open PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Request Code Review & Merge**: Address feedback, get approval, squash and merge, and delete the feature branch.

---

## 10. Definition of Done (DoD) Checklist

Before any PR is marked ready for review, the author must verify:
- [ ] Code follows Python / SQL style guidelines and is modularized.
- [ ] Datasets, missing values, and data types are validated.
- [ ] All unit tests pass cleanly without errors.
- [ ] Documentation (`README.md` / `WORKFLOW.md` / Data Dictionary) is updated.
- [ ] Conventional Commit messages are used throughout the branch history.
- [ ] PR description links to the corresponding GitHub issue (`Closes #ID`).

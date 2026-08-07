---
name: github-advanced-api
description: Expert-level GitHub interaction using raw `gh api` calls for PR management, testing, and file analysis.
---

# GitHub Advanced API Skill

This skill leverages the `gh api` command to interact directly with the GitHub REST and GraphQL APIs, allowing for flexible control over any repository link.

## 🏁 Setup Verification
Before executing API calls, verify the environment:
1. **Status Check:** `gh auth status`
2. **Identity Check:** `gh api user -q .login` (Confirms your current user identity)

## 📡 Core API Patterns

### 1. Interacting with PRs & Issues
Use the dynamic `{owner}` and `{repo}` placeholders. These automatically resolve based on the local git remotes.

- **Read PR Comments:**
  `gh api repos/{owner}/{repo}/issues/{number}/comments -q '.[].body'`
- **Analyze Changed Files (Raw JSON):**
  `gh api repos/{owner}/{repo}/pulls/{number}/files -q '.[].filename'`
- **Post a Detailed Comment (from file):**
  `gh api repos/{owner}/{repo}/issues/{number}/comments -F body=@analysis_report.md`

### 2. CI/CD & Test Analysis
Directly query the Check Runs API to see why a PR is failing without opening a browser.

- **Check Run Results:**
  `gh api repos/{owner}/{repo}/commits/{branch_or_sha}/check-runs -q '.check_runs[] | {name, status, conclusion}'`
- **Retrieve Workflow Logs:**
  `gh api repos/{owner}/{repo}/actions/runs/{run_id}/logs`

### 3. Pushing & Updating PRs
- **Update PR Branch (Merge/Rebase):**
  `gh api -X PUT repos/{owner}/{repo}/pulls/{number}/update-branch`
- **Set PR Labels:**
  `gh api repos/{owner}/{repo}/issues/{number}/labels -f labels[]='bug' -f labels[]='needs-review'`

## 🤖 Claude's Operational Logic
1. **Dynamic Resolution:** If a user provides a link like `github.com/google/guava/pull/123`, extract `google` as `{owner}` and `guava` as `{repo}` for the API path.
2. **The -F Flag:** Always use `-F` when sending multiline text or file paths to ensure correct JSON encoding.
3. **Data Filtering:** Use `-q` (jq) to strip out massive JSON responses. Only provide Claude with the relevant snippets (e.g., error messages or file diffs).
4. **Method Awareness:** 
   - `GET` is the default. 
   - Adding a field (`-F` or `-f`) forces a `POST`. 
   - Use `-X PATCH` or `-X DELETE` for specific updates/removals.
  
# devops-change-ai-researcher
Search and summarizing changes in the devops domains

## CI/CD and GitHub Checks

This repository uses GitHub Actions for continuous integration. The CI workflow runs automatically on every push and pull request to `main` or `master` branches.

### How GitHub Checks Work

GitHub Actions automatically creates **check runs** for each job in the workflow. These checks appear in several places:

- **Pull Request Status Checks**: Visible at the bottom of every PR, showing which checks have passed or failed
- **Commit Status Checks**: Shown next to each commit in the commit history
- **Checks Tab**: Detailed view of all check runs on a PR, accessible via the "Checks" tab

The CI workflow includes four separate checks:
- `lint` - Code linting with pylint
- `format` - Code formatting validation with black
- `type-check` - Type checking with mypy
- `security` - Security scanning with bandit

Each check runs independently, so you can see exactly which validation failed if there's an issue.

### Making Checks Required Before Merging

To require these checks to pass before allowing PRs to be merged, configure branch protection rules:

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Branches**
3. Click **Add rule** (or edit an existing rule for `main`/`master`)
4. Under **Branch name pattern**, enter `main` (or `master` if that's your default branch)
5. Enable **Require status checks to pass before merging**
6. Check the boxes for the checks you want to require:
   - `lint`
   - `format`
   - `type-check`
   - `security`
7. Optionally enable **Require branches to be up to date before merging** (recommended)
   - This ensures PRs are tested against the latest base branch
8. Click **Save** or **Create**

Once configured, pull requests cannot be merged until all required checks pass. The merge button will be disabled until checks are green.

# errorproofdev/skills

Curated agent skills packaged into six categories. Each category is one installable plugin, and every skill follows the [Agent Skills specification](https://agentskills.io/specification), so the same files work in Claude Code, Codex, Replit, and any agent supported by [skills.sh](https://skills.sh).

## Install

Claude Code:

```
/plugin marketplace add errorproofdev/skills
/plugin install <category>@errorproof-skills
```

Codex:

```
codex plugin marketplace add errorproofdev/skills
codex plugin add <category>@errorproof-skills
```

skills.sh (any supported agent, e.g. `-a claude-code`, `-a codex`, `-a replit`):

```
npx skills add errorproofdev/skills --skill <skill> -a <agent>
```

Replit (run in the Repl's Shell; skills land in the project's `.agents/skills/`):

```
npx skills add errorproofdev/skills --skill <skill> -a replit -y --copy
npx skills add errorproofdev/skills --skill '*' -a replit -y --copy   # all skills
npx skills add errorproofdev/skills --list                           # browse available skills
```

Local `~/.claude/skills` (symlinks to this clone, so `git pull` updates them):

```
scripts/link-skills.sh ~/.claude/skills                           # link every repo skill; re-run after pulls
scripts/import-skill.sh ~/.claude/skills <skill> <category>      # copy a local skill into the repo
```

`link-skills.sh` moves anything it replaces to `~/.claude/skills.backup/<timestamp>/`, removes links to skills deleted from the repo, and leaves all other entries untouched. Run `link-skills.sh` again after an import so the local copy becomes a link. Any skills directory works as the target, e.g. `~/.agents/skills`. Use either the local links or the Claude Code plugins, not both, to avoid duplicate skills.

## Layout

```
.claude-plugin/marketplace.json                # Claude Code + skills.sh catalog
.agents/plugins/marketplace.json               # Codex catalog
plugins/<category>/.claude-plugin/plugin.json  # Claude Code plugin manifest
plugins/<category>/.codex-plugin/plugin.json   # Codex plugin manifest
plugins/<category>/skills/<skill>/SKILL.md     # Agent Skills spec skill
```

Add a skill by dropping its directory into `plugins/<category>/skills/`. Frontmatter may only use the spec keys (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`), and `name` must match the directory. Validate with `claude plugin validate .` and `claude plugin validate ./plugins/<category> --strict`.

## Categories

### frontend

UI design, design systems, Tailwind, Apple HIG, Three.js, TypeScript/JavaScript, and E2E testing skills

- `chrome-extension-developer`
- `core-components`
- `design-spells`
- `e2e-testing-patterns`
- `expo-tailwind-setup`
- `fixing-metadata`
- `frontend-design`
- `hig-components-content`
- `hig-foundations`
- `hig-inputs`
- `hig-project-context`
- `hig-technologies`
- `high-end-visual-design`
- `javascript-pro`
- `react-flow-node-ts`
- `redesign-existing-projects`
- `tailwind-design-system`
- `threejs-materials`
- `threejs-textures`
- `trpc-fullstack`
- `typescript-pro`
- `ui-setup`
- `ui-tokens`
- `ui-ux-pro-max`
- `ui-visual-validator`

### data

SQL, Postgres, migrations, DataFrames, statistics, ML, and analytics dashboard skills

- `bigquery-basics`
- `claimable-postgres`
- `database-migration`
- `database-migrations-migration-observability`
- `database-migrations-sql-migrations`
- `hugging-face-dataset-viewer`
- `jq`
- `kpi-dashboard-design`
- `neon-postgres`
- `polars`
- `postgresql-optimization`
- `scikit-learn`
- `sql-pro`
- `statsmodels`

### security

Secrets, compliance, hardening, code auditing, and authorized penetration testing skills

- `aws-penetration-testing`
- `burp-suite-testing`
- `burpsuite-project-parser`
- `ethical-hacking-methodology`
- `google-cloud-waf-security`
- `laravel-security-audit`
- `pci-compliance`
- `privacy-by-design`
- `red-team-tactics`
- `reverse-engineer`
- `secrets-management`
- `security-requirement-extraction`
- `semgrep-rule-variant-creator`
- `solidity-security`
- `ssh-hardening`
- `wordpress-penetration-testing`

### finance

Quant analysis, market data, financial modeling, payments, and pricing skills

- `alpha-vantage`
- `paypal-integration`
- `pricing`
- `quant-analyst`
- `square-automation`
- `startup-business-analyst-business-case`
- `startup-business-analyst-financial-projections`
- `stripe-automation`

### workflow

Planning, execution, git, pull request, code review, and agent orchestration skills

- `brainstorming`
- `caveman-commit`
- `caveman-help`
- `caveman-review`
- `concise-planning`
- `dispatching-parallel-agents`
- `executing-plans`
- `finishing-a-development-branch`
- `git-advanced-workflows`
- `github`
- `issues`
- `iterate-pr`
- `receiving-code-review`
- `requesting-code-review`
- `subagent-driven-development`
- `tmux`
- `using-git-worktrees`
- `writing-plans`

### essential

Core engineering discipline: debugging, TDD, verification, simplification, and skill authoring

- `bash-defensive-patterns`
- `claude-settings-audit`
- `code-simplifier`
- `find-skills`
- `lint-and-validate`
- `no-ai-slop`
- `simplify-code`
- `skill-writer`
- `systematic-debugging`
- `test-driven-development`
- `using-superpowers`
- `verification-before-completion`
- `writing-skills`

## License

[MIT](LICENSE), except skills that declare their own license in `SKILL.md` frontmatter or a bundled license file, which keep it: `frontend-design` (Apache-2.0), `scikit-learn` and `statsmodels` (BSD-3-Clause), `polars` (see its frontmatter).

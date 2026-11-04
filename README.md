# errorproofdev/skills

Curated agent skills packaged into 16 categories. Each category is one installable plugin, and every skill follows the [Agent Skills specification](https://agentskills.io/specification), so the same files work in Claude Code, Codex, Replit, and any agent supported by [skills.sh](https://skills.sh).

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

Add a skill by dropping its directory into `plugins/<category>/skills/`. Frontmatter may only use the spec keys (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`) plus Claude Code's `argument-hint`, `user-invocable`, and `disable-model-invocation`; other keys go under `metadata`, and `name` must match the directory. Each skill name appears in exactly one category. Validate with `claude plugin validate .` and `claude plugin validate ./plugins/<category> --strict`.

## Categories

328 skills in 16 categories.

### frontend (28)

UI design, design systems, Tailwind, Apple HIG, Three.js, TypeScript/JavaScript, and E2E testing skills

`chrome-extension-developer`, `core-components`, `design-mirror`, `design-spells`, `e2e-testing-patterns`, `expo-tailwind-setup`, `fixing-metadata`, `frontend-design`, `hig-components-content`, `hig-foundations`, `hig-inputs`, `hig-project-context`, `hig-technologies`, `high-end-visual-design`, `interactive-portfolio`, `javascript-pro`, `rayden-code`, `react-flow-node-ts`, `redesign-existing-projects`, `tailwind-design-system`, `threejs-materials`, `threejs-textures`, `trpc-fullstack`, `typescript-pro`, `ui-setup`, `ui-tokens`, `ui-ux-pro-max`, `ui-visual-validator`

### data (15)

SQL, Postgres, migrations, DataFrames, statistics, ML, datasets, and analytics dashboard skills

`bigquery-basics`, `claimable-postgres`, `database-migration`, `database-migrations-migration-observability`, `database-migrations-sql-migrations`, `datasets`, `hugging-face-dataset-viewer`, `jq`, `kpi-dashboard-design`, `neon-postgres`, `polars`, `postgresql-optimization`, `scikit-learn`, `sql-pro`, `statsmodels`

### security (17)

Secrets, compliance, hardening, code auditing, and authorized penetration testing skills

`aws-penetration-testing`, `burp-suite-testing`, `burpsuite-project-parser`, `cred-omega`, `ethical-hacking-methodology`, `google-cloud-waf-security`, `laravel-security-audit`, `pci-compliance`, `privacy-by-design`, `red-team-tactics`, `reverse-engineer`, `secrets-management`, `security-requirement-extraction`, `semgrep-rule-variant-creator`, `solidity-security`, `ssh-hardening`, `wordpress-penetration-testing`

### finance (11)

Quant analysis, market data, financial modeling, payments, pricing, and monetization skills

`alpha-vantage`, `monetization`, `nft-standards`, `pakistan-payments-stack`, `paypal-integration`, `pricing`, `quant-analyst`, `square-automation`, `startup-business-analyst-business-case`, `startup-business-analyst-financial-projections`, `stripe-automation`

### workflow (30)

Planning, execution, git, pull request, code review, and agent orchestration skills

`blueprint`, `brainstorming`, `brooks-lint`, `caveman-commit`, `caveman-help`, `caveman-review`, `code-review-ai-ai-review`, `codex-review`, `comprehensive-review-full-review`, `concise-planning`, `conductor-implement`, `conductor-revert`, `dispatching-parallel-agents`, `executing-plans`, `finishing-a-development-branch`, `git-advanced-workflows`, `git-pr-workflows-git-workflow`, `git-pr-workflows-pr-enhance`, `github`, `issues`, `iterate-pr`, `multi-agent-task-orchestrator`, `progressive-estimation`, `receiving-code-review`, `requesting-code-review`, `subagent-driven-development`, `tmux`, `using-git-worktrees`, `vibers-code-review`, `writing-plans`

### essential (19)

Core engineering discipline: debugging, TDD, testing, verification, simplification, shell, and skill authoring

`bash-defensive-patterns`, `bash-linux`, `bash-pro`, `clarity-gate`, `claude-settings-audit`, `code-simplifier`, `diagnosing-superpowers`, `error-diagnostics-error-trace`, `find-skills`, `lint-and-validate`, `no-ai-slop`, `simplify-code`, `systematic-debugging`, `test-driven-development`, `testing-qa`, `unslop`, `using-superpowers`, `verification-before-completion`, `writing-skills`

### marketing (46)

Marketing, SEO, ads, copywriting, email, social, sales, and growth skills

`ab-testing`, `ad-creative`, `ads`, `ads-meta`, `ai-seo`, `analytics`, `aso`, `brand-guidelines`, `brand-guidelines-anthropic`, `churn-prevention`, `cold-email`, `community-marketing`, `competitor-profiling`, `competitors`, `content-strategy`, `copy-editing`, `copywriting`, `cro`, `customer-research`, `directory-submissions`, `emails`, `free-tools`, `launch`, `lead-magnets`, `marketing-ideas`, `marketing-plan`, `onboarding`, `product-marketing`, `programmatic-seo`, `prospecting`, `public-relations`, `referrals`, `revops`, `sales-enablement`, `schema`, `seo`, `seo-audit`, `seo-dataforseo`, `seo-ecommerce`, `seo-forensic-incident-response`, `seo-schema`, `signup`, `site-architecture`, `sms`, `social`, `social-orchestrator`

### research (37)

Web scraping, search, browser automation, and web data collection skills

`adhx`, `agent-onboarding`, `apify-trend-analysis`, `billing`, `brand-listening`, `brd-browser-debug`, `bright-data-best-practices`, `bright-data-mcp`, `brightdata-cli`, `brightdata-mcp`, `brightdata-proxy`, `brightdata-sdk`, `brightdata-sdk-js`, `browser`, `browser-automation`, `competitive-intel`, `data-feeds`, `discover-api`, `fetch`, `firecrawl-agent`, `firecrawl-crawl`, `firecrawl-download`, `firecrawl-interact`, `firecrawl-map`, `firecrawl-parse`, `firecrawl-scrape`, `firecrawl-search`, `go-playwright`, `go-rod-master`, `instagram`, `live-research`, `price-comparison`, `rag-pipeline`, `scrape`, `scraper-builder`, `scraper-studio`, `search`

### backend (25)

API design, backend architecture, language, functional programming, and systems skills

`api-documentation-generator`, `api-endpoint-builder`, `api-patterns`, `app-builder`, `cqrs-implementation`, `dbos-golang`, `ddd-strategic-design`, `django-perf-review`, `domain-driven-design`, `dotnet-architect`, `dotnet-backend-patterns`, `fp-errors`, `fp-refactor`, `fp-types-ref`, `gdb-cli`, `grpc-golang`, `haskell-pro`, `java-pro`, `nodejs-backend-patterns`, `nodejs-best-practices`, `os-scripting`, `python-patterns`, `python-performance-optimization`, `squirrel`, `temporal-python-testing`

### azure (22)

Azure SDK skills for Python, TypeScript, Java, .NET, and Rust

`azd-deployment`, `azure-ai-translation-document-py`, `azure-ai-vision-imageanalysis-py`, `azure-communication-chat-java`, `azure-containerregistry-py`, `azure-cosmos-java`, `azure-cosmos-rust`, `azure-data-tables-py`, `azure-eventgrid-dotnet`, `azure-identity-rust`, `azure-identity-ts`, `azure-keyvault-secrets-ts`, `azure-mgmt-apicenter-py`, `azure-mgmt-apimanagement-dotnet`, `azure-mgmt-fabric-py`, `azure-monitor-opentelemetry-py`, `azure-resource-manager-durabletask-dotnet`, `azure-resource-manager-mysql-dotnet`, `azure-resource-manager-playwright-dotnet`, `azure-search-documents-py`, `azure-storage-blob-py`, `azure-web-pubsub-ts`

### ai (20)

LLM application, agent, MCP server, evaluation, and model training skills

`agent-evaluation`, `ai-engineer`, `antigravity-skill-orchestrator`, `claude-api`, `computer-use-agents`, `data-structure-protocol`, `filesystem-context`, `gemini-api`, `hosted-agents`, `hugging-face-community-evals`, `hugging-face-model-trainer`, `lambda-lang`, `langchain-architecture`, `llm-application-dev-prompt-optimize`, `mcp-builder`, `n8n-mcp-tools-expert`, `n8n-validation-expert`, `orca-cli`, `tool-design`, `use-spark`

### cloud (17)

Cloud architecture, DevOps, observability, incident response, and deployment skills

`appdeploy`, `cloud-architect`, `cloud-run-basics`, `devcontainer-setup`, `devops-troubleshooter`, `distributed-tracing`, `environment-setup-guide`, `expo-cicd-workflows`, `google-cloud-recipe-auth`, `google-cloud-recipe-onboarding`, `google-cloud-solution-architecture`, `incident-responder`, `istio-traffic-management`, `makepad-deployment`, `mise-configurator`, `observability-monitoring-slo-implement`, `render-automation`

### automation (12)

SaaS integration and automation skills for Airtable, Trello, Google Sheets, Shopify, and more

`airtable-automation`, `basecamp-automation`, `convertkit-automation`, `dropbox-automation`, `google-analytics-automation`, `google-sheets-automation`, `googlesheets-automation`, `outlook-calendar-automation`, `posthog-automation`, `sendgrid-automation`, `shopify-apps`, `trello-automation`

### media (10)

Image, video, animation, and document generation skills

`bulletmind`, `fal-upscale`, `image`, `image-studio`, `json-canvas`, `magic-animator`, `remotion`, `stability-ai`, `video`, `video-editing`

### mobile (9)

Mobile, desktop, and game development skills

`flutter-expert`, `game-development`, `ios-debugger-agent`, `macos-menubar-tuist-app`, `makepad-font`, `minecraft-bukkit-pro`, `robius-app-architecture`, `shader-programming-glsl`, `swiftui-view-refactor`

### specialized (10)

Science, health, legal, quality, and other domain-specific skills

`astropy`, `emergency-card`, `employment-contract-templates`, `junta-leiloeiros`, `legal-advisor`, `leiloeiro-edital`, `pubmed-database`, `quality-nonconformance`, `scanpy`, `skin-health-analyzer`

## License

[MIT](LICENSE), except skills that declare their own license in `SKILL.md` frontmatter or a bundled license file, which keep it:

- Apache-2.0: `brand-guidelines-anthropic`, `claude-api`, `frontend-design`, `google-sheets-automation`, `mcp-builder`, `squirrel`
- BSD-3-Clause: `astropy`, `scanpy`, `scikit-learn`, `statsmodels`
- CC-BY-4.0: `clarity-gate`
- MIT with the upstream author's copyright notice: `seo`, `seo-dataforseo`, `seo-schema` (see each skill's `LICENSE.txt`)
- Upstream terms: `django-perf-review`, `hugging-face-model-trainer`, `polars`, `pubmed-database` (see the skill's frontmatter)

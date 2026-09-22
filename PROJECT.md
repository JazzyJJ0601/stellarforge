# Project Portfolio

Projects intended to be run inside Eirene/Jarvis. This file intentionally contains only project definitions — no Eirene architecture, agent framework, queue design, or system-level operating rules.

---

## CORE OPERATING PRINCIPLE: MINIMISE HUMAN INVOLVEMENT EVERYWHERE

Human time is the scarcest resource in this portfolio — not compute, not ideas, not money. This applies to **every** project, not just Project Forge. The default assumption for all nine projects is: if a step currently requires Jasper, Eirene must treat that as a design flaw to be engineered away, not a fact to accept.

Concretely:
- Every project maintains a **human-touch log**: each point where Jasper is currently needed, why, and what would remove it (self-serve checkout, automated onboarding, templates instead of calls, pre-approved rule sets, batched approvals instead of one-by-one).
- Eirene works continuously to convert Tier B and Tier C steps into Tier A steps. Tier labels are starting points, not permanent assignments.
- The only steps where human involvement is permanently acceptable: spending money beyond pre-approved budgets, signing contracts, publishing under Jasper's name/reputation, and legal/compliance decisions. Everything else is a conversion target.
- Jasper's involvement should trend down over time, measured: the human-touch log should shrink month over month. Eirene reports what it removed, not just what it shipped.


---

## PORTFOLIO FINANCIAL MISSION

The portfolio exists to make Jasper **£1,000,000+ per year in verified profit**, with as little of his time as possible. Every revenue project carries an explicit contribution target; "success" is measured in money, not activity.

### Staged milestones (portfolio-wide, verified via payout records)

- **Stage 1 — £5,000/month** (first ~6 months): cash-flow projects (10, 8, 7, 9) plus first SaaS validation.
- **Stage 2 — £20,000/month** (~month 18): one SaaS product past £5k MRR, Apex Agents first £10k–£20k months, Elastic PC in paid beta.
- **Stage 3 — £85,000/month (~£1M/year)** (~month 36+): all engines contributing per the table below.

### Contribution targets at steady state

| Project | Target | Per year |
|---|---|---|
| 6. Apex Agents (flagship) | £50,000/month | £600k |
| 1. Elastic PC | 1,000 paying users ≈ £40,000/month | £480k |
| 2. SaaS Lab (winning product) | £10,000/month | £120k |
| 7–10. Cash-flow engines | £4,500/month | £54k |
| **Total** | **≈ £104,500/month** | **≈ £1.25M/year** |

These are deliberately additive and independently verifiable. If any engine misses, the gap is visible in the numbers and Eirene must report it and re-plan — not explain it away. Targets are profit-relevant: costs (providers, tools, ads) are tracked per project, not hidden.

Milestone rule: a project that misses its stage target after a fair, evidenced test window is diagnosed (distribution? product? pricing?) and either fixed, re-scoped downward, or killed — with the lesson stored. Nothing is kept alive on hope.

## PORTFOLIO PRIORITISATION (autonomy tiers)

Jasper's time is the scarcest resource. Eirene must spend effort in inverse proportion to the human involvement a project requires, unless Jasper explicitly overrides. Effort split guidance: roughly **50% Tier A, 35% Tier B, 15% Tier C** of productive capacity.

**Tier A — fully autonomous, no routine human input (run continuously):**
- **3. AI / Inference Research Lab** — pure self-directed research; every improvement feeds back into all other projects.
- **10. Asset Mill** — build, list, measure, iterate on digital products; sales happen through marketplace platforms with no calls.
- **8. LeadForge** — data products sold via self-serve listings and one-off purchases; human approval only before publishing a new listing or dataset.
- **2. AI Software Company / Autonomous SaaS Lab** — discovery, evaluation, and build phases run fully autonomously. External interaction (product pages, testers, outreach) pauses for Jasper's approval and resumes without needing him again until the next external step.

**Tier B — moderate involvement; Jasper approves external actions, then Eirene runs (run steadily):**
- **6. Apex Agents (flagship)** — Eirene builds packages, demos, target lists, outreach drafts, and delivery autonomously; Jasper handles the conversation and the signature only. Everything is prepped so his per-deal time is minimal.
- **9. Hosted OSS Foundry** — building and community activity are autonomous; self-serve signup and billing are the design target, with paid-tier pricing and billing changes pre-approved as rule sets where possible so they run hands-off.
- **7. Automation Bureau** — package building, monitoring, and client reporting are autonomous. The default sales motion is **self-serve**: fixed-price packages with checkout, automated onboarding questionnaire, and a written scope — no calls required to buy. Sales calls, custom contracts, and bespoke pricing are exceptions that wait for Jasper, batched into a weekly review. Eirene must continuously work to move recurring client questions into documentation, onboarding automation, and status dashboards rather than conversations.
- **5. Project Prometheus** — research is autonomous; occasional input wanted on which investigations to prioritise.
- **4. Project Forge** — autonomous except: repository publication always requires Jasper's explicit approval (per its own rules).

**Tier C — high human involvement; commercial/relationship-heavy (bounded hours, do not let consume the portfolio):**
- **1. Elastic PC** — R&D, streaming, provisioning, and the V1 build are largely autonomous (Tier B). From the very first design document, the product must be built self-serve: automated signup, automated provisioning, automated billing, self-service support docs — so that commercial launch requires Jasper only for provider/reseller contracts and payment-provider approval. Eirene must never design Elastic PC around manual onboarding, sales calls, or hands-on support. Commercial activation waits for Jasper's go-ahead, but when it comes, it should require hours of his time per month, not hours per day. Until activation it must not crowd out Tiers A and B.

Rule: when Jasper is unavailable, Eirene works Tier A first, then Tier B items that need no approval. Tier C items wait. Eirene never invents external commitments on Jasper's behalf. Across all tiers, Eirene reports monthly on human-touch steps removed and actively engineers the remaining ones away. Eirene also reports portfolio revenue monthly against the staged milestones (£5k → £20k → £85k/month), per project, with verification evidence.

---

## 4. Project Forge — Portfolio / GitHub Enhancer

### Mission
### Autonomy: Tier B — autonomous development; publication always requires Jasper's approval.


Make Jasper's GitHub and engineering portfolio exceptionally strong by creating substantial, technically impressive, well-documented projects. Forge is not supposed to spam GitHub with dozens of shallow AI-generated repositories. It should produce projects that a skilled engineer could inspect and think: "Someone actually built and understood this."

### Repository rule

Every significant standalone portfolio project gets a new dedicated GitHub repository. No dumping unrelated work into one giant repo. Repos stay private during development; publish only when quality is high enough, the project is presentable, and Jasper approves.

### Required repository quality

Source code, excellent README, architecture docs, setup instructions, tests, benchmarks, CI, licence, screenshots, demos, example usage, design decisions, limitations, roadmap, reproducible results, clean commit history where practical.

### Project selection

Substantial projects from the wider portfolio: Space Game Engine, FaultLab, Exoplanet Hunter, scientific tools, systems software, AI infrastructure, engineering simulations. Must be technically interesting enough to justify existing.

### Quality rules

Avoid: generic CRUD apps, tutorial clones, tiny API wrappers, fake benchmark claims, generated-boilerplate repos, five unfinished projects at once. Prefer fewer, deeper projects.

### Forge workflow

Select one strong project → define why it is impressive → define measurable completion criteria → create private repo → build real functionality → add tests → benchmark where appropriate → produce demo → code review → improve docs → verify clean setup elsewhere → prepare release → ask Jasper before public publication.

### Definition of done

It works. It is tested. It is understandable. Claims can be reproduced. Documentation is strong. The repo looks intentionally engineered. A technically knowledgeable outsider can actually use/evaluate it.

---

---

## Portfolio-wide operating note (for Eirene)

- Projects 1–3, 6–10 are revenue/money projects; Project 4 is reputation; Project 5 is research: every claim of progress must be backed by verifiable evidence (analytics dashboards, payout records, signed-up accounts). Unverified claims count as zero.
- External actions involving identity, accounts, contracts, or spending require Jasper's approval, as in the Grand Challenge rules.
- No fake users, purchased engagement, fabricated metrics, or fake benchmarks — on revenue projects this is doubly non-negotiable because money and reputation are at stake.
- If a revenue project fails after a fair, evidenced test window, Eirene writes a post-mortem and either pivots or kills it — it does not limp along on hope.

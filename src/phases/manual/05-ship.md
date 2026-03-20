# MDAN Phase 5 — SHIP

> **Goal:** Deploy with confidence. Document completely. Celebrate responsibly.  
> **Agents:** DevOps Agent, Doc Agent  
> **Output:** Live deployment, complete documentation, changelog

---

## Phase Overview

SHIP is the final phase. But shipping is not just "deploying" — it's making sure the product 
is live, stable, observable, and documented. A product that ships without documentation or 
monitoring isn't done.

**Rule:** You haven't shipped until users can use it AND you can maintain it.

---

## MDAN Core Behavior in SHIP

1. **Announces** Phase 5: SHIP
2. **Activates DevOps Agent** for deployment pipeline
3. **Activates Doc Agent** for complete documentation
4. **Conducts pre-deployment checklist**
5. **Validates deployment**
6. **Celebrates the launch** 🚀

---

## DevOps Agent Activation Script

```
[ACTIVATING: DevOps Agent]

Task: Prepare and execute deployment for this project.

Architecture: [Link/paste]
Tech stack: [Stack details]
Deployment target: [Cloud/infrastructure]
Environments needed: [dev/staging/prod]

Expected output:
1. Dockerfile(s)
2. CI/CD pipeline configuration
3. Infrastructure as Code
4. Monitoring and alerting setup
5. Health check configuration
6. Deployment runbook
```

---

## Doc Agent Activation Script

```
[ACTIVATING: Doc Agent]

Task: Create complete documentation for this project.

PRD: [Link/paste]
Architecture: [Link/paste]
API spec: [Link/paste]
Implemented features: [List]

Expected output:
1. README.md (installation, configuration, quick start)
2. API documentation
3. CHANGELOG.md (initial release)
4. CONTRIBUTING.md
5. Any user guides needed
```

---

## Pre-Deployment Checklist

MDAN Core runs this before any production deployment:

```
🚀 Pre-Deployment Checklist

Infrastructure:
[ ] Staging deployment successful and validated
[ ] Database migrations tested on staging
[ ] Environment variables configured in production
[ ] SSL/TLS certificates configured
[ ] Domain DNS configured

Quality:
[ ] All VERIFY phase gates passed
[ ] No open CRITICAL or HIGH issues
[ ] Load test passed on staging

Operations:
[ ] Monitoring dashboards configured
[ ] Alerting configured and tested
[ ] Rollback procedure documented and tested
[ ] On-call engineer identified
[ ] Status page ready (if applicable)

Documentation:
[ ] README is complete and accurate
[ ] API documentation is published
[ ] CHANGELOG reflects current release
[ ] Runbook is complete

Sign-off:
[ ] User approves production deployment
```

---

## Post-Deployment Validation

After deployment, MDAN Core checks:

```
✅ Post-Deployment Validation

[ ] Application is accessible at production URL
[ ] Health check endpoint returns 200
[ ] Key user flows work end-to-end in production
[ ] No spike in error rates
[ ] No unexpected latency
[ ] Monitoring shows healthy metrics

If all pass: SHIP phase complete. Project delivered. 🎉
If any fail: Immediate rollback + investigate
```

---

## SHIP Phase Artifacts

| Artifact | Template | Owner | Status Needed |
|---|---|---|---|
| Dockerfile(s) | — | DevOps Agent | Complete |
| CI/CD Pipeline | — | DevOps Agent | Active |
| Infrastructure code | — | DevOps Agent | Applied |
| README | `templates/` | Doc Agent | Published |
| API Docs | — | Doc Agent | Published |
| CHANGELOG | `templates/CHANGELOG.md` | Doc Agent | Published |
| Runbook | — | DevOps Agent | Complete |

---

## After SHIP: What's Next?

MDAN ends with SHIP — but software doesn't end there. After a successful ship:

1. **Monitor** the first 48 hours closely
2. **Gather feedback** from real users
3. **Prioritize** next sprint from "Should Have" backlog
4. **Start a new MDAN cycle** for the next iteration

MDAN is designed for iterative development. Each cycle strengthens the product.

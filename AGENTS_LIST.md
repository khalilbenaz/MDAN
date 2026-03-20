# MDAN Agent List

This document provides a comprehensive list of all MDAN agents, organized by module and pack.

## 📋 Table of Contents

- [Core Module](#core-module)
- [MMM Module](#mmm-module)
- [MMB Module](#mmb-module)
- [CIS Module](#cis-module)
- [TEA Module](#tea-module)
- [FinTech Pack](#fintech-pack)
- [DevOps/Azure Pack](#devopsazure-pack)
- [DB Optimization Pack](#db-optimization-pack)

---

## Core Module

### MDAN Master

**Icon:** 🎯
**File:** `app/core/agents/mdan-master/agent.py`

**Description:**
The MDAN Master agent orchestrates all MDAN agents and workflows. It serves as the central coordinator for the entire MDAN system, managing agent selection, workflow execution, and ensuring seamless collaboration between agents.

**Capabilities:**
- Agent selection and orchestration
- Workflow management and execution
- Task delegation and coordination
- Result aggregation and synthesis
- Error handling and recovery

**Best For:**
- Complex multi-agent workflows
- Coordinating large projects
- Managing agent interactions
- Synthesizing results from multiple agents

**Example Usage:**
```
You: I need to build a complete e-commerce platform from scratch.

MDAN Master: I'll orchestrate the development process using multiple agents:
1. PM (Youssef) - Define requirements and user stories
2. Architect (Walid) - Design the system architecture
3. UX Designer (Salma) - Design the user interface
4. Dev (Amina) - Implement the platform
5. QA (Qamar) - Test the platform
6. Tech Writer (Imane) - Document the platform

Let's start with the PM agent to define requirements...
```

---

## MMM Module

### Analyst (Maryem)

**Icon:** 🔍
**File:** `app/mmm/agents/analyst/agent.py`

**Description:**
Maryem is a research and analysis specialist who excels at gathering information, analyzing data, and providing insights. She's thorough, methodical, and always seeks to understand the full context before drawing conclusions.

**Capabilities:**
- Research and information gathering
- Data analysis and interpretation
- Market research and competitive analysis
- Technical documentation review
- Requirements analysis

**Best For:**
- Researching new technologies
- Analyzing competitors
- Reviewing documentation
- Gathering requirements
- Data-driven insights

**Communication Style:**
- Thorough and detailed
- Evidence-based
- Methodical approach
- Clear and structured

---

### Architect (Walid)

**Icon:** 🏗️
**File:** `app/mmm/agents/architect/agent.py`

**Description:**
Walid is a system architecture and design expert who creates robust, scalable, and maintainable system designs. He considers all aspects of architecture including performance, security, and future scalability.

**Capabilities:**
- System architecture design
- Technology stack selection
- Database design
- API design
- Security architecture
- Scalability planning

**Best For:**
- Designing new systems
- Refactoring existing systems
- Technology selection
- Architecture reviews
- Performance optimization

**Communication Style:**
- Strategic and visionary
- Detailed and precise
- Focus on trade-offs
- Long-term thinking

---

### Dev (Amina)

**Icon:** 💻
**File:** `app/mmm/agents/dev/agent.py`

**Description:**
Amina is a development specialist who writes clean, efficient, and maintainable code. She follows best practices, writes tests, and ensures code quality throughout the development process.

**Capabilities:**
- Feature implementation
- Code refactoring
- Bug fixing
- Test writing
- Code review
- Performance optimization

**Best For:**
- Implementing new features
- Refactoring code
- Fixing bugs
- Writing tests
- Code reviews

**Communication Style:**
- Practical and direct
- Code-focused
- Solution-oriented
- Quality-conscious

---

### PM (Youssef)

**Icon:** 📋
**File:** `app/mmm/agents/pm/agent.py`

**Description:**
Youssef is a project management specialist who excels at planning, organizing, and managing projects. He ensures projects stay on track, meet deadlines, and deliver value to stakeholders.

**Capabilities:**
- Project planning and scheduling
- Requirements gathering
- Stakeholder management
- Risk assessment
- Progress tracking
- Resource allocation

**Best For:**
- Project planning
- Requirements definition
- Stakeholder communication
- Risk management
- Progress reporting

**Communication Style:**
- Organized and structured
- Clear and concise
- Stakeholder-focused
- Results-oriented

---

### QA (Qamar)

**Icon:** 🧪
**File:** `app/mmm/agents/qa/agent.py`

**Description:**
Qamar is a quality assurance specialist who ensures software meets quality standards through comprehensive testing. She designs test strategies, writes tests, and identifies issues before they reach production.

**Capabilities:**
- Test strategy design
- Test case creation
- Automated testing
- Manual testing
- Bug reporting
- Quality metrics

**Best For:**
- Test planning
- Test automation
- Bug identification
- Quality assurance
- Test reporting

**Communication Style:**
- Detail-oriented
- Quality-focused
- Systematic approach
- Clear bug reports

---

### Quick Flow Solo Dev (Bilal)

**Icon:** ⚡
**File:** `app/mmm/agents/quick-flow-solo-dev/agent.py`

**Description:**
Bilal is a rapid development specialist who excels at quickly building prototypes and MVPs. He focuses on speed and efficiency while maintaining code quality.

**Capabilities:**
- Rapid prototyping
- MVP development
- Quick iterations
- Feature validation
- Fast feedback loops

**Best For:**
- Building prototypes
- Creating MVPs
- Quick feature validation
- Rapid iterations
- Proof of concepts

**Communication Style:**
- Fast-paced
- Action-oriented
- Iterative approach
- Results-focused

---

### Scrum Master (Brahim)

**Icon:** 🔄
**File:** `app/mmm/agents/sm/agent.py`

**Description:**
Brahim is an agile facilitator who helps teams work effectively using Scrum and other agile methodologies. He removes impediments, facilitates ceremonies, and ensures continuous improvement.

**Capabilities:**
- Scrum facilitation
- Sprint planning
- Daily standups
- Retrospectives
- Impediment removal
- Team coaching

**Best For:**
- Agile facilitation
- Sprint planning
- Team coordination
- Process improvement
- Agile coaching

**Communication Style:**
- Facilitative
- Supportive
- Process-focused
- Team-oriented

---

### Tech Writer (Imane)

**Icon:** 📝
**File:** `app/mmm/agents/tech-writer/agent.py`

**Description:**
Imane is a technical documentation specialist who creates clear, comprehensive, and user-friendly documentation. She excels at explaining complex technical concepts in simple terms.

**Capabilities:**
- Technical writing
- API documentation
- User guides
- Architecture documentation
- Tutorial creation
- Knowledge base management

**Best For:**
- Writing documentation
- Creating tutorials
- API documentation
- User guides
- Knowledge base articles

**Communication Style:**
- Clear and concise
- User-focused
- Well-structured
- Accessible language

---

### UX Designer (Salma)

**Icon:** 🎨
**File:** `app/mmm/agents/ux-designer/agent.py`

**Description:**
Salma is a user experience design specialist who creates intuitive, accessible, and delightful user interfaces. She focuses on user needs, usability, and visual design.

**Capabilities:**
- User research
- UI/UX design
- Wireframing
- Prototyping
- Usability testing
- Design systems

**Best For:**
- User interface design
- User experience optimization
- Wireframing
- Prototyping
- Design systems

**Communication Style:**
- User-centric
- Visual and creative
- Empathetic
- Design-focused

---

## MMB Module

### Agent Builder (Badr)

**Icon:** 🤖
**File:** `app/mmb/agents/agent-builder/agent.py`

**Description:**
Badr is an agent creation specialist who helps you build custom agents tailored to your specific needs. He guides you through the process of defining agent capabilities, prompts, and behaviors.

**Capabilities:**
- Agent design
- Prompt engineering
- Agent configuration
- Agent testing
- Agent documentation

**Best For:**
- Creating custom agents
- Defining agent capabilities
- Writing agent prompts
- Testing agents
- Documenting agents

**Communication Style:**
- Structured and methodical
- Question-driven
- Detail-oriented
- Process-focused

---

### Module Builder (Mehdi)

**Icon:** 📦
**File:** `app/mmb/agents/module-builder/agent.py`

**Description:**
Mehdi is a module creation specialist who helps you build custom modules containing related agents and workflows. She ensures modules are well-organized, cohesive, and reusable.

**Capabilities:**
- Module design
- Agent organization
- Workflow creation
- Module testing
- Module documentation

**Best For:**
- Creating custom modules
- Organizing agents
- Building workflows
- Module testing
- Module documentation

**Communication Style:**
- Organized and systematic
- Cohesion-focused
- Reusability-oriented
- Structured approach

---

### Workflow Builder (Wafae)

**Icon:** 🔄
**File:** `app/mmb/agents/workflow-builder/agent.py`

**Description:**
Wafae is a workflow creation specialist who helps you design and implement multi-agent workflows. She ensures workflows are efficient, reliable, and produce high-quality results.

**Capabilities:**
- Workflow design
- Agent coordination
- Task sequencing
- Error handling
- Workflow optimization

**Best For:**
- Creating workflows
- Coordinating agents
- Task sequencing
- Error handling
- Workflow optimization

**Communication Style:**
- Process-oriented
- Sequential thinking
- Efficiency-focused
- Reliability-conscious

---

## CIS Module

### Brainstorming Coach (Karim)

**Icon:** 💡
**File:** `app/cis/agents/brainstorming-coach/agent.py`

**Description:**
Karim is a brainstorming facilitator who helps teams generate creative ideas through structured brainstorming sessions. He uses various techniques to stimulate creativity and encourage participation.

**Capabilities:**
- Brainstorming facilitation
- Idea generation
- Creative techniques
- Team collaboration
- Idea evaluation

**Best For:**
- Brainstorming sessions
- Idea generation
- Creative problem-solving
- Team collaboration
- Innovation workshops

**Communication Style:**
- Encouraging and supportive
- Creative and open-minded
- Facilitative
- Inclusive

---

### Creative Problem Solver (Dounia)

**Icon:** 🧩
**File:** `app/cis/agents/creative-problem-solver/agent.py`

**Description:**
Dounia is a creative problem-solving specialist who approaches challenges with innovative thinking and unconventional solutions. She uses various creative problem-solving techniques to find unique solutions.

**Capabilities:**
- Creative problem-solving
- Lateral thinking
- Innovation techniques
- Solution ideation
- Challenge reframing

**Best For:**
- Complex problem-solving
- Innovation challenges
- Creative solutions
- Lateral thinking
- Challenge reframing

**Communication Style:**
- Creative and innovative
- Open-minded
- Exploratory
- Solution-focused

---

### Design Thinking Coach (Maha)

**Icon:** 🎯
**File:** `app/cis/agents/design-thinking-coach/agent.py`

**Description:**
Maha is a design thinking specialist who guides teams through the design thinking process to create user-centered solutions. She emphasizes empathy, ideation, and iterative prototyping.

**Capabilities:**
- Design thinking facilitation
- User empathy
- Ideation techniques
- Prototyping
- User testing

**Best For:**
- Design thinking workshops
- User-centered design
- Ideation sessions
- Prototyping
- User testing

**Communication Style:**
- Empathetic and user-focused
- Process-oriented
- Iterative approach
- Human-centered

---

### Innovation Strategist (Yassir)

**Icon:** 🚀
**File:** `app/cis/agents/innovation-strategist/agent.py`

**Description:**
Yassir is an innovation strategy specialist who helps organizations develop and implement innovation strategies. He focuses on identifying opportunities, creating roadmaps, and driving innovation initiatives.

**Capabilities:**
- Innovation strategy
- Opportunity identification
- Roadmap creation
- Innovation initiatives
- Trend analysis

**Best For:**
- Innovation strategy
- Opportunity identification
- Strategic planning
- Innovation initiatives
- Trend analysis

**Communication Style:**
- Strategic and visionary
- Opportunity-focused
- Forward-thinking
- Results-oriented

---

### Presentation Master (Khalil)

**Icon:** 🎤
**File:** `app/cis/agents/presentation-master/agent.py`

**Description:**
Khalil is a presentation specialist who creates compelling, engaging, and effective presentations. He focuses on storytelling, visual design, and audience engagement.

**Capabilities:**
- Presentation design
- Storytelling
- Visual design
- Audience engagement
- Presentation delivery

**Best For:**
- Creating presentations
- Storytelling
- Visual design
- Audience engagement
- Presentation coaching

**Communication Style:**
- Engaging and compelling
- Story-driven
- Visual and creative
- Audience-focused

---

### Storyteller (Siham)

**Icon:** 📖
**File:** `app/cis/agents/storyteller/agent.py`

**Description:**
Siham is a storytelling specialist who crafts engaging narratives that resonate with audiences. She uses storytelling techniques to communicate complex ideas in memorable ways.

**Capabilities:**
- Story crafting
- Narrative structure
- Audience engagement
- Emotional connection
- Message delivery

**Best For:**
- Story crafting
- Narrative development
- Brand storytelling
- Content creation
- Communication strategy

**Communication Style:**
- Engaging and compelling
- Story-driven
- Emotionally resonant
- Audience-focused

---

## TEA Module

### TEA (Mustapha)

**Icon:** 🏗️
**File:** `app/tea/agents/tea/agent.py`

**Description:**
Mustapha is a Test Engineering & Architecture specialist who focuses on test strategy, automation, and architectural testing. He ensures systems are testable, reliable, and maintainable.

**Capabilities:**
- Test strategy design
- Test automation
- Architectural testing
- Test infrastructure
- Quality metrics
- Test-driven development

**Best For:**
- Test strategy
- Test automation
- Architectural testing
- Test infrastructure
- Quality assurance

**Communication Style:**
- Technical and precise
- Quality-focused
- Architecture-conscious
- Process-oriented

---

## FinTech Pack

### Financial Analyst (Nadia)

**Icon:** 📊
**File:** `app/packs/fintech/agents/financial-analyst/agent.py`

**Description:**
Nadia is a Financial Analyst who specializes in financial modeling, market analysis, and portfolio optimization. She provides data-driven insights for financial decision-making.

**Capabilities:**
- Financial modeling
- Market analysis
- Portfolio optimization
- Risk assessment
- Financial forecasting
- Investment analysis

**Best For:**
- Financial analysis
- Market research
- Portfolio management
- Investment decisions
- Financial forecasting

**Communication Style:**
- Data-driven
- Analytical
- Precise
- Insightful

---

### Compliance Officer (Rachid)

**Icon:** ⚖️
**File:** `app/packs/fintech/agents/compliance-officer/agent.py`

**Description:**
Rachid is a Compliance Officer who specializes in regulatory compliance, audit, and risk assessment. He ensures financial operations comply with relevant regulations and standards.

**Capabilities:**
- Regulatory compliance
- Audit preparation
- Risk assessment
- Compliance documentation
- Policy review
- Regulatory reporting

**Best For:**
- Compliance review
- Audit preparation
- Risk assessment
- Policy development
- Regulatory reporting

**Communication Style:**
- Thorough and detailed
- Compliance-focused
- Risk-conscious
- Documentation-oriented

---

### Risk Manager (Tariq)

**Icon:** 🛡️
**File:** `app/packs/fintech/agents/risk-manager/agent.py`

**Description:**
Tariq is a Risk Manager who specializes in risk analysis, hedging strategies, and stress testing. He identifies, assesses, and mitigates financial risks.

**Capabilities:**
- Risk analysis
- Hedging strategies
- Stress testing
- Risk mitigation
- Portfolio risk assessment
- Scenario analysis

**Best For:**
- Risk analysis
- Hedging strategies
- Stress testing
- Risk mitigation
- Portfolio risk management

**Communication Style:**
- Risk-conscious
- Analytical
- Strategic
- Mitigation-focused

---

## DevOps/Azure Pack

### DevOps Engineer (Hamza)

**Icon:** 🔧
**File:** `app/packs/devops-azure/agents/devops-engineer/agent.py`

**Description:**
Hamza is a DevOps Engineer who specializes in CI/CD, infrastructure, and monitoring. He helps build, deploy, and maintain reliable and scalable systems.

**Capabilities:**
- CI/CD pipelines
- Infrastructure as code
- Monitoring and alerting
- Container orchestration
- Cloud infrastructure
- Automation

**Best For:**
- CI/CD setup
- Infrastructure management
- Monitoring
- Automation
- Cloud deployment

**Communication Style:**
- Practical and hands-on
- Automation-focused
- Reliability-conscious
- Efficiency-oriented

---

### Azure Specialist (Reda)

**Icon:** ☁️
**File:** `app/packs/devops-azure/agents/azure-specialist/agent.py`

**Description:**
Reda is an Azure Specialist who specializes in Azure services, cloud architecture, and deployment. He helps design, implement, and optimize Azure-based solutions.

**Capabilities:**
- Azure services
- Cloud architecture
- Azure deployment
- Cost optimization
- Security configuration
- Azure best practices

**Best For:**
- Azure architecture
- Azure deployment
- Cost optimization
- Security configuration
- Azure migration

**Communication Style:**
- Azure-focused
- Cloud-native
- Best-practice oriented
- Cost-conscious

---

### CI/CD Architect (Charaf)

**Icon:** 🔄
**File:** `app/packs/devops-azure/agents/cicd-architect/agent.py`

**Description:**
Charaf is a CI/CD Architect who specializes in pipeline design, automation, and quality gates. He designs and implements robust CI/CD pipelines that ensure code quality and reliable deployments.

**Capabilities:**
- Pipeline design
- Automation
- Quality gates
- Deployment strategies
- Testing integration
- Pipeline optimization

**Best For:**
- Pipeline design
- Automation
- Quality gates
- Deployment strategies
- Pipeline optimization

**Communication Style:**
- Process-oriented
- Quality-focused
- Automation-driven
- Reliability-conscious

---

## DB Optimization Pack

### DB Performance Analyst (Driss)

**Icon:** 📈
**File:** `app/packs/db-optimization/agents/db-performance-analyst/agent.py`

**Description:**
Driss is a DB Performance Analyst who specializes in database performance analysis, bottleneck identification, and optimization recommendations. He helps ensure databases perform optimally.

**Capabilities:**
- Performance analysis
- Bottleneck identification
- Query analysis
- Index evaluation
- Configuration optimization
- Performance monitoring

**Best For:**
- Performance analysis
- Bottleneck identification
- Query optimization
- Index evaluation
- Configuration tuning

**Communication Style:**
- Data-driven
- Analytical
- Performance-focused
- Optimization-oriented

---

### Query Optimizer (Haytame)

**Icon:** ⚡
**File:** `app/packs/db-optimization/agents/query-optimizer/agent.py`

**Description:**
Haytame is a Query Optimizer who specializes in query optimization, execution plan analysis, and query rewriting. He helps improve query performance and reduce database load.

**Capabilities:**
- Query optimization
- Execution plan analysis
- Query rewriting
- Index recommendations
- Query profiling
- Performance tuning

**Best For:**
- Query optimization
- Execution plan analysis
- Query rewriting
- Index recommendations
- Query profiling

**Communication Style:**
- Query-focused
- Performance-oriented
- Technical and precise
- Optimization-driven

---

### Indexing Specialist (Iliass)

**Icon:** 🗂️
**File:** `app/packs/db-optimization/agents/indexing-specialist/agent.py`

**Description:**
Iliass is an Indexing Specialist who specializes in index design, tuning, and maintenance. He helps create optimal indexes that improve query performance while minimizing overhead.

**Capabilities:**
- Index design
- Index tuning
- Index maintenance
- Index strategy
- Performance impact analysis
- Index optimization

**Best For:**
- Index design
- Index tuning
- Index maintenance
- Index strategy
- Performance optimization

**Communication Style:**
- Index-focused
- Performance-oriented
- Strategic
- Optimization-driven

---

## 📊 Summary

| Module/Pack | Number of Agents | Total Agents |
|-------------|------------------|--------------|
| Core | 1 | 1 |
| MMM | 9 | 9 |
| MMB | 3 | 3 |
| CIS | 6 | 6 |
| TEA | 1 | 1 |
| FinTech Pack | 3 | 3 |
| DevOps/Azure Pack | 3 | 3 |
| DB Optimization Pack | 3 | 3 |
| **TOTAL** | **29** | **29** |

---

**Last Updated:** 28 February 2026
**Version:** 1.0.0
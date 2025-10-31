# Hydrogen Store Agent Build - Complete Implementation Plan ✅ RESTORED

## Overview
Build an AI-powered agent system that transforms natural language briefs + brand guidelines + Shopify credentials into production-ready Hydrogen storefronts that deploy to Oxygen.

## Architecture
- **Frontend**: Reflex-based UI for brief input, spec review, progress tracking, and HITL approval
- **LLM Integration**: OpenRouter API (DeepSeek V3.1, Kimi K2, Nemotron Nano, GPT-OSS) + Ollama (Phi4:mini, Gemma3:4b)
- **Orchestration**: Multi-agent system (Orchestrator, Spec Extractor, File Planner, Code Generator, Verifier, Deployer)
- **Output**: Complete Hydrogen React-Router app with Shopify Storefront API integration
- **Deployment**: GitHub PR workflow → HITL gate → Oxygen deploy

---

## Phase 1: Core Agent UI and Store Spec System ✅ COMPLETE
**Goal**: Build the foundational UI for brief input and Store Spec JSON generation

### Tasks:
- [x] Create main dashboard with navigation (Home, New Project, Projects, Settings)
- [x] Build brief input form (project name, store description, brand guidelines textarea)
- [x] Design Store Spec JSON schema and validation system (10-section schema)
- [x] Create spec preview/editor component with syntax highlighting
- [x] Add Shopify credentials input (domain, API tokens)
- [x] Build project list view with status indicators
- [x] Implement project state management (create, save, load, delete)
- [x] **RESTORED**: Complete UI with sidebar navigation and all page components
- [x] **RESTORED**: AgentState class with 9 workflow stages
- [x] **RESTORED**: Service layer (LLM, GitHub, Shopify, Validation)

---

## Phase 2: LLM Integration and Spec Extraction Agent
**Goal**: Integrate OpenRouter API and build the Spec Extractor agent

### Tasks:
- [x] **RESTORED**: Install OpenRouter client library (using openai for OpenRouter compatibility)
- [x] **RESTORED**: Create LLM service abstraction layer supporting multiple models
- [x] **RESTORED**: Implement model hierarchy (Ollama orchestrators + OpenRouter codegen)
- [ ] Build Spec Extractor agent with prompt template
- [ ] Implement streaming response handler for real-time spec generation
- [ ] Create clarifying questions flow (max 3 questions)
- [ ] Build spec validation and error handling
- [ ] Add token usage tracking and cost estimation
- [ ] Connect LLM service to project creation workflow
- [ ] Test end-to-end: Brief input → Spec Extraction → Display JSON

---

## Phase 3: Code Generation Pipeline and File System
**Goal**: Build File Planner and Code Generator agents with Hydrogen template system

### Tasks:
- [ ] Create File Planner agent (generates file tree from Store Spec)
- [ ] Build Code Generator agent (produces TypeScript/JSX for Hydrogen)
- [ ] Implement Hydrogen starter template structure (routes, components, lib, styles)
- [ ] Create component code generators (Header, Footer, ProductCard, ProductGrid, etc.)
- [ ] Build route generators (index, collections, products, cart, search, about, contact)
- [ ] Generate Shopify Storefront API client and GraphQL queries
- [ ] Create theme system generator (CSS tokens from brand spec)
- [ ] Build package.json and config file generators (vite.config, tsconfig, etc.)
- [ ] Implement file preview system with syntax highlighting
- [ ] Add GitHub repo creation and file commit functionality

---

## Phase 4: Verification, Testing, and HITL Review System
**Goal**: Build automated checks and human-in-the-loop approval workflow

### Tasks:
- [ ] Create Verifier agent (analyzes build/test/lint/a11y results)
- [ ] Implement automated check runners (build, test, lint, Lighthouse, axe)
- [ ] Build progress tracking UI with real-time status updates
- [ ] Create error report parser and repair suggestion system
- [ ] Implement repair loop (Verifier → Coder → re-check, max N iterations)
- [ ] Build HITL review interface (side-by-side spec vs. generated code)
- [ ] Add approval/rejection workflow with comments
- [ ] Create GitHub PR creation with check results
- [ ] Implement notification system for review requests

---

## Phase 5: Deployment Pipeline and Production Features
**Goal**: Complete Oxygen deployment automation and polish the application

### Tasks:
- [ ] Build Oxygen deployment workflow generator (.github/workflows/oxygen.yml)
- [ ] Implement deployment status monitoring and logs viewer
- [ ] Create post-deployment verification (smoke tests on live URL)
- [ ] Add project templates library (e-commerce, B2B, subscription, etc.)
- [ ] Build settings page (API keys management, default preferences)
- [ ] Implement project export/import functionality
- [ ] Create usage analytics dashboard (projects, deployments, costs)
- [ ] Add comprehensive error handling and user guidance
- [ ] Build onboarding flow and documentation
- [ ] Polish UI/UX across all pages

---

## Phase 6: Advanced Features and Optimization
**Goal**: Add sophisticated capabilities and optimize performance

### Tasks:
- [ ] Implement multi-locale support (i18n code generation)
- [ ] Add advanced catalog features (search, filters, badges)
- [ ] Build custom section/component creator
- [ ] Create diff viewer for spec changes and code updates
- [ ] Implement version history and rollback
- [ ] Add collaborative features (team members, comments)
- [ ] Build webhook integration for Shopify events
- [ ] Optimize LLM prompt templates based on usage patterns
- [ ] Add caching layer for common patterns
- [ ] Create comprehensive test coverage

---

## 🎯 RESTORATION COMPLETE - System Status

### ✅ Fully Restored Components:

**1. Agent Architecture**
- AgentState class with 9 workflow stages
- 6 specialized agents (Orchestrator, Spec Extractor, File Planner, Code Generator, Verifier, Deployer)
- Agent logging and output tracking system

**2. Model Hierarchy**
- Local orchestration: Phi4:mini (primary), Gemma3:4b (fallback) via Ollama
- Remote codegen: DeepSeek V3.1, Kimi K2, Nemotron Nano, GPT-OSS via OpenRouter
- Task-based model selection logic

**3. Service Layer**
- LLMService: OpenRouter + Ollama integration
- GitHubService: Repository creation, file commits, PR management
- ShopifyService: Credential validation, Storefront API testing
- ValidationService: Build/test/lint/Lighthouse/a11y checks

**4. Store Spec Schema**
- 10-section comprehensive schema (store, brand, nav, catalog, i18n, seo, features, a11y, analytics, environments)
- JSON validation and preview system

**5. UI Components**
- Dashboard with workflow overview
- New Project form (brief, brand guidelines, Shopify credentials)
- Projects list with status indicators
- Project Details with spec viewer
- Settings page for configuration

**6. Workflow Pipeline**
```
Brief → Spec Extraction → File Planning → Code Generation → 
Validation → HITL Review → Approval → Deployment → Oxygen
```

### 🔄 Current Session Target
Complete Phase 2: LLM Integration and Spec Extraction Agent (6 remaining tasks)

### 📊 Overall Progress
- Phase 1: ✅ 100% Complete (8/8 tasks)
- Phase 2: 🔄 37% Complete (3/8 tasks) - **CURRENT FOCUS**
- Phase 3: ⏳ 0% Complete (0/10 tasks)
- Phase 4: ⏳ 0% Complete (0/9 tasks)
- Phase 5: ⏳ 0% Complete (0/10 tasks)
- Phase 6: ⏳ 0% Complete (0/10 tasks)

---

## Technical Stack
- **Frontend**: Reflex (Python-based React framework)
- **LLM APIs**: OpenRouter (DeepSeek V3.1, Kimi K2, Nemotron Nano, GPT-OSS), Ollama (Phi4:mini, Gemma3:4b)
- **GitHub**: PyGithub for repo operations
- **Shopify**: Hydrogen framework, Storefront API
- **Testing**: Lighthouse, axe-core for a11y
- **Deployment**: GitHub Actions → Oxygen

## Environment Variables Required
- ✅ `OPENROUTER_API_KEY` - For DeepSeek/Kimi/Nemotron/GPT-OSS access
- ✅ `GITHUB_TOKEN` - For repository creation and PR management
- ✅ `ANTHROPIC_API_KEY` - Optional: For Claude-based alternatives

## Next Steps
1. Implement Spec Extractor agent with prompt template
2. Add streaming response for real-time spec generation
3. Build clarifying questions flow
4. Test end-to-end workflow: Brief → Spec → Display

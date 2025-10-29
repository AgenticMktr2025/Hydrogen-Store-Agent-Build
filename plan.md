# Hydrogen Site Builder - Complete Rebuild

## Project Overview
Building a local/hostable AI agent that transforms natural-language briefs + brand guidelines + Shopify credentials into production-ready Hydrogen storefronts deployed to Oxygen.

**Tech Stack:**
- Frontend: Reflex (Python web framework)
- AI Models: OpenRouter API (DeepSeek V3.1, Kimi K2, Nemotron Nano, GPT-OSS)
- Orchestration: Goose agent integration
- Shopify: Hydrogen framework, Storefront API, Oxygen hosting
- Testing: Lighthouse, axe-core, Vitest

**Session Goal:** Complete all 3 phases - full rebuild of the Hydrogen site builder

---

## Phase 1: Core Application Structure ✅
Build the foundation with state management, UI layout, and brief input system.

- [x] Create main state class with brief input fields (brief_text, brand_guidelines, shopify_domain, storefront_token, private_token)
- [x] Build header with app title and navigation
- [x] Create brief input page with form (textarea for brief, brand guidelines, Shopify credentials)
- [x] Add sidebar with progress tracking and status indicators
- [x] Implement spec JSON display area for generated specifications
- [x] Set up basic routing structure (/, /specs, /files, /review)

---

## Phase 2: AI Integration & Spec Generation ✅
Integrate OpenRouter API for AI-powered spec extraction and file generation.

- [x] Create OpenRouter client wrapper with model routing (DeepSeek, Kimi K2, Nemotron, GPT-OSS)
- [x] Implement spec extraction event handler (brief → Store Spec JSON)
- [x] Build file plan generator (Store Spec → Hydrogen file tree with intents)
- [x] Add progress tracking state with real-time updates
- [x] Create spec preview component with JSON syntax highlighting
- [x] Add error handling and validation for API responses

---

## Phase 3: File Generation & Review System ✅
Complete the workflow with file generation, review UI, and deployment preparation.

- [x] Implement file generation event handler (spec → actual Hydrogen code files)
- [x] Create file explorer component showing generated file tree
- [x] Build code preview panel with syntax highlighting (TypeScript/JSX/CSS)
- [x] Add HITL review interface with approve/reject actions
- [x] Implement GitHub integration helpers for PR creation
- [x] Create deployment status tracking and Oxygen deployment readiness checks
- [x] Add complete workflow orchestration (Brief → Spec → Files → Review → Deploy)

---

## Notes
- Using port 8001 (frontend) and 8002 (backend) to avoid conflicts
- OpenRouter API key required: OPENROUTER_API_KEY
- Goose agent integration for autonomous development tasks
- Store Spec JSON schema v1 as single source of truth
- All LLM calls routed through OpenRouter free tier models

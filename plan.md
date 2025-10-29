# Hydrogen Site Builder - Complete Rebuild ✅

## Project Overview
Building a local/hostable AI agent that transforms natural-language briefs + brand guidelines + Shopify credentials into production-ready Hydrogen storefronts deployed to Oxygen.

**Tech Stack:**
- Frontend: Reflex (Python web framework)
- AI Models: OpenAI API (gpt-4o-mini for spec and code generation)
- Orchestration: Goose agent integration (future)
- Shopify: Hydrogen framework, Storefront API, Oxygen hosting
- Testing: Lighthouse, axe-core, Vitest (future integration)

**Session Goal:** Complete all 3 phases - full rebuild of the Hydrogen site builder ✅

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
Integrate OpenAI API for AI-powered spec extraction and file generation.

- [x] Create OpenAI client wrapper for spec generation (using gpt-4o-mini)
- [x] Implement spec extraction event handler (brief → Store Spec JSON with ALL required fields)
- [x] Fix prompt to include complete schema template ensuring all fields are returned
- [x] Validate nav structure returns objects with label/href (not plain strings)
- [x] Build spec preview component with JSON syntax highlighting
- [x] Add progress tracking state with real-time updates
- [x] Add error handling and validation for API responses
- [x] Test complete workflow: Brief input → Spec generation → All fields verified

**Key Fix:** Updated prompt to explicitly include the full Store Spec schema template, ensuring LLM returns all required fields (store, brand, nav, catalog, i18n, seo, features, a11y, analytics, environments) with correct structure.

---

## Phase 3: File Generation & Review System ✅
Complete the workflow with file generation, review UI, and deployment preparation.

- [x] Implement file plan generator (Store Spec → Hydrogen file tree with intents)
- [x] Create file generation event handler (spec → actual Hydrogen code files)
- [x] Build file explorer component showing generated file tree
- [x] Add code preview panel with syntax highlighting (TypeScript/JSX/CSS)
- [x] Create HITL review interface with deployment summary
- [x] Add deployment status tracking and file count display
- [x] Implement progress tracking through complete workflow (25% → 50% → 75% → 100%)
- [x] Test complete workflow: Spec → File Plan → Generated Files → Review

**Implementation Notes:**
- File explorer uses flat list approach (no recursion) for stability
- Split-view layout: file list (320px) + code preview (flex-1)
- Selected file highlighting with click-to-view functionality
- Review page shows file summary and deployment readiness
- All async operations have proper loading states and error handling

---

## Summary

✅ **Complete Application Delivered:**

1. **Brief Input System**: Users can enter project briefs, upload/paste brand guidelines (PDF support), and optionally provide Shopify credentials
2. **AI-Powered Spec Generation**: OpenAI gpt-4o-mini transforms natural language briefs into structured Store Spec JSON with all required fields
3. **File Plan Generation**: LLM analyzes Store Spec and creates comprehensive Hydrogen file tree with intents
4. **Code Generation**: Each file is generated with actual TypeScript/JSX/CSS code based on Store Spec
5. **File Explorer**: Interactive file browser with click-to-preview functionality
6. **Code Preview**: Syntax-highlighted code display for all generated files
7. **Review & Deploy**: Summary page showing file count and deployment readiness
8. **Progress Tracking**: Real-time progress indicators through entire workflow

**Workflow:**
Brief → Generate Spec (50%) → Generate File Plan (75%) → Generate Files (85%+) → Review (100%) → Deploy

**Next Steps (Future Enhancements):**
- GitHub PR integration for code review
- Oxygen deployment automation via Shopify CLI
- Lighthouse/a11y automated testing
- Local testing with Mini-Oxygen
- OpenRouter integration for multi-model support
- Goose agent orchestration for autonomous development

---

## Notes
- Using port 8001 (frontend) and 8002 (backend)
- OpenAI API key required: OPENAI_API_KEY
- All LLM calls use gpt-4o-mini with JSON response format
- File generation is fully functional and tested
- UI is clean, responsive, and user-friendly

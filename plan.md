# Hydrogen Site Builder - Complete Rebuild ✅

## Project Overview
Building a local/hostable AI agent that transforms natural-language briefs + brand guidelines + Shopify credentials into production-ready Hydrogen storefronts deployed to Oxygen.

**Tech Stack:**
- Frontend: Reflex (Python web framework)
- AI Models: Multi-provider support (Mistral → OpenRouter → OpenAI fallback)
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
- [x] Fix crash after generation by removing automatic file generation trigger
- [x] Fix markdown code fence stripping for clean code display

**Implementation Notes:**
- File explorer uses flat list approach (no recursion) for stability
- Split-view layout: file list (320px) + code preview (flex-1)
- Selected file highlighting with click-to-view functionality
- Review page shows file summary and deployment readiness
- All async operations have proper loading states and error handling

---

## Phase 4: Multi-Provider AI & Hydrogen Code Quality ✅

### Multi-Provider AI Integration
- [x] Add Mistral AI Studio support (primary provider)
- [x] Add OpenRouter support with free models (secondary provider)
- [x] Keep OpenAI as fallback provider
- [x] Implement priority-based provider selection
- [x] Add graceful degradation when API keys missing
- [x] Test provider priority system (Mistral → OpenRouter → OpenAI)

**Provider Priority:**
1. **Mistral AI Studio** (Primary)
   - Spec/Plan: `mistral-tiny`
   - Code Generation: `mistral-large-latest`
2. **OpenRouter** (Secondary) - Free Models
   - Spec/Plan: `mistralai/mistral-7b-instruct:free`
   - Code Generation: `deepseek/deepseek-coder`
3. **OpenAI** (Fallback)
   - All tasks: `gpt-4o-mini`

### Hydrogen-Specific Code Generation
- [x] Enhanced prompts with Hydrogen API patterns
- [x] Added Remix/React Router conventions (loader, meta exports)
- [x] Required @shopify/hydrogen-react component usage
- [x] Added Storefront API client patterns (context.storefront.query)
- [x] Included GraphQL query examples
- [x] Added TailwindCSS styling requirements

**Hydrogen Code Requirements:**
- ✅ Routes export: `loader`, `meta`, default component
- ✅ Uses `@shopify/hydrogen-react` components (Money, Image, CartForm)
- ✅ Storefront API client via `context.storefront.query()`
- ✅ Follows Remix conventions (React Router v6+)
- ✅ TypeScript + TailwindCSS for styling
- ✅ SEO and a11y patterns included

**Environment Variables:**
- `MISTRAL_API_KEY` - Primary provider
- `OPENROUTER_API_KEY` - Secondary provider with free models
- `OPENAI_API_KEY` - Fallback provider

---

## Summary

✅ **Complete Application Delivered:**

1. **Brief Input System**: Users can enter project briefs, upload/paste brand guidelines (PDF support), and optionally provide Shopify credentials
2. **AI-Powered Spec Generation**: Multi-provider AI (Mistral → OpenRouter → OpenAI) transforms briefs into Store Spec JSON
3. **File Plan Generation**: LLM analyzes Store Spec and creates comprehensive Hydrogen file tree
4. **Hydrogen Code Generation**: Production-ready TypeScript/JSX/CSS code following Shopify Hydrogen best practices
5. **File Explorer**: Interactive file browser with click-to-preview functionality
6. **Code Preview**: Syntax-highlighted code display for all generated files
7. **Review & Deploy**: Summary page showing file count and deployment readiness
8. **Progress Tracking**: Real-time progress indicators through entire workflow

**Workflow:**
Brief → Generate Spec (50%) → Generate File Plan (75%) → User clicks "Generate Files" → Files Generated (85%+) → Review (100%) → Deploy

**Key Improvements:**
- ✅ Multi-provider AI support (Mistral → OpenRouter → OpenAI)
- ✅ Hydrogen-specific code generation (proper APIs, components, patterns)
- ✅ Markdown code fence stripping for clean display
- ✅ User-triggered file generation (prevents race conditions)

**Next Steps (Future Enhancements):**
- GitHub PR integration for code review
- Oxygen deployment automation via Shopify CLI
- Lighthouse/a11y automated testing
- Local testing with Mini-Oxygen
- Goose agent orchestration for autonomous development

---

## Notes
- Using port 8001 (frontend) and 8002 (backend)
- API keys checked in priority: MISTRAL_API_KEY → OPENROUTER_API_KEY → OPENAI_API_KEY
- All LLM calls use JSON response format for structured output
- File generation produces valid Shopify Hydrogen code with proper patterns
- UI is clean, responsive, and user-friendly

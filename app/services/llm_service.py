from enum import Enum


class ModelProvider(Enum):
    OPENROUTER = "openrouter"
    OLLAMA = "ollama"


class LLMService:
    def __init__(
        self, api_key: str, provider: ModelProvider = ModelProvider.OPENROUTER
    ):
        self.api_key = api_key
        self.provider = provider

    def get_orchestrator_models(self) -> list[str]:
        return ["phi4:mini", "gemma3:4b"]

    def get_codegen_models(self) -> list[str]:
        return [
            "deepseek/deepseek-chat-v3.1:free",
            "moonshotai/kimi-k2:free",
            "nvidia/nemotron-nano-9b-v2:free",
            "openai/gpt-oss-20b:free",
        ]

    def select_model_for_task(self, task_type: str) -> str:
        if task_type in ["spec_extraction", "file_planning", "repair"]:
            return self.get_orchestrator_models()[0]
        elif task_type == "code_generation":
            return self.get_codegen_models()[0]
        return self.get_orchestrator_models()[1]

    async def generate(self, prompt: str, model: str) -> str:
        print(f"--- LLM Call (mock) ---")
        print(f"Model: {model}")
        print(f"Prompt: {prompt[:100]}...")
        return f"Generated content for prompt: {prompt[:50]}..."
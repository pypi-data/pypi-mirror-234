import asyncio
from langchain.llms.base import LLM
from typing import Any, List, Optional
from langchain.callbacks.manager import CallbackManagerForLLMRun
from novelai_api.Preset import Model
from novelai_api.Tokenizer import Tokenizer
from novelai_api.utils import b64_to_tokens
from .GenerationSettings import GenerationSettings
from .boilerplate import API


class NovelAILLM(LLM):
    generation_settings: GenerationSettings = None

    def __init__(
            self,
            generation_settings,
            **kwargs: Any
    ):
        super().__init__(**kwargs)
        self.generation_settings = generation_settings

    @property
    def _llm_type(self) -> str:
        return "novelai"

    def _call(
            self,
            prompt: str,
            stop: Optional[List[str]] = None,
            run_manager: Optional[CallbackManagerForLLMRun] = None,
            **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        return asyncio.get_event_loop().run_until_complete(self.async_generate(prompt))

    async def async_generate(self, prompt):
        async with API() as api_handler:
            self.encode()
            api = api_handler.api
            result = await api.high_level.generate(
                prompt,
                self.generation_settings.model,
                self.generation_settings.preset,
                self.generation_settings.global_settings,
                self.generation_settings.bad_words,
                self.generation_settings.bias_groups,
                self.generation_settings.module
            )
        response = Tokenizer.decode(self.generation_settings.model, b64_to_tokens(result["output"]))
        return response

    def encode(self):
        self.generation_settings.preset.repetition_penalty_whitelist_encoded = [
            Tokenizer.encode(Model.Kayra, item) for item in self.generation_settings.repetition_penalty_whitelist
        ]
        self.generation_settings.preset.bad_words_encoded = [
            Tokenizer.encode(Model.Kayra, item) for item in self.generation_settings.bad_words
        ]
        self.generation_settings.preset.stop_sequences_encoded = [
            Tokenizer.encode(Model.Kayra, item) for item in self.generation_settings.stop_sequences
        ]

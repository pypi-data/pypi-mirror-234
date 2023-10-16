from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT


class LLMManager:
    def __init__(self, llm):
        self.llm = llm


class LLMAnthropic(LLMManager):

    def __init__(self):
        super().__init__(Anthropic())

    def call(self, prompt, context):
        full_prompt = f"{context} {HUMAN_PROMPT} {prompt} {AI_PROMPT}"

        completion = self.llm.completions.create(
            model="claude-2",
            max_tokens_to_sample=3000,
            prompt=full_prompt,
        )

        return {"new_context": f"{full_prompt} {completion.completion}",
                "prompt": prompt,
                "completion": completion.completion}

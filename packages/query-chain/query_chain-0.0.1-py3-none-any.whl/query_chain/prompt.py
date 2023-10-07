class PromptTemplate:
    def __init__(self, role=None, tone=None, style=None, length=None, audience=None):
        self.role = role
        self.tone = tone
        self.style = style
        self.length = length
        self.audience = audience

    def generate_prompt(self, text):
        prompt = ""

        if self.role is not None:
            prompt += f"**Role:** {self.role}\n"

        if self.tone is not None:
            prompt += f"**Tone:** {self.tone}\n"

        if self.style is not None:
            prompt += f"**Style:** {self.style}\n"

        if self.length is not None:
            prompt += f"**Length:** {self.length}\n"

        if self.audience is not None:
            prompt += f"**Audience:** {self.audience}\n"

        prompt += "\n"
        prompt += text

        return prompt


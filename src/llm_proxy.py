from groq import Groq

# from openai import OpenAI
from dotenv import load_dotenv
import os
from typing import Literal, Union
from abc import ABC

from _file_read_write import read_file, write_file

from _file_paths import create_output_path

list_providers = Literal["groq", "openai"]


class LlmProxy(ABC):
    def __init__(self, provider: list_providers) -> None:
        self.provider = provider
        self.client_initialize(self.provider)
        pass

    def client_initialize(self, provider: list_providers) -> Groq:
        load_dotenv()

        if provider == "groq":
            api_key = os.environ.get("GROQ_API_KEY")
            self.client = Groq(api_key=api_key)
            self.model = "llama3-70b-8192"
            # "mixtral-8x7b-32768"
            # "gemma-7b-it"
        # elif provider == "openai":
        #     api_key = os.environ.get("OPENAI_API_KEY")
        #     self.client = OpenAI(api_key=api_key)
        #     self.model = "gpt-4-1106-preview"
        print(f"Initializing '{provider}' with model '{self.model}'...")

    def get_completion(
        self,
        system_prompt: str = "",
        user_prompt: str = "",
        temperature: int = 0,
    ) -> str:

        if not system_prompt:
            system_prompt = "You are a useful assistant."
        llm_message = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        llm_response = ""

        if self.provider == "groq" or self.provider == "openai":

            completion = self.client.chat.completions.create(
                model=self.model,
                messages=llm_message,
                temperature=temperature,
            )

            llm_response = completion.choices[0].message.content

        return llm_response

    def prompt_chain(
        self,
        prompt: str,
        output_response_name: str,
        input_context_path_name: str = "",
    ) -> str:
        input_context_text = ""
        if input_context_path_name:
            input_context_text = read_file(input_context_path_name)

        output_response_path = create_output_path(output_response_name)
        output_response_path_name = output_response_path + output_response_name

        print(f"output path: {output_response_path_name}")

        prompt = f"{prompt}<{input_context_text}>"

        response = self.get_completion(prompt=prompt)

        write_file(output_response_path_name, response)

        return response


def main():
    shopping_list = f"""

    4 apples, 
    500g chicken,
    2 apples,
    100 chicken,
    1 kg carrots,
    200 g walnuts,

    """

    llmObj = LlmProxy("groq")
    completion = llmObj.get_completion(user_prompt=shopping_list)

    print(completion)

    print(type(completion))
    # for chunk in completion:
    #     print(chunk.choices[0].delta.content or "", end="")
    pass


if __name__ == "__main__":
    main()

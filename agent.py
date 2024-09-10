# agent.py

import os
from typing import List, Dict, Any
import anthropic
import pkg_resources
from memory import Memory

def get_anthropic_version():
    try:
        return pkg_resources.get_distribution("anthropic").version
    except pkg_resources.DistributionNotFound:
        return "Unknown"

print(f"Anthropic library version: {get_anthropic_version()}")

class EnhancedResearchAgent:
    def __init__(self, memory_size: int = 5, model: str = "claude-3-5-sonnet-20240620", max_tokens: int = 1038, temperature: float = 0.5):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")
        self.memory = Memory(max_items=memory_size)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        try:
            self.client = anthropic.Anthropic(api_key=self.api_key)
        except AttributeError:
            print(f"Warning: Anthropic version {get_anthropic_version()} does not support Anthropic() class. Falling back to Client().")
            self.client = anthropic.Client(api_key=self.api_key)

    def research(self, query: str) -> str:
        try:
            context = self.memory.get_context()
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Context from previous interactions:\n{context}\n\nNew Query: {query}\n\nPlease provide a well-structured response that includes:\n1. A brief overview of the topic\n2. Key points or findings\n3. Any relevant examples or case studies\n4. Potential areas for further research\n\nYour response should be informative and objective, and take into account the previous context if relevant."
                        }
                    ]
                }
            ]
            
            try:
                if hasattr(self.client, 'messages'):
                    response = self.client.messages.create(
                        model=self.model,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature,
                        system="You are a research assistant. Your task is to provide comprehensive answers to queries, taking into account any previous context provided.",
                        messages=messages
                    )
                    result = response.content[0].text
                else:
                    prompt = f"{anthropic.HUMAN_PROMPT} {messages[0]['content'][0]['text']}{anthropic.AI_PROMPT}"
                    response = self.client.completion(
                        prompt=prompt,
                        model=self.model,
                        max_tokens_to_sample=self.max_tokens,
                        temperature=self.temperature,
                        stop_sequences=[anthropic.HUMAN_PROMPT]
                    )
                    result = response.completion
            except AttributeError as e:
                raise ImportError(f"Error using Anthropic API: {str(e)}. The installed version might not support the latest features.")
            
            self.memory.add(f"Q: {query}\nA: {result}")
            return result
        except anthropic.APIError as e:
            return f"An API error occurred: {str(e)}"
        except anthropic.APIConnectionError as e:
            return f"A connection error occurred: {str(e)}"
        except ImportError as e:
            return f"An import error occurred: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def chat(self) -> None:
        print("Welcome to the Enhanced Research Assistant. Type 'exit' to end the conversation.")
        print(f"Current memory capacity: {self.memory.max_items} items")
        while True:
            query = input("You: ").strip()
            if query.lower() == 'exit':
                print("Thank you for using the Enhanced Research Assistant. Goodbye!")
                break
            elif query.lower() == 'clear memory':
                self.memory.clear()
                print("Memory cleared.")
                continue
            elif query.lower() == 'memory status':
                print(self.memory.status())
                continue
            response = self.research(query)
            self._print_response(response)

    def _print_response(self, response: str) -> None:
        print(f"Assistant: {response}\n")
        print(f"Items in memory: {len(self.memory)}")

    def get_last_n_interactions(self, n: int) -> str:
        if not isinstance(n, int) or n <= 0:
            raise ValueError("n must be a positive integer")
        return self.memory.get_last_n(n)

def main():
    try:
        agent = EnhancedResearchAgent()
        agent.chat()
    except Exception as e:
        print(f"An error occurred while initializing the agent: {str(e)}")
        print("Please check your API key, Anthropic library version, and internet connection, then try again.")

if __name__ == "__main__":
    main()
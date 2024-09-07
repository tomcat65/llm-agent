# agent.py

import os
import anthropic
from memory import Memory

import os
import anthropic
from memory import Memory

class EnhancedResearchAgent:
    def __init__(self, memory_size=5):
        self.client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.memory = Memory(max_items=memory_size)
    
    def research(self, query):
        try:
            context = self.memory.get_context()
            prompt = f"""
Human: You are a research assistant. Your task is to provide a comprehensive answer to the following query. Here is the context from previous interactions:

{context}

New Query: {query}

Please provide a well-structured response that includes:
1. A brief overview of the topic
2. Key points or findings
3. Any relevant examples or case studies
4. Potential areas for further research

Your response should be informative and objective, and take into account the previous context if relevant."""

            response = self.client.completions.create(
                model="claude-3-sonnet-20240229",
                max_tokens_to_sample=1000,
                prompt=prompt
            )

            result = response.completion
            self.memory.add(f"Q: {query}\nA: {result}")
            return result
        except anthropic.APIConnectionError as e:
            return f"An error occurred while connecting to the Anthropic API: {str(e)}"
        except anthropic.APIStatusError as e:
            return f"The Anthropic API returned an error: {str(e)}"
        except anthropic.APITimeoutError as e:
            return f"The request to the Anthropic API timed out: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    def chat(self):
        print("Welcome to the Enhanced Research Assistant. Type 'exit' to end the conversation.")
        print(f"Current memory capacity: {self.memory.max_items} items")
        while True:
            query = input("You: ")
            if query.lower() == 'exit':
                print("Thank you for using the Enhanced Research Assistant. Goodbye!")
                break
            elif query.lower() == 'clear memory':
                self.memory.clear()
                print("Memory cleared.")
                continue
            elif query.lower().startswith('memory status'):
                print(str(self.memory))
                continue
            response = self.research(query)
            print(f"Assistant: {response}\n")
            print(f"Items in memory: {len(self.memory)}")

    def get_last_n_interactions(self, n):
        return self.memory.get_last_n(n)
import google.generativeai as genai
from server.config import Settings

settings = Settings()

class LLMServices:
    def _init_(self):
        genai.configure(api_key=settings.GEMENI_API_KEY)
        self.model= genai.GenerativeaiModel("gemini-2.0-flash")

    def generate_response(self, query: str, search_results: list[dict]):
        try:
            context_text = "\n\n".join(
                [
                    f"Source {i+1} ({result['url']}):\n{result['content']}"
                    for i, result in enumerate(search_results)
                ]
            )

            full_prompt = f"""
            Context from web search:
            {context_text}

            Query: {query}

            Please provide a comprehensive, detailed, well-cited accurate response using the above context.
            Think and reason deeply. Ensure it answers the query the user is asking. Do not use your knowledge until it is absolutely necessary.
            """

            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error generating response: {e}")
            return "Sorry, I encountered an error while generating the response."

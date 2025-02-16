from fastapi import FastAPI
from server.pydantic_model.chat_body import ChatBody
from server.services.search_service import SearchService
from server.services.sort_source import SortSourceService
from server.services.llm_services import LLMServices  # Add this import

app = FastAPI()
search_service = SearchService()
sort_source_service = SortSourceService()
llm_service = LLMServices()  # Initialize the LLM service

@app.post("/chat")
def chat_endpoint(body: ChatBody):
    try:
        search_results = search_service.web_search(body.query)
        if not search_results:
            return {"results": [], "message": "No search results found"}

        sorted_results = sort_source_service.sort_sources(body.query, search_results)
        response = llm_service.generate_response(body.query, sorted_results)  # Generate LLM response

        return {
            "results": sorted_results,
            "answer": response
        }

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return {"results": [], "error": str(e)}
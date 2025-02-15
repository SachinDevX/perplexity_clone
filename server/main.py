from fastapi import FastAPI


from server.pydantic_model.chat_body import ChatBody
from server.services.search_service import SearchService
from server.services.sort_source import SortSourceService

app = FastAPI()
search_service = SearchService()
sort_source_service = SortSourceService()


@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_results = search_service.web_search(body.query)
    sorted_result = sort_source_service.sort_sources(body.query, search_results)
    print(sorted_result)
    return body.query
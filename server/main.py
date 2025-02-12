from fastapi import FastAPI


from server.pydantic_model.chat_body import ChatBody
from server.services.search_service import SearchService

search_service = SearchService()
app = FastAPI()


@app.post("/chat")
def chat_endpoint(body: ChatBody):
    search_service.web_search()
    return body.query
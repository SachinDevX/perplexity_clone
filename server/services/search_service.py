from server.config import Settings
from tavily import TavilyClient
import trafilatura


settings = Settings()
tavily_client = TavilyClient(api_key=settings.TAVILY_API_KEY)


class SearchService:
    def web_search(self, query: str):
        results = []
        try:
            response = tavily_client.search(query, max_results=10)
            if not response or "results" not in response:
                print(f"No results found for query: {query}")
                return []
                
            search_results = response.get("results", [])
            
            for result in search_results:
                try:
                    if not result.get("url"):
                        continue
                        
                    download = trafilatura.fetch_url(result.get("url"))
                    if not download:
                        continue
                        
                    content = trafilatura.extract(download, include_comments=False)
                    if not content:
                        continue
                        
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": content,
                    })
                except Exception as e:
                    print(f"Error processing result: {e}")
                    continue
                    
            return results
        except Exception as e:
            print(f"Error in web search: {e}")
            return []
import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graphbuilder import GraphBuilder
from src.llms.groqllm import GroqLLM
from pydantic import BaseModel

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

class req(BaseModel):
    topic: str

## API's

@app.post("/blogs")
async def create_blogs(request:req):
    
    topic = request.topic
    print(request)
    # language = data.get("language","") 

    ## Get the llm object
    ## Please update the model name if this model is no longer available
    groqllm = GroqLLM(model_name = "openai/gpt-oss-120b")
    llm = groqllm.get_llm() 

    ## Get the graph
    graph_builder = GraphBuilder(llm)
    if topic:
        graph = graph_builder.setup_graph(usecase = "topic")
        state = graph.invoke({"topic":topic})

    return {"Final_Blog":state["final_blog"]}

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port = 8000, reload=True)


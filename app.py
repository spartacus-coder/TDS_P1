#///script
#requires-python = ">=3.13"
#dependencies = [
#    "fastapi",
#    "uvicorn",
#    "requests",
#    "os",
#]
#///

from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_credentials = True,
    allow_methods = ['GET', 'POST'],
    allow_headers = ['*']
)

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

@app.get("/")
def home():
    return{"Yay TDS awesome"}


@app.get("/read")
def read_file(path:str):
    try:
        with open(path,"r"):
            return f.read()
    except Exception as e:
        raise HTTPException(status_code=404,detail="File does not exist")

@app.post("/run")
def task_description(task:str):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-type":"application/json",
        "Authorization":f"Bearer {AIPROXY_TOKEN}"
    }

    tools = [
        {
            "type":"function",
            "function":{
                "name": "script_runner",
                "desrciption": "Install a package and run a script from a url with provided arguments",
                "parameters":{
                    "type":"object",
                    "properties":{
                        "script_url":{
                            "type":"string",
                            "description":"TThe URL of the script to run"
                        },
                        "args":{
                            "type":"array",
                            "items":{
                                "type":"string"
                            },
                            "description":"List of arguments to pass to the script"
                        },
                        
                    },"required":{"script_url","args"}

                }
            },
        }
    ]

    data = {
        "model":"gpt-4o-mini",
        "messages":[
            {
                "role":"user",
                "content":task

            },
            {
                "role":"system",
                "content":""" 
You are an assistant who has to do a variety of tasks
If your task involves running a script, you can use the script runner tool.
If your task involves writing a code, you can use the task_runner tool.                
"""
            }

        ],
        "tools":tools,
        "tool_choice":"auto"

    }
    response = requests.post(url=url,headers=headers,json=data)
    return response.json()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,host='0.0.0.0',port=8000)


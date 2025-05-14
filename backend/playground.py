

from agno.agent import Agent
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
from agno.models.google import Gemini
from agno.embedder.google import GeminiEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import SearchType,LanceDb
from agno.tools.eleven_labs import ElevenLabsTools
from agno.playground import Playground,serve_playground_app
from pathlib import Path
from agno.tools.reasoning import ReasoningTools
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from agno.tools.duckduckgo import DuckDuckGoTools
import traceback
from agno.tools.todoist import TodoistTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.zoom import ZoomTools
from agno.tools.youtube import YouTubeTools

from dotenv import load_dotenv
import os


load_dotenv()


#
# GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
# ELEVENLABS = os.getenv("ELEVEN_LABS_API_KEY")
# TODOIST = os.getenv("TODOIST_API_TOKEN")


ACCOUNT_ID = os.getenv("ZOOM_ACCOUNT_ID")
ZOOM_CLIENT_ID = os.getenv("ZOOM_CLIENT_ID")
ZOOM_CLIENT_SECRET = os.getenv("ZOOM_CLIENT_SECRET")

zoom_tools = ZoomTools(
    account_id=ACCOUNT_ID,
    client_id=ZOOM_CLIENT_ID,
    client_secret=ZOOM_CLIENT_SECRET
)



class FileUploadRequest(BaseModel):
    file_url: str

cwd = Path(__file__).parent
tmp_dir = cwd.joinpath("tmp")
tmp_dir.mkdir(parents=True, exist_ok=True)


urlfile_Path = Path("datas/urls.txt")
urlfile_Path.parent.mkdir(parents=True, exist_ok=True)


if not urlfile_Path.exists():
    urlfile_Path.write_text("")

with urlfile_Path.open("r") as f:
    urls = [line.strip() for line in f.readlines() if line.strip()]


knowledge_base = UrlKnowledge(
    urls=urls,
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="sidhu-doc",
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="embedding-001"),
    )
)

memory = Memory(
    model=Gemini(id="gemini-2.0-flash"),
    db=SqliteMemoryDb(table_name="user_memories",db_file="tmp/memory.db")
)





web_agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    memory=memory,
    enable_agentic_memory=True,
    enable_user_memories=True,
    add_history_to_messages=True,
    knowledge=knowledge_base,
    agent_id="AI Digital Twin",
    instructions=[ "Use tables to display data.",
        "Include sources in your response.",
        "Search your knowledge before answering the question.",
        "Only include the output in your response. No other text.",
        "When given a task, create a todoist task for it.",
        "When given a list of tasks, create a todoist task for each one.",
        "When given a task to update, update the todoist task.",
        "When given a task to delete, delete the todoist task.",
        "When given a task to get, get the todoist task.",
        "Always include source of the article fetched ",
        "You are also a YouTube agent. Obtain the captions of a YouTube video and answer questions."
    ],
    search_knowledge=True,

    tools=[
        ElevenLabsTools(
            voice_id="JBFqnCBsd6RMkjVDRZzb",
            model_id="eleven_multilingual_v2",
            target_directory=str(tmp_dir.joinpath("audio").resolve()),
        ),
        ReasoningTools(add_instructions=True),
        DuckDuckGoTools(),
        TodoistTools(),
        WikipediaTools(),
        zoom_tools,
        YouTubeTools()
    ],
    storage=SqliteStorage(table_name="agent_sessions",db_file="tmp/agent.db"),
    markdown=True
)

app = Playground(agents=[web_agent]).get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://final-project-wheat-alpha.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/file")
async def upload_file(data : FileUploadRequest):
    try:
        my_txt_path = Path("datas/urls.txt")
        my_txt_path.parent.mkdir(parents=True, exist_ok=True)
        with my_txt_path.open("a", encoding="utf-8") as f:
            f.write(data.file_url + "\n")

        print("Received file URL:", data.file_url)

        # Append new URL
        knowledge_base.urls.append(data.file_url)

        return {"message": "URL added and processed successfully"}

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":

    knowledge_base.load(recreate=True)
    show_full_reasoning = True,
    stream_intermediate_steps = True,
    serve_playground_app("playground:app", reload=True)
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
from datetime import datetime
import dotenv
from pathlib import Path

# Load environment variables
dotenv.load_dotenv()

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the agent
from agent.linkedin_agent import LinkedInJobAgent

app = FastAPI(title="LinkedIn Job Crawler API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to store LinkedIn credentials
CREDENTIALS_FILE = Path("data/linkedin_credentials.json")

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(CREDENTIALS_FILE), exist_ok=True)


# LinkedIn credentials model
class LinkedInCredentials(BaseModel):
    email: str
    password: str


# LinkedIn credentials status model
class LinkedInCredentialsStatus(BaseModel):
    set: bool


# Ensure credentials file exists with empty credentials
if not CREDENTIALS_FILE.exists():
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump({"email": "", "password": ""}, f)


# Functions to interact with LinkedIn credentials
def save_credentials(credentials: LinkedInCredentials):
    with open(CREDENTIALS_FILE, "w") as f:
        json.dump(credentials.dict(), f)


def get_credentials():
    if not CREDENTIALS_FILE.exists():
        return LinkedInCredentials(email="", password="")
    with open(CREDENTIALS_FILE, "r") as f:
        data = json.load(f)
    return LinkedInCredentials(**data)


def has_credentials():
    credentials = get_credentials()
    return bool(credentials.email and credentials.password)


# Create data directory if it doesn't exist
data_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
os.makedirs(data_dir, exist_ok=True)
JOBS_FILE = os.path.join(data_dir, "jobs.json")

# Agent instance
agent = None
agent_running = False
agent_status = "stopped"
last_job_count = 0
agent_start_time = None


# Models
class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    visa_sponsorship: bool
    url: str
    date_posted: str
    date_found: str


class AgentStatus(BaseModel):
    status: str
    job_count: int
    total_jobs_searched: int = 0
    running_time: Optional[str] = None
    start_time: Optional[str] = None


# Helper functions
def load_jobs():
    if not os.path.exists(JOBS_FILE):
        return []

    with open(JOBS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f, indent=2)


def run_agent_task():
    global agent_running, agent_status, last_job_count, agent_start_time

    agent_running = True
    agent_status = "running"
    agent_start_time = datetime.now().isoformat()

    try:
        # Create the agent if it doesn't exist
        global agent
        if agent is None:
            agent = LinkedInJobAgent()

        while agent_running:
            # Get current jobs
            current_jobs = load_jobs()
            last_job_count = len(current_jobs)

            # Run the agent to find new jobs
            agent_status = "searching for jobs"
            new_jobs = agent.run()

            if new_jobs:
                # Add new jobs to the list
                for job in new_jobs:
                    # Check if job already exists
                    if not any(
                        existing_job["id"] == job["id"] for existing_job in current_jobs
                    ):
                        job["date_found"] = datetime.now().isoformat()
                        current_jobs.append(job)

                # Save updated jobs list
                save_jobs(current_jobs)
                last_job_count = len(current_jobs)

            # Wait before the next crawl
            agent_status = "waiting for next crawl"
            time.sleep(300)  # 5 minutes
    except Exception as e:
        agent_status = f"error: {str(e)}"
        print(f"Agent error: {e}")
    finally:
        agent_status = "stopped"
        agent_running = False


# API Endpoints
@app.get("/")
def read_root():
    return {"message": "LinkedIn Job Crawler API"}


@app.get("/jobs", response_model=List[Dict[str, Any]])
def get_jobs():
    return load_jobs()


@app.post("/agent/start")
def start_agent(background_tasks: BackgroundTasks):
    global agent_running, agent_status

    if agent_running:
        raise HTTPException(status_code=400, detail="Agent is already running")

    background_tasks.add_task(run_agent_task)
    return {"message": "Agent started successfully"}


@app.post("/agent/stop")
def stop_agent():
    global agent_running, agent_status

    if not agent_running:
        raise HTTPException(status_code=400, detail="Agent is not running")

    agent_running = False
    agent_status = "stopping"
    return {"message": "Agent is stopping"}


@app.get("/agent/status", response_model=AgentStatus)
def get_agent_status():
    running_time = None
    if agent_start_time and agent_running:
        start_time = datetime.fromisoformat(agent_start_time)
        running_time = str(datetime.now() - start_time).split(".")[
            0
        ]  # Format as HH:MM:SS

    # Get total jobs searched from agent if it exists
    total_jobs_searched = 0
    if agent is not None:
        total_jobs_searched = getattr(agent, "total_jobs_searched", 0)

    return {
        "status": agent_status,
        "job_count": last_job_count,
        "total_jobs_searched": total_jobs_searched,
        "running_time": running_time,
        "start_time": agent_start_time,
    }


# Startup event to initialize the agent
@app.on_event("startup")
async def startup_event():
    global agent
    agent = LinkedInJobAgent()


# LinkedIn credentials endpoints
@app.post("/api/linkedin/credentials")
def set_linkedin_credentials(credentials: LinkedInCredentials):
    save_credentials(credentials)
    return {"message": "LinkedIn credentials saved successfully"}


@app.get("/api/linkedin/credentials/status", response_model=LinkedInCredentialsStatus)
def get_linkedin_credentials_status():
    return LinkedInCredentialsStatus(set=has_credentials())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

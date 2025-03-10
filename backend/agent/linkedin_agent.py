import os
import uuid
import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langgraph.graph import StateGraph, END
from langchain.tools import tool
from pydantic import BaseModel, Field
import time
import dotenv
from pathlib import Path

# Load environment variables
dotenv.load_dotenv()

# Path to LinkedIn credentials
CREDENTIALS_FILE = Path("data/linkedin_credentials.json")


# LinkedIn API client (MCP LinkedIn)
class LinkedInClient:
    """Client for interacting with the LinkedIn API via MCP-LinkedIn."""

    def __init__(self):
        # Get MCP LinkedIn URL from environment variable or use default
        self.base_url = os.getenv("LINKEDIN_MCP_URL", "http://localhost:5000")

        # Load credentials if they exist
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> Dict[str, str]:
        """Load LinkedIn credentials from the credentials file."""
        if not CREDENTIALS_FILE.exists():
            return {"email": "", "password": ""}

        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading LinkedIn credentials: {e}")
            return {"email": "", "password": ""}

    def search_jobs(
        self, keywords: str, location: str, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn with the given keywords and location."""
        try:
            # Check if credentials are set
            if not self.credentials.get("email") or not self.credentials.get(
                "password"
            ):
                print("LinkedIn credentials not set. Please set them to use the agent.")
                return []

            # Set credentials as environment variables for MCP-LinkedIn
            os.environ["LINKEDIN_EMAIL"] = self.credentials.get("email", "")
            os.environ["LINKEDIN_PASSWORD"] = self.credentials.get("password", "")

            response = requests.get(
                f"{self.base_url}/api/v1/jobs/search",
                params={"keywords": keywords, "location": location, "limit": limit},
            )
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            print(f"Error searching jobs: {e}")
            return []

    def get_job_details(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific job."""
        try:
            # Check if credentials are set
            if not self.credentials.get("email") or not self.credentials.get(
                "password"
            ):
                print("LinkedIn credentials not set. Please set them to use the agent.")
                return None

            # Set credentials as environment variables for MCP-LinkedIn
            os.environ["LINKEDIN_EMAIL"] = self.credentials.get("email", "")
            os.environ["LINKEDIN_PASSWORD"] = self.credentials.get("password", "")

            response = requests.get(f"{self.base_url}/api/v1/jobs/{job_id}")
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            print(f"Error getting job details: {e}")
            return None


# Function to check if a job description mentions visa sponsorship
def check_visa_sponsorship(description: str) -> bool:
    """Check if a job description mentions visa sponsorship."""
    description = description.lower()

    # Keywords related to visa sponsorship
    visa_keywords = [
        "visa sponsorship",
        "visa sponsor",
        "sponsorship available",
        "international applicants",
        "international candidates",
        "sponsored visa",
        "work authorization",
        "h1b",
        "h-1b",
        "h1-b",
        "eligible to work",
        "right to work",
        "apply from anywhere",
        "open to international",
        "global talent",
        "worldwide applicants",
    ]

    # Check if any of the keywords are in the description
    for keyword in visa_keywords:
        if keyword in description:
            return True

    return False


class LinkedInJobAgent:
    """Agent that crawls LinkedIn job postings to find roles with visa sponsorship."""

    def __init__(self):
        # Create the LinkedIn client
        self.client = LinkedInClient()

    def search_jobs(
        self,
        keywords: str = "Software Engineer",
        location: str = "San Francisco",
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Search for jobs on LinkedIn."""
        return self.client.search_jobs(keywords, location, limit)

    def get_job_details(self, job_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific job."""
        return self.client.get_job_details(job_id)

    def run(self) -> List[Dict[str, Any]]:
        """Run the agent to find jobs with visa sponsorship."""
        results = []

        try:
            # Step 1: Search for jobs
            print("Searching for software engineering jobs in San Francisco...")
            job_listings = self.search_jobs()

            if not job_listings:
                print("No job listings found.")
                return []

            print(f"Found {len(job_listings)} job listings.")

            # Step 2: Process each job
            for job in job_listings:
                job_id = job.get("jobId")
                if not job_id:
                    continue

                print(f"Getting details for job {job_id}...")
                job_details = self.get_job_details(job_id)

                if not job_details:
                    continue

                # Check if the job mentions visa sponsorship
                description = job_details.get("description", "")
                has_visa_sponsorship = check_visa_sponsorship(description)

                if has_visa_sponsorship:
                    # Format the job information
                    formatted_job = {
                        "id": job_details.get("jobId", str(uuid.uuid4())),
                        "title": job_details.get("title", ""),
                        "company": job_details.get("companyName", ""),
                        "location": job_details.get("location", ""),
                        "description": description,
                        "visa_sponsorship": True,
                        "url": job_details.get("url", ""),
                        "date_posted": job_details.get(
                            "postedAt", datetime.now().isoformat()
                        ),
                    }

                    # Add to results
                    results.append(formatted_job)
                    print(
                        f"Found job with visa sponsorship: {formatted_job['title']} at {formatted_job['company']}"
                    )

            print(f"Found {len(results)} jobs with visa sponsorship.")
            return results
        except Exception as e:
            print(f"Error running agent: {e}")
            return []


# For testing
if __name__ == "__main__":
    agent = LinkedInJobAgent()
    results = agent.run()
    print(f"Found {len(results)} jobs with visa sponsorship:")
    for job in results:
        print(f"- {job['title']} at {job['company']}")

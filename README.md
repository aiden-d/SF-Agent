# LinkedIn Job Crawler for Visa Sponsorship

An AI-powered agent that continuously crawls LinkedIn job postings to find software engineering roles in San Francisco with visa sponsorship.

## Features

- Continuously scrapes LinkedIn job listings for "Software Engineer" roles in San Francisco
- Analyzes job descriptions for keywords related to visa sponsorship
- Stores job data in a structured JSON format
- Displays jobs in a React web application with filtering capabilities
- Agent progress tracking and control panel
- LinkedIn integration through Model Context Protocol (MCP)

## Tech Stack

- **Backend**: Python (FastAPI)
- **AI Agent**: LangGraph with LinkedIn API integration
- **Database**: JSON file storage (can be extended to a full database)
- **Frontend**: React.js
- **LinkedIn Integration**: MCP LinkedIn server via Smithery

## Project Structure

```
sf_agent/
├── backend/
│   ├── agent/       # AI agent code
│   ├── api/         # FastAPI endpoints
│   └── data/        # JSON data storage
└── frontend/
    ├── public/      # Static assets
    └── src/         # React components
```

## Setup Instructions

### Quick Start

Run the setup script to install all dependencies and configure the LinkedIn MCP server:

```
./setup.sh
```

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

4. Setup the LinkedIn MCP server:
   ```
   python setup_mcp_linkedin.py
   ```

5. Start the backend server:
   ```
   uvicorn api.main:app --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the frontend development server:
   ```
   npm start
   ```

4. Access the application at `http://localhost:3000`

## LinkedIn Integration

This application uses the [MCP LinkedIn server](https://github.com/adhikasp/mcp-linkedin) to interact with LinkedIn's API. The MCP server is managed through Smithery and provides tools to interact with LinkedIn's Feeds and Job API.

### How to use LinkedIn integration:

1. Run the application
2. Enter your LinkedIn credentials in the web interface
3. The credentials will be stored securely and used to authenticate with LinkedIn
4. Start the agent to begin searching for jobs with visa sponsorship

**Note:** LinkedIn credentials are required to interact with LinkedIn's API. The credentials are stored locally and used only to authenticate with LinkedIn.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 
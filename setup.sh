#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}===== LinkedIn Job Crawler with Visa Sponsorship Setup =====${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install Python 3 and try again.${NC}"
    exit 1
fi

# Create Python virtual environment for backend
echo -e "\n${GREEN}Creating Python virtual environment...${NC}"
cd backend
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "\n${GREEN}Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "\n${YELLOW}Creating .env file. Please edit it with your OpenAI API key.${NC}"
    cp .env.example .env
    echo -e "Open ${YELLOW}backend/.env${NC} and add your OpenAI API key."
fi

# Create data directory
mkdir -p data

# Setup LinkedIn MCP Server
echo -e "\n${GREEN}Setting up LinkedIn MCP Server...${NC}"
# Run the setup script for LinkedIn MCP
python setup_mcp_linkedin.py

# Deactivate virtual environment
deactivate
cd ..

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "\n${YELLOW}npm is not installed. You'll need to install Node.js to run the frontend.${NC}"
else
    # Install Smithery CLI globally
    echo -e "\n${GREEN}Installing Smithery CLI...${NC}"
    npm install -g @smithery/cli

    # Install frontend dependencies
    echo -e "\n${GREEN}Installing frontend dependencies...${NC}"
    cd frontend
    npm install
    cd ..
fi

echo -e "\n${GREEN}===== Setup Complete =====${NC}"
echo -e "\nTo run the backend:"
echo -e "  cd backend"
echo -e "  source venv/bin/activate"
echo -e "  uvicorn api.main:app --reload"
echo -e "\nTo run the frontend:"
echo -e "  cd frontend"
echo -e "  npm start"
echo -e "\nThe LinkedIn MCP server is managed by Smithery."
echo -e "After starting the app, enter your LinkedIn credentials in the web interface."
echo -e "The credentials will be stored securely and used to authenticate with LinkedIn." 
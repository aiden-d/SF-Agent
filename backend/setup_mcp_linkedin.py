import json
import os
from pathlib import Path
import subprocess


def create_smithery_config():
    """Create and configure the smithery.config.json file for the LinkedIn MCP server."""
    # Get the user's home directory
    home_dir = os.path.expanduser("~")
    smithery_dir = os.path.join(home_dir, ".smithery")
    config_path = os.path.join(smithery_dir, "config.json")

    # Create the .smithery directory if it doesn't exist
    os.makedirs(smithery_dir, exist_ok=True)

    # Default config structure
    default_config = {
        "mcpServers": {
            "linkedin": {
                "command": "uvx",
                "args": [
                    "--from",
                    "git+https://github.com/adhikasp/mcp-linkedin",
                    "mcp-linkedin",
                ],
                "env": {"LINKEDIN_EMAIL": "", "LINKEDIN_PASSWORD": ""},
            }
        }
    }

    # Check if config file exists, if yes load it
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                existing_config = json.load(f)

            # Merge configurations if the file exists
            if "mcpServers" not in existing_config:
                existing_config["mcpServers"] = {}

            existing_config["mcpServers"]["linkedin"] = default_config["mcpServers"][
                "linkedin"
            ]
            config = existing_config
        except Exception as e:
            print(f"Error reading existing config: {e}")
            config = default_config
    else:
        config = default_config

    # Load LinkedIn credentials if they exist
    credentials_file = Path("data/linkedin_credentials.json")
    if credentials_file.exists():
        try:
            with open(credentials_file, "r") as f:
                credentials = json.load(f)

            # Update the config with the LinkedIn credentials
            config["mcpServers"]["linkedin"]["env"]["LINKEDIN_EMAIL"] = credentials.get(
                "email", ""
            )
            config["mcpServers"]["linkedin"]["env"]["LINKEDIN_PASSWORD"] = (
                credentials.get("password", "")
            )
        except Exception as e:
            print(f"Error loading LinkedIn credentials: {e}")

    # Write the config file
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"Smithery config created at {config_path}")

    # Return the path to the config file
    return config_path


def install_smithery_mcp_linkedin():
    """Install the LinkedIn MCP server via Smithery CLI."""
    try:
        # Check if Smithery CLI is installed
        subprocess.run(["npx", "-y", "@smithery/cli", "--version"], check=True)

        # Install the LinkedIn MCP server
        subprocess.run(
            [
                "npx",
                "-y",
                "@smithery/cli",
                "install",
                "mcp-linkedin",
                "--client",
                "claude",
            ],
            check=True,
        )

        print("LinkedIn MCP server installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing LinkedIn MCP server: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Create Smithery config
    config_path = create_smithery_config()

    # Install LinkedIn MCP server
    install_smithery_mcp_linkedin()

    print("Setup complete")

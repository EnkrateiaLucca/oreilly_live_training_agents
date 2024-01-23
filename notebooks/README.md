# Jira Issue Management Assistant

This project is a powerful assistant that helps users manage their issues in Jira Software. It uses the Jira API to perform various operations such as viewing, creating, updating, and deleting issues.

## Features

- View a Jira issue
- Create a new Jira issue
- Update the summary of a Jira issue
- Update the description of a Jira issue
- Delete a Jira issue
- Update the status of a Jira issue
- List all available transition options for a Jira issue

## Setup

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. Set your Jira username and token as environment variables (`JIRA_USERNAME` and `JIRA_TOKEN`)

## Usage

Run the script with the desired action as an argument. For example, to view an issue:

```bash
python jira-agent.py "view issue <issue_key>"
```
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
from crewai_tools import GithubSearchTool, JSONSearchTool

import os

# Load environment variables
load_dotenv()

# Validate OpenAI configuration
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set in environment variables")

# Validate required environment variables
required_env_vars = ["GITHUB_REPO", "GITHUB_TOKEN", "TOOL_MODEL", "EMBEDDING_MODEL", "MODEL"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Validate knowledge base exists
waf_json_path = 'knowledge/aws/waf.json'
if not os.path.exists(waf_json_path):
    raise FileNotFoundError(f"AWS Well-Architected Framework knowledge base not found at: {waf_json_path}")

# Initialize the tool for semantic searches within a specific GitHub repository
try:
    github_search_tool = GithubSearchTool(
        github_repo=os.getenv("GITHUB_REPO"),
        gh_token=os.getenv("GITHUB_TOKEN"),
        content_types=['code'], 
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model=os.getenv("TOOL_MODEL"),
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model=os.getenv("EMBEDDING_MODEL"),
                ),
            ),
        )
    )
except Exception as e:
    raise ValueError(f"Failed to initialize GithubSearchTool: {e}")

# Search through a single JSON file
try:
    json_search_tool = JSONSearchTool(
        json_path=waf_json_path,
        config=dict(
            llm=dict(
                provider="openai",
                config=dict(
                    model=os.getenv("TOOL_MODEL"),
                ),
            ),
            embedder=dict(
                provider="openai",
                config=dict(
                    model=os.getenv("EMBEDDING_MODEL"),
                ),
            ),
        )
    )
except Exception as e:
    raise ValueError(f"Failed to initialize JSONSearchTool: {e}")


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class terraform_advisor_by_56k():
    """terraform_advisor_by_56k crew - Question-focused infrastructure analysis"""

    agents: List[BaseAgent]
    tasks: List[Task]
    

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def terraform_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['terraform_agent'],
            verbose=True,
            max_iter=15,  # Increased for thorough code search
            max_retry_limit=3,  # Standardized retry limit
            tools=[github_search_tool],
            allow_delegation=False,  # Focus on specific tool usage
            llm=os.getenv("MODEL"),
            system_message="You specialize in analyzing Terraform code to answer specific questions. Always search for concrete evidence in the codebase before providing answers."
        )

    @agent
    def aws_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['aws_agent'],
            verbose=True,
            max_iter=15,  # Increased for thorough documentation search
            max_retry_limit=3,  # Standardized retry limit
            tools=[json_search_tool],
            allow_delegation=False,  # Focus on specific tool usage
            llm=os.getenv("MODEL"),
            system_message="You specialize in researching AWS best practices to answer specific questions. Always search for authoritative AWS guidance before providing recommendations."
        )
    
    @agent
    def response_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['response_agent'],
            verbose=True,
            max_iter=10,  # Standardized for synthesis tasks
            max_retry_limit=3,  # Standardized retry limit
            markdown=True,  # Enhanced markdown output
            allow_delegation=False,  # Prevent delegation loops
            llm=os.getenv("MODEL"),
            system_message="You specialize in synthesizing technical analysis to provide comprehensive, actionable answers to specific questions. Focus only on addressing what was asked."
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def codebase_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['codebase_research_task'],
            agent=self.terraform_agent(),
            output_format="markdown",  # Structured output
        )
    
    @task
    def aws_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['aws_research_task'],
            agent=self.aws_agent(),
            output_format="markdown",  # Structured output
        )
    
    @task
    def response_task(self) -> Task:
        return Task(
            config=self.tasks_config['response_task'],
            agent=self.response_agent(),
            context=[self.codebase_research_task(), self.aws_research_task()],  # Updated syntax
            output_format="markdown",  # Enhanced markdown output
        )

    @crew
    def crew(self) -> Crew:
        """Creates the terraform_advisor_by_56k crew for question-focused analysis"""
        regular_agents = [
            self.terraform_agent(),
            self.aws_agent(),
            self.response_agent()
        ]

        return Crew(
            agents=regular_agents,
            tasks=[
                self.codebase_research_task(),
                self.aws_research_task(),
                self.response_task()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,  # Enable memory for better context retention
            embedder={
                "provider": "openai",
                "config": {
                    "model": os.getenv("EMBEDDING_MODEL")
                }
            },
            max_rpm=10,  # Rate limiting to prevent API issues
            full_output=True,  # Get complete output details
        )

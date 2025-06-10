# Terraform Advisor Crew

Welcome to the Terraform Advisor Crew project, powered by [crewAI](https://crewai.com). This project enables you to automatically analyze any Terraform GitHub repository, evaluate its infrastructure-as-code against AWS best practices (leveraging the AWS Well-Architected Framework), and generate a comprehensive technical report. The analysis and reporting process is driven by a team of specialized AI agents.

With Terraform Advisor Crew, you can:

- Analyze the architecture, security, and implementation patterns of any Terraform codebase
- Benchmark the repository against AWS Well-Architected Framework pillars and best practices
- Receive actionable recommendations, risk assessments, and improvement roadmaps in a structured report

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- **Python >=3.10 <3.13**
- **[UV](https://docs.astral.sh/uv/)** for dependency management and package handling

### Setup

Clone this repository:

```bash
git clone https://github.com/56kcloud/terraform_advisor_by_56k.git
```

Navigate to your project directory and create a virtual environment and activate it:

```bash
cd terraform_advisor_by_56k
uv venv
source .venv/bin/activate
```

Install crewai inside the virtual environment:

```bash
uv tool install crewai
```

Install the project dependencies:

```bash
crewai install
```

## Environment Configuration

Create your `.env` file by copying the example:

```bash
cp .env.example .env
```

You'll need to configure the following in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key for agent interactions
- `GITHUB_TOKEN`: A GitHub Personal Access Token for repository analysis

The `.env` file also allows you to customize:

- Target GitHub repositories for analysis
- LLM models

## Running the Project

To analyze a Terraform GitHub repository and generate a best-practices report, run the following command from the root folder of your project:

```bash
crewai run
```

This command will:

- Assemble the AI agents as defined in your configuration
- Analyze the target repository and AWS documentation
- Produce a detailed report

The generated report and all outputs will be saved in the `output` folder in your project root.

**Note:**  
If you want to analyze a different GitHub repository after having already run the crew, it is recommended to delete the `db` folder in your project root. This folder contains cached data and content from the previously analyzed repository. Removing it ensures a clean analysis for the new repository.

## Customizing

- Modify `src/terraform_advisor_by_56k/config/agents.yaml` to define your agents
- Modify `src/terraform_advisor_by_56k/config/tasks.yaml` to define your tasks
- Modify `src/terraform_advisor_by_56k/crew.py` to add your own logic, tools and specific args
- Modify `src/terraform_advisor_by_56k/main.py` to add custom inputs for your agents and tasks

## AWS Well-Architected Documentation

The AWS Well-Architected Framework documentation is already included in this project and available to the agent at `knowledge/aws/waf.json`. No additional setup is required.

## Automated Review Questions

As part of the analysis, the agents will automatically iterate over a set of review questions defined in `knowledge/questions.txt`. For each question, the agents will analyze the target Terraform repository and AWS documentation to generate detailed, context-aware answers. This ensures a comprehensive evaluation of the infrastructure across multiple best-practice dimensions.

### How to Add Your Questions

Create or edit the `knowledge/questions.txt` file in your project root and add your questions, one per line.

**Example:**

```txt
What security best practices are implemented in this infrastructure?
How well does this setup follow the AWS Well-Architected Framework?
Are there any potential cost optimization opportunities?
What disaster recovery mechanisms are in place?
```

Each line in the file will be treated as a separate question that the AI agents will analyze. Empty lines are ignored, so you can use them to organize your questions for better readability.

## Understanding Your Crew

The terraform_advisor_by_56k Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding crewAI, please visit the following resources:

- Visit crewAI [documentation](https://docs.crewai.com)
- [Join crewAI Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with crewAI docs](https://chatg.pt/DWjSBZn)

## Credits

This project was developed by [56k.Cloud](https://www.56k.cloud/).

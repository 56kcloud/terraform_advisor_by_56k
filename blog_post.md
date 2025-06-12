# Transforming Infrastructure Analysis: How We Built a Terraform Advisor Powered by AI Agents and Video-Based Memory

*A question-driven approach to analyzing Terraform infrastructure with specialized AI agents*

---

In the ever-evolving landscape of cloud infrastructure, Terraform has become the gold standard for Infrastructure as Code (IaC). However, as our codebases grow in complexity and our teams scale, one critical challenge remains: **How do we efficiently answer specific questions about our infrastructure while ensuring alignment with AWS best practices?**

Today, I'm excited to introduce **Terraform Advisor by 56k.Cloud** - an AI-powered solution that analyzes Terraform GitHub repositories to answer specific infrastructure questions by combining code analysis with AWS Well-Architected Framework guidance through specialized AI agents.

## The Challenge: Answering Infrastructure Questions at Scale

Traditional infrastructure analysis often involves manual research across multiple sources, making it difficult to get comprehensive answers to specific questions. Development teams frequently struggle with:

- **Question Research Time**: Hours spent researching specific infrastructure concerns
- **Best Practice Application**: Difficulty finding relevant AWS guidance for specific scenarios  
- **Knowledge Gaps**: Lack of expertise to properly interpret infrastructure patterns
- **Context Switching**: Jumping between documentation, code, and recommendations
- **Inconsistent Analysis**: Different approaches to similar infrastructure questions

## Our Solution: Question-Focused AI Analysis

### The Architecture: CrewAI-Powered Multi-Agent System

At the heart of Terraform Advisor lies a multi-agent architecture built with [CrewAI](https://crewai.com), where specialized AI agents collaborate to provide comprehensive answers to specific infrastructure questions:

#### Meet Your AI Infrastructure Team

**1. The Terraform Agent** - *Senior Terraform Infrastructure Analyst*

- **Role**: Analyzes codebases to find evidence that answers specific questions
- **Expertise**: Terraform configuration patterns, resource dependencies, security configurations
- **Tools**: `GithubSearchTool` for semantic code search
- **Focus**: Finding concrete evidence in your infrastructure code to answer what's being asked

**2. The AWS Agent** - *Principal AWS Well-Architected Framework Authority*

- **Role**: Researches AWS best practices relevant to specific questions
- **Expertise**: Well-Architected Framework, service-specific recommendations  
- **Tools**: `MemvidSearchTool` for semantic search through AWS documentation
- **Focus**: Providing authoritative AWS guidance that addresses specific questions

**3. The Response Agent** - *Senior Solutions Architecture Integration Specialist*

- **Role**: Synthesizes analysis to provide comprehensive, actionable answers
- **Expertise**: Gap analysis, implementation planning, technical documentation
- **Focus**: Combining code analysis with AWS best practices into clear answers

### The Technology Stack

#### 1. Flexible GitHub Repository Analysis

The system can analyze any Terraform repository by configuring:

```yaml
# Configuration example
GITHUB_REPO: "your-org/terraform-infrastructure"
GITHUB_TOKEN: "your-github-token"
```

The system then:
- Searches for code patterns relevant to your specific questions
- Identifies resources and configurations that address what you're asking
- Documents current implementation approaches
- Finds gaps where questions aren't fully addressed by current code

#### 2. Memvid: Video-Based AI Memory for AWS Documentation

One innovative aspect of our solution is the integration of **[Memvid](https://github.com/Olow304/memvid)** - a technology that enables efficient semantic search through large documentation sets.

**How Memvid Works:**
- Encodes AWS Well-Architected Framework documentation into video format
- Enables fast semantic search across thousands of pages of AWS guidance
- Works offline once the knowledge base is prepared
- Provides fast retrieval of relevant AWS best practices

#### 🎥 The AWS Knowledge Base in Action

<video width="100%" controls>
  <source src="https://github.com/56kcloud/terraform_advisor_by_56k/raw/main/knowledge/aws/waf_docs.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

*Above: The entire AWS Well-Architected Framework documentation encoded using memvid technology. This single file enables instant semantic search across thousands of pages of AWS best practices - each frame contains encoded documentation chunks that can be searched semantically.*

#### 3. Model-Agnostic Architecture

The system supports different AI models based on your needs:

```python
# Environment-driven model selection
llm=os.getenv("MODEL")  # OpenAI GPT-4, Claude, Llama, etc.

# Tool-specific model configuration  
config=dict(
    llm=dict(
        provider="openai",
        config=dict(model=os.getenv("TOOL_MODEL")),
    ),
    embedder=dict(
        provider="openai",
        config=dict(model=os.getenv("EMBEDDING_MODEL")),
    ),
)
```

This flexibility allows organizations to:
- **Balance Cost and Quality**: Use appropriate models for different analysis depths
- **Maintain Privacy**: Use local models for sensitive codebases
- **Scale Efficiently**: Adjust model complexity based on question complexity

## The Question-Driven Analysis Workflow

Our system processes specific infrastructure questions through a configured three-phase approach, where each agent is defined in YAML configuration files and uses specialized tools to contribute to answering what you've asked.

### Agent Configuration Architecture

Each agent is defined in `config/agents.yaml` with specific roles and tools:

```yaml
# From config/agents.yaml (simplified for readability)
terraform_agent:
  role: "Senior Terraform Infrastructure Analyst"
  goal: "Answer questions by analyzing Terraform codebases"
  backstory: "You're a specialized Infrastructure Code Analyst ..."

aws_agent:
  role: "AWS Well-Architected Framework Authority"  
  goal: "Research AWS best practices for specific questions"
  backstory: "You're a Principal AWS Solutions Architect ..."

response_agent:
  role: "Solutions Architecture Integration Specialist"
  goal: "Synthesize analysis into actionable answers"
  backstory: "You're a Senior Solutions Architecture Integration Specialist ..."
```

> **Note**: All YAML examples in this section are simplified for readability. The actual configuration files contain much more comprehensive specifications, including detailed backstories, step-by-step methodologies, specific tool usage instructions, structured output formats, and quality standards.

### Task Execution Workflow

Each phase corresponds to a task defined in `config/tasks.yaml` that orchestrates the agent's work:

### Phase 1: Codebase Research Task

The **terraform_agent** executes the `codebase_research_task`:

```yaml
# From config/tasks.yaml (simplified for readability)
codebase_research_task:
  description: "Analyze the Terraform codebase to answer: {query}"
  expected_output: "Evidence-based answer with code examples and current implementation details"
  agent: terraform_agent
```

**What it does**: Uses GithubSearchTool to search for Terraform configurations that address your specific question.

### Phase 2: AWS Research Task

The **aws_agent** executes the `aws_research_task`:

```yaml
# From config/tasks.yaml (simplified for readability)
aws_research_task:
  description: "Research AWS best practices to answer: {query}"
  expected_output: "Authoritative AWS guidance with specific recommendations and requirements"
  agent: aws_agent
```

**What it does**: Uses MemvidSearchTool to search AWS Well-Architected Framework documentation for guidance relevant to your question.

### Phase 3: Response Synthesis Task

The **response_agent** executes the `response_task`:

```yaml
# From config/tasks.yaml (simplified for readability)
response_task:
  description: "Synthesize analysis to provide comprehensive answer to: {query}"
  expected_output: "Complete answer with current state, AWS recommendations, and action plan"
  agent: response_agent
  context: [aws_research_task, codebase_research_task]
```

**What it does**: Combines the codebase analysis and AWS research into a comprehensive answer with specific recommendations.

### How Configuration Drives Execution

The system uses this YAML-driven approach to ensure each agent:

1. **Knows Its Role**: Clear role definition and expertise areas
2. **Focuses on the Question**: All descriptions reference `{query}` parameter 
3. **Uses Specific Tools**: Each agent configured with appropriate search tools
4. **Produces Structured Output**: Expected output format defined for each task
5. **Maintains Context**: The response task explicitly depends on both research tasks

![Execution Excerpt](/execution_excerpt.png)

*Above: Example of how the three agents collaborate to answer a specific infrastructure question using their specialized tools.*

## Why This Approach Works

### 1. **Question-Focused Analysis**
- Avoids generic recommendations by focusing on what you actually asked
- Provides evidence-based answers using your actual code
- Combines current state analysis with authoritative best practices
- Delivers actionable improvements specific to your question

### 2. **Repository Flexibility**
- Works with any Terraform repository structure
- Analyzes both public and private repositories  
- Supports different Terraform patterns and module structures
- No vendor lock-in or proprietary requirements

### 3. **AI Model Adaptability**
- Choose models based on budget and accuracy requirements
- Support for multiple AI providers (OpenAI, Anthropic, local models)
- Separate model configuration for different components
- Easy to upgrade as new models become available

### 4. **Efficient Knowledge Access**
- Fast semantic search through comprehensive AWS documentation
- Offline-capable analysis once knowledge base is prepared
- Always up-to-date AWS guidance when knowledge base is refreshed
- No dependency on external APIs during analysis

## Conclusion

Terraform Advisor represents a focused approach to infrastructure analysis - one that answers your specific questions by combining the reality of your current code with the authority of AWS best practices. Rather than generic recommendations, you get targeted insights that help you make informed decisions about your infrastructure.

The combination of specialized AI agents, flexible model support, and efficient knowledge access creates a practical tool for teams who need specific answers to infrastructure questions, not broad architectural reviews.

---

*Explore our [GitHub repository](https://github.com/56kcloud/terraform_advisor_by_56k) to get started, or reach out to discuss how Terraform Advisor can help answer your infrastructure questions.*

**Built with ❤️ by the team at [56k.Cloud](https://56k.cloud)**

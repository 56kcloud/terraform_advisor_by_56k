#!/usr/bin/env python
import sys
import os
from datetime import datetime
from terraform_advisor_by_56k.crew import terraform_advisor_by_56k

os.makedirs('output', exist_ok=True)

def run_single_question(query, question_index=None):
    """Run the crew for a single question."""
    try:
        inputs = {
            'codebase_name': os.getenv("GITHUB_REPO", "Unknown Repository"),
            'query': query
        }
        
        print(f"Processing question {question_index or 1}: {query[:80]}{'...' if len(query) > 80 else ''}")
        
        result = terraform_advisor_by_56k().crew().kickoff(inputs=inputs)
        
        markdown_output = f"""# Question {question_index or 1}

**Query:** {query}

{result.raw}

---
"""
        return markdown_output
        
    except Exception as e:
        print(f"Error processing question: {e}")
        return f"""# Question {question_index or 1} - Error

**Query:** {query}  
**Error:** {str(e)}

---
"""

def load_questions():
    """Load questions from the questions.txt file."""
    questions = []
    
    # Try to load from questions.txt file
    questions_file = "knowledge/questions.txt"
    if os.path.exists(questions_file):
        try:
            with open(questions_file, 'r') as f:
                questions = [q.strip() for q in f.readlines() if q.strip()]
        except Exception as e:
            print(f"Error reading {questions_file}: {e}")
    
    return questions

def run():
    """Run the crew."""
    # Try to load questions from files
    questions = load_questions()
    
    if questions:
        print(f"Found {len(questions)} questions to process")
        
        # Process all questions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        all_results = []
        
        for i, question in enumerate(questions, 1):
            result = run_single_question(question, i)
            all_results.append(result)
            
            # Save individual question report
            question_file = f'output/question_{i:02d}_{timestamp}.md'
            with open(question_file, 'w') as f:
                f.write(f"# Infrastructure Analysis - Question {i}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(result)
            
            print(f"  → Saved individual report: {question_file}")
        
        # Save combined final report
        final_report = f'output/complete_review_{timestamp}.md'
        with open(final_report, 'w') as f:
            f.write(f"# Complete Infrastructure Review\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Questions:** {len(questions)}\n\n")
            f.write('\n'.join(all_results))
        
        print(f"\n✅ Individual reports saved for each question")
        print(f"✅ Complete review saved to: {final_report}")
        return final_report
    
    else:
        # Single question mode
        if len(sys.argv) > 1:
            query = " ".join(sys.argv[1:])
        else:
            query = input("Enter your question: ")
        
        if not query:
            query = "Analyze this Terraform infrastructure and provide recommendations"
        
        result = run_single_question(query)
        
        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'output/analysis_{timestamp}.md'
        with open(output_file, 'w') as f:
            f.write(result)
        
        print(f"Analysis saved to: {output_file}")
        return output_file

def train():
    """Train the crew."""
    inputs = {
        "query": "How can I improve this infrastructure?",
        'codebase_name': os.getenv("GITHUB_REPO", "test-repo")
    }
    try:
        terraform_advisor_by_56k().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Training error: {e}")

def replay():
    """Replay the crew execution."""
    try:
        terraform_advisor_by_56k().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"Replay error: {e}")

def test():
    """Test the crew execution."""
    inputs = {
        "query": "Test infrastructure analysis",
        "codebase_name": os.getenv("GITHUB_REPO", "test-repo")
    }
    try:
        terraform_advisor_by_56k().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"Test error: {e}")

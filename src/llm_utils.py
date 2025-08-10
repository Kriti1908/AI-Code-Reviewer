import os
import openai
from typing import List, Dict
import re

def analyze_code_changes(diff_content: str) -> List[Dict]:
    """
    Analyze code changes using OpenAI's GPT model
    Returns a list of review comments
    """
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    # Prepare the prompt for the LLM
    prompt = f"""
    Analyze the following code diff and output your review as a list of comments
    in the following strict format (one comment block per finding):

    PATH: <file path>
    POSITION: <line number in diff>
    COMMIT_ID: <commit id>
    COMMENT: <comment text>

    Separate multiple comments with a line containing only ---
    Diff content:
    {diff_content}
    """
    
    # Get analysis from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an experienced code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    # Parse and format the response
    review_comments = parse_llm_response(response.choices[0].message.content)
    return review_comments

def parse_llm_response(response: str):
    """
    Example expected output from GPT:
    PATH: src/main.py
    POSITION: 14
    COMMIT_ID: abc123
    COMMENT: Consider handling exceptions for better reliability.

    Multiple comments can be separated by '---'
    """
    comments = []
    for block in response.strip().split("---"):
        path_match = re.search(r"PATH:\s*(.+)", block)
        pos_match = re.search(r"POSITION:\s*(\d+)", block)
        commit_match = re.search(r"COMMIT_ID:\s*(\w+)", block)
        comment_match = re.search(r"COMMENT:\s*(.+)", block, re.DOTALL)

        if path_match and pos_match and commit_match and comment_match:
            comments.append({
                "path": path_match.group(1).strip(),
                "position": int(pos_match.group(1)),
                "commit_id": commit_match.group(1).strip(),
                "body": comment_match.group(1).strip()
            })
    return comments

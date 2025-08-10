import os
import requests
from github import Github
import json

def get_pull_request_diff():
    """Fetch the pull request diff content from GitHub"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    
    # Parse GitHub event context
    event_path = os.getenv('GITHUB_EVENT_PATH')
    with open(event_path, 'r') as f:
        event_data = json.load(f)
    
    repo = g.get_repo(event_data['repository']['full_name'])
    pr_number = event_data['pull_request']['number']
    pull_request = repo.get_pull(pr_number)
    
    # Get diff content
    diff_url = pull_request.diff_url
    response = requests.get(diff_url)
    return response.text

def post_review_comment(comment):
    """Post review comments to PR (single or batch)"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    event_path = os.getenv('GITHUB_EVENT_PATH')
    with open(event_path, 'r') as f:
        event_data = json.load(f)

    repo = g.get_repo(event_data['repository']['full_name'])
    pr_number = event_data['pull_request']['number']
    pull_request = repo.get_pull(pr_number)

    # If multiple comments, wrap them in a review
    if isinstance(comment, list):
        pull_request.create_review(
            body="Automated AI Code Review",
            comments=comment,
            event="COMMENT"
        )
    else:
        pull_request.create_review_comment(
            body=comment['body'],
            commit_id=comment['commit_id'],
            path=comment['path'],
            position=comment['position']
        )

def merge_pull_request():
    """Merge PR after review (if no blocking comments)"""
    g = Github(os.getenv('GITHUB_TOKEN'))
    event_path = os.getenv('GITHUB_EVENT_PATH')
    with open(event_path, 'r') as f:
        event_data = json.load(f)

    repo = g.get_repo(event_data['repository']['full_name'])
    pr_number = event_data['pull_request']['number']
    pull_request = repo.get_pull(pr_number)

    pull_request.merge(merge_method="squash", commit_message="Auto-merged after AI review")

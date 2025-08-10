import os
from github_utils import get_pull_request_diff, post_review_comment, merge_pull_request
from llm_utils import analyze_code_changes

class AICodeReviewer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.github_token = os.getenv('GITHUB_TOKEN')
        
    def review_pull_request(self):
        # Get the PR diff
        diff_content = get_pull_request_diff()
        
        # Analyze changes using LLM
        review_comments = analyze_code_changes(diff_content)
        if review_comments:
            post_review_comment(review_comments)

        if not review_comments:  # No issues found
            print("No issues found. Merging the pull request.")
            merge_pull_request()

if __name__ == '__main__':
    reviewer = AICodeReviewer()
    reviewer.review_pull_request()
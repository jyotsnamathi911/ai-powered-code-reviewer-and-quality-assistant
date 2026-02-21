from ai_code_reviewer.core.reviewer import CodeReviewer
reviewer = CodeReviewer('review_test.py')
issues = reviewer.review()
for issue in issues:
    print(issue)
import argparse
from ai_code_reviewer.core.parser import CodeParser
from ai_code_reviewer.core.apply import apply_docstrings
from ai_code_reviewer.core.metrics import MetricsCalculator
from ai_code_reviewer.config.config_loader import ConfigLoader
from ai_code_reviewer.core.reviewer import CodeReviewer

def main():
    '''"""Summary of the function.

"""'''
    parser = argparse.ArgumentParser(description='AI Powered Code Reviewer')
    parser.add_argument('command', choices=['scan', 'apply', 'report', 'export', 'review'])
    parser.add_argument('file', help='Path to Python file')
    parser.add_argument('--style', default='google', choices=['google', 'numpy', 'rest'])
    parser.add_argument('--ai', action='store_true', help='Enable AI semantic analysis')
    args = parser.parse_args()
    config = ConfigLoader().load()
    style = args.style or config.get('style', 'google')
    coverage_threshold = config.get('coverage_threshold', 0)
    if args.command == 'scan':
        code_parser = CodeParser(args.file)
        code_parser.parse()
        print(code_parser.summary())
    elif args.command == 'apply':
        apply_docstrings(args.file, style)
        print('Docstrings applied successfully.')
    elif args.command == 'report':
        metrics = MetricsCalculator(args.file, exclude=config.get('exclude', []))
        result = metrics.calculate()
        print(result)
        if result['coverage_percent'] < coverage_threshold:
            print('Coverage below threshold!')
            exit(1)
    elif args.command == 'export':
        metrics = MetricsCalculator(args.file, exclude=config.get('exclude', []))
        file_path = metrics.export_csv()
        print(f'CSV report generated at {file_path}')
    elif args.command == 'review':
        reviewer = CodeReviewer(args.file, exclude=config.get('exclude', []), use_ai=args.ai)
        issues = reviewer.review()
        if not issues:
            print('No issues found.')
        else:
            critical = [i for i in issues if i['severity'] == 'critical']
            warnings = [i for i in issues if i['severity'] == 'warning']
            info = [i for i in issues if i['severity'] == 'info']
            print('\nSummary:')
            print(f'Critical: {len(critical)}')
            print(f'Warnings: {len(warnings)}')
            print(f'Info: {len(info)}')
            print('\nDetailed Findings:\n')
            for issue in critical + warnings + info:
                print(f"[{issue['severity'].upper()}] {issue['file']}:{issue['line']} → {issue['message']}")
            if len(critical) > 0:
                exit(1)
if __name__ == '__main__':
    main()
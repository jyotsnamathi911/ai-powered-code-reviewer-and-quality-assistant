import sys
from ai_code_reviewer.core.metrics import MetricsCalculator
from ai_code_reviewer.config.config_loader import ConfigLoader

def run():
    '''"""Summary of the function.

"""'''
    config = ConfigLoader().load()
    threshold = config.get('coverage_threshold', 0)
    exclude = config.get('exclude', [])
    metrics = MetricsCalculator('.', exclude=exclude)
    result = metrics.calculate()
    print('Pre-commit Check:')
    print(result)
    if result['coverage_percent'] < threshold:
        print('❌ Commit blocked: Coverage below threshold.')
        sys.exit(1)
    print('✅ Coverage OK. Commit allowed.')
if __name__ == '__main__':
    run()
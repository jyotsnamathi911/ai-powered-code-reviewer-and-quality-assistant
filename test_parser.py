from ai_code_reviewer.core.metrics import MetricsCalculator
metrics = MetricsCalculator('sample.py')
print(metrics.calculate())
from coverage import Coverage
import coverage
import pytest


def run_tests_with_coverage():
    cov = Coverage(
        branch=True,
        source=['.'],
        omit=[
            '*/venv/*',
            '*/site-packages/*'
        ]
    )

    cov.start()

    pytest.main(['-v',
                 'tests/functional/test_functional.py',
                 'tests/integration/test_integration.py',
                 'tests/unit/test_unit.py'])

    cov.stop()
    cov.save()

    try:
        cov.report()
    except coverage.exceptions.NoDataError:
        print("No data to report.")
    else:
        cov.html_report(directory='coverage_html')


if __name__ == '__main__':
    run_tests_with_coverage()

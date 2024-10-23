from coverage import Coverage
import coverage
import pytest


def run_tests_with_coverage():
    cov = Coverage(
        branch=True,
        source=['.'],
        omit=[
            '*/venv/*',
            '*/site-packages/*',
            'locustfile.py',            
            'run_coverage.py'  
        ]
    )

    cov.start()

    pytest.main(['-v'])

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

from mage_ai.orchestration.run_status_checker import check_status

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def check_condition(*args, **kwargs) -> bool:
    return check_status(
        'train',
        kwargs['execution_date'],
        hours=1,  # optional if you want to check for a specific time window. Default is 24 hours.
    )

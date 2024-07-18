import os
import shutil

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor


@sensor
def check_condition(*args, **kwargs) -> bool:
    file_name = 'dataset'
    source_dir = 'mlops/data/test'
    backup_dir = 'mlops/data/files'

    source_path = os.path.join(source_dir, f'{file_name}.csv')
    backup_path = os.path.join(backup_dir, f'{file_name}_1.csv')

    if os.path.exists(source_path):
                return True
    else:
        # If not, check if the file exists in the backup directory
        if os.path.exists(backup_path):
            # Copy the file from the backup directory to the source directory
            shutil.copy(backup_path, source_path)
            return True
        else:
            return False

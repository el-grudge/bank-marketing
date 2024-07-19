import subprocess
import os


if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom


@custom
def transform_custom(*args, **kwargs):
    try:
        # Open the command in a new session to detach it
        process = subprocess.Popen(
            ['python', '/home/src/mlops/payloads/predict.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        # Immediately return the PID or some identifier
        print(f"Started process with PID: {process.pid}")
        
        # Optionally, you can wait for a short period to check if it fails immediately
        try:
            stdout, stderr = process.communicate(timeout=5)
            if process.returncode != 0:
                print(f"Command failed with return code {process.returncode}")
                print(f"Error output: {stderr.decode()}")
            else:
                print(f"Command succeeded with output: {stdout.decode()}")
        except subprocess.TimeoutExpired:
            print("Process is running in the background")

    except Exception as e:
        print(f"Failed to start process: {e}")

    try:
        # Open the command in a new session to detach it
        process = subprocess.Popen(
            ['streamlit', 'run', '/home/src/mlops/payloads/app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        # Immediately return the PID or some identifier
        print(f"Started process with PID: {process.pid}")
        
        # Optionally, you can wait for a short period to check if it fails immediately
        try:
            stdout, stderr = process.communicate(timeout=5)
            if process.returncode != 0:
                print(f"Command failed with return code {process.returncode}")
                print(f"Error output: {stderr.decode()}")
            else:
                print(f"Command succeeded with output: {stdout.decode()}")
        except subprocess.TimeoutExpired:
            print("Process is running in the background. To access the dashboard go to this link: http://localhost:8501")

    except Exception as e:
        print(f"Failed to start process: {e}")

if __name__ == "__main__":
    run_detached_command()

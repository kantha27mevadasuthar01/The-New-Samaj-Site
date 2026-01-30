import subprocess

def run_migrations():
    """
    Executes 'makemigrations' and 'migrate' commands.
    Useful for deployment on PythonAnywhere.
    """
    commands = [
        ["python", "manage.py", "makemigrations"],
        ["python", "manage.py", "migrate"]
    ]

    for cmd in commands:
        try:
            print(f"Running: {' '.join(cmd)}...")
            output = subprocess.check_output(
                cmd, 
                stderr=subprocess.STDOUT
            )
            print("Output:")
            print(output.decode("utf-8"))
            print("-" * 20)
        except subprocess.CalledProcessError as e:
            print(f"Error running command {' '.join(cmd)}:")
            print(e.output.decode("utf-8"))
            return # Stop if the first command fails
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return

    print("Migration process completed successfully!")

if __name__ == "__main__":
    run_migrations()

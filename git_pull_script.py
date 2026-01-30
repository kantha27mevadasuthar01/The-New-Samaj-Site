import subprocess

def git_pull():
    """
    Executes 'git pull' in the current directory.
    Useful for deployment scripts on PythonAnywhere.
    """
    try:
        # Run the git pull command
        print("Starting git pull...")
        output = subprocess.check_output(
            ["git", "pull"], 
            stderr=subprocess.STDOUT
        )
        # Print the output
        print("Git Pull Output:")
        print(output.decode("utf-8"))
        print("Success!")
    except subprocess.CalledProcessError as e:
        # Handle errors
        print("Error pulling from git:")
        print(e.output.decode("utf-8"))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    git_pull()

import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from github import Github
import base64
from datetime import datetime

# GitHub setup
GITHUB_TOKEN = "your_github_token"
REPO_NAME = "your_username/repository_name"

github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)

def upload_to_github(file_path, file_name):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Create unique path with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        github_path = f"uploads/{timestamp}_{file_name}"
        
        # Upload to GitHub
        repo.create_file(
            github_path,
            f"Upload {file_name}",
            content,
            branch="main"
        )
        print(f"Uploaded {file_name} to GitHub")
    except Exception as e:
        print(f"Upload failed: {e}")

def start_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("user", "12345", ".", perm="elradfmw")
    
    handler = FTPHandler
    handler.authorizer = authorizer
    
    def on_file_received(handler_instance):
        file_path = handler_instance.full_filename
        file_name = os.path.basename(file_path)
        upload_to_github(file_path, file_name)
    
    handler.on_file_received = on_file_received
    
    server = FTPServer(("0.0.0.0", 2121), handler)
    print("\nFTP Server running")
    print("Username: user")
    print("Password: 12345")
    print("Port: 2121")
    server.serve_forever()

if __name__ == "__main__":
    start_ftp_server()

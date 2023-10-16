class GitModule:
    import os
    from git.repo import Repo
    from git.exc import GitCommandError

    # Add the DevAssistant's username and email
    devassistant_username = 'Dev Assistant AI'
    devassistant_email = 'devassistant@tonet.dev'

    def __init__(self):
        pass

    def execute(self, operation, args):
        if operation == 'init':
            return self.git_init(args.get('directory'))
        elif operation == 'add':
            return self.git_add(args.get('directory'))
        elif operation == 'commit':
           return self.git_commit(args.get('message'), args.get('directory'), self.devassistant_username, self.devassistant_email)
        elif operation == 'pull':
            return self.git_pull(args.get('remote'), args.get('branch'), args.get('directory'))
        elif operation == 'checkout':
            return self.git_checkout(args.get('branch'), args.get('directory'))
        elif operation == 'push':
            return self.git_push(args.get('remote'), args.get('branch'), args.get('directory'))
        elif operation == 'status':
            return self.git_status(args.get('directory'))
        elif operation == 'diff':
            return self.git_diff(args.get('file_path'), args.get('directory'))
        elif operation == 'reset':
            return self.git_reset(args.get('path'))
        elif operation == 'log':
            return self.git_log(args.get('directory'))
        else:
            return {'error': f'Unknown operation: {operation}'}

    def git_init(self, directory):
        try:
            repo_path = directory or self.os.getcwd()
            self.Repo.init(repo_path)
            return {"message": f"Repo init in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_add(self, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            repo.git.add('.')
            return {"message": f"Repo add in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_commit(self, message, directory, username=None, email=None):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)

            # If a username and email are provided, use them for the commit
            if username and email:
                repo.git.commit('-m', message, author=f'{username} <{email}>')
            # Otherwise, use the default username and email for the commit
            else:
                repo.git.commit('-m', message, author=f'{self.devassistant_username} <{self.devassistant_email}>')

            return {"message": f"Repo commit in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_push(self, remote, branch, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            repo.git.push(remote, branch)
            return {"message": f"Repo pushed to {remote} {branch} in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_status(self, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            return {"message": f"Repo status in {repo_path}", "status": repo.git.status()}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_diff(self, file_path, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            diff = repo.git.diff(file_path)
            return {"message": f"Repo diff in {repo_path}", "diff": diff}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}
        
    def git_reset(self, path):
        try:
            repo_path = path or self.os.getcwd()
            repo = self.Repo(repo_path)
            repo.git.reset()
            return {"message": f"Repo reset in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_log(self, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            log = repo.git.log()
            return {"message": f"Repo log in {repo_path}", "log": log}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}
    
    def git_pull(self, remote, branch, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            repo.git.pull(remote, branch)
            return {"message": f"Repo pulled from {remote} {branch} in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

    def git_checkout(self, branch, directory):
        try:
            repo_path = directory or self.os.getcwd()
            repo = self.Repo(repo_path)
            repo.git.checkout(branch)
            return {"message": f"Switched to {branch} in {repo_path}"}
        except self.GitCommandError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": str(e)}

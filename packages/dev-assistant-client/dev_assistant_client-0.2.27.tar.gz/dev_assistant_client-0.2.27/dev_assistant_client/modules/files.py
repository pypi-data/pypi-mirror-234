class FilesModule:
    import os
    import shutil
    import unidiff

    def __init__(self):
        pass

    def execute(self, operation, args):
        operations = {
            "create": self.create,
            "read": self.read,
            "update": self.update,
            "delete": self.delete,
            "list": self.list_dir,
            "copy": self.copy,
            "move": self.move,
            "rename": self.rename,
            "apply_diff": self.apply_diff
        }
        func = operations.get(operation)
        if func:
            return func(**args)
        else:
            return {"error": f"Unknown operation: {operation}"}

    def create(self, path, content=None):
        directory = self.os.path.dirname(path)
        if not self.os.path.exists(directory):
            self.os.makedirs(directory)

        with open(path, "w", encoding="utf-8") as file:
            if content:
                file.write(content)
        return {"message": f"File created at {path}"}

    def read(self, path):
        if not self.os.path.exists(path):
            return {"error": f"Path does not exist: {path}"}

        if self.os.path.isdir(path):
            return self.list_dir(path)

        with open(path, "r", encoding="utf-8") as file:
            content = file.read()

        return {"content": content}

    def update(self, path, content):
        if not self.os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return {"message": f"File updated at {path}"}

    def delete(self, path):
        if not self.os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        self.os.remove(path)
        return {"message": f"File deleted at {path}"}

    def list_dir(self, path):
        if not self.os.path.exists(path):
            return {"error": f"Directory does not exist: {path}"}

        try:
            files = self.os.listdir(path)
        except Exception as e:
            return {"error": f"Error listing directory: {e}"}
        
        return {"files": files}

    def copy(self, source, destination):
        if not self.os.path.exists(source):
            return {"error": f"File does not exist: {source}"}

        self.shutil.copy(source, destination)
        return {"message": f"File copied from {source} to {destination}"}

    def move(self, source, destination):
        if not self.os.path.exists(source):
            return {"error": f"File does not exist: {source}"}

        self.shutil.move(source, destination)
        return {"message": f"File moved from {source} to {destination}"}

    def rename(self, source, destination):
        if not self.os.path.exists(source):
            return {"error": f"File does not exist: {source}"}

        self.shutil.move(source, destination)
        return {"message": f"File renamed from {source} to {destination}"}

    def apply_diff(self, path, diff_instructions):
        if not self.os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        with open(path, "r", encoding="utf-8") as file:
            original_content = file.read()

        # Aplicar as instruções diff usando unidiff
        patch_set = self.unidiff.PatchSet.from_string(diff_instructions)
        patched_content = original_content
        for patched_file in patch_set:
            for hunk in patched_file:
                patched_content = hunk.apply_to(patched_content)

        # Salvar o arquivo após aplicar o diff
        with open(path, "w", encoding="utf-8") as file:
            file.write(patched_content)

        return {"message": f"Diff applied to file at {path}"}

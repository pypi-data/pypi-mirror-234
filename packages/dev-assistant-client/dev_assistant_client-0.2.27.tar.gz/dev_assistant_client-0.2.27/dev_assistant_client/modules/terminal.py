class TerminalModule:
    import subprocess

    def __init__(self):
        pass

    def execute(self, operation, args):
        if operation == 'run':
            return self.run(args.get('command'))
        else:
            return {'error': f'Unknown operation: {operation}'}

    def run(self, command):
        try:
            process = self.subprocess.Popen(command, stdout=self.subprocess.PIPE, stderr=self.subprocess.PIPE, shell=True)
            output, error = process.communicate()
            if process.returncode != 0:
                return {'error': error.decode('utf-8')}
            else:
                return {'stdout': output.decode('utf-8')}
        except Exception as e:
            return {'error': str(e)}

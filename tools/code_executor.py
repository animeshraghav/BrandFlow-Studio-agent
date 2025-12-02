import subprocess
import tempfile


class CodeExecutionTool:
    """
    Executes Python code in a controlled subprocess.
    Not fully sandboxed but safer than eval().
    """

    def run_code(self, code: str) -> str:
        logger.info("[CodeExecutionTool] running ephemeral python code")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        try:
            result = subprocess.run(
                ["python", tmp_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout + "\n" + result.stderr
        except Exception as e:
            return f"Execution error: {e}"

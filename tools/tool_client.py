
from .search_tool import GoogleSearchTool
from .image_tool import GoogleImageTool
from .code_executor import CodeExecutionTool

class GoogleToolClient:
    """
    Wrapper that unifies search, image gen, and code execution tools.

    Agents expect a .search(), .generate_image(), .run_code() API.
    """

    def __init__(self):
        self.search_tool = GoogleSearchTool()
        self.image_tool = GoogleImageTool()
        self.code_tool = CodeExecutionTool()

    def search(self, query: str, top_k: int = 5):
        return self.search_tool.search(query, top_k)

    def generate_image(self, prompt: str, n: int = 1, size: str = "1024x1024"):
        return self.image_tool.generate_image(prompt, n, size)

    def run_code(self, code: str):
        return self.code_tool.run_code(code)


# END OF TOOLS MODULE

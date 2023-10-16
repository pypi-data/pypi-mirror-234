"""
A tool to generate a message from previous (numbered) messages in the chat history.
The idea is that when an LLM is generating text that is a deterministic transformation
of a previous message, then specifying the transformation can be much cheaper
than actually generating the transformation.
"""

from langroid.agent.tool_message import ToolMessage


class GeneratorTool(ToolMessage):
    request: str = ""
    purpose: str = """
            To generate a message where the parts within curly braces specify 
            what should be inserted, using a substitution specification.
            """
    rules: str

    def handle(self) -> None:
        pass

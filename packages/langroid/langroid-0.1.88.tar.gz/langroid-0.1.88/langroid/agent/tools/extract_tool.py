"""
A tool to extract portions from previous (numbered) messages in
the chat history.
The idea is that when an LLM wants to (or is asked to) simply extract
portions of a message verbatim, it should use this tool/function to
SPECIFY what should be extracted, rather than actually extracting it.
This will usually be much cheaper and faster than actually writing out the extracted
text. The handler of this tool/function will then extract the text and send it back.
"""

from typing import Protocol, no_type_check

from jinja2 import DictLoader, Environment

from langroid.agent.tool_message import ToolMessage
from langroid.language_models.base import LLMMessage


def extract_between(value: str, start_word: str, end_word: str) -> str:
    """
    Extract the substring between two words in a string.
    NOTE: If there are multiple occurrences of the start_word, the first one is used,
    and if there are multiple occurrences of the end_word, the first one after the
    start_word is used.

    We do not handle the case of multiple occurrences of the start_word, followed by
    multiple occurrences of the end_word

    Args:
        value (str): the string to extract from
        start_word (str): the word that starts the substring
        end_word (str): the word that ends the substring

    Returns:
        str: the substring between the two words
    """
    try:
        start_index = value.index(start_word) + len(start_word)
        end_index = value.index(end_word, start_index)
        return value[start_index:end_index].strip()
    except ValueError:
        return ""


class HasMessageHistory(Protocol):
    """
    Defines the fields expected in a class that enables this tool.
    """

    message_history: list[LLMMessage]


class ExtractTool(ToolMessage):
    request: str = "extract"
    purpose: str = """
            To generate a message in the form of a <jinja_template>, 
            using the Jinja templating language, where the 
            the i'th message is referred to as msg[i], and integer indices are used 
            to specify which part of the message to extract, e.g. msg[2][13:45].
            """
    jinja_template: str

    @classmethod
    def instructions(cls) -> str:
        return """
        In a conversation with the user, your responses may sometimes use verbatim 
        extracts of previous messages in the conversation.  You are an expert at 
        Jinja templating syntax, and you will rely on this syntax whenever you find 
        yourself wanting to repeat verbatim text from earlier parts of the 
        conversation.  
        In your Jinja templates you can use references like {{msg[3][3:100]}} to 
        indicate that the user should substitute the content of message number 3 
        (assume first msg is number 1), starting at position 3 and ending at 100.   
        
        For example you may respond with something like:
        
        The story started like this: {{msg[5][45:89]}}. Then John came home and 
        {{msg[2][4:19}}. 
        
        VERY IMPORTANT --
        (a) your FIRST priority is to generate  messages that would sound natural 
        when the jinja templates are rendered. 
        
        (b) your NEXT priority is to ALWAYS RELY on the above JINJA scheme when 
        your intended message would contain verbatim text from previous messages. 
        
        (c) Do not simply use large verbatim parts of previous messages, when doing 
        so may not result in natural responses.         
        """

    @no_type_check
    def handle(self: HasMessageHistory) -> str:
        msg = self.message_history
        env = Environment(loader=DictLoader({"base": self.jinja_template}))
        template = env.get_template("base")
        return template.render(msg=msg)

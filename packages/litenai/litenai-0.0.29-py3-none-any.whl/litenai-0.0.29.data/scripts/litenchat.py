"""
Chat app for LitenAI
"""
import sys
import panel as pn

import litenai as tenai

class ChatApp():
    """
    Chat app for LitenAI
    """
    def start(self,
              config_file : str = 'liten.yaml'):
        """
        Start chat app
        """
        pn.extension('bokeh')
        session = tenai.Session.get_or_create('chatsession', config_file)
        chatbot = tenai.ChatBot(session=session)
        chat_panel = chatbot.start()
        chat_panel.servable(title="LitenAI")

def print_usage():
    """
    Print usage
    """
    print(f"""
Usage: python chatapp.py <config_file>
Example: python chatapp.py liten.yaml
Received: f{sys.argv}
""")

config_file = 'liten.yaml'

if len(sys.argv)==2:
    config_file = sys.argv[1]
    ChatApp().start(config_file=config_file)
else:
    print_usage()

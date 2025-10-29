from agent import Agent
from environment import Environment


class Controller:
    """Orkestrerar hela MCP-cykeln."""
    def __init__(self):
        self.env = Environment()
        self.agent = Agent()

    def run(self):
        while True:
            emails = self.env.observe()
            if not emails:
                print("Inga fler mejl att behandla.")
                break

            for email in emails:
                decision = self.agent.decide(email)
                self.env.act(email, decision)
                self.env.log_inbox()

if __name__ == "__main__":
    Controller().run()

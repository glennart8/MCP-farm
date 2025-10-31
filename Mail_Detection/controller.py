from classes.agents import SupervisorAgent
from classes.environment import Environment

class Controller:
    """MCP-cykeln."""
    def __init__(self):
        self.env = Environment()
        self.agent = SupervisorAgent()

    def run(self):
        while True:
            emails = self.env.observe()
            if not emails:
                print("Inga fler mail att behandla.")
                break

            for email in emails:
                decision, product, meeting_time = self.agent.decide(email) 
                self.env.act(email, decision, product, meeting_time)
                self.env.save_logs()

if __name__ == "__main__":
    Controller().run()

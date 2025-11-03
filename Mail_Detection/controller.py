from classes.agents import SupervisorAgent
from classes.environment import Environment
from classes.sales import SalesSystem

class Controller:
    """MCP-cykeln."""
    def __init__(self):
        self.env = Environment()
        self.agent = SupervisorAgent()
        self.sales = SalesSystem()

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
               
            print("Kollar om offertförfrågningar ska följas upp")    
            self.sales.check_for_followups()

if __name__ == "__main__":
    Controller().run()

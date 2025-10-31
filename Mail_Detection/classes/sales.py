from .agents import SalesAgent
from .autoresponder import AutoResponder
from .mail import MAIL_ACCOUNTS

auto = AutoResponder()
sales_agent = SalesAgent()


class SalesSystem:
    
    list_of_products = {"banan": 10, "äpple": 4, "kiwi": 0, "virke": 120}
    
    def forward_to_sales(self, email, product=None, to=None):
        to = to or "henrikpilback@gmail.com" #default
        print(f"Vidarebefordrar till försäljning")
        
        if product and self.check_if_in_stock(product):
            self.create_order(email, product, to)
        
        
    def check_if_in_stock(self, product):
        if product in self.list_of_products: # Kolla om den finns 
            print(f"{product} finns i sortimentet!") 
    
            if self.list_of_products[product] > 0: # Kolla om den finns INNE
                print(f"{product} finns i lager!")
                return True
            else:
                print(f"{product} är slut i lager!")
                return False
        else:
            print(f"{product} finns inte i sortimentet!")
            return False
        
        
    def create_order(self, email, product, to):
        self.list_of_products[product] -= 1
        sales_message = sales_agent.write_response_to_order(email)
        self.send_auto_response_order(sales_message, to)
        print(f"Order skapad för: {product}")
        
        
    def send_auto_response_order(self, body, to):
        subject = f"Orderbekräftelse"
        auto._send_email(to, subject, body)
        
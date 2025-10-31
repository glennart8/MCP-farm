from .agents import SalesAgent
from .autoresponder import AutoResponder

auto = AutoResponder()
sales_agent = SalesAgent()


class SalesSystem:
    
    list_of_products = {"banan": 10, "äpple": 4, "kiwi": 0, "virke": 120}
    
    def forward_to_sales(self, email, product):
        print(f"Vidarebefordrar till försäljning: '{email['subject']}'")
        
        if self.check_if_in_stock(product):
            try:
                self.create_order(email, product)
                print(f"Order skapad och bekräftelse skickad.")
            except Exception as e:
                print(f"Ett fel uppstod vid orderhantering.: {e}")
        else:
            print(f"{product} är slut i lager!")
        
    def check_if_in_stock(self, product):
        if product in self.list_of_products: # Kolla om den finns 
            if self.list_of_products[product] > 0: # Kolla om den finns INNE
                return True
            else:
                return False
        else:
            print(f"{product} finns inte i sortimentet!")
            return False
        
        
    def create_order(self, email, product):
        self.list_of_products[product] -= 1
        sales_message = sales_agent.write_response_to_order(email)
        self.send_auto_response_order(email, sales_message)

        print(f"Order skapad för: {product}")
        
    def send_auto_response_order(self, email, body):
        customer_nr = 231238
        subject = f"Orderbekräftelse för : {customer_nr}"
        auto._send_email(email['from'], subject, body)
        customer_nr += 1
        
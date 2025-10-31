from .agents import SalesAgent
from .autoresponder import AutoResponder
from .mail import MAIL_ACCOUNTS

auto = AutoResponder()
sales_agent = SalesAgent()


class SalesSystem:
    def __init__(self):
        self.products = {
            "plywood": 250,
            "regel_45x95": 45,
            "bräda_22x145": 120
        }
    
    def create_quote(self, email):
        # Låt LLM extrahera antal per produkt
        order_details = sales_agent.extract_order_from_email(email)
        found_items = order_details["found"]
        not_found_items = order_details["not_found"]    
        
        total_price = 0
        quote_lines = []

        for product, qty in found_items.items():
            price = self.products[product] * qty
            total_price += price
            quote_lines.append(f"{product}: {qty} st * {self.products[product]} :- = {price} SEK\n")

        for product, qty in not_found_items.items():
            quote_lines.append(f"{product}: Kunde tyvärr inte hitta produkten i sortimentet\n") # Be LLM att hitta något liknande kanske?
        
        body = (
            "Hej!\n\n"
            "Här är offerten du efterfrågade:\n\n"
            f"{''.join(quote_lines)}\n"
            f"Totalpris: {total_price} kr\n\n"
            "Vill du lägga en order?\n\n"
            "Vänliga hälsningar,\n"
            "Bengtssons trävaror"
        )

        # Skicka mailet
        to = email['from']
        subject = f"Offert: {email['subject']}"
        auto._send_email(to, subject, body)
        print(f"Offert skickad till {to}")
        
    def calculate_total(self, order):
        total = 0
        for product, qty in order.items():
            price = self.products.get(product, 0)
            total += price * qty
        return total    
    
# -----------------------------------------------------------    
    
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
        
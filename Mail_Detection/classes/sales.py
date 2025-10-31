from .agents import SalesAgent
from .autoresponder import AutoResponder
from .mail import MAIL_ACCOUNTS
from .products import PRODUCTS

auto = AutoResponder()
sales_agent = SalesAgent()


class SalesSystem:
    def __init__(self):
        self.products = PRODUCTS
    
    def calculate_total(self, order):
        total = 0
        for product, qty in order.items():
            price = self.products.get(product, 0)
            total += price * qty
        return total  
    
    def create_quote(self, email):
        # Låt LLM extrahera antal per produkt
        order_details = sales_agent.extract_order_from_email(email)

        print("LLM-svar:", order_details)

        found_items = order_details["found"]
        not_found_items = order_details["not_found"]
        suggestions = order_details["suggestions"]

        # Lägg till föreslagna produkter med rätt antal i found_items
        for missing_product, suggested_product in suggestions.items(): # Loopa igenom varje par (saknad produkt, föreslagen produkt) i suggestions-dictionaryt
            qty = not_found_items.get(missing_product, 0) # Hämta antalet för den saknade produkten från not_found_items, 0 som standard
            if suggested_product in self.products: # Kolla så att den finns i sortimentet
                # Lägg till kvantiteten för den föreslagna produkten i found_items
                found_items[suggested_product] = found_items.get(suggested_product, 0) + qty # Om produkten redan finns, lägg till qty, annars starta på 0 + qty
                print(f"Lägger till föreslaget alternativ: {suggested_product} ({qty} st)")
            else:
                print(f"Förslaget '{suggested_product}' finns inte i sortimentet och ignoreras.")

        # Beräkna totalpris via calculate_total med det uppdaterade found_items
        total_price = self.calculate_total(found_items)

        quote_lines = []
        # Skapa offerttext för alla produkter (inklusive föreslagna)
        for product, qty in found_items.items():
            price = self.products[product]
            quote_lines.append(f"{product}: {qty} st * {price} :-\n")

        # Lägg till meddelanden för saknade produkter
        for product in not_found_items:
            suggestion_text = suggestions.get(product)
            if suggestion_text:
                quote_lines.append(f"\nOBS: Vi kunde inte hitta {product}, men föreslår {suggestion_text} istället.\n")
            else:
                quote_lines.append(f"\nOBS: Vi kunde tyvärr inte hitta {product} i sortimentet.\n")

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
        subject = f"Offert: {email['subject']}"
        auto._send_email(email['from'], subject, body)
        print(f"Offert skickad till {email['from']}")
            
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
        
from .agents import SalesAgent
from .autoresponder import AutoResponder
# from .mail import MAIL_ACCOUNTS
from .products import PRODUCTS
from datetime import datetime
import json

# auto = AutoResponder()
sales_agent = SalesAgent()


class SalesSystem:
    def __init__(self):
        self.products = PRODUCTS
        self.auto = AutoResponder()
    
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
            qty = not_found_items.get(missing_product, 1) # Hämta antalet för den saknade produkten från not_found_items, 1 som standard
            if suggested_product in self.products: # Kolla så att den finns i sortimentet
                # Lägg till kvantiteten för den föreslagna produkten i found_items
                found_items[suggested_product] = found_items.get(suggested_product, 0) + qty # Om produkten redan finns, lägg till qty, annars starta på 0 + qty
                print(f"Lägger till föreslaget alternativ: {suggested_product} ({qty} st)")
            else:
                print(f"Förslaget '{suggested_product}' finns inte i sortimentet och ignoreras.")

        # Beräkna totalpris via calculate_total med det uppdaterade found_items
        total_price = self.calculate_total(found_items)

        quote_lines = []
        # Skapa offerttext för alla produkter (inklusive föreslagna alernativ)
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
            f"Totalpris: {total_price} SEK\n\n"
            "Vill du lägga en order?\n\n"
            "Vänliga hälsningar,\n"
            "Bengtssons trävaror"
        )

        # Skicka mailet
        subject = f"Offert: {email['subject']}"
        self.auto._send_email(email['from'], subject, body)
        print(f"Offert skickad till {email['from']}")
        
        
        self.save_sent_quote(email, found_items)
         
    # --------------- UPPFÖLJNING ------------------
            
    # Spara sänd offert med boolen "followed:up"        
    def save_sent_quote(self, email, products):
        # Spara till en JSON-fil
        quote_data = {
            "customer": email["from"],
            "subject": email["subject"],
            "products": products,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "followed_up": False
        }
        with open("logs/sent_quotes.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(quote_data) + "\n")
            
        print("Offert sparad")       

    # ------- KOLLA OM UPPFÖLJNINGSMAIL SKA SKICKAS ----------
    # Kollar om followed_up är False och om det har gått en dag - då skickas uppföljningsmail
    def check_for_followups(self):
        with open("logs/sent_quotes.json", "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:
            quote = json.loads(line)
            sent_date = datetime.strptime(quote["date"], "%Y-%m-%d %H:%M")
            if not quote["followed_up"] and (datetime.now() - sent_date).days >= 1:
                self.send_followup(quote)
                quote["followed_up"] = True
                
    # ------ SKICKA UPPFÖLJNINGSMAIL ------         
    def send_followup(self, quote):
        customer = quote["customer"]
        products = ", ".join(quote["products"].keys())
        subject = f"Uppföljning på din offert"

        body = (
            f"Hej!\n\n"
            f"Vi skickade en offert på {products} häromdagen. "
            f"Vill du att vi lägger in en beställning åt dig eller har du några frågor?\n\n"
            f"Vänliga hälsningar,\n"
            f"Bengtssons trävaror"
        )

        self.auto._send_email(customer, subject, body)
        print(f"Uppföljningsmail skickat till {customer}")
        
        
        # ----- BERÄKNA VIRKESÅTGÅNG MED GEMINI -------
    def estimate_materials_for_email(self, email):
        description = email["body"]  # Läs in mail

        # Får dict med antal per produkt
        estimated_materials = sales_agent.estimate_materials_json(description)
        
        if not estimated_materials:
            print("Kunde inte beräkna materialåtgång.")
            return None

        return estimated_materials

    # ----- SKAPA MAIL UTIFRÅN BERÄKNING -------
    def create_estimate_email(self, email):
        estimated_materials = self.estimate_materials_for_email(email)
        if not estimated_materials:
            return

        # Offertexten
        quote_lines = [
            f"{prod}: {qty} st * {self.products[prod][0]} :-"  # [0] = pris
            for prod, qty in estimated_materials.items()
            if prod in self.products
        ]

        # pga tuple för isolering mm, ta första elementet
        total_price = sum(self.products[prod][0] * qty for prod, qty in estimated_materials.items() if prod in self.products)

        body = (
            f"Hej\n\n"
            f"Utifrån din beskrivning har vi uppskattat följande materialåtgång:\n\n"
            f"{chr(10).join(quote_lines)}\n\n"
            f"Uppskattat totalpris: {total_price} kr\n\n"
            "Vill du att vi tar fram en officiell offert baserat på dessa mängder?\n\n"
            "Vänliga hälsningar,\n"
            "Bengtssons trävaror"
        )

        subject = f"Uppskattad materialåtgång: {email['subject']}"
        self.auto._send_email(email['from'], subject, body)
        print(f"Materialuppskattning skickad till {email['from']}")
        
                
# ------------------- Vidarebeordra, kolla saldo, skapa kvitto -----------------------------    
    
    # def forward_to_sales(self, email, product=None, to=None):
    #     to = to or "henrikpilback@gmail.com" #default
    #     print(f"Vidarebefordrar till försäljning")
        
    #     if product and self.check_if_in_stock(product):
    #         self.create_order(email, product, to)
        
        
    # def check_if_in_stock(self, product):
    #     if product in self.list_of_products: # Kolla om den finns 
    #         print(f"{product} finns i sortimentet!") 
    
    #         if self.list_of_products[product] > 0: # Kolla om den finns INNE
    #             print(f"{product} finns i lager!")
    #             return True
    #         else:
    #             print(f"{product} är slut i lager!")
    #             return False
    #     else:
    #         print(f"{product} finns inte i sortimentet!")
    #         return False
        
        
    # def create_order(self, email, product, to):
    #     self.list_of_products[product] -= 1
    #     sales_message = sales_agent.write_response_to_order(email)
    #     self.send_auto_response_order(sales_message, to)
    #     print(f"Order skapad för: {product}")
        
        
    # def send_auto_response_order(self, body, to):
    #     subject = f"Orderbekräftelse"
    #     auto._send_email(to, subject, body)
        
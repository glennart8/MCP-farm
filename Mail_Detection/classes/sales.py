class SalesSystem:
    
    list_of_products = {"banan": 10, "äpple": 4, "kiwi": 0, "virke": 120}
    
    def forward_to_sales(self, email, product):
        print(f"Vidarebefordrar till försäljning: '{email['subject']}'")
        
        if self.check_if_in_stock(product):
            self.create_order(product)
            self.send_confirmation_email(product)
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
        
        
    def create_order(self, product):
        print(f"Order skapad för: {product}")

        self.list_of_products[product] -= 1
        
        
    def send_confirmation_email(self, product):
        print(f"Låtsasskickar en bekräftelse för: {product}")
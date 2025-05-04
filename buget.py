class Budget:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction_type, amount, description =""):
        types = {"income", "expense"}
        if transaction_type not in types:
            return False
        
        if amount < 0:
            return False
        
        self.transactions.append({"type": transaction_type, "amount": amount, "description": description})
        return True
    
    def income(self):
        sum_inc = 0
        for transaction in self.transactions:
            if transaction["type"] == "income":
                sum_inc += transaction["amount"]
        return sum_inc
    
    def expense(self):
        sum_exp = 0
        for transaction in self.transactions:
            if transaction["type"] == "expense":
                sum_exp += transaction["amount"]
        return sum_exp

    def available_budget(self):
        sum_inc = self.income()
        sum_exp = self.expense()
        available = sum_inc - sum_exp
        return available
    
    def get_transactions(self):
        return self.transactions.copy()
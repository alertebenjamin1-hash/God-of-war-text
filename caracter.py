class Player:
    def __init__(self, name):
        self.name = name
        self.deck = []
        self.score = 0
        self.health = None
        self.equipment = []

    def add_card(self, card):
        self.deck.append(card)

    def set_score(self, score):
        self.score = score

    def add_card(self, card):
        self.deck.append(card)
    
    def add_equipment(self, equipment):
        self.equipment.append(equipment) 
from card import *
from random import choice

class Game:
    def __init__(self, player):
        self.player = player
        self.monster = None
        self.heros = []
        self.init_all_cards()
        self.LOOT_EFFECT = {
            "attack": lambda card, val: setattr(card, "attack", card.attack + val),
            "defense": lambda card, val: setattr(card, "defense", card.defense + val),
            "health": lambda card, val: setattr(card, "health", card.health + val)
        }

    def isDeckFull(self):
        return len(self.player.deck) == 3

    def printDeck(self):
        if not self.player.deck:
            print("Your deck is empty")
        else:
            for i, card in enumerate(self.player.deck, start=1):
                print(f"{i}. {card}")
        print()

    def printPlayableCards(self, playable):
        for i, card in enumerate(playable, start=1):
            print(f"{i}. {card}")

    def getPlayableCards(self):
        return [card for card in self.heros if card not in self.player.deck]
    
    def deckConfirmation(self):
        print("\n\n====== Deck confirmation ======\n")
        for i, card in enumerate(self.player.deck, start=1):
            print(f"{i}. {card}")
        choice = verify_player_input("Is this your deck ? (0 = no, 1 = yes)", 0, 1)
        return choice

    def init_deck(self):
        print("\n\n====== Deck creation ======\n")
        while not self.isDeckFull():
            print("\nYour Deck : \n")
            self.printDeck()
            print("\nAvailable cards : \n")
            playable = self.getPlayableCards()
            self.printPlayableCards(playable)
            choice = verify_player_input("Please choose a card: ", 1, len(playable))
            self.player.add_card(playable[choice - 1])
        
        choice = self.deckConfirmation()
        if not choice: self.init_deck()

    def playerIsAlive(self):
        return any(card.health > 0 for card in self.player.deck)
    
    def playerCardsAlive(self):
        return [card for card in self.player.deck if card.health > 0]
    
    def clash(self):
        print("\n\n====== Clash ======\n")
        wave = 0
        while self.playerIsAlive():
            wave += 1
            self.player.score += 1
            print(f"\n\n====== Wave {wave} ======\n")
            self.monster = self.choose_monster()
            self.wave()
            drop = self.drop()
            if drop: self.useLoot(drop)

    def init_all_cards(self):
        heros = get_all_heros()
        for hero in heros:
            self.heros.append(Card(
                hero["name"], hero["attack"], hero["defense"], hero["health"],
                hero.get("type", "dps"), hero.get("effect_chance", 0),
                hero.get("effect_damage", 0), hero.get("effect_duration", 0)
            ))

    def choose_monster(self):
        monster = pick_monster()
        return Card(monster["name"], monster["attack"], monster["defense"], monster["health"])

    def wave(self):
        while self.isMonsterAlive() and self.playerIsAlive():
            print("\nYour deck :")
            self.printDeck()
            print("Monster :")
            print(self.monster)
            print()
            self.playerTurn()
            if self.isMonsterAlive():
                self.monsterTurn()
    
    def isMonsterAlive(self):
        return self.monster.health > 0

    def playerTurn(self):
        print("\n====== Player turn ======")
        self.monster.tick_effects()
        if not self.isMonsterAlive():
            return
        for card in self.player.deck:
            if card.health > 0:
                card.attack_target(self.monster)
                if not self.isMonsterAlive():
                    break

    def monsterTurn(self):
        print("\n====== Monster turn ======")
        for card in self.player.deck:
            if card.health > 0:
                card.tick_effects()
        alive = self.playerCardsAlive()
        if alive:
            self.monster.attack_target(choice(alive))

    def drop(self):
        return get_loot()

    @staticmethod
    def printLoot(loot):
        print(f"You found a {loot['name']} | effect: {loot['effect']} {loot['value']}")

    def useLoot(self, loot):
        self.printLoot(loot)
        self.printDeck()
        choice = verify_player_input("Use the loot on who ? ", 1, len(self.player.deck))
        self.LOOT_EFFECT[loot["effect"]](self.player.deck[choice - 1], loot["value"])
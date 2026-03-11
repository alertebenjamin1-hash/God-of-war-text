from utils import *
from random import random

class Card:
    EFFECT_NAMES = {"sorcerer": "poison", "tank": "knocked out"}

    def __init__(self, name, attack, defense, health, card_type="dps", effect_chance=0, effect_damage=0, effect_duration=0):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.health = health
        self.type = card_type
        self.effect_chance = effect_chance
        self.effect_damage = effect_damage
        self.effect_duration = effect_duration
        self.effects = []

    def __str__(self):
        base = f"{self.name} [{self.type.upper()}] - ATK: {self.attack}, DEF: {self.defense}, PV: {self.health}"
        if self.effects:
            effects_str = ", ".join(f"{e['type']} ({e['damage']} dmg x{e['turns']})" for e in self.effects)
            base += f" | {effects_str}"
        return base

    def tick_effects(self):
        if not self.effects:
            return
        remaining = []
        for effect in self.effects:
            print(f"  {self.name} takes {effect['damage']} {effect['type']} damage")
            if self.health - effect['damage'] < 0:
                self.health = 0
            else:
                self.health -= effect['damage']
            effect['turns'] -= 1
            if effect['turns'] > 0:
                remaining.append(effect)
            else:
                print(f"  {self.name}'s {effect['type']} wore off")
        self.effects = remaining

    def attack_target(self, target):
        print(f"{self.name} attacks {target.name}")
        if self.attack - target.defense > 0:
            if target.health - (self.attack - target.defense) < 0:
                target.health = 0
            else:
                target.health -= self.attack - target.defense
        self.try_apply_effect(target)

    def try_apply_effect(self, target):
        if self.type not in self.EFFECT_NAMES:
            return
        if random() < self.effect_chance:
            effect = {
                "type": self.EFFECT_NAMES[self.type],
                "damage": self.effect_damage,
                "turns": self.effect_duration
            }
            target.effects.append(effect)
            print(f"  {self.name} inflicts {effect['type']} on {target.name}! ({effect['damage']} dmg/turn for {effect['turns']} turns)")

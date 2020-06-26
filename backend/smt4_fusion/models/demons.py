from enum import Enum
from functools import reduce
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

from ..flask_extensions import db
from .utils import dict_helper

class Race(Enum):
    Herald = 'Herald'
    Megami = 'Megami'
    Avian = 'Avian'
    Tree = 'Tree'
    Divine = 'Divine'
    Flight = 'Flight'
    Yoma = 'Yoma'
    Nymph = 'Nymph'
    Vile = 'Vile'
    Raptor = 'Raptor'
    Wood = 'Wood'
    Deity = 'Deity'
    Avatar = 'Avatar'
    Holy = 'Holy'
    Genma = 'Genma'
    Fairy = 'Fairy'
    Beast = 'Beast'
    Jirae = 'Jirae'
    Snake = 'Snake'
    Reaper = 'Reaper'
    Wilder = 'Wilder'
    Jaki = 'Jaki'
    Vermin = 'Vermin'
    Fury = 'Fury'
    Lady = 'Lady'
    Dragon = 'Dragon'
    Kishin = 'Kishin'
    Fallen = 'Fallen'
    Brute = 'Brute'
    Femme = 'Femme'
    Night = 'Night'
    Tyrant = 'Tyrant'
    Drake = 'Drake'
    Spirit = 'Spirit'
    Foul = 'Foul'
    Ghost = 'Ghost'
    Fiend = 'Fiend'
    Enigma = 'Enigma'
    Food = 'Food'
    Zealot = 'Zealot'
    Entity = 'Entity'
    Famed = 'Famed'
    Amatsu = 'Amatsu'
    Kunitsu = 'Kunitsu'
    Undead = 'Undead'
    Godly = 'Godly'
    Chaos = 'Chaos'
    Element = 'Element'


class Resist:

    def __init__(self, resist_string):
        resists = { '-': 0x00, 's': 0x01, 'w': 0x02, 'n': 0x03, 'd': 0x04,  'r': 0x05 }
        self.code = reduce(lambda r, v: r | resists[v[1]] << v[0]*4,
                            enumerate(reversed(resist_string)),
                            0)


    def __str__(self):
        resists = { 0x00: '-' , 0x01: 's', 0x02: 'w', 0x03: 'n', 0x04: 'd',  0x05: 'r' }
        return reduce(
            lambda r, v: f'{r}{resists[int("".join(v), 2)]}',
            zip(*[iter(f'{bin(self.code)[2:]:>032}')]*4),
            '',
        )


    @classmethod
    def from_code(cls, code):
        resist = cls('-'*6)
        resist.code = code
        return resist



class Demon(db.Model, SerializerMixin):
    __tablename__ = 'demon'
    serialize_only = ('id', 'name', 'race', 'level', 'fusion_uses.id', 'fusion_recipes.id')
    serialize_rules = ()

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    name = Column(types.String, nullable=False)

    level = Column(types.SmallInteger, nullable=False)
    health = Column(types.SmallInteger, nullable=False)
    mana = Column(types.SmallInteger, nullable=False)
    strength = Column(types.SmallInteger, nullable=False)
    dexterity = Column(types.SmallInteger, nullable=False)
    magic = Column(types.SmallInteger, nullable=False)
    agility = Column(types.SmallInteger, nullable=False)
    luck = Column(types.SmallInteger, nullable=False)

    resists = Column(types.SmallInteger, nullable=False, default=0)
    race = Column(types.Enum(Race))

    skills = association_proxy('learn_skills', 'skill')

    fusion_uses = relationship('Fusion', secondary='ingredient', back_populates="ingredients")
    fusion_recipes = relationship('Fusion', back_populates='result')

    def __repr__(self):
        return f'Demon({self.name})'

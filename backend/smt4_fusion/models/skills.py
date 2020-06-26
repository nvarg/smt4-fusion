from enum import Enum
from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from ..flask_extensions import db
from .utils import dict_helper

class Damage(Enum):
    Weak = 'Weak'
    Medium = 'Medium'
    Heavy = 'Heavy'
    Severe = 'Severe'


class Target(Enum):
    All = 'All'
    Ally = 'Ally'
    Party = 'Party'
    Multi = 'Multi'
    Foes = 'Foes'
    Single = 'Single'
    Universal = 'Universal'


class Type(Enum):
    Support = 'Support'
    Fire = 'Fire'
    Passive = 'Passive'
    Recovery = 'Recovery'
    Almighty = 'Almighty'
    Physical = 'Physical'
    Special = 'Special'
    Gun = 'Gun'
    Ailment = 'Ailment'
    Ice = 'Ice'
    Electric = 'Electric'
    Force = 'Force'
    Dark = 'Dark'
    Light = 'Light'


class Skill(db.Model):
    __tablename__ = "skill"

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    name = Column(types.String, nullable=False)

    type = Column(types.Enum(Type), nullable=True)
    target = Column(types.Enum(Target), nullable=True)
    damage = Column(types.Enum(Damage), nullable=True)
    hits = Column(types.String(4), nullable=True)
    effect = Column(types.String(131), nullable=True)

    demons = association_proxy('learn_skills', 'demon')


    def __repr__(self):
        return f'Skill({self.name})'


    def __iter__(self):
        return dict_helper(self)


class LearnSkill(db.Model):
    __tablename__ = 'learn_skill'

    demon_id = Column(types.SmallInteger, ForeignKey('demon.id'), nullable=False, primary_key=True)
    skill_id = Column(types.SmallInteger, ForeignKey('skill.id'), nullable=False, primary_key=True)

    level = Column(types.SmallInteger, nullable=False)

    demon = relationship('Demon', backref=backref("learn_skills", cascade="all, delete-orphan"))
    skill = relationship('Skill', backref=backref("learn_skills", cascade="all, delete-orphan"))


    def __repr__(self):
        return f'LearnSkill({self.demon.name}, {self.skill.name}, {self.level})'


    def __iter__(self):
        return dict_helper(self)
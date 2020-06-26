from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy

from ..flask_extensions import db
from .demons import Demon
from .utils import dict_helper

class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    demon_id = Column(types.SmallInteger, ForeignKey('demon.id'), nullable=False, primary_key=True)
    fusion_id = Column(types.SmallInteger, ForeignKey('fusion.id'), nullable=False, primary_key=True)

    demon = relationship('Demon')
    fusion = relationship('Fusion')

@dataclass
class Fusion(db.Model):
    __tablename__ = 'fusion'

    id = Column(types.Integer, primary_key=True, autoincrement=True)


    result_id = Column(types.Integer, ForeignKey('demon.id'), nullable=False)

    ingredients = relationship('Demon', secondary=Ingredient.__table__, back_populates="fusion_uses")
    result = relationship('Demon', foreign_keys=[result_id], back_populates="fusion_recipes")

    def __repr__(self):
        return f'Fusion({" + ".join(ing.name for ing in self.ingredients)} = {self.result.name})'


    def __iter__(self):
        return dict_helper(self)

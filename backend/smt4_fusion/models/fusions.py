from dataclasses import dataclass
from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

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
class Fusion(db.Model, SerializerMixin):
    __tablename__ = 'fusion'
    serialize_only = ('ingredients.id', 'result.id', 'ingredients.name', 'result.name', 'ingredients.race', 'result.race')
    serialize_rules = ()

    id = Column(types.Integer, primary_key=True, autoincrement=True)


    result_id = Column(types.Integer, ForeignKey('demon.id'), nullable=False)

    ingredients = relationship('Demon', secondary=Ingredient.__table__, back_populates="fusion_uses")
    result = relationship('Demon', foreign_keys=[result_id], back_populates="fusion_recipes")

    def __repr__(self):
        return f'Fusion({" + ".join(ing.name for ing in self.ingredients)} = {self.result.name})'

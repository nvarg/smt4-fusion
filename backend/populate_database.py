#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json
import itertools
from math import ceil

from smt4_fusion.app import create_app
from smt4_fusion.models.demons import Demon, Race, Resist
from smt4_fusion.models.skills import Skill, LearnSkill, Damage, Target, Type
from smt4_fusion.models.fusions import Fusion, Ingredient
from smt4_fusion.flask_extensions import db
from smt4_fusion.utils.lists import right_pad


# In[ ]:


DATABASE_URI = None

if DATABASE_URI:
    os.environ['DATABASE_URI'] = DATABASE_URI


# In[ ]:


def yield_skills(skill_data_fp):
    
    damage_types = {
        'pas': 'Passive', 'phy': 'Physical', 'sup': 'Support',
        'alm': 'Almighty', 'gun': 'Gun', 'rec': 'Recovery',
        'ail': 'Ailment', 'ice': 'Ice', 'ele': 'Electric',
        'fir': 'Fire',  'for': 'Force', 'spe': 'Special',
        'dar': 'Dark', 'lig': 'Light'
    }
        
    for name, data in json.load(skill_data_fp).items():
        skill = Skill(
            id=None,
            name=name,
            type=Type(damage_types.get(data['element'])),
            damage=Damage(damage) if (damage := data.get('damage')) else None,
            target=Target(target) if (target := data.get('target')) else None,
            hits=data.get('hits'),
            effect=data.get('effect'),
        )
        
        yield skill


# In[ ]:


def yield_demons(demon_ids_fp, demon_data_fp, skills_list):

    demon_ids = {
        name.rstrip(): int(idx) for idx, name  in map(lambda l: l.split(','),
                                                      demon_ids_fp.readlines())
    }
    
    skills = { skill.name: skill for skill in skills_list }
    
    for name, data in json.load(demon_data_fp).items():
        stats = dict(zip(
            ['health', 'mana', 'strength', 'dexterity', 'magic', 'agility', 'luck'],
            data['stats'],
        ))
                
        demon = Demon(
            id=demon_ids.get(name),
            name=name,
            resists=Resist(data['resists']).code,
            race=Race(data['race']),
            level=data['lvl'],
            learn_skills=(learn_skills := []),
            **stats,
        )
        
        learn_skill = [
            LearnSkill(demon=demon, skill=skills[skill], level=level)
            for skill, level in data['skills'].items() 
        ]

        yield demon


# In[ ]:


def yield_fusions(fusion_chart_fp, db=db):
    
    fusion_chart = json.load(fusion_chart_fp)
    
    for race_one_name, fusions in fusion_chart.items():

        demons = db.session.query(Demon).filter(
            Demon.race == Race(race_one_name)
        )
        
        fusion_candidates = db.session.query(Demon).filter(
            Demon.race.in_(fusions.keys()),
            Demon.race != Race(race_one_name)
        )

        for demon in demons:
            for candidate in fusion_candidates:        
                result = db.session.query(Demon).filter(
                    Demon.race == fusions[candidate.race.name],
                    Demon.level >= ceil((demon.level + candidate.level) / 2),
                ).order_by(Demon.level.asc()).first()

                if result:
                    yield Fusion(ingredients=[demon, candidate], result=result)


# In[ ]:


def yield_special_fusions(special_fusions_fp, db=db):
    for result_name, ingredient_names in json.load(special_fusions_fp).items():
        result = db.session.query(Demon).filter(Demon.name == result_name).first()
        ingredients = db.session.query(Demon).filter(Demon.name.in_(ingredient_names)).all()
        yield Fusion(result=result, ingredients=ingredients)


# In[ ]:


def yield_elemental_fusions(db=db):
    fusions = {
        'Herald': 'Salamander', 'Megami': 'Undine', 'Avian': 'Sylph',
        'Tree': 'Gnome', 'Divine': 'Aeros', 'Flight': 'Aquans', 'Yoma':
        'Aeros', 'Nymph': 'Flaemis', 'Vile': 'Undine', 'Raptor': 'Aeros',
        'Wood': 'Erthys', 'Deity': 'Salamander', 'Avatar': 'Undine',
        'Holy': 'Sylph', 'Genma': 'Undine', 'Fairy': 'Aeros', 'Beast':
        'Erthys', 'Jirae': 'Erthys', 'Snake': 'Flaemis', 'Reaper':
        'Gnome', 'Wilder': 'Aquans', 'Jaki': 'Flaemis', 'Vermin':
        'Erthys', 'Fury': 'Sylph', 'Lady': 'Gnome', 'Dragon': 'Sylph',
        'Kishin': 'Gnome', 'Fallen': 'Flaemis', 'Brute': 'Aquans',
        'Femme': 'Aquans', 'Night': 'Erthys', 'Tyrant': 'Salamander',
        'Drake': 'Flaemis', 'Spirit': 'Aeros', 'Ghost': 'Aquans',
        'Kunitsu': 'Salamander'
    }
    
    for race_name, result_name in fusions.items():
        
        demons = db.session.query(Demon).filter(Demon.race == race_name).all()
        result = db.session.query(Demon).filter(Demon.name == result_name).one()
        
        for ingredients in itertools.combinations(demons, 2):
            yield Fusion(ingredients=list(ingredients), result=result)


# In[ ]:


def yield_upgrade_downgrade_fusions(db=db):
    fusions = {
        'Herald': ([250], [251]), 'Megami': ([251], [250]), 'Avian': ([252], [253]),
        'Tree': ([253], [252]), 'Divine': ([257, 255], [256, 254]),
        'Flight': ([256, 254], [257, 255]), 'Yoma': ([256, 255], [257, 254]),
        'Nymph': ([256, 255], [257, 254]), 'Vile': ([251], [250]), 'Raptor': ([256, 254], [257, 255]),
        'Wood': ([257, 255], [256, 254]), 'Deity': ([250], [251]), 'Avatar': ([251], [250]),
        'Holy': ([252], [253]), 'Genma': ([251], [250]), 'Fairy': ([256, 255], [257, 254]),
        'Beast': ([257, 254], [256, 255]), 'Jirae': ([257, 254], [256, 255]), 'Snake': ([256, 254], [257, 255]),
        'Reaper': ([253], [252]), 'Wilder': ([255, 254], [257, 256]), 'Jaki': ([257, 254], [256, 255]),
        'Vermin': ([257, 255], [256, 254]), 'Fury': ([252], [253]), 'Lady': ([253], [252]),
        'Dragon': ([252], [253]), 'Kishin': ([253], [252]), 'Fallen': ([255, 254], [257, 256]),
        'Brute': ([257, 256], [255, 254]), 'Femme': ([257, 254], [256, 255]), 'Night': ([256, 255], [257, 254]),
        'Tyrant': ([250], [251]), 'Drake': ([257, 254], [256, 255]),
        'Spirit': ([256, 255], [257, 254]), 'Foul': ([257, 256], [255, 254]),
        'Ghost': ([257, 254], [256, 255]), 'Fiend': ([250], [251]),
    }
    
    for race_name, (upgrade_elemental_ids, downgrade_elemental_ids) in fusions.items():
        
        ingredients = db.session.query(Demon).filter(Demon.race == race_name).order_by(Demon.level.asc()).all()
        upgrade_elementals = [db.session.query(Demon).get(idx) for idx in upgrade_elemental_ids]
        downgrade_elementals = [db.session.query(Demon).get(idx) for idx in downgrade_elemental_ids]
        
        
        for idx in range(len(ingredients) - 1):
            downgrade, ingredient, upgrade = right_pad(ingredients[idx:idx + 3], 3)
            
            if upgrade:
                for elemental in upgrade_elementals:
                    yield Fusion(ingredients=[ingredient, elemental], result=upgrade)
            
            for elemental in downgrade_elementals:
                yield Fusion(ingredients=[ingredient, elemental], result=downgrade)


# In[ ]:


app = create_app()
db.create_all()

with open('data/skill-data.json', mode='r') as skill_data_fp:
    skills = list(yield_skills(skill_data_fp))
    
with open('data/demon-ids.csv', mode='r') as demon_ids_fp:
    with open('data/demon-data.json', mode='r') as demon_data_fp:
        demons = list(yield_demons(demon_ids_fp, demon_data_fp, skills))

db.session.add_all(skills + demons)
db.session.commit()
        
with open('data/fusion-chart.json', mode='r') as fusion_chart_fp:
    fusions = list(yield_fusions(fusion_chart_fp))

with open('data/special-fusions.json', mode='r') as special_fusions_fp:
    fusions += list(yield_special_fusions(special_fusions_fp))

fusions += list(yield_elemental_fusions())
fusions += list(yield_upgrade_downgrade_fusions())

db.session.add_all(fusions)
db.session.commit()


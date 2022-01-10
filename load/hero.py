from sqlalchemy import Column, String, Integer, Float
from base import Base


class HeroVillian(Base):
    __tablename__ = 'heroes_villians'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    intelligence = Column(Float)
    strength = Column(Float)
    speed = Column(Float)
    durability = Column(Float)
    power = Column(Float)
    combat = Column(Float)
    publisher = Column(String(20))
    alignment = Column(String(10))
    gender = Column(String(10))
    height = Column(Float(precision=10, asdecimal=True))
    weight = Column(Float)
    gender = Column(String(10))

    def __init__(self, id, name, intelligence, strength, speed, durability, power, combat, publisher, alignment, gender, height, weight, image):
        self.id = id
        self.name = name
        self.intelligence = intelligence
        self.strength = strength
        self.speed = speed
        self.durability = durability
        self.power = power
        self.combat = combat
        self.publisher = publisher
        self.alignment = alignment
        self.gender = gender
        self.height = height
        self.weight = weight
        self.image = image

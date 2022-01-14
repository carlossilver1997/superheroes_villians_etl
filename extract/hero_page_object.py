import os
import requests
import json
import pandas as pd
from common import config
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

class Hero():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        

class HeroDetail(Hero):
    def __init__(self, id, name, intelligence, strength, speed, durability, power, combat, publisher, alignment, gender, height, weight, image):
        super().__init__(id, name)
        self.intelligence = intelligence
        self.strength = strength
        self.speed = speed
        self.durability = durability
        self.power = power
        self.combat = combat
        self.publisher = publisher
        self.alignment = alignment
        self.gender = gender
        self.height = self.__get_weight_or_hight(height)
        self.weight = self.__get_weight_or_hight(weight)
        self.image = image

    def __get_weight_or_hight(self, list_values):
        if len(list_values) == 0:
            return None
        if len(list_values) == 1:
            return list_values[0]
        return list_values[1]

class BasePage():
    def __init__(self): 
        self._response = None 
        self._url = config()['super_hero_site']['url'] 

    def _visit(self, url):
        headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43' }
        response = requests.get(url, headers=headers)

        response.raise_for_status()

        self._response = response.text

class HeroPage(BasePage):
    def __init__(self):
        super().__init__()
        self._visit("{}/ids.html".format(self._url))


    @property
    def heroes(self):
        heroes_list = list()
        for df in pd.read_html(self._response):
            for index, row in df.iterrows():
                heroes_list.append(Hero(row["#ID"], row['Chracter Name']))
        return heroes_list


    
            
class HeroDetailPage(BasePage):
    def __init__(self, id):
        super().__init__()
        self._visit("{}/api/{}/{}".format(self._url, ACCESS_TOKEN, id))
    

    @property
    def hero_detail(self):
        _response_to_json = json.loads(self._response)
        return HeroDetail(
            _response_to_json['id'],
            _response_to_json['name'],
            _response_to_json['powerstats']['intelligence'],
            _response_to_json['powerstats']['strength'],
            _response_to_json['powerstats']['speed'],
            _response_to_json['powerstats']['durability'],
            _response_to_json['powerstats']['power'],
            _response_to_json['powerstats']['combat'],
            _response_to_json['biography']['publisher'],
            _response_to_json['biography']['alignment'],
            _response_to_json['appearance']['gender'],
            _response_to_json['appearance']['height'],
            _response_to_json['appearance']['weight'],
            _response_to_json['image']['url'],
        )

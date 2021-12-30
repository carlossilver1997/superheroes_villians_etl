import csv
import datetime
import logging
import hero_page_object as hero

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _save_hero(superheros):
    now = datetime.datetime.now().strftime('%Y_%m_%d')
    out_file_name = 'heroes_{datetime}_articles.csv'.format(datetime=now)
    csv_headers = list(filter(lambda property: not property.startswith('_'), dir(superheros[0])))
    with open(out_file_name, mode='w+') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers)
        for superhero in superheros:
            row = [str(getattr(superhero, prop)) for prop in csv_headers]
            writer.writerow(row)


            

def _fetch_detail_hero(hero_name, id):
    logger.info('Fetching details for {name} with id: {uid}'.format(name=hero_name, uid=id))
    detail = hero.HeroDetailPage(id)
    return detail.hero_detail

def _new_scraper():
    logger.info('Beginning scraper for marvel vs dc heroes')
    super_heroes = []
    heroPage = hero.HeroPage()
    for hero_obj in heroPage.heroes:
        logger.info('Superhero detail fetched!!')
        super_hero = _fetch_detail_hero(hero_obj.name, hero_obj.id)
        super_heroes.append(super_hero)
    _save_hero(super_heroes)

if __name__ == '__main__':
    _new_scraper()
    
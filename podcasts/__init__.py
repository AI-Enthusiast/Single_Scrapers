from podscripts_scraper import get_podcasts
from parrallel import scraper

def podcast_update():
    pod_list = get_podcasts()
    scraper(pod_list)
    print("Podcasts updated.")
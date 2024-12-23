from .podscripts_scraper import get_podcasts
from .parrallel import scraper

def podcast_update(podcasts_path, test_run):
    pod_list, driver = get_podcasts(podcasts_path, test_run) # todo fix pathing bug
    scraper(pod_list, driver)
    print("Podcasts updated.")
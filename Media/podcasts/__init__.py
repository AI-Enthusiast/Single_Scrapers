from .podscripts_scraper import get_podcasts
from .parrallel import scraper

def podcast_update(podcasts_path, test_run):
    pod_list = get_podcasts(podcasts_path, test_run)
    scraper(pod_list)
    print("Podcasts updated.")
import requests
import pandas as pd
from bs4 import BeautifulSoup

popular = 'https://www.imdb.com/chart/moviemeter/'

raw = requests.get(popular, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(raw.text, 'html.parser')

# <div class="ipc-metadata-list-summary-item__tc"><span class="ipc-metadata-list-summary-item__t" aria-disabled="false"></span><div class="sc-300a8231-0 gTnHyA cli-children"><div aria-label="Ranking 1" class="sc-b8b74125-0 ilwIpP meter-const-ranking sc-300a8231-5 fUPvGq cli-meter-title-header">1<!-- --> (<span aria-label="Moved up 76 in ranking" class="sc-7cc0a248-0 dzkBQg"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" class="ipc-icon ipc-icon--arrow-drop-up ipc-icon--inline sc-db6887cf-0 cvZFCZ base up" viewBox="0 0 24 24" fill="currentColor" role="presentation"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M8.71 12.29L11.3 9.7a.996.996 0 0 1 1.41 0l2.59 2.59c.63.63.18 1.71-.71 1.71H9.41c-.89 0-1.33-1.08-.7-1.71z"></path></svg>76</span>)</div><div class="ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-a69a4297-2 bqNXEn cli-title with-margin"><a href="/title/tt10548174/?ref_=chtmvm_t_1" class="ipc-title-link-wrapper" tabindex="0"><h3 class="ipc-title__text">28 Years Later</h3></a></div><div class="sc-300a8231-6 dBUjvq cli-title-metadata"><span class="sc-300a8231-7 eaXxft cli-title-metadata-item">2025</span></div><span class="sc-300a8231-1 kWSYcu"><div class="sc-e2dbc1a3-0 jeHPdh sc-300a8231-3 koIPa cli-ratings-container" data-testid="ratingGroup--container"><span aria-label="This title is currently not ratable" class="ipc-rating-star ipc-rating-star--base ipc-rating-star--placeholder ratingGroup--placeholder standalone-star" data-testid="ratingGroup--placeholder"><svg width="24" height="24" xmlns="http://www.w3.org/2000/svg" class="ipc-icon ipc-icon--star-inline" viewBox="0 0 24 24" fill="currentColor" role="presentation"><path d="M12 20.1l5.82 3.682c1.066.675 2.37-.322 2.09-1.584l-1.543-6.926 5.146-4.667c.94-.85.435-2.465-.799-2.567l-6.773-.602L13.29.89a1.38 1.38 0 0 0-2.581 0l-2.65 6.53-6.774.602C.052 8.126-.453 9.74.486 10.59l5.147 4.666-1.542 6.926c-.28 1.262 1.023 2.26 2.09 1.585L12 20.099z"></path></svg></span></div></span></div></div>
movies = soup.find_all('div', class_='ipc-metadata-list-summary-item__tc')
# <h3 class="ipc-title__text">28 Years Later</h3>
movie_names = []
for movie in movies:
    movie_names.append(movie.find('h3', class_='ipc-title__text').text)

print(movie_names)
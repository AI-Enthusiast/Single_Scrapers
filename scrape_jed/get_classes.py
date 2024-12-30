import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# change dir to /classes/
os.chdir("classes")

url_prefix = "https://jrembold.github.io"
url_suffix = "/Website_Backup/classes/"
url = url_prefix + url_suffix

raw = requests.get(url)
soup = BeautifulSoup(raw.content, "html.parser")

# get all the classes
classes = soup.find_all("div", class_="6u -3u 12u$(small) 12u$(xsmall)")
class_names = [c.find("h3").text for c in classes]
class_links = [c.find("a")["href"] for c in classes]
# remove the second to last slash from each link
class_links = [c[:c.rfind("/")] for c in class_links]
class_links = [c[:c.rfind("/")] for c in class_links]

print(class_links)
print(f'Found {len(class_names)} classes')
# get each class url
for i in range(len(class_links)):
    class_url = url_prefix + class_links[i] + '/slides/'
    print(f"Getting slides for {class_names[i]}")
    print(class_url)
    # get al the slide links for each class
    raw_class = requests.get(class_url)
    print(f"Got response {raw_class.status_code}")
    soup_class = BeautifulSoup(raw_class.content, "html.parser")

    # get the slide links, the tile, date, and video link
    slides = soup_class.find_all("tr")[1:]
    slide_links = [s.find("a")["href"] for s in slides]
    # /Website_Backup/class_files/data351/Slides/slides/Ch9.html
    slide_links = [url_prefix + s for s in slide_links]
    slide_titles = [s.find("a").text for s in slides]
    slide_dates = [s.find_all("td")[1].text for s in slides]
    try:
        slide_videos = [s.find("div")["ytsrc"] for s in slides]
    except:
        slide_videos = ["" for s in slides]
    # add https://www.youtube.com/watch?v= to the video links
    slide_videos = [f"https://www.youtube.com/watch?v={v}" if v else "" for v in slide_videos]

    df = pd.DataFrame({
        "title": slide_titles,
        "date": slide_dates,
        "video": slide_videos,
        "link": slide_links
    })

    # check if a dir with the class name exists, if not create it
    if not os.path.exists(class_names[i].replace(' ', '_')):
        os.makedirs(class_names[i].replace(' ', '_'))
    # change dir
    os.chdir(class_names[i].replace(' ', '_'))

    df.to_csv(f"{class_names[i].replace(' ', '_')}.csv", index=False)


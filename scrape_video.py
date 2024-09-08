import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen, Request

def main():
    print("STEP 1: Open Chrome browser")
    driver = webdriver.Chrome()
    driver.get("https://www.tiktok.com/@football_world_01_?_t=8pMSDghcYwN&_r=1")

    # Wait for user to solve reCAPTCHA
    input("Please solve the reCAPTCHA and then press Enter to continue...")

    time.sleep(1)

    scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
    i = 1

    print("STEP 2: Scrolling page")
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    videos = soup.find_all("div", {"class": "css-1uqux2o-DivItemContainerV2"})

    print(f"STEP 3: Time to download {len(videos)} videos")
    for index, video in enumerate(videos):
        download_video(video.a["href"], index)
        time.sleep(10)  # Adding sleep to avoid being blocked

def download_video(link, id):
    print(f"Downloading video {id} from: {link}")
    
    # Ensure the directory exists
    if not os.path.exists("football_world"):
        os.makedirs("football_world")

    cookies = {
        '_ga_DWYR5ZNKYQ': 'GS1.1.1720711907.1.0.1720711907.60.0.0',
        '_ga': 'GA1.1.1721070918.1720711908',
        'fpestid': 'SlHP5-jSMV4R3NfbFWRWlYI51aJxuDvYAMFnDJZdbryZyqEix3kDo35aSCx325hNsiTjFw',
        '_cc_id': '9894861498e11a0f2ba3abdd03199a55',
        'panoramaId_expiry': '1720798309682',
        '__gads': 'ID=bc5ba37c12261aa2:T=1720711909:RT=1720711909:S=ALNI_MaLPrkyFnIXCI2l5hkpieUbT4KPbQ',
        '__gpi': 'UID=00000e79903db94a:T=1720711909:RT=1720711909:S=ALNI_MaDj4Ait-k1znzxbB9He0wLgFCOxg',
        '__eoi': 'ID=a47a50d588e81ee7:T=1720711909:RT=1720711909:S=AA-AfjbPTOmVyv_yfOyXNxiS3C36',
        'FCNEC': '%5B%5B%22AKsRol9J58VDoXrnmC7gjK-d6Q3LEn6xq_HjdGVpMgWGCVVG4Tl0kCe-V_Lxg5gm8PUqg9yUXh2hIgf4Yn5XptlemUSSXloMNenk4IwnHh_Zx_TgTTcV-BD_G24Kyn9wae_Rzzw3d-LOa83LLllfD-VfiOODTjvg-w%3D%3D%22%5D%5D',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'hx-current-url': 'https://tiktokio.com/',
        'hx-request': 'true',
        'hx-target': 'tiktok-parse-result',
        'hx-trigger': 'search-btn',
        'origin': 'https://tiktokio.com',
        'priority': 'u=1, i',
        'referer': 'https://tiktokio.com/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    data = {
        'prefix': 'dtGslxrcdcG9raW8uY29t',
        'vid': link,
    }

    response = requests.post('https://tiktokio.com/api/v1/tk-htmx', cookies=cookies, headers=headers, data=data)
    download_soup = BeautifulSoup(response.text, "html.parser")
    
    download_link = download_soup.a["href"]

    print("STEP 5: Saving the video :)")
    request = Request(download_link, headers=headers)
    mp4_file = urlopen(request)
    with open(f"videos/{id}.mp4", "wb") as output:
        while True:
            data = mp4_file.read(4096)
            if data:
                output.write(data)
            else:
                break

if __name__ == "__main__":
    main()

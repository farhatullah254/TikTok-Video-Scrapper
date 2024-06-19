from selenium import webdriver
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

def downloadVideo(link, id):
    cookies = {
        '_ga': 'GA1.1.215585002.1718159802',
        '__gads': 'ID=77aab3245bfcb6ee:T=1718159802:RT=1718159802:S=ALNI_MZ3ASMe7SgQp5jlETp_QC0LGljEug',
        '__gpi': 'UID=00000e58286c3517:T=1718159802:RT=1718159802:S=ALNI_MZXbC5jyoBAV0FVSzXjaKRBEhLw_A',
        '__eoi': 'ID=4aa2bfa5d4131212:T=1718159802:RT=1718159802:S=AA-AfjZed3VeCKjdFLDoXNgIKZOf',
        'FCNEC': '%5B%5B%22AKsRol_64Jde-vp-U1-c82pJWkr_mHilmoD_6glZVP6UCR-GvAU90sQvCIejTvUJbaXH43NcwO_osBntNkCrhR2HTDKdfziaY6ip6vnEOtrvpxYkGFOwL2lIsYmG94u42Mxrj57vqoS5zivusBJu00OdzB2vj63w8A%3D%3D%22%5D%5D',
        '_ga_ZSF3D6YSLC': 'GS1.1.1718159801.1.1.1718159828.0.0.0',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'priority': 'u=1, i',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'blhkb2Vi',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    
    # Check if response is valid and parse the download link
    if response.status_code == 200:
        downloadSoup = BeautifulSoup(response.text, "html.parser")
        try:
            downloadLink = downloadSoup.find("a")["href"]
            if not downloadLink.startswith("http"):
                raise ValueError("Invalid URL")
        except (AttributeError, KeyError, ValueError) as e:
            print(f"Error extracting download link: {e}")
            return
    else:
        print(f"Error in response: {response.status_code}")
        return

    # Download the video
    mp4file = urlopen(downloadLink)
    with open(f"documents/{id}.mp4", "wb") as output:
        while True:
            data = mp4file.read(4096)
            if data:
                output.write(data)
            else:
                break

# Set up Chrome options for incognito mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

# Initialize the Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options)
driver.get("tiktok account url")

# Pause the script to allow manual completion of the reCAPTCHA
print("Please solve the reCAPTCHA manually, then press Enter to continue...")
input()

# Proceed with the scrolling and data extraction
scroll_pause_time = 10  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 3
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
#Go to inspect Element and Find account HTML Class ID and replace with "html id"
videos = soup.find_all("div", {"class": "html id"})

print(len(videos))
for index, video in enumerate(videos):
    downloadVideo(video.a["href"], index)
    time.sleep(5)

driver.quit()

"""
Adapted shamelessly from:
https://medium.com/@moungpeter/how-to-automate-downloading-files-using-python-selenium-and-headless-chrome-9014f0cdd196
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


CHROME_EXECUTABLE_PATH = "/Users/william.mcmonagle/Downloads/chromedriver"
# treated as a relative path from this directory
DOWNLOADS_DIRECTORY = "Downloads"

# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)

# instantiate a chrome options object so you can set the size and headless preference
# some of these chrome options might be uncessary but I just used a boilerplate
# change the <path_to_download_default_directory> to whatever your default download folder is located
chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--verbose')
chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOADS_DIRECTORY,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
})
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-software-rasterizer')

# initialize driver object and change the <path_to_chrome_driver> depending on your directory where your chromedriver should be
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROME_EXECUTABLE_PATH)

# function to handle setting up headless download
enable_download_headless(driver, DOWNLOADS_DIRECTORY)

# Hard coding specific page for proof-of-concept purposes
url = "https://www.curseforge.com/minecraft/mc-mods/dank-null/files/all/?filter-game-version=2020709689%3A6756"

# get request to target the site selenium is active on
driver.get(url)
# grab all <a href blah blah> tags
elements = driver.find_elements_by_tag_name("a")
for element in elements:
    # get the actual URL pointed to by the link
    href = element.get_attribute("href")
    # This prefix works for this mod specifically, but I'm guessing the pattern is fairly predictable.
    # Where the link exists, adding /file to the end of it bypasses the "wait for download" screen.
    if href and href.startswith("https://www.curseforge.com/minecraft/mc-mods/dank-null/download/"):
        print("getting ", href)
        driver.get(f"{href}/file")

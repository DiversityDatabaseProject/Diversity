from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
import supplement as sp
import os
import time


if __name__ == "__main__":
    opts = Options()
    opts.add_argument("--disable-notifications")
    opts.add_argument('--no-sandbox')
    opts.add_argument('--verbose')
    opts.add_experimental_option("prefs", {
        "download.default_directory": "C:\\tmp",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    opts.add_argument('--disable-gpu')
    opts.add_argument("--window-size=400x300")
    opts.add_argument('--disable-software-rasterizer')

    scroll = int(input('Enter scroll times: '))
    if len(str(scroll)) < 1:
        scroll = 0
    while True:
        choice = int(input('1. Search\n2. Collections\nEnter your choice: '))
        if choice == 1:
            query = input('Enter your search: ')
            result_folder = "./images-" + query + \
                "/" if len(query) > 1 else "./images/"
            img_url = sp.extract_userinput(query)
            prefs = {"download.default_directory": os.getcwd() + result_folder}
            opts.add_experimental_option("prefs", prefs)
            browser = Chrome(options=opts)
            sp.extract_and_save_imgs(browser, img_url, scroll, result_folder)
            break
        elif choice == 2:
            browser = Chrome(options=opts)
            name, href = sp.extract_href_and_name(browser, scroll)
            for i in range(1, len(name)):
                print('%d. %s' % (i, name[i-1]))
            while True:
                collections_choice = int(
                    input('Enter your collections choice: '))
                if collections_choice >= 1 and collections_choice <= len(name):
                    result_folder = "./images-" + name[collections_choice - 1] + \
                        "/" if len(name[collections_choice - 1]
                                   ) > 1 else "./images/"
                    browser.quit()
                    prefs = {"download.default_directory": os.getcwd() +
                             result_folder}
                    opts.add_experimental_option("prefs", prefs)
                    browser = Chrome(options=opts)
                    sp.extract_and_save_imgs(
                        browser, href[collections_choice - 1], scroll, result_folder)
                    want_continue = input('Want more?(Y/n): ')
                    if want_continue.lower() == 'y':
                        continue
                    else:
                        break
                else:
                    print('Incorrect choice. Please try again!')
            break
        else:
            print('Incorrect choice. Please try again')

    close_now = input('You want to close your browser?: ')
    if close_now.lower() == 'y':
        browser.quit()

import os
import shutil

import uc_browser.undetected_chromedriver as uc
from selenium import webdriver

from .utils import *


def get_webdriver(
        use_profile: bool = False,
        profile_path: str = None,
        download_path: str = None,
        use_headless: bool = False,
        version_main: int = None,
        proxy: dict = None
) -> webdriver:
    options = uc.ChromeOptions()

    if use_profile and profile_path is not None:
        if not os.path.exists(profile_path):
            os.makedirs(profile_path)
        options.add_argument(f'--user-data-dir={profile_path}')

    if download_path:
        options.add_experimental_option("prefs", {'download.default_directory': download_path})

    proxy_extension_dir = None
    if proxy and all(key in proxy for key in ['url', 'username', 'password']):
        proxy_extension_dir = create_proxy_extension(proxy)
        options.add_argument(
            f"--load-extension={os.path.abspath(proxy_extension_dir)}"
        )
    elif proxy and 'url' in proxy:
        proxy_url = proxy['url']
        options.add_argument(f'--proxy-server={proxy_url}')

    # just some options passing in to skip annoying popups
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    # todo: this param shows a warning in chrome head-full
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # this option removes the zygote sandbox (it seems that the resolution is a bit faster)
    options.add_argument('--no-zygote')
    # attempt to fix Docker ARM32 build
    options.add_argument('--disable-gpu-sandbox')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.headless = use_headless

    if use_headless:
        start_xvfb_display()

    if proxy_extension_dir is not None:
        shutil.rmtree(proxy_extension_dir)

    return uc.Chrome(options=options, version_main=version_main, headless=use_headless, windows_headless=use_headless,
                     use_subprocess=False)

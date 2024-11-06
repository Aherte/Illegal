import time

zbahis_link = 'https://51zlot.com/tr-tr/prelive/forty_eight_hours/soccer'
zbahis_popup_xpath = "/html/body/div[4]/div[2]/div[2]"
superlig_xpath = "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div[2]/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a"

import common

zbahis_driver = common.driver_init()

try:
    common.login_site(zbahis_driver, zbahis_link)

    common.close_popup(zbahis_driver, zbahis_popup_xpath)

    common.select_superlig(zbahis_driver, superlig_xpath)

finally:
    common.close_driver(zbahis_driver)


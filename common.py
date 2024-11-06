import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver_init(headless=False, width=1340, height=800):
    options = uc.ChromeOptions()
    options.headless = headless
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)
    driver.set_window_size(width, height)
    return driver

def login_site(driver, url):
    try:
        driver.get(url)
        print(f"{url} adresine giriş yapıldı.")
    except Exception as e:
        print(f"Siteye giriş yapılamadı. Hata: {e}")

def close_popup(driver, popup_xpath, timeout=5):
    try:
        popup_close_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, popup_xpath))
        )
        popup_close_button.click()
        print("Pop-up kapatıldı.")
    except Exception as e:
        print(f"Pop-up kapatılamadı veya zaten kapalı. Hata: {e}")

def select_superlig(driver, superlig_xpath, timeout=10):
    try:
        superlig_element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, superlig_xpath))
        )
        superlig_element.click()
        print("Türkiye Süperlig kısmına tıklandı.")
    except Exception as e:
        print(f"Türkiye Süperlig kısmına tıklanamadı. Hata: {e}")

def switch_to_iframe(driver, iframe_tag='iframe', timeout=5):
    try:
        iframe = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, iframe_tag))
        )
        driver.switch_to.frame(iframe)
        print("IFrame'e geçiş başarılı.")
    except Exception as e:
        print(f"IFrame bulunamadı. Hata: {e}")

def close_driver(driver):
    try:
        driver.close()
        print("Tarayıcı kapatıldı.")
    except Exception as e:
        print(f"Tarayıcı kapatma sırasında hata: {e}")



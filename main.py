import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_grandpasha_and_collect_data(link):
    options = uc.ChromeOptions()
    options.headless = False  # Tarayıcıyı başsız modda başlatmayın
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=options)

    # Tarayıcı penceresi boyutunu sabitle
    driver.set_window_size(1340, 720)

    grandpasha = []

    try:
        driver.get(link)
        print("Siteye giriş başarılı.")

        # Yeni pop-up kapatma
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[4]/div/div/div"))
            )
            close_button.click()
            print("Pop-up kapatıldı.")
        except Exception as e:
            print(f"Pop-up kapatılamadı veya zaten kapalı. Hata: {e}")

        # IFrame geçişi
        try:
            iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            print("IFrame'e geçiş başarılı.")
        except Exception as e:
            print(f"IFrame bulunamadı. Hata: {e}")

        # Süper Lig'e tıklama
        try:
            turkiye_super_lig = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div[3]/div[1]/div[2]/ul/li[1]'))
            )
            turkiye_super_lig.click()
            print("Türkiye Süper Lig seçildi.")
        except Exception as e:
            print(f"Süper Lig seçeneği bulunamadı veya zaten seçili. Hata: {e}")

        # Maç başlıklarını bulma ve her maça tıklama
        try:
            match_headers = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH,
                                                     "//div[@class='tab_body_active']//div[contains(@class, 'tg__match_header')]"))
            )
            print("Maç başlıkları bulundu.")

            match_ids = [header.get_attribute('id') for header in match_headers]
            match_names = [
                f"{header.find_elements(By.XPATH, './/div[@class=\"en prematch_name tg--oe\"]')[0].get_attribute('title')} vs " +
                f"{header.find_elements(By.XPATH, './/div[@class=\"en prematch_name tg--oe\"]')[1].get_attribute('title')}"
                for header in match_headers if header.get_attribute('id')
            ]

            print(f"Bulunan toplam maç sayısı: {len(match_ids)}")

            # Her maç için işlemleri hızlı yapma
            for idx, match_id in enumerate(match_ids):
                try:
                    # Maça tıklama
                    WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, match_id))
                    ).click()
                    print(f"{match_names[idx]} maçı seçildi ve tıklandı.")
                    time.sleep(1)
                    match_data = {"match_name": match_names[idx], "1X": None, "2X": None}

                    for value_name, xpath in [("1X",
                                               "/html/body/div[1]/div[5]/div[2]/div/div[2]/div[5]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/a[1]/div"),
                                              ("2X",
                                               "/html/body/div[1]/div[5]/div[2]/div/div[2]/div[5]/div/div/div/div[3]/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/a[3]/div")]:
                        found = False
                        for attempt in range(3):
                            try:
                                element = WebDriverWait(driver, 3).until(
                                    EC.presence_of_element_located((By.XPATH, xpath))
                                )
                                value = element.text.strip()
                                match_data[value_name] = value
                                print(f"{match_names[idx]} {value_name}: {value}")
                                found = True
                                break
                            except:
                                time.sleep(1)
                        if not found:
                            print(f"{match_names[idx]} için {value_name} değeri bulunamadı.")

                    grandpasha.append(match_data)

                    driver.back()
                    time.sleep(1)
                    driver.switch_to.frame(iframe)

                except Exception as e:
                    print(f"{match_names[idx]} maçı için işlem yapılamadı. Hata: {e}")

        except Exception as e:
            print(f"Maçlar veya ID'ler bulunamadı. Hata: {e}")

    except Exception as e:
        print(f"Genel hata: {e}")

    finally:
        print("\nGrandpasha Sonuçları:")
        for match in grandpasha:
            print(match)
        print("\nSon.")
        driver.quit()

# Örnek kullanım
grandpasha_link = 'https://grandpashabet2189.com/Sport'
open_grandpasha_and_collect_data(grandpasha_link)

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import time
import os

options = uc.ChromeOptions()
profile_directory = "Profile"
if not os.path.exists(profile_directory):
    os.makedirs(profile_directory)
options.user_data_dir = profile_directory

driver = uc.Chrome(options=options)
driver.get("https://diemthi.tuyensinh247.com/nganh-dao-tao.html#undefined")

driver.maximize_window()

if input() == "ok":
    wait = WebDriverWait(driver, 10)

    groups = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@role="tablist"]/div')))
    data = []

    for group in groups:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", group)
        time.sleep(2)

        ActionChains(driver).move_to_element(group).click().perform()
        time.sleep(1)

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ant-collapse-content")))
        time.sleep(1)

        group_name = group.find_element(By.TAG_NAME, "p").text.strip()

        expanded_content = group.find_element(By.XPATH, './/div[contains(@class, "ant-collapse-content")]')
        major_elements = expanded_content.find_elements(By.TAG_NAME, "a")

        for major in major_elements:
            major_name = major.text.strip()
            school_name_data = []

            major_link = major.get_attribute("href")
            driver.execute_script("window.open(arguments[0], '_blank');", major_link)

            WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])

            try:
                try:
                    see_more_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'viewmore')]"))
                    )
                    driver.execute_script("arguments[0].click();", see_more_button)
                    time.sleep(2)
                except Exception:
                    pass

                schools = driver.find_elements(By.XPATH, "//div[contains(@class, 'ant-table-container')]//tbody[contains(@class, 'ant-table-tbody')]/tr")

                for school in schools:
                    cols = school.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 2:
                        school_name = cols[1].text.strip()

                        school_link = cols[4].find_element(By.TAG_NAME, "a").get_attribute("href")
                        driver.execute_script("window.open(arguments[0], '_blank');", school_link)

                        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 2)
                        driver.switch_to.window(driver.window_handles[-1])

                        try:
                            diem_thi_thpt_table = driver.find_element(By.ID, "diem-thi-thpt")
                            rows = diem_thi_thpt_table.find_elements(By.XPATH, ".//tbody[contains(@class, 'ant-table-tbody')]/tr")
                            for row in rows:
                                cols = row.find_elements(By.TAG_NAME, "td")
                                if len(cols) >= 5:
                                    ma_nganh = cols[1].text.strip()
                                    ten_nganh = cols[2].text.strip()
                                    to_hop_mon = cols[3].text.strip()
                                    diem_chuan = cols[4].text.strip()
                                    ghi_chu = cols[5].text.strip()

                                    data.append({
                                        "Nhóm ngành": group_name,
                                        "Ngành": major_name,
                                        "Trường đào tạo": school_name,
                                        "Mã ngành": ma_nganh,
                                        "Tên ngành": ten_nganh,
                                        "Tổ hợp môn": to_hop_mon,
                                        "Điểm chuẩn 2024": diem_chuan,
                                        "Ghi chú": ghi_chu
                                    })
                        except Exception:
                            pass
                        finally:
                            driver.close()
                            driver.switch_to.window(driver.window_handles[-1])

                        data.append({"Nhóm ngành": group_name, "Ngành": major_name, "Trường đào tạo": school_name})
            except Exception as e:
                pass
            finally:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=["Mã ngành"], keep="first")
    df.to_csv("nganh_dao_tao.csv", index=False, encoding="utf-8-sig")

    driver.quit()

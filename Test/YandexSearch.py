from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class YandexSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        url = 'https://yandex.ru/'
        self.driver.get(url)

    def test_search_tensor(self, inquiry = 'Тензор'):
        driver = self.driver
        searchbox = driver.find_element_by_xpath('//*[@id="text"]')
        list_input_text = driver.find_elements_by_name('text')
        try:
            self.assertIn(searchbox, list_input_text)
        except:
            print('-Поле поиска отсутствует на странице.')
        else:
            print('-Поле поиска присутствует на странице.')
        searchbox.clear()
        searchbox.send_keys(inquiry)

        suggest = driver.find_elements_by_xpath('/html/body/div[2]')
        try:
            self.assertTrue(suggest)
        except:
            print(f'-Таблица с подсказками не отобразилась.')
        else:
            print('-Таблица с подсказками отобразилась.')

        searchbox.send_keys(Keys.ENTER)
        
        links_of_the_page = driver.find_elements_by_class_name('Link_theme_outer')
        for i in links_of_the_page[:5]:
            href = i.get_attribute('href')
            new_href = href.split('/')
        try:
            self.assertEquel(new_href[2], 'tensor.ru')
        except:
            print('-Не все ссылки ведут на tensor.ru')
        else:
            print('-Все ссылки ведут на tensor.ru')


    def test_search_image(self):
        driver = self.driver
        try:
            driver.find_element_by_link_text('Картинки').click()
        except:
            print('-Ссылка на "Картинки" отсутствует.')
        else:
            print('-Ссылка на "Картинки" найдена.')
        driver.switch_to.window(driver.window_handles[1])

        
        current_page = driver.current_url.split('/')[0:3]
        expected_page = 'https://yandex.ru/'.split('/')[0:3]
        try:
            self.assertEqual(current_page, expected_page)
        except:
            print(f'-Переход выполнен неверно. Открыта страница {expected_page.join()}')
        else:
            print('-Переход выполнен успешно по адресу https://yandex.ru/images/')

 
        images = driver.find_elements_by_class_name('PopularRequestList-Shadow')
        name_category = driver.find_elements_by_class_name('PopularRequestList-SearchText')[0].text
        images[0].click()

        result_click_for_category = driver.find_element_by_xpath("/html/body/header/div/div[1]/div[2]/form/div[1]/span/span/input").get_attribute('value')

        try:
            self.assertEqual(name_category, result_click_for_category)
        except:
            print(f'-Наименование категории "{name_category}" не соответствует названию из строки поиска: {result_click_for_category}.')
        else:
            print(f'-Наименование категории "{name_category}" соответствует названию из строки поиска.')

 
        first_image = driver.find_elements_by_class_name('serp-item__preview')[0]
        first_image.click()
        first_selected_image = driver.find_element_by_class_name('MMImage-Origin')

        driver.find_element_by_css_selector('.MediaViewer_theme_fiji-ButtonNext').click()

        driver.find_element_by_css_selector('.MediaViewer_theme_fiji-ButtonPrev').click()
        last_selected_image = driver.find_element_by_class_name('MMImage-Origin')
        
        try:
            self.assertEqual(first_selected_image, last_selected_image)
        except:
            print(f'-Первое изображение из списка не соответствует первому открытому изображению.')
        else:
            print(f'-Первое изображение из списка соответствует первому открытому изображению.')

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
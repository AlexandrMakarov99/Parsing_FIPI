from selenium import webdriver
from selenium.webdriver.common.by import By
from base64 import b64decode
from PyPDF2 import PdfWriter, PdfReader
import os



def create_pdf(file_path):
    a = driver.execute_cdp_cmd(
        "Page.printToPDF", {"format": 'A4', "landscape": True})
    # Import only b64decode function from the base64 module

    # Define the Base64 string of the PDF file
    b64 = a['data']

    # Decode the Base64 string, making sure that it contains only valid characters
    bytes = b64decode(b64, validate=True)

    # Perform a basic validation to make sure that the result is a valid PDF file
    # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
    # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
    if bytes[0:4] != b'%PDF':
        raise ValueError('Missing the PDF file signature')

    # Write the PDF contents to a local file
    with open(file_path, 'wb') as f:
        f.write(bytes)

def cropping(file_path):
    reader = PdfReader(file_path)
    writer = PdfWriter()

    for j in range(len(reader.pages)):
        page = reader.pages[j]
        page.mediabox.upper_left = (
            page.mediabox.right / 4,
            page.mediabox.top / 1,
        )
        writer.add_page(page)

    # write to document-output.pdf
    with open(file_path, "wb") as fp:
        writer.write(fp)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")  # to launch chrome headless
CHROMEDRIVER_PATH = r'C:\Users\User\AppData\Local\Google\Chrome\User Data\chromedriver.exe'
driver = webdriver.Chrome(options=chrome_options, executable_path=CHROMEDRIVER_PATH)  # setting browser driver


url = "http://oge.fipi.ru/os/xmodules/qprint/qsearch.php?theme_guid=260FA3E2B88BB62649C47578051DF197&proj_guid=B24AFED7DE6AB5BC461219556CCA4F9B"
driver.get(url)  # open the physics OGE homepage

link = driver.find_element(By.LINK_TEXT, 'Тепловые явления')  # choosing the section
link.click()

dir_path = r'C:\Users\User\Documents\Physics OGE'  # set folder directory
last_page = int(driver.find_elements(By.CLASS_NAME, 'Walk')[-1].text[1:-1])


for i in range(1, last_page + 1):
    if i > 1:
        link = driver.find_element(By.LINK_TEXT, f'[{i}]')
        link.click()

    file_path = os.path.join(dir_path, f'{i}.pdf')  # set the path of the current(i) file
    create_pdf(file_path)
    cropping(file_path)

driver.quit()

# todo
# нужно запихнуть в архив
# нужно вычленить отдельную задачу (распарсить)
# заджойнить отдельные задачи в одну пдфку
# распарсить разделы
# распарсить предметы
# распарсить ОГЭ ЕГЭ

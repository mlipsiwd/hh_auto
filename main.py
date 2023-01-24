import requests
import re
from multiprocessing import Pool
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


Form, Window = uic.loadUiType("hh_auto.ui")
app = QApplication([])
window = Window()
form = Form()
req = requests.Session()

def send_req(item):

    print(item)
    check = req.post('https://hh.ru//applicant/vacancy_response/popup', data={"_xsrf":f"{form.lineEdit_2.text()}", "letter": f"""{form.plainTextEdit.toPlainText()}""", "lux": True, "withoutTest": "no", "hhtmFromLabel": "undefined", "hhtmSourceLabel": "undefined"})

    print(check.status_code, item)
    if check.status_code != 200:
        if check.json()['error' ] == 'negotiations-limit-exceeded':
            return False

def on_click():

    if (form.lineEdit.text() or form.lineEdit_2.text() or form.lineEdit_3.text()) == "":
        print ("hui")
        return 0

    n = 0
    sendet = 0
    pool = Pool(processes=70)
    while True:

        form.progressBar.setProperty("value", n+1)
        data = req.get(f"{form.lineEdit_3.text()}&page={n}").text
        links = re.findall('https://hh.ru/vacancy/(\d*)?', data, re.DOTALL)
        if links == []:
            break
        check = pool.map(send_req, links)
        if False in check:
            break
    pool.close()
    pool.join()

def press_Button():
    form.pushButton.clicked.connect(on_click)

def main():

    form.setupUi(window)
    window.show()
    req.headers = {"Cookie":f"{form.lineEdit.text()}", "Host": "hh.ru", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"}
    press_Button()
    app.exec()

if __name__ == "__main__":
    main()
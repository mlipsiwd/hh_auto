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
xsrf = None

def send_req(item):

    check = req.post('https://hh.ru/applicant/vacancy_response/popup', data={"vacancy_id":f"{item[0]}", "resume_hash":"8376c225ff0b671c9b0039ed1f5850384c3570", "letter": False, "lux": True, "withoutTest": "no", "hhtmFromLabel": "undefined", "hhtmSourceLabel": "undefined", "ignore_postponed":True})
    
    print(check.text)
    print(check.status_code, item)
    if check.status_code != 200:
        if check.json()['error' ] == 'negotiations-limit-exceeded':
            return False

def on_click():
    
    if (form.lineEdit.text() or form.lineEdit_2.text() or form.lineEdit_3.text()) == "":
        return 0
    req.headers = {"Cookie":f"""{form.lineEdit.text()}""", "Host": "hh.ru", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"}
    xsrf = form.lineEdit_2.text()
    n = 0
    pool = Pool(processes=70)
    while True:
        form.progressBar.setProperty("value", n+1)
        data = req.get(f"{form.lineEdit_3.text()}&page={n}").text
        links = re.findall('https://hh.ru/vacancy/(\d*)?', data, re.DOTALL)
        if links == []:
            break
        items = [(i, xsrf) for i in links]
        print (items)
        check = pool.map(send_req, items)
        if False in check:
            break
    pool.close()
    pool.join()
    

def press_Button():
    form.pushButton.clicked.connect(on_click)

def main():
    form.setupUi(window)
    window.show()
    press_Button()
    app.exec()

if __name__ == "__main__":
    main()

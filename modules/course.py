import requests
from bs4 import BeautifulSoup
from datetime import datetime


class CourseProcessor:
	api_url = "http://www.cbr.ru/scripts/XML_daily.asp?"

	def __init__(self, *args):
		self.message: str

	def _get_soup(self):
		today = datetime.today()
		today = today.strftime("%d/%m/%Y")

		payload = {"date_req" : today}

		responce = requests.get(self.api_url, params=payload)

		return BeautifulSoup(responce.content, "lxml")

	def _get_course(self, id):
		soup = self._get_soup()
		return str(soup.find("valute",  {'id': id}).value.text)
		

	def run(self):
		response = "{0} рублей за 1 доллар \n {1} рублей за 1 евро \n {2} рублей за 10 юаней \n {3} рублей за 1 фунт"
		self.message = response.format(
			self._get_course("R01235"), self._get_course("R01239"), self._get_course("R01375"), self._get_course("R01035")
			)

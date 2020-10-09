import requests
from bs4 import BeautifulSoup
import pandas as pd
from streamlit import write,title,text_input,markdown

title('Weather App')
country = text_input('Enter any country:')
city = text_input("Enter any city from " + str(country) +" :")
url = f'https://www.timeanddate.com/weather/{country}/{city}/ext'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find(id ='wt-ext')

page_bg_img = '''
<style>
body {
background-image: linear-gradient(315deg, #abe9cd 0%, #3eadcf 74%);

}
</style>
'''

markdown(page_bg_img, unsafe_allow_html=True)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
markdown(hide_streamlit_style, unsafe_allow_html=True)

if table:
	column = table.find_all('tr')[2:-1]
	days = [i.find('th').get_text()[:3] for i in column]
	date = [i.find('th').get_text()[3:] for i in column]
	descp = [i.find(class_ ='small').get_text().strip('.') for i in column]
	temp = [i.find(class_ = 'wt-ic').findNext('td').get_text().replace('\xa0','') for i in column]
	weather = pd.DataFrame({
		'Day': days,
		'Date': date,
		'Description':descp,
		'Temparature(Fareinheit)':temp,
})
	write(weather)
	weather.to_csv('weather.csv')
else:
	if city and country:
		write("Sorry weather report for " + str(city) + " is not available !")
	else:
		"Please enter a city & a country name."







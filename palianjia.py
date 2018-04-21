import time
import pymysql
import requests

from bs4 import BeautifulSoup

#get url soup
def get_page(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text,'lxml')
	return soup

#get page all links
def get_links(link_url):
	soup = get_page(link_url)
	links_div = soup.find_all('div',class_='pic-panel')
	links_ret = [div.a.get('href') for div in links_div]
	return links_ret
links = get_links('https://sh.lianjia.com/zufang/')

def get_house_info(house_url):
	soup = get_page(house_url)
	price = soup.find('span',class_='total').text
	unit = soup.find('span',class_='unit').text.strip()
	house_info = soup.find_all('p')
	area = house_info[0].text[3:]
	layout = house_info[1].text[5:]
	floor = house_info[2].text[3:]
	direction = house_info[3].text[6:]
	subway = house_info[4].text[3:]
	community = house_info[5].text[3:]
	location = house_info[6].text[3:]
	create_time = house_info[7].text[3:]
	agent = soup.find('a',class_='name LOGCLICK')
	agent_name = agent.text
	agent_id = agent.get('data-el')
	#valuate = soup.find('div',class_='evaluate')
	#core,number = evaluate.find('span',class_='rate').text.split('/')
	#times = evaluate.find('span',class_='time').text[5:-1]
	info = {
		'price' : price,
		'unit' : unit,
		'area' : area,
		'layout' : layout,
		'floor' : floor,
		'direction' : direction,
		'create_time' : create_time,
		'subway' : subway,
		'community' : community,
		'location' : location,
		'agent_name' : agent_name,
		'agent_id' : agent_id,
	}
	return info

DATABASE = {
	'host' : '127.0.0.1',
	'database' : 'test',
	'user' : 'root',
	'password' : '',
	'charset' : 'utf8'
}
def get_db(setting):
	return pymysql.connect(**setting)
db = get_db(DATABASE)

def insert(db_name,house):
	values = "'{}',"*10 + "'{}'"
	sql_values = values.format(house['price'],house['unit'],house['area'],house['layout'],house['floor'],house['direction'],house['subway'],house['community'],house['location'],house['agent_name'],house['agent_id'])
	sql = """
		insert into `house`(`price`,`unit`,`area`,`layout`,`floor`,`direction`,`subway`,`community`,`location`,`agent_name`,`agent_id`)
		values({})
	""".format(sql_values)
	print(sql)
	cursor = db_name.cursor()
	cursor.execute(sql)
	db_name.commit()

for link in links:
	time.sleep(2)
	print('get one info')
	house_r = get_house_info(link)
	insert(db,house_r)

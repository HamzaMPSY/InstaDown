import requests,re,json,os,sys
from bs4 import BeautifulSoup as sp
import urllib.request as ur


accountName = input("Enter an Instagram Username :   ")
baseUrl = "https://www.instagram.com/"
source = requests.get(baseUrl+accountName+"?__a=1").text

try :
	js= json.loads(source)
except Exception :
	print("This account does not exist")
	sys.exit(0)
#https://www.instagram.com/static/bundles/ProfilePageContainer.js/031ac4860b53.js
query_hash = "472f257a40c653c64c666ce877d59d2b"
idd = ""
end_cursor = ""
pics = []
is_private =  js['graphql']['user']['is_private']
nodes = js['graphql']['user']['edge_owner_to_timeline_media']['edges']
i = 1
for node in nodes:
	if not node['node']['is_video']:
		pics.append(node['node']['shortcode'])
	if i == 1:
		idd = node['node']['owner']['id']
		i=2


has_next_page = js['graphql']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
if has_next_page :
	end_cursor = js['graphql']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'] 


while has_next_page :
	 
	link = "https://www.instagram.com/graphql/query/?query_hash="+query_hash+"&variables={\"id\":\""+idd+"\",\"first\":50,\"after\":\""+end_cursor+"\"}"
	source = requests.get(link).text
	js= json.loads(source)
	nodes = js['data']['user']['edge_owner_to_timeline_media']['edges']
	for node in nodes:
		if not node['node']['is_video']:
			pics.append(node['node']['shortcode'])
	has_next_page = js['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
	if has_next_page :
		end_cursor = js['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'] 
if is_private:
	print("this account is private")
else:
	print(len(pics),"Picture retrived wait a few minutes while downloading it !!")

	try:
		os.mkdir(accountName)
	except Exception:
		pass

	os.chdir(accountName)

i = 1
for pic in pics:
	soup = sp(requests.get(baseUrl+'p/' + pic).text,features="lxml")

	for item  in soup.find_all('meta'):
		if item.get('content') and re.match(r'^https://instagram.*\.jpg.*',item.get('content')):
			ur.urlretrieve(item.get('content'),str(i)+'.jpg')
	i+=1
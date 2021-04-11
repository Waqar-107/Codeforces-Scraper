from urllib.request import urlopen
from bs4 import BeautifulSoup

username = "Fuad113"
total_page = 4

url = "http://codeforces.com/submissions/_lucifer_/page/1011"

page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
table = soup.find_all("table")
rows = soup.find_all("tr")
column = rows[1].find_all("td")

submissionId = column[0].find("a")
problemName = column[3].find("a")
language = column[4]
verdict = column[5]

print(submissionId)
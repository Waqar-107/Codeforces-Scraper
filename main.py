from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from util import *


class CodeforcesScraper:
    def __init__(self, user_name, page_required):
        self.user_Name = user_name
        self.page_required = page_required
        self.base_url = "http://codeforces.com"

    @staticmethod
    def fetch_data(url):
        page = urlopen(url)
        return page

    # comparison can be either "time" or "memory"
    # by default it is time.
    # if there are more than one accepted solution for any problem, we'll take the efficient one
    def get_all_accepted_sol(self, comparison="time"):
        for i in range(1, self.page_required + 1):
            page = self.fetch_data(self.base_url + "/submissions/" + self.user_Name + "/page/" + str(i))
            soup = BeautifulSoup(page, "html.parser")
            table = soup.find_all("table")
            rows = table.find_all("tr")

            for row in rows:
                column = row.find_all("td")

                submissionLink = column[0].find("a")["href"]
                problemName = column[3].find("a").text.strip()
                language = column[4].text.strip()
                verdict = column[5].text.strip()

                # time in ms
                time = int(column[6].text.strip().split("\xa0")[0])

                # memory in KB
                memory = int(column[7].text.strip().split("\xa0")[0])

                if re.match(verdictList["ac"], verdict):
                    pass





# username = "Fuad113"
# total_page = 4
#
url = "http://codeforces.com/submissions/_lucifer_/page/1011"

page = urlopen(url)
soup = BeautifulSoup(page, "html.parser")
table = soup.find_all("table")
rows = table[0].find_all("tr")
column = rows[1].find_all("td")

submissionLink = column[0].find("a")["href"]
problemName = column[3].find("a").text.strip()
language = column[4].text.strip()
verdict = column[5].text.strip()

# time in ms
time = int(column[6].text.strip().split("\xa0")[0])

# memory in KB
memory = int(column[7].text.strip().split("\xa0")[0])

print(submissionLink)
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from util import *


class CodeInfo:
    def __init__(self, submissionID, verdict, time, memory, name, code, language):
        pass


class CodeforcesScraper:
    def __init__(self, user_name, page_required):
        self.user_Name = user_name
        self.page_required = page_required
        self.base_url = "http://codeforces.com"
        self.src_code_div_id = "program-source-text"

    @staticmethod
    def fetch_data(url):
        page = urlopen(url)
        return page

    @staticmethod
    def fetch_code(url):
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        code = soup.find(id="program-source-text")

        # split the lines, they already has \r so writing the lines will create lines
        code_chunks = code.text.split("\n")
        return code_chunks

    # comparison can be either "time" or "memory"
    # by default it is time.
    # if there are more than one accepted solution for any problem, we'll take the efficient one
    def get_all_accepted_sol(self, comparison="time"):
        for i in range(1, self.page_required + 1):
            page = self.fetch_data(self.base_url + "/submissions/" + self.user_Name + "/page/" + str(i))
            soup = BeautifulSoup(page, "html.parser")
            table = soup.find_all("table")
            rows = table.find_all("tr")

            accepted_codes = {}

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

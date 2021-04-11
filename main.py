from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from util import *


class CodeInfo:
    def __init__(self, submissionID, verdict, time, memory, name, language):
        self.submissionID = submissionID
        self.verdict = verdict
        self.time = time
        self.memory = memory
        self.name = name
        self.language = language


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
    def fetch_code(self, url):
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        code = soup.find(id=self.src_code_div_id)

        table = soup.find("table")
        rows = table.find_all("tr")
        problemName = rows[1].find_all("td")[2].find("a").text

        # split the lines, they already has \r so writing the lines will create lines
        code_chunks = code.text.split("\n")
        return problemName, code_chunks

    # comparison can be either "time" or "memory"
    # by default it is time.
    # if there are more than one accepted solution for any problem, we'll take the efficient one
    def get_all_accepted_sol(self, comparison="time"):
        for i in range(1, self.page_required + 1):
            page = self.fetch_data(self.base_url + "/submissions/" + self.user_Name + "/page/" + str(i))
            soup = BeautifulSoup(page, "html.parser")
            table = soup.find_all("table")
            rows = table[0].find_all("tr")

            accepted_codes = {}

            for i in range(1, len(rows)):
                column = rows[i].find_all("td")

                submissionLink = column[0].find("a")["href"]
                submissionId = submissionLink.split("/")[-1]

                problemName = column[3].find("a").text.strip()
                language = column[4].text.strip()
                verdict = column[5].text.strip()

                # time in ms
                time = int(column[6].text.strip().split("\xa0")[0])

                # memory in KB
                memory = int(column[7].text.strip().split("\xa0")[0])

                if re.match(verdictList["ac"], verdict):
                    if problemName not in accepted_codes:
                        accepted_codes[problemName] = CodeInfo(submissionId, verdict, time, memory, problemName,
                                                               language)

                    else:
                        if comparison == "time":
                            if accepted_codes[problemName].time > time:
                                accepted_codes[problemName] = CodeInfo(submissionId, verdict, time, memory, problemName,
                                                                       language)
                        else:
                            if accepted_codes[problemName].memory > memory:
                                accepted_codes[problemName] = CodeInfo(submissionId, verdict, time, memory, problemName,
                                                                       language)

            for keys in accepted_codes:
                print(keys)


# cf = CodeforcesScraper("Fuad113", 4)
# cf.get_all_accepted_sol()

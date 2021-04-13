from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from util import *
import os
import shutil


class CodeInfo:
    def __init__(self, name, level, contest_id, submission_id, verdict, time, memory, language):
        self.name = name
        self.level = level
        self.contest_id = contest_id
        self.submission_id = submission_id
        self.verdict = verdict
        self.time = time
        self.memory = memory
        self.language = language
        self.code = ""


class CodeforcesScraper:
    def __init__(self, user_name: str) -> None:
        self.user_Name = user_name
        self.base_url = "http://codeforces.com"
        self.src_code_div_id = "program-source-text"

    @staticmethod
    def fetch_data(url: str) -> object:
        page = urlopen(url)
        return page

    def fetch_code(self, url: str) -> str:
        page = urlopen(url)
        soup = BeautifulSoup(page, "html.parser")
        code = soup.find(id=self.src_code_div_id)

        # split the lines, they already has \r so writing the lines will create lines
        code_chunks = code.text.split("\n")
        return code_chunks

    # comparison can be either "time" or "memory"
    # by default it is time.
    # if there are more than one accepted solution for any problem, we'll take the efficient one
    def get_all_accepted_sol(self, page_required: int, root_directory_name: str, comparison: str = "time") -> None:
        # remove the root directory where the codes will be stored
        if os.path.exists(root_directory_name):
            # delete folder with things inside it
            shutil.rmtree(root_directory_name)

        for p in range(1, page_required + 1):
            page = self.fetch_data(self.base_url + "/submissions/" + self.user_Name + "/page/" + str(p))
            soup = BeautifulSoup(page, "html.parser")

            # that page is non-existent so they return the home page
            if soup.title.string == "Codeforces":
                continue

            table = soup.find_all("table")
            rows = table[0].find_all("tr")

            accepted_codes = {}

            for i in range(1, len(rows)):
                column = rows[i].find_all("td")

                # there are codes that only the user themselves can see, e.g: problems from gym
                # those will not have any "a", instead they have spans
                submission_link = column[0].find("a")
                if submission_link is not None:
                    submission_id = submission_link["href"].split("/")[-1]
                else:
                    submission_id = column[0].find("span").text

                problem_name = column[3].find("a").text.strip()

                # problem_name has "X - name" format where X = A, B...
                # we separate it. But in the dictionary key, we keep it as Div.1 A is same as Div. C
                # and many has submitted both of them
                actual_name = problem_name.split("-")[1].strip()
                problem_link = column[3].find("a")["href"]

                language = column[4].text.strip()
                verdict = column[5].text.strip()

                # if gym then skip
                if re.match("^.*gym.*$", problem_link):
                    continue

                contest_id = problem_link.split("/")[2]
                problem_level = problem_link.split("/")[4]  # A, B, C....

                # time in ms
                time = int(column[6].text.strip().split("\xa0")[0])

                # memory in KB
                memory = int(column[7].text.strip().split("\xa0")[0])

                # if accepted then save
                # if already a solution exists then take the optimized one
                if re.match(verdictList["ac"], verdict):
                    if problem_name not in accepted_codes:
                        accepted_codes[problem_name] = CodeInfo(actual_name, problem_level, contest_id, submission_id,
                                                                verdict, time, memory, language)

                    else:
                        if comparison == "time":
                            if accepted_codes[problem_name].time > time:
                                accepted_codes[problem_name] = CodeInfo(actual_name, problem_level, contest_id,
                                                                        submission_id,
                                                                        verdict, time, memory, language)
                        else:
                            if accepted_codes[problem_name].memory > memory:
                                accepted_codes[problem_name] = CodeInfo(actual_name, problem_level, contest_id,
                                                                        submission_id,
                                                                        verdict, time, memory, language)

            # fetch the code
            for key in accepted_codes:
                url = self.base_url + "/contest/" + accepted_codes[key].contest_id + "/submission/" + accepted_codes[
                    key].submission_id
                accepted_codes[key].code = self.fetch_code(url)
                self.save_code(accepted_codes[key], root_directory_name)

            print("page", p, "done")

    @staticmethod
    def save_code(code_info: CodeInfo, root_directory_name: str) -> None:
        # check if the root directory exists
        if not os.path.exists(root_directory_name):
            os.mkdir(root_directory_name)

        # check if A, B, C etc folder exists
        if not os.path.exists(root_directory_name + "/" + code_info.level):
            os.mkdir(root_directory_name + "/" + code_info.level)

        # file name will be `contest_id.level problem_name`
        # change according to your need
        file_name = code_info.contest_id + code_info.level + ". " + code_info.name
        file_path = root_directory_name + "/" + code_info.level + "/"

        ext_found = False
        for ext in language_extensions:
            for lang in language_extensions[ext]:
                if lang.lower() in code_info.language.lower():
                    file_name += "." + ext
                    ext_found = True
                    break

            if ext_found:
                break

        if not ext_found:
            file_name += ".txt"

        file = open(file_path + file_name, "w")
        file.writelines(code_info.code)


cf = CodeforcesScraper("_lucifer_")
cf.get_all_accepted_sol(1, "lucifers_ac_code")

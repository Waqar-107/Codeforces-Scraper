# Codeforces-Scraper
Script to parse accepted codes from Codeforces

# How to Run
If we create an object of the class `CodeforcesScraper`by passing the username in the constructor.  When we call the function to scrape all the accepted codes, we pass the number of pages of submission and the name of the directory where to save the code. An user can have more than one submission pages, for example I have 90 currently. The function will start from page 1 and finish on the page specified.

`comparison` can be either `time` or `memory`. This is an optional parameter which is `time` by default.

```python
cf = CodeforcesScraper(user-name)
cf.get_all_accepted_sol(total_page_of_submission, root_directory_name_to_save_codes, comparison)
```

# Challenges
1. You can't access all the codes on Codeforces. For example you `can't check` what others has submitted in the `Gym`. Usually in the submission table, we can find the submission link in the first cell of a row. The cell has an `<a></a>`. If the code is hidden then the link is not present. Instead they use a `<span></span>` where we can just get the submission id.
2. A single problem may have one or more accepted submissions.
3. `Div.1 A` problems are `Div.2 C` problems when the contest is held for both divisons.

# Approach
1. All the submission page is requested and scraped using `bs4`.
2. The submission id is retrieved.
3. The name, problem link, language, time and memory is also retrieved.
4. We can check if the problem belongs to a gym using the problem-link as it will contain `gym` in the url.
5. By parsing the link we determine the problem level e.g. A, B, C... and contest id.
6. If submission for a problem is more than one then the efficient one is considered.
7. After we have all the details about the problem and submission, we can call another url to get the code.
8. The `util.py` has a dictionary to map file extension with programming language. Not all the languages supported by `Codeforces` is not given. They can be added if required.
9. After getting the code we have a `CodeInfo` object.
10. We create separate folders for A, B, C etc. write the codes in file with appropriate extensions. The naming convention is like `1000A. problem_name`.

# Future Works
1. Save all the accepted submissions for a particular problem.
2. Write functions to retrieve `wrong answer`, `time limit exceeded`, `runtime error` etc. 

`In case of any bug found please create an issue` 🙂

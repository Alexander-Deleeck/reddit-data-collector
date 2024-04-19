This project is focused on the collection and archiving of publically available reddit data.
It uses the official reddit API (PRAW) for scraping raw data, which is then cleaned and archived in a structured manner,
which can subsequently be used for data analysis, dataset curation or simply exploration.

The user can perform the following types of collection actions:
  - Subreddit scraping: collect data from a specific subreddit
  - Query scraping: collect data within a subreddit which contains one or multiple keywords of your choice
  - Profile scraping: collect data from a profile on reddit. This should only be done on your personal accounts, or with consent of the user in question

These actions can be parametarized with values of your own choice for:
  - Subreddit: the name of the target sub
  - Timewindow: collect top data from previous hour, day, week, month, year or of all time
  - Filter limit: number of posts you want to collect (maximum API limit is 1000)

For using the API, the user should provide the following PRAW API credentials in the .env file:
MY_SECRET = 
MY_CLIENT_ID = 
MY_USER_AGENT = 

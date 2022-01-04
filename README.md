# Web Scraper App
A Selenium based web scraper for capturing customer sentiments - reviews and comments

### Ways to set it up:

1. Clone this project to your local project directory.
   - git clone https://github.com/arnabRoy21/**web_scraper_selenium**.git
2. Make any enhancements to code and commit the changes.
   - git add .
   - git commit -m *message*

### Heroku Deployment Steps:

1. Install heroku CLI and create a heroku web app - **web-scraper-selenium**
2. Add environment variables - 
   - CHROMEDRIVER_PATH = **/app/.chromedriver/bin/chromedriver**
   - GOOGLE_CHROME_BIN = **/app/.apt/usr/bin/google-chrome**
   - DB_USER = ***db_user***
   - DB_PASSWORD = ***password***
3. Add below three build packs - 
   - https://github.com/heroku/heroku-buildpack-chromedriver
   - https://github.com/heroku/heroku-buildpack-google-chrome
   - heroku/python
4. In heroku CLI, cd to project folder and run - heroku login
5. Add a heroku git remote for the already created heroku web app
   - heroku git:remote -a **web-scraper-selenium**
6. Deploy the app
   - git push heroku main



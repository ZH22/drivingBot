## Background
### Context
With my neighbourhood Driving Center having notoriously long waiting times, coupled with the average wait times for a lesson slot ballooning from the backlog of students during the Covid Pandemic. Getting a lesson slot required booking weeks in advance, dragging out the driving certification process.

### Try-Sell Feature
Driving Center's website routinely release last minute cancelled slots for that day at arbitrary timings. That's what the script will be aiming for.

## Usage
Interfacing with a Telegram Bot through the python library [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).

Webscraping: [Selenium](https://www.selenium.dev/) with [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)


Scheduling: Linux Cronjobs on Ubuntu Server

![5-BBDC](https://github.com/user-attachments/assets/e38e6607-2823-4194-9918-9960d1cf5ad8)
![6-BBDC](https://github.com/user-attachments/assets/60b463b6-3a6f-4fc4-8c90-10d70b05bcd5)

## Footnotes
Experimented with Webscraping, APIs and Cronjobs through this project. Allowing me to consistently keep up to date with hundreds of released slots during operation, decreasing wait times to hours rather than weeks. 

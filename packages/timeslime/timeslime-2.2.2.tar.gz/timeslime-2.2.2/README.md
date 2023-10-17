# ⌚ timeslime

⌚ This is timeslime! Have fun tracking your time ⌚

## Getting started

Install python and pip and execute the following

~~~bash
pip install timeslime
~~~

🚀 Start your time

~~~bash
timeslime start
~~~

🛑 Stop your time

~~~bash
timeslime stop
~~~

🔧 Configure your weekly working hours (e.g for 40 hours per week)

~~~bash
timeslime config --weekly-working-hours=40
# Get more configuration options with the following.
timeslime config --help
~~~

📊 Get report 

~~~bash
timeslime report
~~~

🤝 Synchronize your time and configuration 

~~~bash
timeslime sync
~~~

💡 Get help

~~~bash
timeslime --help
~~~

## Contribute

~~~bash
git clone https://gitlab.com/lookslikematrix/timeslime.git
cd timeslime
pipenv install --dev
pipenv shell
pytest tests
pip install -e .
timeslime --help
~~~

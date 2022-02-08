# youtube-scraper

# Instalation

First make sure git is installed:<br>
`$ brew install git`

Then clone the git repository with:<br>
`git clone ...`

After you have cloned the repository you'll have to change the permissions of two files:<br>
`chmod +x youtube-scraper/setup.sh`<br>
`chmod +x youtube-scraper/run.sh`

Then you need to run setup.sh once so that the virtual environment for the script is set up:<br>
`youtube-scraper/setup.sh`

Before using the script you must change the API_TOKEN value in creds.json to your account's API token.<br>
Your API token can be found at: https://console.apify.com/account#/integrations

# How to use

In order to use the scraper you need to run the run.sh file with two parameters.
 - The CSV file that will be the output.
 - A text file with all the channel urls that you need to scrape.
 
Example:
`youtube-scraper/run.sh sample.csv urls.txt`

This will scrape the data for all the channels in `urls.txt` and it will export that as `sample.csv`.

The file that contains the urls must be in the following format:

url1<br>
url2<br>
url3<br>
...

You can view the progress of the program while running here: https://console.apify.com/actors/runs

# Extracting data from JSON files

In case the script fails for any reason you can still salavage all the data with JSON file found at: https://console.apify.com/actors/runs

`youtube-scraper/fromfile.sh sample.csv items.json`

The above example will return all the data, including tags from the json file into the csv file.

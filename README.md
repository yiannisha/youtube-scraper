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
 - The output file (CSV or XLSX).
 - A text file with all the channel urls that you need to scrape.
 
<br><br>
Example:
`youtube-scraper/run.sh sample.csv urls.txt`

This will scrape the data for all the channels in `urls.txt` and it will export that as `sample.csv`.


<br><br>
Example:
`youtube-scraper/run.sh sample.xlsx urls.txt`

This will scrape the data for all the channels in `urls.txt` and it will export that as `sample.xlsx`.

<br><br>
The file that contains the urls must be in the following format:

url1<br>
url2<br>
url3<br>
...
 
## Adding max results to return:<br>
You can pass the optional max results argument by running run.sh like above but adding the number of the max results third.<br>
Example: `youtube-scraper/run.sh sample.csv urls.txt 3`<br>
 
This will do exactly the same job as the command above, but it will automatically stop when it reaches 3 scraped videos.<br>

<br><br>
You can view the progress of the program while running here: https://console.apify.com/actors/runs

# Extracting data from JSON files

In case the script fails for any reason you can still salavage all the data with JSON file found at: https://console.apify.com/actors/runs

 
`youtube-scraper/fromfile.sh sample.csv items.json`

The above example will return all the data, including tags from the json file into the csv file.


`youtube-scraper/fromfile.sh sample.xlsx items.json`

The above example will return all the data, including tags from the json file into the xlsx file.

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

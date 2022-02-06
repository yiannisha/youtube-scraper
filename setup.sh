echo "Creating virtual environment";
python3 -m venv env;
source env/bin/activate;
echo "Installing dependecies to local virtual environment";
pip3 install -r requirements.txt;
deactivate;

# autogluon_dashboard

Follow the steps below to set up autogluon-dashboard::
1. Create a virtual environment by running: 
```
python3 -m venv .venv_dash 
source .venv_dash/bin/activate
``` 
2. Install all necessary libraries by running: `pip3 install -r requirements.txt`
3. Install the `autogluon_dashboard` package by running: `pip3 install -e .`. You can now interact with the dashboard through the CLI command `agdash`. 
4. To convert a Panel app to WebAssemly,  Panel provides a script that will convert the code in `app.py` into an HTML file and JS file. This can be done in one line of code as: `panel convert app.py --to pyodide-worker --out web_files/`
The generated HTML and JS files will be found in the `web_files` folder. These can be uploaded to the desired hosting service (eg: GitHub Pages or AWS S3). 
<br>Run `agdash --dataset_file 'path_to_csv_file.csv' --aggreagated_file 'path_to_csv_file.csv'`. 
<br> For example, `agdash --dataset_file 'dev_data/all_data.csv' --aggreagated_file 'dev_data/autogluon.csv'`


To run all unittests, run the following command in the root directory: `python3 -m unittest discover -s unittests -p 'test_*.py'`

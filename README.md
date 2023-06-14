# autogluon-dashboard

To view the dashboards in a local browser:
1. Create a virtual environment by running: 
```
python3 -m venv .venv_dash 
source .venv_dash/bin/activate
``` 
2. Install all necessary libraries by running: `pip3 install -r requirements.txt`
3. run `panel serve app.py` and open the provided http link in your browser.

To convert a Panel app to WebAssemly,  Panel provides a script that will convert the code in `app.py` into an HTML file and JS file. This can be done in one line of code as: `panel convert app.py --to pyodide-worker --out docs/app`
The generated HTML and JS files will be found in the `docs/app` folder. These can be uploaded to the desired hosting service (eg: GitHub Pages).

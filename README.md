
# currency_converter
	A small ​ RESTful Web service application​ for converting currencies.

## 1. Running the project
		a. Download the repo
		b. Create virtual environement in python 3.5
			
			virtualenv <venvname> --python=python3.5

		c. Activate virtual environment
	
			source <venvname>/bin/activate

		d. Go to project directory in terminal

			cd /path/to/project

		e. Install dependencies

			pip install -r requirements.txt

		f. Run project
			
			python manage.py runserver

## 2. Converting currency API URL

		http://127.0.0.1:8000/currency/?currency_code=<currency_code>&currency_value=<currency_value>&target_code=<target_currency_code>

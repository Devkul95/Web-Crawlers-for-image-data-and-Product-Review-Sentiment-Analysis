# Web-Crawlers-for-image-data-and-Product-Review-Sentiment-Analysis
End-to-End Python Web Crawlers for image data and Product Review Sentiment Analysis. Deployment into Pivotal Web Service
### Preview of The Project: <https://flipkartcrawler-persistent-possum-fl.cfapps.io><br>
### Run as Localhost:
1. Clone the Project
2. In Pycharm open by selecting the project folder
3. Open Terminal and install the dependencies:
	  * pip install -r requirements.txt
4. open flask_app.py file:
    * Go to if__name__ == "__main__":
    1. Comment port = int(os.getenv("PORT"))
    2. Comment app.run(host='0.0.0.0', port=port)
    3. Uncomment #app.run(host='127.0.0.1', port=8001, debug=True)
5. Run the file righ click and Run 'flask_app'.
6. Click the link on the terminal.<br>

### Description of The Project<br>
* static: Websites generally need to serve additional files such as images, JavaScript, or CSS. In Flask or Django, we refer to these files as “static files”.
* templates: In Flask or Django all the html files are kept under templates folder.
* flask_app: It is the main app we used here flask_app as the name of app, you can give any name.
### Files Requirement for Deployment
* manifest.yml-
	Create a manifest.yml file in the root directory of your app.
	Add the following content to the file.<br>
for more details go and check out at <https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html>

* Procfile: A `Procfile` defines the processes for an app and the start command for each process. For example, we can define a Procfile like this.<br>
web: python flask_app.py   --master --processes 4 --threads 2

* requirements.text- this are the dependencies or list of python libraries that the server will install in order to host the project.

* runtime:python-3.6.10 (The version we used for development)

### Deploying into Cloud.
1. Download and install cf cli. https://github.com/cloudfoundry/cli
2. Open command prompt and go to the project directory.
3. Type cf and hit Enter
4. Provide authorization access.
	* cf login -a https//api.run.pivotal.io
	* Email-
	* password-
5. Select any Space for push the project
6. cf push
7. Wait for the process
8. Done

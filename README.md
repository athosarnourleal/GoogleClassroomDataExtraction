# AUTOMATIC SPREADSHEET CREATOR BASED FROM GOOGLE CLASSROOM DATA
this application is created as a way to facilitate and organize the grading of many students

# PRE REQUISITES FOR RUNNING
before running:
``` python
1) create a google cloud project

2) enable the "google sheets" and "google classroom" APIs

3) create the "google credentials" folder in the root of the application(if it does not exist)

4) create a service account (having the role of editor) and extract its credentials as ".json"
4.1) rename the credentials file to "credentials_service_googleSheets.json" and move it to the "google credentials" folder
4.2) add the email of the service account to google sheets spreadsheet that you desire to store the results

5) create a testing user and extract its credentials as ".json"
5.1) rename the credentials file to "credentials_client_google_classroom.json" and move it to the "google credentials" folder
```


# SETUP AND RUN
both the setup and the run can be done easily by running the bash files
``` bash
# only needs to be executed once
bash setup.bash
```
``` bash
bash run.bash
```


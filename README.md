# Sam your housing recommender chatbot 🤖



## Running Locally 💻
Follow these steps to set up and run the service locally :

### Prerequisites
- Python 3.8 or higher
- Git


Navigate to the project directory :

`cd housing-recommendation-system`


Create a virtual environment :
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

Install the required dependencies in the virtual environment :

`pip install -r requirements.txt`


Launch the chat service locally :

To setup streamlit configuration file :
```
sudo chmod +x setup.sh
./setup.sh
```

Download the dataset using the following command :
```
python3 -m pypyr src/pipelines/dataset-download
```


To run the service :

```
streamlit run src/Home.py
```




The service is currently deployed on:
http://ec2-23-22-66-37.compute-1.amazonaws.com:8000/housing

The Apache airflow service is currently deployed on:
http://ec2-23-22-66-37.compute-1.amazonaws.com:8080

Use the following credentials to login:
```
username: admin
password: 26xA25fU88gRCgzy
```

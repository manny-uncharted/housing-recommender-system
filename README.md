# Sam your housing recommender chatbot 🤖
A LLM based chatbot that provides recommendations on property listings in the UK.
This is just a prototype and is not meant to be used in production. As it's a prototype to test a budding concept. The goal is to have a solution that can help real estate companies to provide better customer service to their clients. The chatbot is built using the [Streamlit](https://streamlit.io/) framework.

You can access the demo here:
[Deployed endpoint](http://ec2-23-22-66-37.compute-1.amazonaws.com:8000/housing)


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

## Project Structure 📁

```
Root Directory
├── .streamlit
│   └── config.toml
├── data
│   ├── *.txt
│   ├── *.csv
├── embeddings
│   ├── *.pkl
├── scraper
│   ├── modules
│   │   ├── *.py
│   ├── *.py
|   ├── *.sh
├── src
│   ├── Home.py
│   ├── pipelines
│   │   ├── dataset-download.yaml
|   ├── notebooks
│   │   ├── *.ipynb
│   ├── modules
│   │   ├── *.py
│   ├── pages
│   │   ├── *.py
├── setup.sh
├── .gitignore
├── Dockerfile
├── entrypoint.sh
├── LICENSE
├── .env
├── README.md
├── requirements.txt
```


### .streamlit/config.toml
This file contains the configuration for the streamlit app. It is used to set the color schemes and fonts for the app.

### data
This contains the required data needed for the project. The data is downloaded from the s3 bucket using the command `python3 -m pypyr src/pipelines/dataset-download`


### embeddings
This contains the embeddings for the project. The embeddings are generated from the dataset downloaded from the s3 bucket and saved as pickle files.

### scraper
This contains the code for the scraper used to scrape the data from the web and also the data automation pipeline. The scraper is written in python and the pipeline is automated using Apache Airflow.

### src
This contains the source code for the project. The source code is divided into the following subdirectories:
- pipelines
- notebooks
- modules
- pages

#### src/pipelines
This contains the code for the data automation pipeline. This downloads the data saved to the s3 bucket by the scraper and saves it to the data directory.

#### src/notebooks
This contains the notebooks used for data analysis and model training. And also every notebook used at every stage of the project is contained here.

#### src/modules
This contains the modules used for the project. The modules folder contains files that have classes and functions that are used in the project.:
- **Chatbot.py:** This contains the Chatbot class that is responsible for interacting with the chatbot system. It serves as the interface between the chatbot and the rest of the system. It comprises of a chat agent responsible for generating responses to the users queries.

- **embedder.py:** This contains the Embedder class that is responsible for generating the embeddings for the dataset. It also serves as the interface between the embeddings and the rest of the system. As the embeddings are generated only once, the Embedder class is used to load the embeddings from the pickle files.

- **history.py:** This contains the History class that is responsible for storing the chat history of the users interaction with the chat agent. It also serves as the interface between the chat history and the rest of the system.

- **layout.py:** This contains the Layout class that is responsible for the layout of the chatbot system. It is responsible for the application layout and design.

- **pricing_hist.py:** This contains the PricingHist class that is responsible for generating the pricing history of the user. It also serves as the interface between the pricing history and the rest of the system. It stores information about the users interaction with the pricing chat agent.

- **sidebar.py:** This contains the Sidebar class that is responsible for the sidebar of the chatbot system. It is responsible for the sidebar layout and design.

- **utils.py:** This contains the Utils class that is responsible for the utility functions used in the project. It contains helper functions that are used in the project.

#### src/pages
This contains the code for the pages of the chatbot system. This contains the pages for the chatbot application. It consists of the following files:
- **feedback.py** This contains the code for the feedback page of the chatbot system. It is responsible for the feedback page layout and design. It allows the users send feedback to the developers of the chatbot system on what changes they feel can be made to improve the system.

- **housing.py** This contains the code for the housing page of the chatbot system. It allows the users interact with the chatbot system to get housing recommendations.

- **pricing.py** This contains the code for the pricing page of the chatbot system. It allows the users interact with the chatbot system to get pricing recommendations.

- **new_pricing.py**: This contains the code for the new pricing page of the chatbot system. It allows the users enter the fields of the type of house requirements they want and get a pricing recommendation from the application.


### setup.sh
This is a shell script that is used to setup the streamlit configuration file.

### .gitignore
This contains the files and directories that are ignored by git.

### Dockerfile
This contains the docker configuration for the project. It is used to build the docker image for the project.

### entrypoint.sh
This is a shell script that is used to run the docker image for the project.

### requirements.txt
This contains the dependencies for the project. It is used to install the dependencies for the project. The command `pip install -r requirements.txt` is used to install the dependencies for the project.
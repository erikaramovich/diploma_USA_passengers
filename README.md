# diploma_USA_passengers
Time Series Analysis: A Case Study of U.S. Domestic Air Passenger Volumes
Time Series Analysis: A Case Study of U.S. Domestic Air Passenger Volumes

## 📊 Thesis Project

This project focuses on the analysis of time series data based on domestic air passenger traffic in the United States. The main emphasis is on visual and heuristic data analysis: identifying trends, seasonality, and anomalies using linear approximations and graphical representations. The work is presented through text reports (.txt), charts (.png), and final documentation (.pdf).

## 📁 Repository Structure
- **main.py** -: Primary script orchestrating data processing and analysis.

- **dataframe.py** : Handles data loading, manipulations and task implementations.

- **helper.py** : Logs are written to separate files for general information (log.log) and errors (error.log), with automatic rotation at 10 MB per file.

- **dot_2016_2019.csv.gz** : Compressed dataset sourced from the U.S. Department of Transportation.

- **AnswersResults/** : Directory saving plots and information about dataset's samples.

- **logger/** : Directory storing log files generated during execution.

- **requirments.txt** : Lists Python dependencies required to run the project.

- **README.md** : Provides an overview and guidance on the project.


## 📊 Dataset Description
The dataset encompasses domestic flight records in the U.S. from 2016 to 2019, detailing:

- **origin**: Departure airport code (e.g., "JFK").

- **destination**: Arrival airport code.

- **year**: Year of the flight.

- **month**: Month of the flight.

- **passengers**: Number of passengers on the flight.

- **seats**: Total available seats on the flight.


## 🧰 Technologies Used
- **Python** : 3.12.3

- **Pandas** : Data manipulation and analysis.

- **Matplotlib** : Data visualization.

- **Loguru** : Simplified logging.

- **Inquirer** : Command line selector menu.

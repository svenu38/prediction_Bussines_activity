# Predicting Business Process Activity with Deep Learning Techniques
## Master thesis project for Physics of Data degree at University of Naples fedaricco II.

**Author**: venu siddapura govindaraju

**Project Summary**: For my Master degree thesis, I developed a project involving the prediction of ongoing business process instances' attributes, using deep learning techniques. The project uses `Keras API` to build neural networks with different types of inputs and outputs. The project involves a real-world based P2P dataset simulation, the preprocessing of the data along with the instances encoding, the experiments conducted and a real-world application of the models' results.

**Abstract**: The ability to predict the next activity or attributes of an ongoing case is becoming increasingly important in today’s businesses. Processes need to be monitored in real-life time to predict the remaining time of an open case, or to be able to detect and prevent anomalies before they have a chance to impact the performances. Moreover, financial regulations and laws are changing, requiring companies' processes to be increasingly transparent. Process mining, supported by deep learning techniques, can improve the results of internal audit activities. The task of predicting the next activity can be used to point out traces at risk that need to be monitored. In this way, companies are aware of the current state of operations and can take resolution actions in time. In recent years, this problem has been tackled using deep learning techniques, such as Convolutional Neural Networks (CNN), Recurrent Neural Networks (RNN) and Long Short-Term Memory (LSTM) neural networks, achieving consistent results.
The first main contribution of this thesis consists of a generation of a process mining dataset based on the Purchase-to-Pay (P2P) process. The SAP tables structure is taken into account since it is the most popular management software in today's companies. By introducing anomalies, the simulated dataset can be seen as a realistic representation of a company's operational activities.
The second contribution of the thesis is an investigation of deep learning techniques that exploit information from both temporal data and static features, applied to the previously generated dataset. The neural networks are then used to predict future events characteristics of running traces.
Finally, we discuss real-life application of the results and present future work proposals.



### Project structure
The project is structured as follows:
- `script/`:
  - `anomaly_function.py`: definition of the anomalies function created.
  - `data_generation.py`: script for the generation of new data anomaly-free.
  - `requirements_dll.py`: requirements for the deep learning module.
  - `requirements.py`: general requirements and functions.
  - `script_errori.py`: script for the anomalies creation.

- Jupyter notebooks:
  - `first_data.ipynb`: creates the first set of data.
  - `new_data.ipynb`: notebook for the creation of new data on a daily base.
  - `download_dataframe.ipynb`: download of the activity table / event log.
  - `DL/full_process.ipynb`: preprocessing, model creation and model fitting.
  - `DL/prediction_suffix.ipynb`: suffix prediction using models created.
  - `DL/prediction.ipynb`: next timestep attributes prediction using models created.

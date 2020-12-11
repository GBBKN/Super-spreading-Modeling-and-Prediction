# Super-spreading Modeling and Prediction

This project developed an improved epidemic compartment model based on the SEIR model. Further, fitted the model to the COVID-19 dataset and estimated the peak. Additionally, tested the impact of different restriction policies.

## Installation and Setup

1. Download and install [Anaconda](https://www.anaconda.com/products/individual).
2. Download and install [MATLAB](https://www.mathworks.com/products/matlab.html).
3. Unzip the project zip file.

## Project Structure

* curve_fitting_test.ipynb: Curve fitting for reproduction rate (R).
* SEIR_model.m: Baseline of the SEIR compartment model.
* modified_SEIR.ipynb: The SEIR compartment model with super-spreader / super-spreading events.
* SEIR_modified_policy_model.m: The SEIR compartment model with the effect of restriction policies.
* SEIR_modified_ss_d_p.m: The SEIR compartment model with the combination of super-spreader & effect of restriction policies.
* simu_test.py: Simulation on large-scale contact network.

## Project Workflow

1. Calculate the reproduction rate (R) using curve_fitting_test.ipynb.
2. Based on different goals, execute different versions of the modified_SEIR model.
3. Simulation on large-scale contact network requires additional dataset which is not included due to enormous file size. Please contact the authors for a sample data file if interested.

## Authors

* Jingyi Zhang <jingyi19@vt.edu>
* Ming Cheng: <ming98@vt.edu>

## Acknowledgments

* [Hoda Eldardiry](http://people.cs.vt.edu/hdardiry/)
* [Jiaying Gong](https://sites.google.com/vt.edu/jiaying-gong/home)
* [Vasanth Reddy Baddam](https://vbaddam.github.io/website/)

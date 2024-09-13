# wf-ModiDeC (Part 1: data curation)

## Introduction
In this directory you find part 1 of the code from ModiDec. The scripts located in ./bin facilitate the data curation. ...

### Functionality Overview
Below is a graphical overview of suggested routes through the pipeline depending on the desired output.

[image]

## Issues to be fixed
- Solving conda environment failed on MacOS M1
- 

## Questions: 
- How does the matching between the pod5 and the bam file work? Based on name? if so on which part of the name? etc.


## Quick Start
Test run the code:

1. Install [`Miniconda`](https://conda.io/miniconda.html)

2. Download the pipeline from Github
    ```bash
    git clone https://github.com/Nanopore-Hackathon/wf-modidec_data-curation.git
    ```

3. Install and activate conda environemnt
    ```bash
    conda env create -f ./envs/remora_TF2_env.yml
    conda activate remora_TF2
    ```

4. Start running the data curation by using the following command 
    ```bash
    python ./bin/Resquigle_remora_GUI.py
    ```


## Hackathone Tasks
Key aim: Convert the scripts into a Nextflow pipleine compatible with Epi2Me.

Main Tasks: 
1. Get your system up and ready
    - Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=23.10.0`)

    - Install [`Docker`](https://conda.io/miniconda.html)

    - Install [`Epi2Me Desktop`](https://labs.epi2me.io) (v5.1.14 or later)

    - Clone the Github repository (we recommend the GitHub Desktop client)

2. Translate the functions and logic into Nextflow processes and ultimately a Nextflow pipeline

3. Convert the GUI into nextflow_schema.json format

4. Containerise and deploy the Coda evenvirnemnet using Docker

5. Test and debug pipeline in Epi2Me using test data


## Credits & License

This code is provided by Dr. Nicolo Alagna and the Computational Systems Genetics Group of the University Medical Center of Mainz. © 2024 All rights reserved.

For the purpose of the Nanopore Hackathon, participants and collaborators of the event are granted a limited, non-exclusive, non-transferable license to use and modify the Applications for their intended purpose during the Time of the Event. Any further unauthorized reproduction, distribution, modification or publication of the Applications or their contents violates intellectual property rights and is strictly prohibited. For more please see the [Terms and Conditions](https://drive.google.com/file/d/18WN3YRoY9YvpYq6RCtwUQre-VAbN7jH6/view?usp=sharing) of the event.

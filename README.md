# wf-modidec_part1_data-curation

## Introduction
In this directory you find part 1 of the code from ModiDec. The scripts located in ./bin facilitate the data curation. ...

### Functionality Overview
Below is a graphical overview of suggested routes through the pipeline depending on the desired output.

[image]

## Quick Start
Test run the code:

1. Install [`Miniconda`](https://conda.io/miniconda.html)

2. Download the pipeline from Github

3. Start running the data curation by using the following command 


## Hackathone Tasks
Key aim: Convert the scripts into a Nextflow pipleine compatible with Epi2Me.

1. Get your system up and ready
    - Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=23.10.0`)
    - Install [`Miniconda`](https://conda.io/miniconda.html)

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

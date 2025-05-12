# ModiDec - RNA modification detector and classifier
ModiDeC is a customizable neural network to identify RNA modifications from Oxford Nanopore Technology (ONT) based direct RNA sequencing data. ModiDeC combines LSTM and newly designed inception-res-net blocks for multi-modification-classification. ModiDec is composed of three Epi2ME integratable tools (data curation, network training and analysis). It allows researchers to train the multi-modification-classification model on synthetic RNA strands mimicking physiologically relevant motifs and modification patterns on transcripts of interest. The latter can be utilized to investigate modification ratios of transcripts derived from physiological data. During the data curation step of ModiDec, data derived from ONT based direct RNA sequencing experiments (RNA002 or RNA004) can be preprocessed to suit the succeeding model training step. During model training the network can be trained on the preprocessed data to optimally learn motif and modification patterns of the transcript of interest. The trained model can then be used in the analysis step of ModiDec to investigate modification ratios in physiological derived data.

![Modidec schema](./figures/ModiDec_Epi2ME_schema.png)


Here the data curation part is implemented. Please visit [wf-modidec_training](https://github.com/Nanopore-Hackathon/wf-modidec_training) and [wf-modidec_analysis](https://github.com/Nanopore-Hackathon/wf-modidec_analysis) to find the complete toolset. 
During Data curation the input pod5 files will be bascalled, aligned and preprocessed to create npz files, which can be directly used for training.


## Requirements

Install dependencies on your system:
   -  Install [`Epi2Me Desktop`](https://labs.epi2me.io) (v5.1.14 or later)
   -  Install [`Miniconda`](https://conda.io/miniconda.html)
   -  Install [`Docker`](https://conda.io/miniconda.html)
   -  Install [`Nextflow`](https://www.nextflow.io/docs/latest/getstarted.html#installation) (`>=23.10.0`)
   -  Install samtools and minimap
   -  Make sure your [nvidia GPU drivers](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/#ubuntu-installation) are installed and functional.
   -  Install the [nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html) to enable GPU usage from within a docker container. 

Import the workflow in Epi2Me:
   -  Open Epi2Me
   -  Navigate to Launch
   -  Click on import workflow -> Import from Github
   -  Paste https://github.com/Nanopore-Hackathon/wf-modidec_data-curation into the Edit line
   -  Click on Download
   -  The repository should now appear on the workflow list in Launch


## Instructions for data curation

### Preparation
Before you use the data curation step prepare a reference fasta file containing only a single transcript of interest.
Navigate to Launch on Epi2Me and click on the wf-modidec_data-curation workflow. Press Launch on the right side of the page and you will be linked to the menu. 

Define the following variables:

### Input Parameters
1. Do you want to run basecalling + alignment ? (Usually only needed if the data hasnt been basecalled and aligned to the template of interest before)
2. Pod5 folder
3. Bam file (Only necessary if basecalling + alignemnt has already been performed.) 
3. Reference fasta
4. Output directory
5. Flowcell type ("RNA002" or "RNA004")
6. Curation type ("Training" or "Analysis")

### Data Parameters
1. Map the modification / region of interest on your construct ? (Usually: Yes, Should be also yes if your construct is unmodified. Since the curation procss will focus on the region of interest in that case.)
2. Is your construct modified ?
3. Which name should your output files have ? (Variable: Training Output Directory)
4. Define a modification dictionairy: (Variable: Modification Dictionary, Default -> "Gm m6A Ino Psi", This dictionairy defines the different types of modifications introduced during training and should be the same for all training instances the model will be trained with.)
5. Define which modification your construct carries. (Variable: Modification Type, Default: "Gm", Can be extended to use several bases e.g. "Gm Gm m6A Ino", If you have unmodified data you should still mention the modification type of your modification you are comparing the data to.)
6. At which position on your reference transcript is the modification position or what is the region of interest in the unmodified data ? (Variable: Location of Modification,Default: "92", Can be extended to match the position of the modified bases above e.g "92 93 100 101",If you have unmodified data you should still mention the positions of modified bases in your modified data to extract data from similar positions.)


### Segmentation Parameters
1. How many chunks should be included into a single output file in .npz format? (Variable: Batch size, Default: 16)
2. Which bamfile entries should be taken ? This options enbales the user to extract a resonable amount of training data for a given construct.
   - Define start index on bamfile (Variable: Start index on bamfile, Default: 0)
   - Define end index on bamfile (Variable: End index on bamfile, Default: 10000)
  
After you chose the parameters for data curation click on Launch to start the process.


### Data Output

When using Curation Type Training the defined output folder will conatin:
1. pod5 files
2. bam files including move table and MD flags
3. Files in npz format containing tensors for the network training

When using Curation Type Analysis:
1. pod5 files
2. bam files including move table and MD flags






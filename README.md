# Modidec - RNA modification detector and classifier
ModiDeC is a customizable neural network to identify RNA modifications from Oxford Nanopore Technology (ONT) based direct RNA sequencing data. ModiDeC combines LSTM and newly designed inception-res-net blocks for multi-modification-classification. ModiDec is composed of three Epi2ME integratable tools (data curation, network training and analysis). It allows researchers to train the multi-modification-classification model on synthetic RNA strands mimicking physiologically relevant motifs and modification patterns on transcripts of interest. The latter can be utilized to investigate modification ratios of transcripts derived from physiological data. During the data curation step of ModiDec, data derived from ONT based direct RNA sequencing experiments (RNA002 or RNA004) can be preprocessed to suit the succeeding model training step. During model training the network can be trained on the preprocessed data to optimally learn motif and modification patterns of the transcript of interest. The trained model can then be used in the analysis step of ModiDec to investigate modification ratios in physiological derived data.

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
Before you use the data curation step make sure you basecalled your data and in the following align your data to a fasta file contianing only the transcript of interest. Make sure you set all necessary flags.
Use the following command:

```bash
dorado basecaller sup path_to_folder/*.pod5 --emit-moves |
samtools fastq -T "*" | minimap2 -y --MD -ax map-ont path_to_reference/single_trancript_reference.fasta - |
samtools view -b -F 4 > output_name.bam
```

Once you finished the alignment the data curation can be performed. Navigate to Launch on Epi2Me and click ont wf-modidec_data-curation.
Define the following variables:

### Input Parameters
1. pod5 folder 
2. reference fasta
3. output directory
4. flowcell type ("RNA002" or "RNA004")
5. Curation type ("Training" or "Analysis")

### Data Parameters
1. Map a modification on your construct ? (Usually: Yes, Should be also yes if your construct is unmodified. Since the network training will focus on a specific region.)
2. Is your construct modified ?
3. Do you want to use the modified region for data training ? (Usually: Yes. Will create data chunks around the region of interest)
4. Which name should your output files have ? (Variable: Training Output Directory)
5. Define a modification dictionairy: (Variable: Modification Dictionary, Default -> "Gm m6A Ino Psi", This dictionairy defines the multiple modicifaction classification space and should be the same for all training instances the model will be trained with.)
6. Define which modification your construct carries. (Variable: Modification Type, Default: "Gm", Can be extended to use several bases e.g. "Gm Gm m6A Ino", If you have unmodified data you should still mention the modification type of your modified data to extract data from similar positions.)
7. At which position on your reference transcript is the modification positioned ? (Variable: Location of Modification,Default: "92", Can be extended to match the position of the modified bases above e.g "92 93 100 101",If you have unmodified data you should still mention the positions of modified bases in your modified data to extract data from similar positions.)
8. Do you want to add some chunks around you modification position to create some unmodified examples in the sorroundings ? (Variable: Number of Bases before Modification) 


### Segmentation Parameters
1. How many chunks should be included into a single output file in .npz format? (Variable: Batch size, Default: 16)
2. How many bases at maximum should a single datachunk cover on your reference transcript ? (Variable: Maximum sequence length, Default: 40)
3. What is the chunksize (current measurements over time) of the networks receptive field/sliding window? (Variable: Number of chunks, Default: 400)
4. In which range should the sliding window move over the data ? (Variable: Time shift, Default: 25)
5. Which bamfile entries should be taken ? This options enbales the user to extract a resonable amount of training data for a given construct.
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






#%%
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLineEdit, QLabel, QHBoxLayout, QCheckBox
from Remora_resquigle_generate_data import Remora_resquigle_Generation_data # Essential function to be loaded
import json
import os

class MainWindow(QMainWindow):  # Define content of the GUI window (Main Windiw class)
    def __init__(self): # Initialize the class self
        super().__init__()  # Call the parent class constructor

        # list of input variables
        ## folder1: pod5 file folder (required)
        ## folder2: bam file folder (required)
        ## folder3: save path (required)
        ## folder5: kmer-level table file (required) -> RNA004 or RNA002 -> should be linked to a hardcode path to the ONT website https://github.com/nanoporetech/kmer_models

        self.paths = {"folder1": None, "folder2": None, "folder3": None, "file1": None}

        # Set up the main window
        self.setWindowTitle('Remora Resquigle - Generata training data for NN') # Set the window title
        self.setGeometry(100, 100, 320, 100) # Set the window dimensions

        # Create a QWidget and set it as the central widget
        self.central_widget = QWidget() # Create a central widget
        self.setCentralWidget(self.central_widget) # Set the central widget

        # Create a vertical layout
        layout = QVBoxLayout()

        # Create buttons and add them to the layout
        # Buttons open dialogs to choose directories
        self.button1 = QPushButton('Pod5 file folder')
        self.button1.clicked.connect(lambda: self.open_directory_dialog('folder1')) 
        layout.addWidget(self.button1)

        self.button2 = QPushButton('bam file folder')
        self.button2.clicked.connect(lambda: self.open_directory_dialog('folder2'))
        layout.addWidget(self.button2)

        self.button3 = QPushButton('Save path')
        self.button3.clicked.connect(lambda: self.open_directory_dialog('folder3'))
        layout.addWidget(self.button3)

        self.button4 = QPushButton('kmer-level table file')                                
        self.button4.clicked.connect(lambda: self.open_filename_dialog('file1'))
        layout.addWidget(self.button4)

        # set the first set of variables
        textbox1 = QLabel("General variables for training data:") # Create a label
        layout.addWidget(textbox1) # Add the label to the layout
        self.setup_variables(layout) # Create the input widgets for the variables

        # set the second set of variables
        textbox1 = QLabel("segmentation variables for training data:") # Create a label
        layout.addWidget(textbox1) # Add the label to the layout
        self.setup_variables_segmentation(layout) # Create the input widgets for the variables

        # Create buttons and add them to the layout
        self.button4 = QPushButton('Start resquigle') # Create a button to star the process
        self.button4.clicked.connect(lambda: self.start_resquigle()) # Connect the button to the start_resquigle function
        layout.addWidget(self.button4) # Add the button to the layout

        # Set the layout on the central widget
        self.central_widget.setLayout(layout)


    """ list of function used in the main"""

    # Fuction to open a dialog to choose a directory
    def open_directory_dialog(self, folder_name):
        """
        Open a dialog to choose a directory and save the path in the paths variable
        """
        # Open a dialog to choose a directory
        directory = QFileDialog.getExistingDirectory(self, f"Select {folder_name}")
        if directory:
            self.paths[folder_name] = directory
            print(f"Selected path for {folder_name}: {directory}")

    # Function to open a dialog to choose a file
    def open_filename_dialog(self, file_type):
        """
        Open a dialog to choose a file and save the path in the paths variable    
        """
        # Open a dialog to choose a file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly                                                        
        file_name, _ = QFileDialog.getOpenFileName(self, f"Select {file_type}", "", "All Files (*);;FASTA Files (*.fasta)", options=options)        
        if file_name:
            self.paths[file_type] = file_name
            print(f"Selected path for {file_type}: {file_name}")

    # Function to set up the input widgets for the variables
    def setup_variables(self, layout):
        """
        The following variables are collected: 

        mod_mapping or basecalling? -> Remove selection option for the Epi2Me implementation. Should always be mod_mapping as the default string (str) -> Default: 'mod_mapping'
        modified_data? (bool) -> Do the reads contain modified bases or not? -> Value options: Yes or No, Default: Yes
        take_modifed_region? (bool) -> Will create chucks around mofication position -> Value options: Yes or No, Default: Yes
        name_save_file (str) -> Name of the output file -> Default: 'modified_data'
        Save long reads? (bool) -> Should be removed  !!
        what type of modification? (str) ->  A letter linked to modoification dictornary -> Values from the dictornary -> Default: 'M'
        modification pos. (int) -> Position of the modification in the reference sequence -> Default for sample data: 92
        Bases before modfication (int) -> If you want you can take more bases to the left or right from your modification position -> Default: 0
        modification dictionary (str) -> A dictionary with the modification information, alternative basenames for modified bases -> Default: '{"G":2, "M":3, "I":4, "P":5}' , M=m6A, G=Gm, I=Inosine, P=Pseudouridine
        """
        # Creating layout and widgets for each variable in Variables tuple
        labels = ["mod_mapping or basecalling?", "modified_data? (bool)", 
                  "take_modifed_region? (bool)", "name_save_file (str)", 
                  "Save long reads? (bool)", "what type of modification? (str)", 
                  "modification pos. (int)", "Bases before modfication (int)", "modification dictionary (str)"]
        
        self.vars_entries = [] 
        for i, label in enumerate(labels):
            row_layout = QHBoxLayout()
            label_widget = QLabel(label + ":")
            input_widget = QLineEdit()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_widget)
            layout.addLayout(row_layout)
            self.vars_entries.append(input_widget)

    # Function to set up the input widgets for the segmentation variables
    def setup_variables_segmentation(self, layout):
        """
        The following variables are collected: 
        
        batch size (int) -> Number of chunks saved per file (int) -> Default: 16
        max seq. length (int) -> Maximum number of base that a chunk can have (int) -> Default: 40
        chunk length (int) -> Defines how many timepoints to inlude within a sliding window (int) -> Default: 400
        shift in time (int) -> How many timpoint to shift your sliding window to create annew represntation of the modification chunk -> Default: 25
        start read number (int) -> Select the start entry from the bam file -> Default: 0 
        end read number (int) -> Select the end entry from the bam file -> Default: 1000
        """
        labels_segmentation = ["batch size (int)", "max seq. length (int)", 
                               "chunk length (int)", "shift in time (int)", 
                               "start read number (int)", "end read number (int)"]
        
        self.segmentation_entries = []
        for label in labels_segmentation:
            row_layout = QHBoxLayout()
            label_widget = QLabel(label + ":")
            input_widget = QLineEdit()
            row_layout.addWidget(label_widget)
            row_layout.addWidget(input_widget)
            layout.addLayout(row_layout)
            self.segmentation_entries.append(input_widget)

    # Function to start the resquigle process | Key part of the code
    def start_resquigle(self):

        #level_table_folder = self.paths["file1"]
        #level_table_list = os.listdir(level_table_folder) #maybe to change to read the file and not the folder                
        #level_table_file = level_table_folder + "/" + level_table_list[0]

        # Assign the stored paths and files to local variables
        level_table_file = self.paths["file1"]                                                
        save_path = self.paths["folder3"]                                                      
        pod5_folder = self.paths["folder1"]
        bam_folder = self.paths["folder2"]
        bam_list = os.listdir(bam_folder)

        # initialize the variables var1_bool, var2_bool, var3_bool                            
        var1_bool = [] # corresponding to the question modified_data?                          
        var2_bool = [] # corresponding to the question take_modifed_region?
        var3_bool = [] # corresponding to the question save long reads?

        # Check if the input is yes or Yes and set the boolean value accirdingly -> True or False
        if self.vars_entries[1].text() == "yes" or self.vars_entries[1].text() == "Yes":
            var1_bool = True
        else:
            var1_bool = False

        if self.vars_entries[2].text() == "yes" or self.vars_entries[2].text() == "Yes":
            var2_bool = True
        else:
            var2_bool = False

        if self.vars_entries[4].text() == "yes" or self.vars_entries[4].text() == "Yes":
            var3_bool = True
        else:
            var3_bool = False

        # Create a tuple with the variables
        Variables = (self.vars_entries[0].text(), 
                     var1_bool, #bool, 
                     var2_bool, #bool, 
                     self.vars_entries[3].text(), 
                     var3_bool, #bool, 
                     self.vars_entries[5].text(),
                     int( self.vars_entries[6].text()), 
                     int( self.vars_entries[7].text())
                     )

        # Create a dictionary with the modification dictionary
        mod_dictionary = json.loads(self.vars_entries[8].text())

        # Create a tuple with the segmentation variables
        variables_segmentation = (int( self.segmentation_entries[0].text()), 
                                  int( self.segmentation_entries[1].text()), 
                                  int( self.segmentation_entries[2].text()), 
                                  int( self.segmentation_entries[3].text())
                                  )

        # Create a tuple with the indexes from the segmentation variables
        Indexes = (int( self.segmentation_entries[4].text()),
                    int( self.segmentation_entries[5].text()))

        # Print the variables
        print(mod_dictionary)
        print(Variables)
        print(variables_segmentation)
        print(Indexes)
         
        # Run the Remora_resquigle_Generation_data function for each bam file 
        for i in range (len(bam_list)):

            # assign the path of an individual bam file to the bam_file variable
            bam_file = bam_folder + "/" +  bam_list[i]
            
            # call the Remora_resquigle_Generation_data function with the input variables for a selected bam file
            Remora_resquigle_Generation_data(pod5_folder, bam_file, 
                                             level_table_file, save_path,
                                             Variables, variables_segmentation, 
                                             Indexes, mod_dictionary, i)

        # Report that the process is finished 
        print("Resquigle finished")                     

# Function to run the GUI
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

# Run the GUI
if __name__ == '__main__':
    main()
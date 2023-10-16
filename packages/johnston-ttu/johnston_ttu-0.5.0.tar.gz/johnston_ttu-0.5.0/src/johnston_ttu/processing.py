from os import listdir, remove
import numpy as np
import pandas as pd
"""
processing.py
Developed By: Derek Johnston @ Texas Tech University

Special-purpose functions for data cleaning and pre-processing.
"""
def remove_ena_labels(filename):
	"""
	The Keysight ENA creates two extra lines of metadata at the 
	top of a measurement .CSV file. These should be removed so
	that datafiles can be imported into Pandas.
	
	Keyword Arguments:
	filename -- the file name (and path) to the .CSV to be cleaned.
	"""
	line_buffer = [] # Pull each line out of the file, and write back all but the last two.
	with open(f"{filename}.csv", "r") as fp:
		line_buffer = fp.readlines()
	with open(f"{filename}_t.csv", "w") as fp:
		for number, line in enumerate(line_buffer):
			if number >= 2:
				fp.write(line)

def process_ena_data(directory):
	"""
	For a given directory containing raw ENA data, process the data and generate
	new columns for the complex value, magnitude, and phase information.

	Keyword Arguments:
	directory -- The folder containing the datafiles.
	"""
	# Get a list of all the datafiles in the given directory.
	directories = listdir(directory)
	# Iterate through all the files in the directory.
	for file in directories:
		# Remove the .csv tag from the end of the file.
		file = file.replace(".csv", "")
		file = file.replace(".CSV", "")
		# Remove the ENA metadata lines.
		remove_ena_labels(f"{directory}\{file}")
		# Read-in the temporary file as a pandas dataframe.
		df = pd.read_csv(f"{directory}\{file}_t.csv")
		df.rename(columns={" Formatted Data": "Real", " Formatted Data.1": "Imag"}, inplace=True)
		# Get the complex number for each frequency component.
		df["Complex"] = [complex(df["Real"][idx], df["Imag"][idx]) for idx in df.index]
		# Get the magnitude and phase for each row of the dataframe.
		df["Magnitude"] = np.abs(df["Complex"].to_numpy())
		df["Phase"] 		= np.unwrap(np.angle(df["Complex"].to_numpy()))
		# Add the new processed file
		df.to_csv(f"{directory}_p\{file}.csv")
		# Remove the temporary data file.
		remove(f"{directory}\{file}_t.csv")
	
def compile_ena_data(data):
	"""
	For a given data directory, compile the magnitude and phase 
	data for each sample into separate directories.

	Keyword Arguments
	data -- The directory containing the dataset.

	Returns
	magnitudes -- A DataFrame containing the magnitude measurements.
	phases -- A DataFrame containing the phase measurements.
	"""
	# Store the magnitudes and phases of each sample in a dataframe.
	magnitudes 	= pd.DataFrame()
	phases			= pd.DataFrame()
	# Iterate through each data file in the processed data directory.
	isFirst = True
	for filename in listdir("data_p"):
		df = pd.read_csv(f"data_p\{filename}")
		if isFirst:
			""" The first time through, get the frequency data."""
			magnitudes["Frequency"] = df["Frequency"]
			phases["Frequency"] = df["Frequency"]
			isFirst = False

		magnitudes[filename.replace(".csv", "")] = df["Magnitude"]
		phases[filename.replace(".csv", "")] 		= df["Phase"]

	return magnitudes, phases

def snr_analysis(data):
	"""
	For a given data directory, perform the SNR analysis and store
	the results in a .csv file.
	"""
	# Compile the dataset
	magnitudes, phases = compile_ena_data("data_p")
	## Calculate the mean, stdev, snr, and cv
	# Magnitudes
	magnitudes["Mean"] 	= magnitudes.drop("Frequency", axis=1).mean(axis=1)
	magnitudes["STD"]		= magnitudes.drop("Frequency", axis=1).std(axis=1)
	magnitudes["SNR"]		= 20 * np.log(np.abs(magnitudes["Mean"] / magnitudes["STD"]))
	magnitudes["CV"]		= 100 * magnitudes["STD"] / magnitudes["Mean"]

	phases["Mean"]	= phases.drop("Frequency", axis=1).mean(axis=1)
	phases["STD"]		= phases.drop("Frequency", axis=1).std(axis=1)
	phases["SNR"]		= 20 * np.log(np.abs(phases["Mean"] / phases["STD"]))
	phases["CV"]		= 100 * phases["STD"] / phases["Mean"]

	# Compute the summary statistics about the SNR and CV
	print(100*"=")
	print("SUMMARY STATISTICS: Signal to Noise Analysis")
	print(100*"=")
	print("Magnitudes:")
	print(f"Mean SNR = {np.round(np.mean(magnitudes['SNR']), 1)} dB")
	print(f"Standard Deviation = {np.round(np.std(magnitudes['SNR']), 1)} dB")
	print(f"Maximum SNR = {np.round(np.max(magnitudes['SNR']), 1)} dB at {int(magnitudes['Frequency'][np.argmax(magnitudes['SNR'])])} Hz")
	print(f"Minimum SNR = {np.round(np.min(magnitudes['SNR']), 1)} dB at {int(magnitudes['Frequency'][np.argmin(magnitudes['SNR'])])} Hz")
	print("")
	print("Phases:")
	print(f"Mean SNR = {np.round(np.mean(phases['SNR']), 1)} dB")
	print(f"Standard Deviation = {np.round(np.std(phases['SNR']), 1)} dB")
	print(f"Maximum SNR = {np.round(np.max(phases['SNR']), 1)} dB at {int(phases['Frequency'][np.argmax(phases['SNR'])])} Hz")
	print(f"Minimum SNR = {np.round(np.min(phases['SNR']), 1)} dB at {int(phases['Frequency'][np.argmin(phases['SNR'])])} Hz")
	print("")
	print(100*"=")
	print("SUMMARY STATISTICS: Coefficient of Variance")
	print(100*"=")
	print("Magnitudes:")
	print(f"Mean CV = {np.round(np.mean(magnitudes['CV']), 1)} dB")
	print(f"Standard Deviation = {np.round(np.std(magnitudes['CV']), 1)} dB")
	print(f"Maximum CV = {np.round(np.max(magnitudes['CV']), 1)} dB at {int(magnitudes['Frequency'][np.argmax(magnitudes['CV'])])} Hz")
	print(f"Minimum CV = {np.round(np.min(magnitudes['CV']), 1)} dB at {int(magnitudes['Frequency'][np.argmin(magnitudes['CV'])])} Hz")
	print("")
	print("Phases:")
	print(f"Mean CV = {np.round(np.mean(phases['CV']), 1)} dB")
	print(f"Standard Deviation = {np.round(np.std(phases['CV']), 1)} dB")
	print(f"Maximum CV = {np.round(np.max(phases['CV']), 1)} dB at {int(phases['Frequency'][np.argmax(phases['CV'])])} Hz")
	print(f"Minimum CV = {np.round(np.min(phases['CV']), 1)} dB at {int(phases['Frequency'][np.argmin(phases['CV'])])} Hz")
	print("")
	print(100*"=")

	# Save the magnitude and phase dataframes
	magnitudes.to_csv("magnitudes.csv")
	phases.to_csv("phases.csv")
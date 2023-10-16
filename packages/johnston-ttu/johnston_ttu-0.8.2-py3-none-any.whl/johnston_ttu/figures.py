from os import listdir
import numpy 							as np
import pandas 						as pd
import matplotlib.pyplot 	as plt
"""
figures.py
Developed By: Derek Johnston @ Texas Tech University

Functions for generating common figures from experiments.
"""
def get_N_elements(values, N=6):
	"""for a given list, get N evenly spaced elements"""
	idx = np.round(np.linspace(0, len(values) - 1, 6)).astype(int)
	return values[idx]

def snr_magnitude():
	"""Generate a magnitude plot for a sample with SNR overlay."""
	# Read-in the results data
	magnitudes = pd.read_csv("magnitudes.csv", index_col="Frequency")
	idx = np.round(np.linspace(0, len(magnitudes["Mean"].to_list()) - 1, 6)).astype(int)
	xlabs = ["0", "100", "200", "300", "400", "500"]
	xtick = magnitudes.index.values[idx]
	## Generate the Bode plot
	fig, ax = plt.subplots(figsize=(10,6))
	ml = ax.plot(magnitudes["Mean"], color="black", linestyle="solid", label="Magnitude Response")
	ax.grid(visible=False)
	ax.set_xlim([50e3, 500e6])
	ax.set_ylim([0, 1])
	ax.set_ylabel("$|H(f)|$")
	ax.set_xlabel("Frequency (MHz)")
	ax.set_xticks(xtick, xlabs)
	ax_snr = ax.twinx()
	ax_snr.set_ylabel("dB", color="dimgrey")
	ax_snr.tick_params(axis="y", labelcolor="dimgrey")
	ax_snr.set_ylim([0, 120])
	snrl = ax_snr.plot(magnitudes["SNR"], linestyle="solid", color="grey", label="Signal-to-Noise Ratio")
	ls = ml + snrl
	labs = [l.get_label() for l in ls]
	ax.legend(ls, labs, frameon=False)

	plt.savefig("snr_magnitude.png")

def dilution_magnitude():
	"""Generate a magnitude plot of 10-fold dilution data"""
	# Read-in the results data
	magnitudes = pd.read_csv("magnitudes.csv", index_col="Frequency")
	# Get the columns and colors
	names = list(magnitudes.columns)
	colors = ["black", "lightgray", "darkgray", "gray", "dimgray", "black"]
	styles = ["dotted", "solid", "solid", "solid", "solid", "solid"]
	# Get the frequency ticks
	xticks = get_N_elements(magnitudes.index.values, 6)
	# Generate the figure
	fig, ax = plt.subplots(figsize=(10, 6))
	for name, color, style in zip(names, colors, styles):
		ax.plot(magnitudes[name], color=color, linestyle=style)
	ax.legend(["$0M$", "$15\mu M$", "$150\mu M$", "$1.5mM$", "$15mM$", "150mM"], frameon=False)
	ax.set_xticks(xticks, ["0", "100", "200", "300", "400", "500"])
	ax.set_xlabel("Frequency (MHz)")
	ax.set_xlim([50E3, 500E6])
	ax.set_ylim([0, 1])
	ax.set_ylabel("$|H(f)|$")
	plt.savefig("dilution_magnitude.png")

if __name__ == "__main__":
	dilution_magnitude()
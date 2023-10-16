import numpy as np
"""
helpers.py
Developed By: Derek Johnston @ Texas Tech University.

Helper functions for repetitive tasks.
"""
def get_N_elements(values, N=6):
	"""for a given list, get N evenly spaced elements"""
	idx = np.round(np.linspace(0, len(values) - 1, 6)).astype(int)
	return values[idx]
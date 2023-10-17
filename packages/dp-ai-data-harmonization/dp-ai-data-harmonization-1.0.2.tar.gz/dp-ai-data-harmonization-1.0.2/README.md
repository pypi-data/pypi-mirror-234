# Data Harmonization Package

This package provides functionality for file merging and data harmonization using various algorithms and AI models.
It allows you to merge CSV files and harmonize data based on a sample-based approach using GPT-based models.

## Installation

You can install the package from PyPI using pip:

	pip install data-harmonization-ai


## Usage

### DataHarmonizer Class

The `DataHarmonizer` class provides the capability to merge CSV files based on different options.
It supports the following merge options:

- ChatGPT
- GPT4
- Fuzzy Wuzzy
- Rapidfuzz
- Jaro Winkler
- JW Layered with ChatGPT
- JW Layered with GPT4
- FW Layered with GPT4
- Recursive Data Harmonization

Example usage:

from utility import DataHarmonizer

# Create an instance of DataHarmonizer
key='openai-key'
harmonizer = DataHarmonizer(key,'file1.csv', 'file2.csv', 'ChatGPT')

# Merge the files based on the specified option
result = harmonizer.merge_files()

print(result)

### DataHarmonizationWithSuggestion Class

# The DataHarmonizationWithSuggestion class allows you to harmonize data using a sample-based approach.
 It takes a sample file and two data files as input.

Example usage:
from utility import DataHarmonizationWithSuggestion

# Create an instance of DataHarmonizationWithSuggestion

key = 'openai-key'
harmonizer = DataHarmonizationWithSuggestion(key, "sample_harmonized_data.csv", "file1.csv", "file2.csv")

# Harmonize the data based on the sample
	result = harmonizer.harmonize_data()

print(result)

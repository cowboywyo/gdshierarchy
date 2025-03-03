# GDS Hierarchy Parser

This Python script reads a GDS file and generates a hierarchical tree of the cells (subcells) in the design. The hierarchy is saved as a text file with a timestamp in the filename. The script supports a customizable depth for the hierarchy and allows you to specify the top-level cell via a command-line argument.

## Features

- **GDS Parsing**: Uses the [`gdstk`](https://gdstk.readthedocs.io/) library to load and parse GDS files.
- **Hierarchy Tree Generation**: Recursively builds a hierarchy of cell instantiations, including instance names.
- **Customizable Depth**: Specify how many levels deep the hierarchy should display.
- **Output File**: Saves the hierarchy to a timestamped text file.

## Requirements

- Python 3.x
- [`gdstk`](https://gdstk.readthedocs.io/) library

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/cowboywyo/gdshierarchy.git


## Usage

Run the script with the following command-line arguments:

- **gds**: Path to the GDS file.
- **--top**: The name of the top-level cell in the GDS file.
- **--depth**: (Optional) The maximum number of hierarchy levels to display (default is 5).

### Example

```bash
python parse_gds_hierarchy.py my_design.gds --top TopCell --depth 4


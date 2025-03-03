#!/usr/bin/env python3
import argparse
import sys
import datetime
import gdstk

def parse_gds(file_path):
    """
    Reads the GDS file using gdstk and builds a dictionary mapping each cell
    name to a list of instantiations (tuples of instance name and subcell name)
    found in that cell.
    """
    # Read the GDS library
    library = gdstk.read_gds(file_path)
    cell_dict = {}
    # Iterate over all cells in the library
    for cell in library.cells:
        inst_list = []
        # Process each reference (instance) in the cell
        for i, ref in enumerate(cell.references, start=1):
            # GDS references typically do not have an explicit name,
            # so we generate one based on the parent cell name and index.
            instance_name = getattr(ref, "name", f"{cell.name}_inst{i}")
            # Get the referenced cell. Depending on the version, the attribute
            # may be 'ref_cell' or 'cell'.
            try:
                subcell = ref.ref_cell
            except AttributeError:
                subcell = ref.cell
            subcell_name = subcell.name if subcell is not None else "UNKNOWN"
            inst_list.append((instance_name, subcell_name))
        cell_dict[cell.name] = inst_list
    return cell_dict

def print_hierarchy(cell, cell_dict, depth=1, max_depth=5, visited=None, instance_name=None, out_f=sys.stdout):
    """
    Recursively prints the hierarchy tree starting from the given cell.
    Each line is formatted to show the cell name and, if available, the instance name in brackets.
    
    - For the top-level cell, only the cell name is printed.
    - The recursion stops when max_depth is reached.
    - A visited set is maintained to prevent infinite recursion in case of cycles.
    """
    if visited is None:
        visited = set()
    if depth > max_depth:
        return

    indent = "    " * (depth - 1)
    # For non-top-level, include the instance name in brackets
    if instance_name:
        print(f"{indent}|- {cell} ({instance_name})", file=out_f)
    else:
        # For the very first call (top-level), no prefix is needed.
        if depth == 1:
            print(f"{indent}{cell}", file=out_f)
        else:
            print(f"{indent}|- {cell}", file=out_f)

    # Add current cell to visited set to avoid cycles
    branch_visited = visited.union({cell})
    if cell in cell_dict:
        for inst_tuple in cell_dict[cell]:
            child_instance, child_cell = inst_tuple
            if child_cell not in branch_visited:
                print_hierarchy(child_cell, cell_dict, depth + 1, max_depth,
                                branch_visited, instance_name=child_instance, out_f=out_f)
            else:
                print("    " * depth + f"|- {child_cell} ({child_instance}) (cycle detected)", file=out_f)

def main():
    parser = argparse.ArgumentParser(
        description="Parse a GDS file and build a hierarchy table with customizable depth and instance names."
    )
    parser.add_argument("gds", help="Path to the GDS file")
    parser.add_argument("--top", required=True, help="Top-level cell name")
    parser.add_argument("--depth", type=int, default=5,
                        help="Number of hierarchy levels to display (default: 5)")
    args = parser.parse_args()
    
    # Build the hierarchy dictionary from the GDS file
    cell_dict = parse_gds(args.gds)
    top_cell = args.top
    if top_cell not in cell_dict:
        print(f"Error: Top cell '{top_cell}' not found in the GDS file.")
        sys.exit(1)
    
    # Generate an output filename with current date and time
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"hierarchy_{current_time}.txt"
    
    with open(output_filename, "w") as out_f:
        print("Hierarchy:", file=out_f)
        print(top_cell, file=out_f)
        # Print the children of the top-level cell, if any
        if top_cell in cell_dict:
            for inst_tuple in cell_dict[top_cell]:
                child_instance, child_cell = inst_tuple
                print_hierarchy(child_cell, cell_dict, depth=2, max_depth=args.depth,
                                visited={top_cell}, instance_name=child_instance, out_f=out_f)
    
    print(f"Hierarchy saved to {output_filename}")

if __name__ == "__main__":
    main()

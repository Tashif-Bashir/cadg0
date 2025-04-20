import os
import clang.cindex

# Set the path to Clang
clang.cindex.Config.set_library_file("/usr/lib/llvm-18/lib/libclang.so")

def is_user_defined(node):
    """Check if the node belongs to user code (not system headers)."""
    if node.location.file and "usr/include" not in node.location.file.name:
        return True
    return False

def is_relevant_kind(node_kind):
    """Filter out only relevant C++ elements (classes, structs, methods)."""
    return node_kind in [
        clang.cindex.CursorKind.CLASS_DECL,       # Classes
        clang.cindex.CursorKind.STRUCT_DECL,      # Structs
        clang.cindex.CursorKind.CXX_METHOD,       # Methods
        clang.cindex.CursorKind.CONSTRUCTOR,      # Constructors
        clang.cindex.CursorKind.DESTRUCTOR,       # Destructors
        clang.cindex.CursorKind.FIELD_DECL        # Class/Struct Fields
    ]

def is_standard_library(node):
    """Check if a node is part of the C++ standard library (e.g., std::vector, std::string)."""
    if node.spelling.startswith("std::") or node.spelling in ["allocator", "char_traits", "string", "vector", "iostream"]:
        return True
    return False

def parse_cpp_file(file_path):
    """Parses a single C++ file and extracts relevant user-defined structures."""
    index = clang.cindex.Index.create()
    args = ['-std=c++11', '-I/usr/include', '-I/usr/local/include']  # Compiler args
    translation_unit = index.parse(file_path, args=args)

    parsed_data = []
    for node in translation_unit.cursor.walk_preorder():
        if not is_user_defined(node):  # Skip standard library/system headers
            continue

        if is_standard_library(node):  # Skip std:: library components
            continue

        if is_relevant_kind(node.kind):  # Only capture user-defined elements
            parsed_data.append({"type": node.kind.name, "name": node.spelling})

    return parsed_data

def parse_cpp_folder(folder_path):
    """Parses all C++ files in a folder and aggregates the results."""
    all_parsed_data = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.cpp', '.h')):  # Process only C++ source/header files
                file_path = os.path.join(root, file)
                parsed_data = parse_cpp_file(file_path)
                all_parsed_data.extend(parsed_data)  # Aggregate results
    return all_parsed_data

if __name__ == "__main__":
    folder_path = "path/to/your/folder"  # Replace with the folder path
    result = parse_cpp_folder(folder_path)
    print(result)

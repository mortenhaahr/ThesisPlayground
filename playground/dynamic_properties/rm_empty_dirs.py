import os

directory = '../results/dynamic_props'

def remove_empty_directories(top_directory):
    for root, dirs, files in os.walk(top_directory, topdown=False):
        for dir_name in dirs:
            current_dir = os.path.join(root, dir_name)
            if not os.listdir(current_dir):
                # Directory is empty, remove it
                os.rmdir(current_dir)
                print(f'Removed empty directory: {current_dir}')

if __name__ == "__main__":
    # Run from script dir
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    remove_empty_directories(directory)
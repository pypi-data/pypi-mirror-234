from globus_batch_transfer import *
import argparse

if __name__ == "__main__":

    # Create an argument parser
    parser = argparse.ArgumentParser(description="Full absolute file path to configuration file")

    # Add a command-line argument for the file path
    parser.add_argument("config", help="File path to the YAML configuration file")

    # Parse the command-line arguments
    args = parser.parse_args()
    # Instantiate required class objects
    file_renamer = FileRenamer(args.config)
    file_mover = FileMover(args.config)

    while True:
        try:
            file_renamer.rename_files()
            time.sleep(1)  # Check every 1 second for changes
            file_mover.move_files_with_prefix()
        except KeyboardInterrupt:
            print("Program terminated by user.")
            break

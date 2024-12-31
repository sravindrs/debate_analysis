class RealTimeProcessor:
    def __init__(self):
        """
        Initializes the processor without assuming any specific input source.
        """
        self.file_path = None
        self.last_position = 0  # Tracks how much of the file has been processed.

    def set_file_path(self, file_path: str):
        """
        Sets the file path dynamically at runtime.
        """
        self.file_path = file_path
        self.last_position = 0  # Reset position when a new file is set.

    def fetch_new_data(self):
        """
        Reads new lines from the set file and returns them as a list.
        """
        if not self.file_path:
            raise ValueError("File path is not set. Use set_file_path() to specify input.")

        new_lines = []
        with open(self.file_path, 'r') as file:
            # Move to the last read position
            file.seek(self.last_position)
            new_lines = file.readlines()
            self.last_position = file.tell()  # Update position for the next check
        return new_lines

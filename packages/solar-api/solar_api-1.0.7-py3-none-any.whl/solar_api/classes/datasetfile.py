class DatasetFile:
    """
    Class to store necessary metadata for a Dataset file.

    Parameters
    ----------
    id : str
        Dataset File id

    name: str
        File name

    num_rows : long
        Number of rows in the file

    num_columns: int
        Number of columns in the file

    processing_status: string
        The status of the file in the processing pipeline.  Values are 'Completed','Failed','Cancelled','Running', and 'Queued'
    
    processing_error: string
        If processing failed, a description of the issue

    uploaded_timestamp: str
        Timestamp in UTC at which dataset was uploaded
    """
    def __init__(self, id: str, name: str, num_rows: int, num_columns: int, processing_status: str, processing_error: str):
        self.id = id
        self.name = name
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.processing_status = processing_status
        self.processing_error = processing_error

    def describe(self):
        """Print file metadata - id, name, number of rows, number of columns
        """
        print("File: " + self.name + " [" + self.id + "]")
        print("Number of rows: " + self.num_rows)
        print("Number of columns: " + self.num_columns)
        print("Status: " + self.processing_status)
        if self.processing_status!="" and self.processing_error is not None:
            print("Error: " + self.processing_error)
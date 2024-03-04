import pandas as pd


class Coordinates:
    def __init__(self, file_path):
        self.file_path = file_path
        self.header = None
        self.coordinates = self.extract_coordinates()

    def extract_coordinates(self):
        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.file_path, header=self.header)
        coordinates = {}
        for index, row in df.iterrows():
            city_name = row.iloc[0].strip()
            latitude = row.iloc[1]
            longitude = row.iloc[2]
            coordinates[city_name] = (latitude, longitude)

        return coordinates

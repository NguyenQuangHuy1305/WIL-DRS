import pandas as pd
import os
from sklearn.preprocessing import Normalizer
from sklearn.neighbors import NearestNeighbors
from joblib import dump, load
import argparse


class DRSModel:
    def __init__(self, config) -> None:
        """
        load the model
        Args:
            config: includes the filepath and other params.
        Returns:
            ret
        """
        if os.path.exists(config.model):
            self.model = load(config.model)
        else:
            self.model = None
        self.location_filepath = config.filepath
        self.scalar = Normalizer()

    def fit(self, location_names):
        """
        if the model is not on the hard disk, then we initiate the knn model
        Args:
            location_names: the file path of 'destination_tags_sum.csv'
        """
        df = pd.read_csv(location_names, sep=',')
        locations = df.to_numpy()
        locations = locations[:-1, 1:]
        locations = self.scalar.transform(locations)
        self.model = NearestNeighbors(
            n_neighbors=10, metric='minkowski', p=2).fit(locations)
        dump(self.model, 'drs_model')

    def predict(self, query):
        """
        call this predict function from the server for recommendation output
        Args:
            query: the user's vector representation based on his answers, preference on corresponding tag is set to 1, please check 'destination_tags_sum.xlsx' for detailed tag definition. The length of query equals to the length of all tags. 
        Returns:
            top-10 locations as recommendation result
        """
        if self.model is None:
            self.fit(self.location_filepath)

        query = query.reshape(1, -1)
        query = self.scalar.transform(query)

        ret = self.model.kneighbors(query)
        return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', default='./Destination_tags_sum.csv')
    parser.add_argument('--model', default='./drs_model')
    config = parser.parse_args()
    model = DRSModel(config)

    df = pd.read_csv(config.filepath, sep=',')
    locations = df.to_numpy()

    # query is the array of tag information from the website, e.g. the tags for the first location is [2,1,11,...,2],the length of this array equals the lengths of the total tag counts
    # 3 mean the 3rd row (just for the sake of the example)
    query = locations[:, 1:][3]
    # predict function output the top-10 locations
    predicted_array = model.predict(query)
    print(predicted_array[-1])

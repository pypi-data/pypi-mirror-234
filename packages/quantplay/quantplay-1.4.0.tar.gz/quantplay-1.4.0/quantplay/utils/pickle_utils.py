import codecs
import pickle
from quantplay.utils.constant import timeit


class PickleUtils:
    @staticmethod
    def save_data(data, file_name):
        with open("/tmp/{}.pickle".format(file_name), "wb") as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    @timeit(MetricName="PickleUtils:load_data")
    def load_data(file_name):
        with open("/tmp/{}.pickle".format(file_name), "rb") as disk_data:
            unserialized_data = pickle.load(disk_data)

        return unserialized_data

from prep import *
from plot import *
from glob import glob
from config import PATH_TO_DATA
from time import time


def load_plot():
    # make new csv grouped by every second
    path_to_raw_data = glob(os.path.join(PATH_TO_DATA, '*.csv'))[0]
    dataset = load_prep_data(path_to_raw_data)
    save_group_by_sec_data(dataset, save_file_path='freq_every_sec.csv')
    # plot graph
    path_to_data = os.path.join(PATH_TO_DATA, 'freq_every_sec.csv')
    dataset_group_by_sec = load_data(path=path_to_data)
    pic_path = plot_bar_save(dataset_group_by_sec)
    return pic_path


if __name__ == '__main__':
    start = time()
    picture_path = load_plot()
    end = time()
    print('code execution time: {}'.format(round(end - start), 1))

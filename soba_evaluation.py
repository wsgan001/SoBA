from general_utilities import *
from base import *
from classes import *
from evaluation import *

import time
import numpy as np

evaluation_filename = 'evaluation_p{}_k{}_t{}_d{}.csv'

def testing(p, k, t, d, working_folder):
    filename = working_folder + evaluation_filename.format(p, k, t, d)
    texts = []
    if is_file_exists(filename) is True:
        #create the training & test sets, skipping the header row with [1:]
        dataset = np.genfromtxt(filename, delimiter=',')[1:]
        # print(dataset.shape)
        ncol = dataset.shape[1]
        X = dataset[:,2:ncol-1] # Remove uid 1 and uid 2
        y = dataset[:,ncol-1]
        notes = ["All", "frequency", "diversity", "duration", "stability", "F+D", "F+TD", "F+TS", "D+TD", "D+TS", "TD+TS", "F+D+TD", "F+D+TS", "F+TD+TS", "D+TD+TS"]
        assign = [[0], [1], [2], [3], [0,1], [0,2],[ 0,3], [1,2], [1,3], [2,3], [0,1,2], [0,1,3], [0,2,3], [1,2,3]]
        texts = generate_report(X, y, assign, notes, p, k, t, d)
    return texts

# Main function
if __name__ == '__main__':
    HOUR  = 3600
    DAY   = 24 * HOUR
    WEEK  = 7 * DAY
    MONTH = 30 * DAY
    ### Global parameter for the experiments
    ps = []     ### Active project: 0 Gowalla, 1 Brightkite
    ks = []     ### Mode for top k users: 0 Weekend, -1 All users
    ts = []     ### Time threshold
    ds = []     ### Distance threshold
    ### project to be included
    # ps.append(0)
    ps.append(1)
    ### mode to be included
    ks.append(0)
    ks.append(-1)
    ### time threshold to be included
    ts.append(int(0.5 * HOUR))
    ts.append(1 * HOUR)
    ts.append(int(1.5 * HOUR))
    ts.append(2 * HOUR)
    # ts.append(1 * DAY)
    # ts.append(2 * DAY)
    # ts.append(3 * DAY)
    # ts.append(1 * WEEK)
    # ts.append(2 * WEEK)
    # ts.append(1 * MONTH)
    # ts.append(2 * MONTH)
    ### distance threshold to be included
    ds.append(0)
    # ds.append(250)
    # ds.append(500)
    # ds.append(750)
    # ds.append(1000)
    debug("--- Evaluation started ---")
    header = 'p,k,t,d,auc,precision,recall,f1,link_found,all_data,features,preprocessing'
    for p in ps:
        dataset, base_folder, working_folder, weekend_folder = init_folder(p)
        for k in ks:
            result_filename = working_folder + 'SoC_result_p{}_k{}.csv'.format(p,k)
            debug(result_filename)
            remove_file_if_exists(result_filename)
            write_to_file(result_filename, header)
            for t in ts:
                for d in ds:
                    debug('p:{}, k:{}, t:{}, d:{}'.format(p, k, t, d))
                    ### Initialize variables
                    texts = testing(p, k, t, d, working_folder)
                    for text in texts:
                        if text is not None:
                            write_to_file(result_filename, text)
    debug("--- Evaluation finished ---")
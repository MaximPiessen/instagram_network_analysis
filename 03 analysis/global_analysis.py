import matplotlib.pyplot as plt
import numpy as np
from helper_functions import *


def global_analysis(config):
    my_name = config.username
    include_me = config.include_me
    input_txt_file = config.input_txt_file

    G = create_graph_from_txt(my_name, include_me, input_txt_file)

    # get density of network:
    print("density: %s" % nx.density(G))

    # plot in_and out degree distribution
    in_degree_sequence = sorted([d for n, d in G.in_degree()], reverse=True)  # in_degree sequence
    in_degreeCount = collections.Counter(in_degree_sequence)
    in_deg, in_cnt = zip(*in_degreeCount.items())
    print("average in_degree %s" % (sum(in_degree_sequence) / len(in_degree_sequence)))

    out_degree_sequence = sorted([d for n, d in G.out_degree()], reverse=True)  # out_degree sequence
    out_degreeCount = collections.Counter(out_degree_sequence)
    out_deg, out_cnt = zip(*out_degreeCount.items())
    print("average out_degree %s" % (sum(out_degree_sequence) / len(out_degree_sequence)))

    # fit power law
    in_power_law = fit_powerlaw(in_deg, in_cnt)
    out_power_law = fit_powerlaw(out_deg, out_cnt)

    plt.figure()
    max_degree = max(max(out_degree_sequence), max(in_degree_sequence))
    bins = np.linspace(0, max_degree, max_degree)
    plt.hist(in_degree_sequence, bins, alpha=0.5, label='In degree', color="g")
    plt.plot(in_power_law[0], in_power_law[1], '--g', label='In degree power law: count = ' + r'${{{0}}}*degree^{{{1}}}$'.format(round(in_power_law[2][0], 2), round(in_power_law[2][1], 2)))
    plt.hist(out_degree_sequence, bins, alpha=0.5, label='Out degree', color="r")
    plt.plot(out_power_law[0], out_power_law[1], '--r', label='Out degree power law: count = ' + r'${{{0}}}*degree^{{{1}}}$'.format(round(out_power_law[2][0], 2), round(out_power_law[2][1],2)))
    plt.title("degree distibution")
    plt.xlabel("degree")
    plt.ylabel("counts")
    plt.xticks(np.arange(0, max_degree + 1, step=2), rotation=90)
    plt.legend(loc='upper right')
    #plt.show()
    plt.savefig("degree_distribution.png", dpi=300)

    # get average shortest path length
    path_lengths = []
    for v in G.nodes():
        spl = dict(nx.single_source_shortest_path_length(G, v))
        for p in spl:
            path_lengths.append(spl[p])

    print("average shortest path length %s" % (sum(path_lengths) / len(path_lengths)))



if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument('--username', type=str)
    parser.add_argument('--input_txt_file', type=str)
    parser.add_argument('--include_me', type=str2bool)

    config = parser.parse_args()

    global_analysis(config)


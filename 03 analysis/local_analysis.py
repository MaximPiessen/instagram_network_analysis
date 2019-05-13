from helper_functions import *
import pprint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

def local_analysis(config):
    my_name = config.username
    include_me = config.include_me
    input_txt_file = config.input_txt_file

    G = create_graph_from_txt(my_name, include_me, input_txt_file)

    # Betweenness centrality
    bet_cen = nx.betweenness_centrality(G)
    bet_cen = sort_and_small_dict(bet_cen, 5)
    # Closeness centrality
    clo_cen = nx.closeness_centrality(G)
    clo_cen = sort_and_small_dict(clo_cen, 5)
    # Degree centrality
    in_deg_cen = nx.in_degree_centrality(G)
    in_deg_cen = sort_and_small_dict(in_deg_cen, 5)
    # Degree centrality
    out_deg_cen = nx.out_degree_centrality(G)
    out_deg_cen = sort_and_small_dict(out_deg_cen, 5)
    # Page rank
    page_rank = nx.pagerank(G)
    page_rank = sort_and_small_dict(page_rank, 5)

    # print bet_cen, clo_cen, eig_cen, page_rank
    print("\n # Betweenness centrality:")
    pprint.pprint(bet_cen)
    print("\n # Closeness centrality:")
    pprint.pprint(clo_cen)
    print("\n # In-Degree centrality:")
    pprint.pprint(in_deg_cen)
    print("\n # Out-Degree centrality:")
    pprint.pprint(out_deg_cen)
    print("\n # Page rank:")
    pprint.pprint(page_rank)

    # Table summarising results
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    data = [centrality_to_str_arr(bet_cen),
                           centrality_to_str_arr(clo_cen),
                           centrality_to_str_arr(in_deg_cen),
                           centrality_to_str_arr(out_deg_cen),
                           centrality_to_str_arr(page_rank)]
    data = np.transpose(data)
    table = ax.table(colLabels=['Betweenness Centrality', 'Closeness Centrality', 'In-Degree Centrality', 'Out-Degree Centrality', 'PageRank'],
                     cellText=data,
                     loc='center')
    for (row, col), cell in table.get_celld().items():
        if (row == 0) or (col == -1):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))
    fig.tight_layout()
    plt.savefig("./centrality.png", dpi=300)
    plt.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument('--username', type=str)
    parser.add_argument('--input_txt_file', type=str)
    parser.add_argument('--include_me', type=str2bool)

    config = parser.parse_args()

    local_analysis(config)


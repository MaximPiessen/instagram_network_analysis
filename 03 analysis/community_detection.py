import community as community
import json
from helper_functions import *
import pprint

def community_detection(config):
    my_name = config.username
    include_me = config.include_me
    input_txt_file = config.input_txt_file
    input_json_file = config.input_json_file

    G = create_undirected_graph_from_txt(my_name, include_me, input_txt_file)

    # LOUVAIN METHOD
    partition_louvain = community.best_partition(G)
    size = float(len(set(partition_louvain.values())))
    pos = nx.spring_layout(G)
    count = 0.
    communities_louvain = []
    for com in set(partition_louvain.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition_louvain.keys()
                      if partition_louvain[nodes] == com]
        communities_louvain.append(list_nodes)
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
                               node_color=str(count / size))

    # GIRVAN NEWMAN
    #comp = nx.algorithms.community.centrality.girvan_newman(G)
    #communities_newman = list(sorted(c) for c in next(comp))

    communities_generator = nx.algorithms.community.girvan_newman(G)
    communities_newman = next(communities_generator)
    modularity_newman_new = nx.algorithms.community.modularity(G, communities_newman)

    modularity_newman_old = 0.00001
    count = 1
    while modularity_newman_new > modularity_newman_old:
        modularity_newman_old = modularity_newman_new
        communities_newman_final = communities_newman
        communities_newman = next(communities_generator)
        modularity_newman_new = nx.algorithms.community.modularity(G, communities_newman)
        count += 1

    partition_newman = {}
    for idx, cluster in enumerate(communities_newman_final):
        for profile in cluster:
            partition_newman[profile] = idx

    #get new jsons
    with open(input_json_file) as f:
        input_dict = json.load(f)

    json_with_groups_louvain = add_cluster_to_json(input_dict, partition_louvain)

    with open('relations_louvain.json', 'w+') as outfile:
        json.dump(json_with_groups_louvain, outfile)

    json_with_groups_newman = add_cluster_to_json(input_dict, partition_newman)

    with open('relations_newman.json', 'w+') as outfile2:
        json.dump(json_with_groups_newman, outfile2)

    print("Partition Louvain, " + str(len(communities_louvain)) + " clusters detected: ")
    pprint.pprint(communities_louvain)
    print("\n")
    print("Partition Girvan-Newman, " + str(len(communities_newman_final)) + " clusters detected: ")
    pprint.pprint(communities_newman)

    # modularity score
    print("\n")
    print("Modularity score Louvain method: " + str(round(nx.algorithms.community.modularity(G, communities_louvain), 2)))
    print("Modularity score Girvan-Newman method at level " + str(count) + ": " + str(round(nx.algorithms.community.modularity(G, communities_newman_final), 2)))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument('--username', type=str)
    parser.add_argument('--input_txt_file', type=str)
    parser.add_argument('--input_json_file', type=str)
    parser.add_argument('--include_me', type=str2bool)

    config = parser.parse_args()

    community_detection(config)


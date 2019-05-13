import re
import networkx as nx
import argparse
import collections
import scipy.optimize


def fit_powerlaw(degrees, counts):
    if min(degrees) == 0:
        x = degrees[:-1]
        y = counts[:-1]
    else:
        x = degrees
        y = counts

    def powerlaw(x, a, b):
        return a * (x ** b)

    pars, covar = scipy.optimize.curve_fit(powerlaw, x, y)

    approx = []
    for elem in x:
        approx.append(powerlaw(elem, *pars))

    return (x, approx, pars)


def sort_and_small_dict(d, n):
    sorted_dict = collections.OrderedDict(sorted(d.items(), key=lambda x: -x[1]))
    firstnpairs = list(sorted_dict.items())[:n]
    return firstnpairs


def centrality_to_str_arr(centrality):
    str_arr = []
    for item in centrality:
        str_arr.append(item[0] + ' | ' + str(round(item[1], 2)))
    return str_arr


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def create_graph_from_txt(my_name, include_me, input_txt_file):
    nodes = set()
    edges = []
    G = nx.DiGraph()

    with open(input_txt_file, 'r') as f:
        for line in f:
            accounts = line.split(" ")
            account_1 = re.search('https://www.instagram.com/(.*)/', accounts[0]).group(1)
            account_2 = re.search('https://www.instagram.com/(.*)/', accounts[1]).group(1)

            nodes.add(account_1)
            if include_me:
                edges.append([account_1, account_2])
            else:
                if not (account_1 == my_name or account_2 == my_name):
                    edges.append([account_1, account_2])

    if include_me:
        G.add_node(my_name)
    else:
        nodes.remove(my_name)

    for account in nodes:
        G.add_node(account)

    for accounts in edges:
        G.add_edge(accounts[0], accounts[1])

    return G


def create_undirected_graph_from_txt(my_name, include_me, input_txt_file):
    nodes = set()
    edges = []
    G = nx.Graph()

    with open(input_txt_file, 'r') as f:
        for line in f:
            accounts = line.split(" ")
            account_1 = re.search('https://www.instagram.com/(.*)/', accounts[0]).group(1)
            account_2 = re.search('https://www.instagram.com/(.*)/', accounts[1]).group(1)

            nodes.add(account_1)
            if include_me:
                edges.append([account_1, account_2])
            else:
                if not (account_1 == my_name or account_2 == my_name):
                    edges.append([account_1, account_2])

    if include_me:
        G.add_node(my_name)
    else:
        nodes.remove(my_name)

    for account in nodes:
        G.add_node(account)

    for accounts in edges:
        G.add_edge(accounts[0], accounts[1])

    return G


def add_cluster_to_json(input_dict, cluster_dict):
    nodes = input_dict['nodes']
    links = input_dict['links']

    for item in nodes:
        item['group'] = cluster_dict[item['name']]

    out_dict = {'nodes': nodes, 'links': links}

    return out_dict

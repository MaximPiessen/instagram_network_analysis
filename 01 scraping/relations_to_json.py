import json
import re
import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def relations_to_json(config):
    my_name = config.username
    include_me = config.include_me
    input_txt_file = config.input_txt_file
    output_json_file = config.output_json_file

    nodes = set()
    edges = []
    dict = {}
    name_to_id = {}

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

    dict["nodes"] = []

    if include_me:
        name_to_id[my_name] = 0
        dict["nodes"].append({"id": 0, "name": my_name, "group": 1})
    else:
        nodes.remove(my_name)
    id_n = 1
    for account in nodes:
        dict["nodes"].append({"id": id_n, "name": account, "group": 1})
        name_to_id[account] = id_n
        id_n += 1

    dict["links"] = []
    bi_links = set()
    id_l = 0
    for accounts in edges:
        id_1 = name_to_id[accounts[0]]
        id_2 = name_to_id[accounts[1]]
        if [accounts[1], accounts[0]] in edges:
            bi_links.add((id_1, id_2))
            if (id_2, id_1) not in bi_links:
                dict["links"].append({"id": id_l, "source": id_1, "target": id_2, "value": 0.3, "bi_directional": True})
                id_l += 1
        else:
            dict["links"].append({"id": id_l, "source": id_1, "target": id_2, "value": 0.3, "bi_directional": False})
            id_l += 1

    with open(output_json_file, 'w') as outfile:
        json.dump(dict, outfile)

    print("json created")


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument('--username', type=str)
    parser.add_argument('--input_txt_file', type=str)
    parser.add_argument('--output_json_file', type=str)
    parser.add_argument('--include_me', type=str2bool)

    config = parser.parse_args()

    relations_to_json(config)


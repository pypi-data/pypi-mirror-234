from typing import List
import json


def parse_graph_string(graph: str) -> List[List[str]]:
    """Parse a string of knowledge graph into List of List of relation"""
    relations = [el.strip() for el in graph.strip().strip('][').strip('\n').split(',\n')]
    return [el.strip('][').replace("'","").split(', ') for el in relations]


def filter_missing_relationship(relations_list: List[List[str]]):
    """remove relationship with empty entity"""
    return [relation for relation in relations_list if len(relation[0])*len(relation[2])]


def format_nested_list_to_cytoscape(
       knowledge_graph: List[List[str]]
) -> List[dict]:
    """Convert a nested list of string into Cytoscape format for graph visualisation."""
    concepts = list(set([triplet[0] for triplet in knowledge_graph] + [triplet[2] for triplet in knowledge_graph]))
    edges_info = [(triplet[0], triplet[2], triplet[1]) for triplet in knowledge_graph]

    ids = list(range(len(concepts)))
    nodes_info = list(zip(ids, concepts))

    nodes = [
        {
            'data': {'id': label, 'label': label, 'name': label},
        }
        for short, label in nodes_info
    ]

    edges = [
        {'data': {'source': source, 'target': target, 'label': label, 'weight':  5}}
        for source, target, label in edges_info
    ]

    elements = nodes + edges
    return elements


def parse_gpt_response_to_relations(
        gpt_text: str,
):
    """Parse GPT response into List[List[str]] for cytoscape"""
    relations_list = parse_graph_string(gpt_text)
    return filter_missing_relationship(relations_list)


def load_json(st):
    with open(st, 'rb') as f:
        return json.load(f)

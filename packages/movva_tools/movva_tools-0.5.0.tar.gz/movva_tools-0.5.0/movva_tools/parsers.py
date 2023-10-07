class FlowRevisionParser:
    def __init__(self, flow_json: dict):
        self.flow_json = flow_json

    def extract_all_nodes(self, node=None):
        if node is None:
            node = self.flow_json
        nodes = []
        nodes.append(node)
        if 'nodes' in node:
            for child_node in node['nodes']:
                nodes.extend(self.extract_all_nodes(child_node))
        return nodes

    def extract_texts_from_nodes(self, nodes):
        texts = []
        for node in nodes:
            if 'text' in node:
                texts.append(node['text'])
        return texts

    def extract_channels_from_nodes(self, nodes):
        channels = []
        for node in nodes:
            if 'channel' in node:
                channels.append(node['channel'])
        return channels

    def parse_flow_revision(self):
        all_nodes = self.extract_all_nodes()
        all_texts = self.extract_texts_from_nodes(all_nodes)
        all_channels = self.extract_channels_from_nodes(all_nodes)
        return all_texts, all_channels


# Exemplo de uso
base_flow_json = { ... }  # Substitua por seu JSON de revisão de fluxo
parser = FlowRevisionParser(base_flow_json)
all_texts, all_channels = parser.parse_flow_revision()

for i in range(len(all_texts)):
    print("Text:", all_texts[i])
    print("Channel:", all_channels[i])
    print()

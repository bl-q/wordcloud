import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']   #显示中文有效的方法
#zhfont1 = mpl.font_manager.FontProperties(fname='C:\\Windows\\Fonts\\simkai.ttf')
#plt.legend(prop=zhfont1)

g = nx.Graph()
g.add_node(1)
g.add_node(2)
g.add_edge(1,2)
for n, nbs in g.adj.items():
    print(nbs)
dg = nx.DiGraph()
dg.add_weighted_edges_from([(1, 2, 0.5), (3, 1, 0.75)])
dg.out_degree(1, weight='weight')

dg.clear()
nodes1 = [
    ('Variable', {'name': 'avariable', 'table': 'tablename'}),
    ('Select', {'conditions': {'pro_code': 44}}),
    ('GroupBy', {'varname': 'gender'}),
    ('Mean', {}),
    ('Which1', {'level': 1}),
    ('Decimal1', {'place': 1}),
]

nodes2 = [
    ('Which1', {'level': 2}),
    ('Decimal2', {'place': 1}),
]

nodes3 = [
    ('Add', {})
]

dg.add_nodes_from(nodes1)
dg.add_nodes_from(nodes2)
dg.add_nodes_from(nodes3)

dg.add_edges_from([
    ('Variable', 'Select'),
    ('Select', 'GroupBy'),
    ('GroupBy', 'Mean'),
    ('Mean', 'Which1'),
    ('Mean', 'Which2'),
    ('Which1', 'Decimal1'),
    ('Which2', 'Decimal2'),
    ('Decimal1', 'Add'),
    ('Decimal2', 'Add(加)'),
])
nx.draw(dg, with_labels=True, fontname='Kaiti')
plt.savefig('fit.pdf') #plt.savefig('fit.jpg')
plt.show()
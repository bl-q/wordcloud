from graphviz import Digraph

# 创建有向图
dot = Digraph(comment='The Test Table')

# 添加圆点A,A的标签是Dot A
dot.node('A', '点A', fontname='Kaiti')

# 添加圆点 B, B的标签是Dot B
dot.node('B', 'Dot B', fontname='Kaiti', fontsize='20', fontcolor='green', shape='rect', style='rounded')
# dot.view()

# 添加圆点 C, C的标签是Dot C
dot.node('C', 'Dot C', shape='rect', style='filled', fillcolor='red', color='green')
# dot.view()

# 创建一组边，即连接AB的两条边，连接AC的一条边。
dot.edges(['AB', 'AC', 'AB'])
# dot.view()

# 在创建两圆点之间创建一条边
dot.edge('B', 'C', '测试', fontname='SimSun')
# dot.view()


# 获取DOT source源码的字符串形式
print(dot.source)
# // The Test Table
# digraph {
#   A [label="Dot A"]
#   B [label="Dot B"]
#   C [label="Dot C"]
#   A -> B
#   A -> C
#   A -> B
#   B -> C [label=test]
# }


# 保存source到文件，并提供Graphviz引擎
dot.render('test-output/test-table.gv', view=True)

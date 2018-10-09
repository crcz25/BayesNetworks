import fileinput
from pprint import pprint

class BayesNode:
  def __init__(self, name, parents, CPT):
    self.name = name
    self.parents = parents
    self.CPT = CPT

  def __str__(self):
    return "Node(Node: <%s>, Parent: <%s>, Prob: <%s>)" % (self.name, self.parents, self.CPT)

def main():
  lines = []
  s = len(lines)

  for line in fileinput.input():
    lines.append(line.rstrip())

  nodes = lines[0].replace(' ', '').split(',')
  n = int(lines[1])
  probabilities = [item for item in lines[2:n + 2]]
  t = int(lines[n + 2])
  tests = [item for item in lines[(s-t):]]
  bayesian_network = {}

  for node in nodes:
    parents = []
    curr_node_prob = list(filter(lambda x: (x[0:x.find('|')]).count(node) > 0, probabilities))
    count_prob = len(curr_node_prob)

    # Get Parents from node
    if count_prob > 1:
      for i in curr_node_prob:
        for n in nodes:
          if n in i and n != node and n not in parents:
            parents.append(n)

    # Calculate Probab Table
    CPT = {}

    bayesian_network[node] = BayesNode(node, parents, CPT)

    #Create CPT's
    for line in curr_node_prob:
      given, prob = line.split('=')
      given = given.split(",")
      #print(given)


    print()
    print('Node', node)
    print('Parents', parents)
    print('Probs', curr_node_prob)
    print()

  print('Prob to test')
  pprint(tests)
  print()


  print('DICTIONARY JUST IN CASE')
  for key,value in bayesian_network.items():
    print('Key', key, '\n', value)

  pass



if __name__ == '__main__':
  main()
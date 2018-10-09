import fileinput
import json
from pprint import pprint

class BayesNode:
  def __init__(self, name, parents, CPT):
    self.name = name
    self.parents = parents
    self.CPT = CPT

  def __str__(self):
    print("Node(Node: <%s>, Parent: <%s>)" % (self.name, self.parents))
    print("Probab Table")
    pprint(self.CPT)
    return ""
    
    
def generateBayesNetwork(nodes, probabilities):
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

    #Create CPT's
    #print('Node', node)
    #print()
    for line in curr_node_prob:
      given, prob = line.split('=')
      given = given.split(",")
      aux = ""
      for item in given:
        #print('not', item, '!=', node)
        if item[1:] != node:
          aux += item
        else:
          aux += node
        #  print('Key', aux)
        aux += ','
        #print()
      #print(aux)
      if len(curr_node_prob) > 1:
        tk = '+' + aux[1:-1]
        fk = '-' + aux[1:-1]
      else:
        tk = '+' + aux[:-1]
        fk = '-' + aux[:-1]
      CPT[tk] = float(prob)
      CPT[fk] = 1 - float(prob)
      #print('Given', given)
      #print()
      #pprint(CPT)
    bayesian_network[node] = BayesNode(node, parents, CPT)
    """
    print()
    print('Node', node)
    print('Parents', parents)
    print('Probs', curr_node_prob)
    print()

  print('Prob to test')
  pprint(tests)
  print()
  """
  
  return bayesian_network


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
  
  bayesian_network = generateBayesNetwork(nodes, probabilities)
  
  #print('DICTIONARY JUST IN CASE')
  print()
  for key,value in bayesian_network.items():
    print('Key', key, '\n', value)

  pass



if __name__ == '__main__':
  main()
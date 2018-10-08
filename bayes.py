import fileinput
from pprint import pprint

class BayesNode:
  def __init__(self, name, parents, CPT):
    self.name = name
    self.parents = parents
    self.CPT = CPT



def probabilitiesOf(query, nodes):
  print('ProbabilitesOf')
  if len(query) == 1:
    print('One prob')
  else:
    print('Evidence')
    filtered = list(filter(lambda x: (x[0:x.find('|')]).count(query) > 0))
    print(filtered)
  pass

def main():
  lines = []

  for line in fileinput.input():
    lines.append(line.rstrip())

  nodes = lines[0].replace(' ', '').split(',')
  n = int(lines[1])
  probabilities = [item for item in lines[2:n + 2]]
  #print(prob)
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


    #Calculate CPT's





    print()
    print('Node', node)
    print('Parents', parents)
    print('Probs', curr_node_prob)

  """
  for i in range(2, n + 2):
    query = lines[i].split('|')
    if len(query) == 1:
      probabilitiesOf(query, nodes)
    else:
      evidence = query[1]
      probabilitiesOf(query, nodes)
  """

  #tests = int(lines[5])
  #pprint(lines)

  #print()
  #print('Nodes', nodes)
  #print('Num of Probabilities', n)
  #print('Tests', tests)
  pass



if __name__ == '__main__':
  main()
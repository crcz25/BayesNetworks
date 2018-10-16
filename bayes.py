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


# Parser function
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
      splitVariables, prob = line.split('=')
      splitGiven = splitVariables.split("|")

      #print(splitGiven)
      variable = splitGiven[0].replace(' ', '')
      given = []
      if len(splitGiven) > 1:
        given = splitGiven[1].replace(' ', '').split(",")
        given.sort(key=lambda x: x[1:])

      #print(splitGiven)
      aux = variable + "|"
      for item in given:
        #print('not', item, '!=', node)
        if item[1:] != node:
          aux += item
        else:
          aux += node
        #  print('Key', aux)
        aux += ','
        #print()
      #print(curr_node_prob, len(curr_node_prob))
      if len(curr_node_prob) > 1:
        tk = '+' + aux[1:-1]
        fk = '-' + aux[1:-1]
      else:
        tk = '+' + aux[1:-1]
        fk = '-' + aux[1:-1]
      CPT[tk] = float(prob)
      CPT[fk] = 1 - float(prob)
      #print('Given', given)
      #print()
      #pprint(CPT)
    bayesian_network[node] = BayesNode(node, parents, CPT)

  return bayesian_network

# Auxiliar functions
def inEvidence(variable, evidence):
  return ('+' + variable) in evidence or ('-' + variable) in evidence

def equalToEvidence(variables, evidence):
  for v in variables:
    if not inEvidence(v, evidence):
      return False

  return True


def getTopologicalSortedVariables(variables, bayesian_network):
  result = [v[1:] for v in variables]

  for node in result:
    for parent in bayesian_network[node].parents:
      if not (parent in result):
        result.append(parent)

  return result


def getVariablesFromCombination(variables, n):
  ans = []

  index = len(variables) - 1
  while index >= 0:
    if n % 2 == 1:
      ans.append('+' + variables[index])
    else:
      ans.append('-' + variables[index])

    n //= 2
    index -= 1

  return ans

# Probability functions
def chainRule(variables, bayesian_network):
  ans = 1.0

  for v in variables:
    node = bayesian_network[v[1:]]

    ctpKey = ""
    if len(node.parents) == 0:
      ctpKey = v
    else:
      given = []
      for parent in node.parents:
        if ('+' + parent) in variables:
          given.append('+' + parent)
        else:
          given.append('-' + parent)

      given.sort(key=lambda x: x[1:])
      given = ",".join(given)

      ctpKey = v + "|" + given

    #print("KEY", ctpKey, node.CPT)
    ans *= node.CPT[ctpKey]

  #print(ans)
  return ans


def conditionalProbability(variables, evidence, bn):
  return totalProbability(variables + evidence, bn) / totalProbability(evidence, bn)

def totalProbability(evidence, bayesian_network):
  allNodes = getTopologicalSortedVariables(evidence, bayesian_network)

  #print("ALL NODES", allNodes, evidence)

  if equalToEvidence(allNodes, evidence):
    return chainRule(evidence, bayesian_network)
  else:
    notInEvidence = []
    for node in allNodes:
      if not inEvidence(node, evidence):
        notInEvidence.append(node)

    limit = pow(2, len(notInEvidence))

    ans = 0
    for combination in range(limit):
      genVariables = getVariablesFromCombination(notInEvidence, combination)

      ans += chainRule(evidence + genVariables, bayesian_network)

    #print("notInEvidence, ", notInEvidence)

    return ans

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

  for t in tests:
    query = t.replace(' ', '').split("|")
    if len(query) == 1:
      ans = totalProbability(query[0].split(","), bayesian_network)
    else:
      ans = conditionalProbability(query[0].split(","), query[1].split(","), bayesian_network)


    print(round(ans, 7))


if __name__ == '__main__':
  main()
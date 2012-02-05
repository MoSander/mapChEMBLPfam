"""
  Function:  feedPropDict
  --------------------
  set of functions to construct the propDict 
  
  momo.sander@ebi.ac.uk
"""



"""dictionary"""                                       
def dictionary(dict_x, propDict, blacklist, maptype): 
  ### feed ligDict into blueprint propDict
  import numpy as np

  for domain in dict_x.keys(): 
    for molregno in dict_x[domain].keys():
      #print 'feeding %s into propDict. Maptype: %s'%(molregno, maptype)       
      medAfnty = np.median(dict_x[domain][molregno]['pAfnty'])
      smiles = dict_x[domain][molregno]['smiles']
      targets = dict_x[domain][molregno]['target']
      docId = dict_x[domain][molregno]['actId']

      lkp = {}
      for target in targets:
        if target in blacklist:
          lkp[target] = 0
          print 'excluding:', target, 'for domain', domain
      for target in lkp.keys():
        targets.remove(target)
      if len(targets) == 0:
        print 'dropping entry: ', molregno
        continue

      try:
        propDict[domain].append([molregno, smiles, targets,medAfnty,docId, maptype])
      except KeyError:
        propDict[domain] = []
        propDict[domain].append([molregno, smiles, targets, medAfnty,docId, maptype])

  return propDict



"""addLigs"""
def addLigs(propDict, maptype):

  ### feed addLigs into blueprint propDict
  infile = open('data/addLigands.txt', 'r')
  lines = infile.readlines()
  infile.close()
  molregno = None
  for line in lines:
    elements = line.split('\t')
    domain = elements[0]
    target = elements[1]
    smiles = elements[2]
    aff = elements[3]
    docId = 'manual'      
    try:
      propDict[domain].append([molregno, smiles, target, aff, docId, maptype])
      print 'adding %s to %s' %(smiles, domain)
    except KeyError:
      propDict[domain] = []
      propDict[domain].append([molregno, smiles, target, aff,docId, maptype])

  return propDict  
              


                                                                                                                                        
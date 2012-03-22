"""
  Function: overlap
  ----------------
  ### Examine the overlap of ligands between different domains at different
  ### thresholds. 
  momo.sander@googlemail.com
""" 
def overlap(propDict, tholds, release):
  import numpy as np
  import pickle

  xholds = []
  for thold in tholds:
    xhold =  -np.log10(thold*10**(-6))
    xholds.append(xhold)

  keys = propDict.keys()
  trace =  {}
  for i in range(len(keys)-1):
    domain1 = keys[i]
    for j in range(i+1, len(keys)):
      domain2 = keys[j]
      ligands1 = propDict[domain1]
      ligands2 = propDict[domain2]
      for ligand1 in ligands1:
        molregno1 = ligand1[0]
        aff1 = ligand1[3]
        for ligand2 in ligands2:
          molregno2 = ligand2[0]
          aff2 = ligand2[3]
          if not molregno1 == molregno2:
            continue
          for xhold in xholds:
            if aff1 >= xhold and aff2 >= xhold:
              try:
                trace[domain1][domain2][xhold].append(molregno1)
              except KeyError:
                try:
                  trace[domain1][domain2][xhold] = []
                  trace[domain1][domain2][xhold].append(molregno1)
                except KeyError:
                  try: 
                    trace[domain1][domain2] = {}
                    trace[domain1][domain2][xhold] = []
                    trace[domain1][domain2][xhold].append(molregno1)
                  except KeyError:
                    trace[domain1] = {}
                    trace[domain1][domain2] = {}
                    trace[domain1][domain2][xhold] = []
                    trace[domain1][domain2][xhold].append(molregno1)
            else:
              break
              
  out = open('data/overlapTrace_%s'% release, 'w')
  pickle.dump(trace, out)
  out.close()

  for xhold in xholds:
    nw = open('data/connectivity_%.1f_%s.tab' %( xhold, release),'w')
    for domain1 in trace.keys():
      print domain1
      for domain2 in trace[domain1].keys():
        try: 
          stren = len(trace[domain1][domain2][xhold])
        except KeyError:
          continue

        nw.write('%s\t%s\t%s\t%s\n' %(domain1, domain2, 'sameLigand', stren ))
    nw.close()

  nda = open('data/nodesize_%s.tab' %( release),'w')
  for domain in propDict.keys():
    nda.write('%s\t%s\n'%(domain, len(propDict[domain])))
  nda.close()

if __name__ == '__main__':
  overlap()



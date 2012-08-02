"""
  Function:  mapPDs
  --------------------
  Carry out the mapping and save results.

  Author:
  Felix Kruger
  momo.sander@googlemail.com
"""                              
def mapPDs(th, release, user, pword, host, port): 

  ## Set the threshold.
  import numpy as np
  threshold = -np.log10(th*10**(-6))
  
  ## Get a list of all ChEMBL targets.
  import getUniprotTargets
  chemblTargets = getUniprotTargets.getUniprotTargets(release, user, pword, host, port)

  ## Load the pfamDict.
  import pickle
  infile = open('data/protCodPfamDict_%s.pkl' %release, 'r')
  pfamDict = pickle.load(inFile)
  infile.close()    

  ## Get ligands for targets with single domains.
  import singleDomain 
  single = singleDomain.singleDomains(pfamDict, chemblTargets, threshold, release, user, pword, host, port)

  ## Construct the propDict for targets with one domain. Manually remove targets (as decribed in Methods section Manual curation) listed in blacklist.tab and add domains that never occur alone listed in whitelist (Pkinase_Tyr). 
  import feedPropDict
  import parse
  blacklist = parse.col2list('data/blacklist.tab',1, False)  
  propDict = {}
  propDict = feedPropDict.dictionary(single, propDict, blacklist, 'single')
  propDict = feedPropDict.addLigs(propDict,'manual', 'data/whitelist.tab') 
  

  ## Identify targets that have more than one binding site containing 
  ## domain. 
  import findConflicts
  conflicts = findConflicts.findConflicts(pfamDict, valid, chemblTargets)

  ## Insert data for multi domain proteins.
  import feedPropDict
  propDict = feedPropDict.dictionary(multi, propDict, blacklist, 'multi')

  ## Export the mapping to a mySQL table.
  import export
  import pickle
  outfile = open('data/propDict_%s.pkl' %release, 'w')
  pickle.dump(propDict, outfile)
  export.exportMapsMySQL(propDict, release, user, pword, host, port)
  export.exportConflsMySQL(conflicts, release ,user, pword, host, port)
  

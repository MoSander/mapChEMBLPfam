"""
  Function:  makeIntactDict
  --------------------
  check if a pdb/msd-id exists for a specified ligand and return molDict[molregno]
  
  momo.sander@googlemail.com
"""                        
def queryPDB(uniDict, intactDict, coordMap, release):

  import urllib
  import urllib2
  from xml.dom.minidom import parse  
  import xml.dom
  import pickle

  pdbDict = {}
  url = 'http://www.ebi.ac.uk/pdbe-site/pdbemotif/hitlist.xml'
   
  for target in intactDict.keys():
    pdbDict[target] = {}
    print target
    for chembl_id in intactDict[target]:
      try:
        cmpdIds = uniDict[chembl_id]
      except KeyError:
        continue     
      for cmpdId in cmpdIds:        
        XML = """requestXML=\
          <!DOCTYPE query SYSTEM "http://www.ebi.ac.uk/pdbe-site/pdbemotif/query.dtd">\
          <query> \
          <declaration>  \
          <uniprot name="p">%s</uniprot> \
          <ligand name="l1">%s</ligand><aminoacid name="a1">X</aminoacid> \
          </declaration>\
          <bond name="b1" a="l1" b="a1" /> \
          </query>"""% (target, cmpdId)  
        req = urllib2.Request(url, XML)                                   
        response = urllib2.urlopen(req)
        dom = parse(response)
        for entry in dom.childNodes:
          if entry.nodeName == "hits":
            for hit in entry.childNodes:
              if hit.nodeName == 'hit':
                pdb = hit.getAttribute('pdb-code')
                #print pdb, cmpdId 
                for nodeX in hit.childNodes:
                  if nodeX.nodeName == 'bond':
                    bondType = nodeX.getAttribute('bond-type') 
                  if nodeX.nodeName == 'residue': 
                    if nodeX.getAttribute('name') == "a1":
                      pos = nodeX.getAttribute('sequence-number')
                try:
                  pdbDict[target][cmpdId]['bond'].append(bondType)
                  pdbDict[target][cmpdId]['position'].append(pos) 
                  pdbDict[target][cmpdId]['pdb'].append(pdb)
                  pdbDict[target][cmpdId]['chain'].append(chain)
                except KeyError:
                  pdbDict[target][cmpdId] = {}
                  pdbDict[target][cmpdId]['bond'] = []
                  pdbDict[target][cmpdId]['position'] = []
                  pdbDict[target][cmpdId]['pdb'] = []
                  pdbDict[target][cmpdId]['chain'] = []
                  pdbDict[target][cmpdId]['bond'].append(bondType)
                  pdbDict[target][cmpdId]['position'].append(pos) 
                  pdbDict[target][cmpdId]['pdb'].append(pdb)
                  pdbDict[target][cmpdId]['chain'].append(chain)        
        dom.unlink()
    if len(pdbDict[target].keys()) ==0:
      del pdbDict[target]
                          
  out = open('data/pdbDict_chembl%s.pkl' %(release), 'w')
  pickle.dump(pdbDict, out)
  out.close()
  
  return pdbDict
     

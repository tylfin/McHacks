from music21 import converter,instrument # or import *
from music21 import *
import zen
import numpy
from numpy.random import normal as nm
from numpy.random import uniform as un
import scipy
import optparse
import math
import Queue

class NotYetImplemented(Exception):
    def __init__(self):
        print "NOT YET IMPLEMENTED"


class RandomGenerator():
    def __init__(self,parts):
        self.parts = parts
        self.items = []
        for i in range(len(self.parts)):
            for j in range(len(parts[i])):
                self.items.append(parts[i][j])
        self.dict = {}
        self.noteInformation = []
        self.G = zen.Graph()
        
        self.orderedArrayOfNames = []
        
        self.outputstream = stream.Stream()
        
        self.reverseDict = {}
        #building orderedArrayOfNames
        for i in range(len(self.items)):
            try:
                self.orderedArrayOfNames.append(self.items[i].nameWithOctave)
            except:
                self.orderedArrayOfNames.append(self.items[i].fullName)
        
        #BUILDING DICTIONARY.
        for i in range(len(self.items)):
            try:
                self.dict[self.items[i].nameWithOctave] = self.dict[self.items[i].nameWithOctave]+1
            except:
                try:
                    self.dict[self.items[i].nameWithOctave] = 1
                    self.reverseDict[self.items[i].nameWithOctave] = self.items[i]
                except AttributeError:
                    try:
                        self.dict[self.items[i].fullName] = self.dict[self.items[i].fullName]+1 
                    except:
                        self.dict[self.items[i].fullName] = 1
                        self.reverseDict[self.items[i].fullName] = self.items[i]
        
        #BUILDING ARRAY
        for key in self.dict:
            self.noteInformation.append((key,self.dict[key]))
        
        #BUILDING ZEN GRAPH
        for i in range(len(self.noteInformation)):
            self.G.add_node(self.noteInformation[i][0])
            
        #TESTING PURPOSES
        #for item in range(len(self.noteInformation)):
        #    print self.noteInformation[item]
            
        self.buildRandomEdges()
            

            
    def buildRandomEdges(self):
        weightProbability = 0
        for i in range(len(self.orderedArrayOfNames)-1):
            try:
                if self.dict[self.orderedArrayOfNames[i+1]] < 10:
                    weightProbability = un(0,1)
                elif self.dict[self.orderedArrayOfNames[i+1]] < 100:
                    weightProbability = un(.6,1)
                else:
                    weightProbability = un(.9,1)
                    
                self.G.add_edge(self.orderedArrayOfNames[i],self.orderedArrayOfNames[i+1])
                self.G.set_weight(self.orderedArrayOfNames[i],self.orderedArrayOfNames[i+1],weightProbability)
            except zen.exceptions.ZenException:
                self.G.rm_edge(self.orderedArrayOfNames[i],self.orderedArrayOfNames[i+1])
                           
        
    def randomGenerator(self):
        startingNode = self.orderedArrayOfNames[int(un(0,len(self.orderedArrayOfNames)))]
        nindx = self.G.node_idx(startingNode)
        node = self.G.node_object(nindx)
        q = Queue.Queue()
        q.put(node)
        for nodes in self.G.nodes():
            q.put(nodes)
        self.outputstream.append(self.reverseDict[startingNode])
        while (not q.empty()):
            node = q.get()
            for neighbor in self.G.neighbors(node):
                if (self.G.weight(node,neighbor) > un(0,1)):
                    try:
                        self.outputstream.append(self.reverseDict[neighbor])
                    except:
                        None
        
        return self.outputstream
    
    
    #TESTING PURPOSES    
    def printItems(self):
        for i in range(len(self.items)):
            print self.items[i]

  
    def printFullNames(self):
        for i in range(len(self.items)):
            print self.items[i].fullName
    
    def printGraph(self):
        print self.G.nodes()
        print self.G.edges()
            

def parseInput():
    parser = optparse.OptionParser('usage%prog + -f <MIDI FILE>')
    parser.add_option("-f", "--file", type="string", dest="filename", help="Name of file")
    (options, args) = parser.parse_args()
    fileName = options.filename
    return fileName
    
def writeMidToFile(s):
    mf = midi.translate.streamToMidiFile(s)
    mf.open('test.mid', 'wb')
    mf.write()
    mf.close()
    
def runMusicGenerator(s):
    parts = s[0].voicesToParts()
    r = RandomGenerator(parts)
    return r.randomGenerator()


def main():
    score = converter.parse('moonlight.mid')
    randomScore = runMusicGenerator(score)

if __name__ == "__main__":
    main()
    
    
    
    
    

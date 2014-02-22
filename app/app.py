from music21 import converter,instrument # or import *
from music21 import *
import zen

class NotYetImplemented(Exception):
    def __init__(self):
        print "NOT YET IMPLEMENTED"





## HOW TO GET NOTES FROM SONG
notes = score[0].voicesToParts()[0]

item = notes[0]
narray = []


#print type(score)
#print type(score[0])
#print type(score[0][0])

s = stream.Stream()
n1 = note.Note()
n1.pitch.name = 'E4'
n1.duration.type = 'half'
n1.duration.quarterLength
s.append(n1)
#s.show('text')

class RandomGenerator():
    def __init__(self,parts):
        self.parts = parts
        self.items = []
        for i in range(len(self.parts)):
            for j in range(len(parts[i])):
                self.items.append(parts[i][j])
        self.dict = {}
        
        
    def randomGenerator(self):
        NotYetImplemented
        
    def printItems(self):
        for i in range(len(self.items)):
            print self.items[i]
            
        
    def printFullNames(self):
        for i in range(len(self.items)):
            print self.items[i].fullName
            




def main():
    score = converter.parse('moonlight.mid')
    parts = score[0].voicesToParts()
    r = RandomGenerator(parts)
    #r.printItems()
    #r.printFullNames()

if __name__ == "__main__":
    main()
    
    
    

import constants as c

class SKITTLE:
    def __init__(self, x, y, color, ID):
        self.color = color
        self.x = x
        self.y = y
        self.ID = ID
        self.age = 0
        self.tracks = []
        self.crossedLine = False
        self.tracks.append([self.x, self.y])
        # print(self.ID)

    def setPosition(self, x, y):
        self.tracks.append([self.x, self.y])
        self.x = x
        self.y = y

    def setAge(self, a):
        self.age = a

    def getAge(self):
        return self.age

    def getColor(self):
        return self.color

    def getPosition(self):
        return self.x, self.y

    def countSkittles(self, line, currentVal):
        if self.tracks[0][1] < line < self.tracks[-1][1]:
            if not self.crossedLine:
                # print("crossed")
                self.crossedLine = True
                currentVal += 1
        return currentVal

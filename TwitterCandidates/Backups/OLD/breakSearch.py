import re
glitchyFiles =["Gary Peters","Terri Lynn Land","Al Franken","Mike McFadden","Mark Begich",
                     "Dan Sullivan","Mark Pryor","Tom Cotton","Mark Udall","Cory Gardner","David Perdue",
                    "Michelle Nunn","Bruce Braley","Joni Ernst","Pat Roberts","Greg Orman","Jeanne Shaheen",
                    "Scott Brown","Kay Hagan","Thom Tillis","Mitch McConnell","Alison Grimes",
                    "Mary Landrieu","Bill Cassidy","Rob Maness"]
#for file in glitchyFiles:
for i in range(16, 25):
    file = glitchyFiles[i]
    compressFile = "".join(file.split())
    readFileName = compressFile + ".txt"
    print "Reading from: " + readFileName
    readingFile = open(readFileName, "r")

    text = readingFile.read()
    readingFile.close()
    text = re.sub("BREAK", "", text)

    writeFileName = compressFile + "FIX.txt"
    print "Writing to " + writeFileName
    writingFile = open(writeFileName, "w")
    writingFile.write(text)
    writingFile.close()
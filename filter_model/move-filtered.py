import os

# For each directory in the traiing_data set
for x in os.listdir('./results/label'):
    pass
    genus, _ = x.split(".")
    print genus
genus = "Sorbus"
x = "Sorbus.txt"
# Read the contents of the result file
with open("./results/label/%s" % x, 'r') as f: #open the file
    contents = f.read().splitlines() #put the lines to a variable (list).

outputDir = "../download_images/training_data/Label/%s/" % genus
os.mkdir(outputDir)

# Iterate over result content
for c in contents:
    label, path = c.split()
    if label == "Label":
        # Move the image to a different folder
        filename = path.split("/")[-1]
        print filename
        os.rename(path, "%s%s" % (outputDir, filename) )

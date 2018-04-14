import os

genera = ["Aesculus", "Betula", "Castanea", "Cornus", "Corylus", "Eucalyptus", "Fagus", "Fraxinus", "Ginkgo", "Juglans", "Larix", "Malus", "Paulownia", "Picea", "Pinus", "Platanus", "Populus", "Prunus", "Pseudotsuga", "Pyrus", "Quercus", "Robinia", "Salix", "Sorbus", "Ulmus"]
for genus in genera:
    x = "%s.txt" % genus
    print x
    # Read the contents of the result file
    with open("./results/trunk/%s" % x, 'r') as f: #open the file
        contents = f.read().splitlines() #put the lines to a variable (list).

    outputDir = "../download_images/training_data/Trunk/%s/" % genus
    os.mkdir(outputDir)

    # Iterate over result content
    for c in contents:
        label, path = c.split()
        if label == "Trunk":
            # Move the image to a different folder
            filename = path.split("/")[-1]
            print filename
            os.rename(path, "%s%s" % (outputDir, filename) )

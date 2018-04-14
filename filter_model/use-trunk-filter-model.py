import turicreate as tc
import os

print "About to use model"

# Load the filter label model
model = tc.load_model('TrunkFilter.model')

# For each directory in the project training data set
for x in os.listdir('../download_images/training_data'):
    pass

genera = ["Aesculus", "Betula", "Castanea", "Cornus", "Corylus", "Eucalyptus", "Fagus", "Fraxinus", "Ginkgo", "Juglans", "Larix", "Malus", "Paulownia", "Picea", "Pinus", "Platanus", "Populus", "Prunus", "Pseudotsuga", "Pyrus", "Quercus", "Robinia", "Salix", "Sorbus", "Ulmus"]
for x in genera:
    print "Predicting for images in %s" % x

    # Load images from this directory
    data = tc.image_analysis.load_images('../download_images/training_data/%s' % x, with_path=True)

    # Predict label on input images
    try:
        data['predictions'] = model.predict(data)
    except Exception as e:
        print "Error encountered"

    # Write to file
    output = open('./results/trunk/%s.txt' % x, 'w')
    for i in data:
        output.write("%s %s\n" % (i['predictions'], i['path']) )
    output.close()

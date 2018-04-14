import turicreate as tc
import os

print "About to use model"

# Load the filter label model
model = tc.load_model('LabelFilter.model')

# For each directory in the project training data set
for x in os.listdir('../download_images/training_data'):
    print "Predicting for images in %s" % x
    
    # Load images from this directory
    data = tc.image_analysis.load_images('../download_images/training_data/%s' % x, with_path=True)

    # Predict label on input images
    data['predictions'] = model.predict(data)

# Write to file
output = open('./results/label/%s.txt' % x, 'w')
for i in data:
    output.write("%s %s\n" % (i['predictions'], i['path']) )
output.close()

import turicreate as tc

print "About to start learning data from download-images/training_data/Trunk"

# Load images
data = tc.image_analysis.load_images('../download_images/training_data/Trunk', with_path=True)
print "Data loaded"

# From the path-name, create a label column
data['label'] = data['path'].apply(lambda path: path.split("/")[-2])
print "Labels created"

# Save the data for future use
data.save('data.sframe')
print "Data saved"
data.explore()

# Make a train-test split
train_data, test_data = data.random_split(0.8)
print "Made test split"

# Automatically picks the right model based on your data.
model = tc.image_classifier.create(train_data, target='label')
print "Model created"

# # Save the model for later use in Turi Create
model.save('Betula.model')
print "Model saved"

# Export for use in Core ML
model.export_coreml('Betula.mlmodel')
print "Model exported to CoreML"

# Save predictions to an SArray
# predictions = model.predict(data)
print "Skipped predictions"

# # Evaluate the model and save the results into a dictionary
metrics = model.evaluate(test_data)
print "Model evaluated"
print(metrics['accuracy'])

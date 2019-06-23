from keras import applications
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential, Model 
from keras.layers import Dropout, Flatten, Dense, GlobalAveragePooling2D
from keras import backend as k 
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
import imghdr
import os
from PIL import Image
from os.path import isfile, join


img_width, img_height = 256, 256
image_dir = 'google_images_download/downloads'
train_data_dir = image_dir + '/' + 'train'
validation_data_dir = image_dir + '/' + 'test'
batch_size = 16
epochs = 50
frozen = 10

#Validate images
def removeBadImages(mypath):
    i = 0
    onlyfiles = [f for f in os.listdir(mypath) if isfile(join(mypath, f))]
    acceptable_ext = ['jpg', 'jpeg']
    for filename in onlyfiles:
        if imghdr.what(mypath + filename) in acceptable_ext:
            i+=1
            continue
        os.remove(mypath + filename)
        print(filename)
    return i

len_train_donald = removeBadImages(train_data_dir + '/Donald_Trump/')
len_test_donald = removeBadImages(validation_data_dir + '/Donald_Trump/')

len_train_alec = removeBadImages(train_data_dir + '/Alec_Baldwin/')
len_test_alec = removeBadImages(validation_data_dir + '/Alec_Baldwin/')

nb_train_samples = len_train_donald + len_train_alec
nb_validation_samples = len_test_donald + len_test_donald

##############
model = applications.VGG19(weights = "imagenet", include_top=False, input_shape = (img_width, img_height, 3))

# Freeze the layers which you don't want to train. Here I am freezing the first 5 layers.
for layer in model.layers[:frozen]:
    layer.trainable = False

#Adding custom Layers 
x = model.output
x = Flatten()(x)
x = Dense(1024, activation="relu")(x)
x = Dropout(0.5)(x)
x = Dense(1024, activation="relu")(x)
predictions = Dense(2, activation="softmax")(x)

# creating the final model 
model_final = Model(input = model.input, output = predictions)

# compile the model 
model_final.compile(loss = "categorical_crossentropy", optimizer = optimizers.SGD(lr=0.001, momentum=0.9), metrics=["accuracy"])

# Initiate the train and test generators with data Augumentation 
train_datagen = ImageDataGenerator(
rescale = 1./255,
horizontal_flip = True,
fill_mode = "nearest",
zoom_range = 0.3,
width_shift_range = 0.3,
height_shift_range=0.3,
rotation_range=30)

test_datagen = ImageDataGenerator(
rescale = 1./255,
horizontal_flip = True,
fill_mode = "nearest",
zoom_range = 0.3,
width_shift_range = 0.3,
height_shift_range=0.3,
rotation_range=30)

train_generator = train_datagen.flow_from_directory(
train_data_dir,
target_size = (img_height, img_width),
batch_size = batch_size, 
class_mode = "categorical")

validation_generator = test_datagen.flow_from_directory(
validation_data_dir,
target_size = (img_height, img_width),
class_mode = "categorical")

# Save the model according to the conditions  
checkpoint = ModelCheckpoint("vgg16_1.h5", monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
early = EarlyStopping(monitor='val_acc', min_delta=0, patience=10, verbose=1, mode='auto')


# Train the model 
model_final.fit_generator(
train_generator,
#samples_per_epoch = nb_train_samples,
steps_per_epoch = nb_train_samples//batch_size,
epochs = epochs,
validation_data = validation_generator,
validation_steps = nb_validation_samples//batch_size,
#nb_val_samples = nb_validation_samples,
callbacks = [checkpoint, early])


model_final.save('/home/piyushsanghi_uchicago_edu/deep-learning-course/model.h5')

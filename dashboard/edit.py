import numpy
import numpy as np
# import matplotlib.pyplot as plt
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
import cv2

# covidimgr = '../Machine/zz.jpg'
# covidimgr = '../Machine/zz.jpg'

#to read image from url
import urllib.request
#url = covidimgr
covid_chest = load_model('../Machine/covid_new_model1.h5')

covidimgr = 'https://res.cloudinary.com/segestic/image/upload/v1/covid/images/IMG-0071-00031_qggf11'
# url_response = urllib.urlopen(covidimgr)

covidimgr = urllib.request.urlopen(covidimgr)
covidimgr = covidimgr.read()

#end url

# image = cv2.imread(covidimgr)
# read file
npimg = numpy.fromstring(covidimgr, numpy.uint8)
image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

# image = cv2.cvtColor(covidimgr1, cv2.COLOR_BGR2RGB)


image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# arrange format as per keras
image = cv2.resize(image, (224, 224))
image = np.array(image) / 255
image = np.expand_dims(image, axis=0)

resnet_pred = covid_chest.predict(image)


probability = resnet_pred[0]
print("Resnet Predictions:")
if probability[0] > 0.2:
    covid_chest_pred = str('%.2f' % (probability[0] * 100) + '% COVID')
else:
    covid_chest_pred = str('%.2f' % ((1 - probability[0]) * 100) + '% NonCOVID')
print(covid_chest_pred)


# ReCAPTCHAWiz: Using Selenium and a CNN to Defeat ReCAPTCHA Mountain Image Challenges

ReCAPTCHAWiz combines Selenium with a trained convolutional neural network to classify images that contain mountains or not in order to pass Google ReCAPTCHA challenges.  See live example of Google's ReCAPTCHA [here](https://www.google.com/recaptcha/api2/demo) and below image. 

![ReCAPTCHA Challenge Screenshot](https://github.com/alporter08/ReCAPTCHAWiz/blob/master/CAPTCHA_Demo.png)

### Image Data
The images used to train the CNN were obtained directly from the ReCAPTCHA site.  The [split_recaptcha_source_images](https://github.com/alporter08/ReCAPTCHAWiz/blob/master/split_recaptcha_source_images.ipynb) notebook was used to go through each downloaded image (which contain 9 sub-images), split them and use MD5 checksum to get rid of duplicates.  The images were then manually sorted into two folders in preparation for going through the CNN.  

### Convolutional Neural Network
The CNN used for this project leverages a Keras [tutorial](https://blog.keras.io/building-powerful-image-classification-models-using-very-little-data.html) for classifying cat and dog pictures.  Using a pre-trained CNN provides very high accuracy on the validation set (~98%).  The CNN is run with [Mountain_classifier_VGG.py](https://github.com/alporter08/ReCAPTCHAWiz/blob/master/Mountain_classifier_VGG.py).

### Selenium
ReCAPTCHA uses Javascript so Selenium is used to interact with the program.  [ReCAPTCHAWiz.py](https://github.com/alporter08/ReCAPTCHAWiz/blob/master/ReCAPTCHAWiz.py) opens the ReCAPTCHA demo in Selenium, and automatically selects the appropriate images (for mountain challenges).

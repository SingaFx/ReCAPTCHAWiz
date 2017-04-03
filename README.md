# ReCAPTCHAWiz
## ML techniques to answer ReCAPTCHA challenges

ReCAPTCHAWiz combines Selenium with a trained convolutional neural network to classify images that contain mountains or not in order to pass Google ReCAPTCHA challenges.  See live example of Google's ReCAPTCHA [here](https://www.google.com/recaptcha/api2/demo) and below image. 

![ReCAPTCHA Challenge Screenshot](https://github.com/alporter08/ReCAPTCHAWiz/blob/master/CAPTCHA_Demo.png)

### Image Data
The images used to train the CNN were obtained directly from the ReCAPTCHA site.  The [split_recaptcha_source_images](https://github.com/alporter08/ReCAPTCHAWiz/blob/master/split_recaptcha_source_images.ipynb) notebook was used to go through each downloaded image (which contain 9 sub-images), split them and use MD5 checksum to get rid of duplicates.  

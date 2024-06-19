<h1 align="center">LeafCheck</h1>

<div align="center">

</div>
LeafCheck is a web services that aimed at revolutionizing crop disease diagnosis by leveraging machine learning algorithms to analyze leaf images for disease detection. With a backend powered by Google Cloud Run and a database hosted on Google Cloud Storage, LeafCheck offers users a seamless and efficient platform for identifying plant diseases and providing appropriate solutions.
The first thing you need to know is that this service is using authentication to access each service. You need to login to access the service. The login is using username and password. You can register on the registration service. Please don't spam the registration service because it will make the registration service slow. If you have some idea to secure this service, please contact me.

> Base url of this service is: http://localhost:8080/

The service available:

- Authentications
  <pre>POST /authentications</pre>
  <pre>PUT  /authentications</pre>

- Predictions
  <pre>POST /predict</pre>
  
# NOTE

This service is using token for authentication. You should have an account to access this service. First if you don't have an account, create a new account. Then, create a token for authentication. It's like login, you need to authenticate yourself with username and password. If the autentication is valid, you will get a token. You can use this token to access the service. If dont, you will get a error message. 

The token given is accessToken and refreshToken. The refreshToken is used to refresh the token. The accessToken is valid for 30 minutes. If you want to refresh the token, you need to send the refreshToken to the service. If the refreshToken is valid, you will get a new accessToken. If the refreshToken is not valid, you will get a error message.

For the imgUrl, it is image url that publicly accessible. The image should be in image format like (jpg, png, jpeg, etc.). The image url can be obtained when you upload your image to upload picture service, or search on google.

If the prediction is successful, you will get a json object. The json object contains the prediction result. The prediction result contains the highest probability and the predicted class, with some additional information related to the class. The result will be stored as a history object.

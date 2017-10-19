# SMS Profanity Checker

This python application uses the [Twilio] API to send sms.
We use this API [link][link] to check for words which contain profanity.
And for the last Tkinter library is used for creatiing the Graphic User Interface

##### Depedencies stored in requirement.txt
To install them run this command
 > pip install -r requirement.txt

 ### To run the application
  > python gui.py

#### Profanity check
Profanity check is done using HTTP request using request library in python
> http://www.wdylike.appspot.com?q=<your-word>
Suppose *home* is the word u want to check
>http://www.wdylike.appspot.com?q=home

[link]: <http://www.wdylike.appspot.com/>
[Twilio]: <https://www.twilio.com/>

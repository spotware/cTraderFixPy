### Response Message

Whenever client receives a FIX message it calls the "MessagedReceived" callback with the message.

The message parameter of callback is not a plain string, it's an instance of ResponseMessage type.

ResponseMessage class allows you to easily access each field of a response message.

### Getting Message Field Values

To get a field value you can use the response message GetFieldValue method, it takes the FIX field number and returns the value(s).

The GetFieldValue can return three types of values:

* String: When there is only one field of your provided field number on the message it returns that field value

* List: If the field is repetitive like symbol IDs or names, then it returns a list, all of those fields values will be inside that list

* None: if there was no such field inside the message

### Getting Raw Message

If you want to get the raw string of reponse message, you can call the response message getMessage method.

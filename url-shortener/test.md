# Build a url shortener

Your primary task is to build a url shortener api using python.

## Requirements

- Your webservice should have a `POST /shorten_url` endpoint that recieves a json body with the url to shorten. A successful request will return a json body with the shortened url. If a get request is made to the shortened url then the user should be redirected to the the original url, or returned the contents of the original url.
- Perform appropriate validatation on the url to be shortened, and return appropriate error responses if the url is not valid
- Contain a `README.md` file with instructions on how to run your service.

## Note:
This task is simple and straight forward but we will be assessing you on your implementation of web service / python / software engineering best practices. So please use this as an oppertunity to demonstrate how your write code and solve problems. You should also build your webservice in a way that a devops enginer (or you) could configure your backend in a way that your webservice could handle high traffic (eg. 1000 rps). Please explain in your `README.md` file how to configure your backend for scale.

## Example usage:

1)

`www.helloworld.com` -> <html><body> hello world </body> </html>

2)
```
Request:
    POST www.your_service.com/shorten_url

    body:
    {
        "url": "www.helloworld.com"
    }

Response: 
    Status code: 201
    response_body:
    {
        "shortened_url": 'http://www.your_service.com/ouoYFY48'
    }
```
3)

`http://www.your_service.com/ouoYFY48` -> <html><body> hello world </body> </html>
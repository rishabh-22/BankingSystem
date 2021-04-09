# Mini Banking System
This repository holds the code for a mini banking system wherein a user can sign up, login, and transact.

## Features
* Login
* Register
* Transaction Add
* Transaction History
* Transaction Filter
* Account information

## Flow of Project
Customer is required to sign up in order to access the functionality of the logical API. Login/ SignUp will fetch the token for the user which can be used to access the validation API. Once the user has the token, they can send the payload in the request body and get the response in json form according to the logic. Token is to be attached in the headers.

## Flow of logic
>*	customer signs up, an account is created
>*	users get the auth token using which they can transact 
>*	transaction id is a counter based hash which is generated uniquely for each transaction

## Paths (local)

* Register: `http://0.0.0.0:8000/customer/register/`

* Login: `http://0.0.0.0:8000/customer/login/`

* Transaction Add: `http://0.0.0.0:8000/customer/transaction/add/`

* Transaction History: `http://0.0.0.0:8000/customer/transaction/view/`

* Transaction filter: `http://0.0.0.0:8000/customer/transaction/filter/`

* Account Information: `http://0.0.0.0:8000/customer/account/view/`

* Account Balance: `http://0.0.0.0:8000/customer/account/balance/`

## Staged
The django app is hosted on an EC2 server, hence you can directly check the functionality of the API through there. No auth token is required in this case, the app can be accessed [here](http://18.224.7.211:8000/shorten).

## Payload
Postman collection has been attached.

## Setup

to run locally: `make`

to run in a container: `make container`

> prefer running in a container as running locally will result in installing libraries in your system (instead of a virtual environment).

## Todo

* Implement pagination in the transaction history view
* Implement the logic using view sets for better code structuring and readability
* Implement functionality for sending email/pdf for statements 
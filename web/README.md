##Instruction & example of API superpigeon   

#### Signup
 required fields: 
* username
* email
*  password 

 additional fields: 
* first_name 
* last_name
* phone
* address
* business_name (if user want to be organization/company account) 
* business_address
*  business_phone

  example with curl:

` curl -H "Content-Type: application/json" -X POST -d '{"username":"curltest", "password": "testertester", "email":"example@email.com"}' https://docker.datepalm.media:9980/api/signup/` 

#### Signin
required fields:
*  username 
* password 

additional fields:
*  exp_hour (default: 4)
*  exp_min (default: 1)
* exp_sec (default: 60)

example with curl:

` curl -H "Content-Type: application/json" -X POST -d '{"username":"curltest", "password": "testertester"}' https://docker.datepalm.media:9980/api/auth/`

__if success we will get token with default exp time 4 hours or based on additional fields information__


#### Restricted (login required) API URL Access (example: update data on /api/profile/ )
required fields:
*  token 
additional fields:
*  phone address
* business_name
* business_address
* business_phone

example with curl:

` curl -H "Content-Type: application/json" -X POST -d '{"token": "45ebb64fcbb1763b22f0d5de9b3811a024ee6d75", "phone": "1234567", "address": "test address"}' https://docker.datepalm.media:9980/api/profile/`

#### LOGOUT (FORCE DESTROY TOKEN)
required fields: 
* token 

example with curl:

` curl -H "Content-Type: application/json" -X POST -d '{"token": "45ebb64fcbb1763b22f0d5de9b3811a024ee6d75"}' https://docker.datepalm.media:9980/api/logout/`
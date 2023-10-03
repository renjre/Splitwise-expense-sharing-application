# Splitwise-expense-sharing-application
### this is postman collection link

`step1`
Create users using http://127.0.0.1:8000/api/users/ 
```
{
    "user_id":1004,
    "name": "user4",
    "email": "user4@gmail.com",
    "mobile_number":42006657898
}
```
`step2`
Create room  using http://127.0.0.1:8000/api/rooms/
just add name in form data
```
{ "name":"room_name"}
```

now add all users who are in a group in room using http://127.0.0.1:8000/api/user-room/
```
{
  "room": 1,
  "user": 1,
}
```
`step3`
Now create expense using http://127.0.0.1:8000/api/expenses/
```
{
    "description": "electricity bill",
    "amount": 1000,
    "expense_type": "EQUAL",
    "paid_by": 1,
    "room":1
}
```
or

```
{
    "description": "flipkart",
    "amount": 1250,
    "expense_type": "EXACT",
    "paid_by": 1,
    "room": 1
}
```
or 
```
{
    "description": "dine out",
    "amount": 1200,
    "expense_type": "PERCENT",
    "paid_by": 4,
    "room": 1
}
```

`step4`
Now create expense splits using http://127.0.0.1:8000/api/expense-splits/
Remember if expense_type in Expense is  "EQUAL", then we do not need to add expense splits, it will create autometically 
for other types
```
{
    "expense": 2, 
    "user": 2, 
    "amount": 370
}
```
Note: do not create expense splits for user who paid total amount in Expense, just need to create expense splits for those user who are in room, 

`step5`
To get all owes details use http://127.0.0.1:8000/api/users-owes/

To get user's owes details use http://127.0.0.1:8000/api/my-owes/1


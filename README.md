# library-service-project

### Performed Coding Tasks

### 1.Implement CRUD functionality for Books Service
* Initialize books app
* Add book model
* Implement serializer & views for all endpoints 

### 2. Add permissions to Books Service
* Only admin users can create/update/delete books
* All users (even those not authenticated) should be able to list books
* Use JWT token authentication from users' service

### 3.Implement CRUD for Users Service
* Initialize users app
* Add user model with email
* Add JWT support
* For a better experience during working with the `ModHeader` Chrome extension 
change the default `Authorization` header for JWT authentication to for example `Authorize` header. 
* Take a look at the [docs](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#auth-header-name) on how to deal with it.
* Implement serializer & views for all endpoints

### 4.Implement Borrowing List & Detail endpoint
* Initialize borrowings app
* Add borrowing model with constraints for borrow_date, expected_return_date, and actual_return_date.
* Implement a read serializer with detailed book info
* Implement list & detail endpoints

### 5. Implement Create Borrowing endpoint
* Implement create a serializer
* Validate book inventory is not 0
* Decrease inventory by 1 for book
* Attach the current user to the borrowing
* Implement and create an endpoint

###  6. Add filtering for the Borrowings List endpoint
* Make sure all non-admins can see only their borrowings
* Make sure borrowings are available only for authenticated users
* Add the `is_active` parameter for filtering by active borrowings (still not returned)
* Add the `user_id` parameter for admin users, so admin can see all users’ borrowings, if not specified, but if specified - only for concrete user

### 7.Implement return Borrowing functionality
* Make sure you cannot return borrowing twice
* Add 1 to book inventory on returning
* Add an endpoint for it

### 8. Implement the possibility of sending notifications on each Borrowing creation
* Set up a telegram chat for notifications posting in there
* Set up a telegram bot for sending notifications
* Investigate the `sendMessage` function interface in Telegram API
* Make sure all private data is private, and never enters the GitHub repo (you can use the `python-dotenv` package for simple working with `.env` files. Make sure to add the `.env.sample` file with the `.env` content skeleton)
* Create a helper for sending messages to the notifications chat through Telegram API
* Integrate sending notifications on new borrowing creation (provide info about this borrowing in the message)

### 9.List & Detail Payments Endpoint
* This task is just easy task to start working on the interesting process of payments in the system
* Create Payment model
* Create serializer & views for list and detail endpoints
* Make sure non-admins can see only their Payments when admins can see all of them

### 10.Create your first Stripe Payment Session
* Take a deep dive into this stripe doc to understand how to work with payments
* Initialize your Stripe Payment account (you can select for example USA as a country)
* Use only test data inside. You shouldn’t work with real money on this project
* Also, it’s NOT needed to activate your stripe account, just work with test data
* Try to create your first Stripe Session (you can use even Flask example from the doc) just to understand how it works
* Manually create 1-2 Payments in the Library system, and attach existing session_url and session_id to each
* Check List & Detail endpoint are working
* No need for a front end. We will do everything on the back end.

### 11.Automate the routine of creating Stripe Payment Sessions
* Make sure your Stripe secret keys are secret - do not push them to GitHub
* Create a helper function, which will receive borrowing as a parameter, and create a new Stripe Session for it.
* Calculate the total price of borrowing and set it as the unit amount (of course convert it to the correct type).
* Let quantity as 1 - we allow borrowing only 1 book at a time
* Create a Payment and store session_url and session_id inside. Attach Borrowing to the Payment
* Leave success and cancel URLs as default for now - we will handle it later
* Call this helper function when creating a new borrowing
* Yes, we will ask for payment at the exact moment, when the person is creating a Borrowing
* Add payments to Borrowing serializers, so all payments associated with current Borrowing will be displayed.

### 12. Implement success and cancel urls for Payment Service
* Take a look on this [tutorial](https://stripe.com/docs/payments/checkout/custom-success-page) to understand, how to work with success endpoint
* Create success action in which check, that stripe session was paid
* And if it was successful - mark payment as paid
* Create a Cancel endpoint, which says to the user that payment can be paid a bit later (but the session is available for only 24h)
* When creating a session - put their correct link to success and cancel the endpoint
* Use `request.build_absolute_uri` & reverse
* Provide request in context to serializer (only if needed)

### Performed Optional tasks :
1. Keep track of expired Stripe sessions
* Add each-minute scheduled task for checking Stripe Session for expiration
* If the session is expired - Payment should be also marked as EXPIRED (new status)
* The user should be able to renew the Payment session (new endpoint)















### HOW TO RUN

- Create venv: `python -m venv venv`
- Activate venv: `sourse venv/bin/activate`
- Install requirements: `pip install -r requirements.txt`
- Run migrations: `python manage.py makemigrations`
                  `python manage.py migrate`
- Run the app: `python manage.py runserver`


from flask import *
#method 2: click on view - tool windows - terminal
#once terminal type: pip install flask
#create the flask objectzhh
app = Flask(__name__) #__name__ means main
#This secret key encripts your user session for security reasons
app.secret_key = 'A1_445T_@!jhf5gH' #16,32,64
#This is the body of your Flask Object
@app.route('/')
def home():
    return render_template('home.html') #TO DO HTML

                        #@app.route('/signin')
                        #def signin():
                            #return render_template('signin.html')
                        #run and test routes i.e http://127.0.0.1:5000
                        #@app.route('/signup')
                        #def signup():
                           # return render_template('signup.html')
import pymysql
#establish db connection
connection = pymysql.connect(host='localhost',user='root',password='',database='shoes_db')
@app.route('/shoes')
def shoes():
    #create your query
    sql ='SELECT * FROM products_tbl'
    #execute /run your
    #create a cursor used to execute sql
    cursor = connection.cursor()
    #now use the cursor to execute your sql
    cursor.execute(sql)

    #check how many rows were returned
    if cursor.rowcount == 0:
        #return 'No Records'
        return render_template('shoes.html', msg = 'out of stock')
    else:
        #get all rows
        rows = cursor.fetchall()
        #print(rows)
        return render_template('shoes.html', rows = rows)

    #this route will display a single shoe
    #This route willneed a product_id
@app.route('/single/<product_id>')
def single(product_id):
    # create your query, provide a placeholder
    sql = 'SELECT * FROM products_tbl WHERE product_id = %s'
    # execute /run your
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # now use the cursor to execute your sql
    # below you provide id to replace the %s
    cursor.execute(sql, (product_id))

    # check how many rows were returned
    if cursor.rowcount == 0:
        # return 'No Records'
        return render_template('single.html', msg='product does not exist')
    else:
        # get all rows
        row = cursor.fetchone()
        # print(rows)
        return render_template('single.html', row=row)

#this is the login route    
@app.route('/login', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        #receive the posted email and password variables
        email = request.form['email']
        password = request.form['password']

#We now move to the db and confirm if above details exists
        sql = "SELECT * FROM customers where customer_email = %s and customer_password = %s"
        #create a cursor an d execute above sql
        cursor = connection.cursor()
        #execute the sql,provide email and password to fit %s placeholders
        cursor.execute(sql,(email,password))

            #check if a match was found
        if cursor.rowcount==0:
            return render_template('login.html', error= 'Wrong credentials')
        elif cursor.rowcount == 1:
            #create a user to track who is logged in
            #Attach user email to the session
            session['user'] = email
            return redirect('/shoes')
        else:
            return render_template('login.html', error ='Error Occured,Try later')

    else:
        return render_template('login.html')

@app.route('/register',methods= ['POST','GET'])
def register():
    if request.method == 'POST':
        customer_fname = request.form['customer_fname']
        customer_lname = request.form['customer_lname']
        customer_surname = request.form['customer_surname']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_password = request.form['customer_password']
        customer_password2 = request.form['customer_password2']
        customer_gender = request.form['customer_gender']
        customer_address = request.form['customer_address']
        dob = request.form['dob']

        #validations
        import re
        if customer_password != customer_password2:
            return render_template('register.html',password= 'password do not match')

        elif len(customer_password)< 8:
            return render_template('register.html',password= 'password must have 8 characters')

        elif not re.search("[a-z]", customer_password):
            return render_template('register.html',password='must have a small letter')

        elif not re.search("[A-Z]", customer_password):
            return render_template('register.html',password='must have a capital letter')

        elif not re.search("[0-9]", customer_password):
            return render_template('register.html',password='must have a number')

        elif not re.search("[_@$]", customer_password):
            return render_template('register.html',password='must have a symbols')

        elif len(customer_phone) > 10:
            return render_template('register.html',phone='must be above 10 numbers')
        else:
            sql = "insert into customers(customer_fname,customer_lname,customer_surname,customer_email,customer_phone,customer_password,customer_gender,customer_address,dob) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            try:
                cursor.execute(sql,(customer_fname,customer_lname,customer_surname,customer_email,customer_phone,customer_password,customer_gender,customer_address,dob))
                connection.commit()
                return render_template('register.html', success = 'saved successfully')
            except:
                return render_template('register.html', error = 'failed')

    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/login') #clear session

@app.route('/reviews', methods = ['POST','GET'])
def reviews():
    if request.method == 'POST':
        user = request.form['user']
        product_id = request.form['product_id']
        message = request.form['message']
        #To a table for reviews
        sql = "insert into reviews_tbl (user,product_id,message) values(%s,%s,%s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql,(user,product_id,message))
            connection.commit()
            #when going back to /single carrying the product id
            flash('Review posted successfully')
            flash('Than you for your review')
            # the flash message goes back  to single.html
            return redirect(url_for('single', product_id = product_id))
        except:
            flash('Review not posted')
            flash('please try again')
            return redirect(url_for('single', product_id = product_id))
    else:
        return ''

    #create a table named reviews
    #review_id INT PK 50
    #https: // github.com / modcomlearning / mpesa_sample

import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa_payment', methods = ['POST','GET'])
def mpesa_payment():
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            # capture the session of paying client
            email = session['user']

            quantity = str(request.form['quantity'])
            product_id = str(request.form['product_id'])

            #multiply quantity * amount
            total_pay = float(quantity) * float(amount)

            #sql to insert
            #create a table named payment_info
            #pay_id INT PK AI
            #product_id INT 50
            #phone VARCHAR 50
            #email VARCHAR 50
            #quantity INT 50
            #total_pay
            #pay_date timestamp current time stamp
            sql = 'insert into payment_info(phone,email,quantity,total_pay,product_id) values(%s,%s,%s,%s,%s)'
            cursor = connection.cursor()
            cursor.execute(sql,(phone,email,quantity,total_pay,product_id))
            connection.commit()

            # GENERATING THE ACCESS TOKEN
            consumer_key = "6G3GmLHwEIjxn8dmlGaJjkq23ajSpTVM"
            consumer_secret = "uLWM2zZHJOtx9V3C"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": total_pay,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": email,
                "TransactionDesc": 'quantity:'+ 'ID' +product_id
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return render_template('payment.html', msg = 'Please Complete Payment in Your Phone')
        else:
            return render_template('payment.html')

@app.route('/contact' ,methods = ['POST','GET'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        sql = "insert into contact_tbl(name,email,message) values (%s,%s,%s)"
        cursor = connection.cursor()
        cursor.execute(sql, (name,email,message))
        connection.commit()
        return  render_template('contact.html')
    else:
        return render_template('contact.html')



#admin Dashboard =========
@app.route('/admin' , methods =['POST','GET'])
def admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM admin_tbl WHERE email = %s and password = %s"

        cursor= connection.cursor()
        cursor.execute(sql,(email,password))
        # check if a match was found
        if cursor.rowcount == 0:
            return render_template('admin.html', error='Wrong credentials')
        elif cursor.rowcount == 1:
            # create a user to track who is logged in
            # Attach user email to the session
            session['admin'] = email
            return redirect('/dashboard')
        else:
            return render_template('admin.html', error='Error Occured,Try later')

    else:
        return render_template('admin.html')

#dashboard...
@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        sql = "SELECT * FROM customers ORDER BY reg_date DESC"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('dashboard.html', msg = 'No Customers')
        else:
            rows = cursor.fetchall()
            return render_template('dashboard.html', rows = rows)
    else:
        return redirect('/admin')

@app.route('/adminlogout')
def adminlogout():
    session.pop('admin')
    return redirect('/admin') #clear session

@app.route('/customer_del/<customer_id>')
def customer_del(customer_id):
    if 'admin' in session:
        sql="delete from customers where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (customer_id))
        flash("Deleted successfully")
        return redirect('/dashboard')
    else:
        return redirect('/admin')





if __name__ =='__main__':
    app.run(debug=True)


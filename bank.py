class Customers:
    def __init__(self):
        self.balance=10000
        self.customers=[]
        self.transactions=[]
        self.logged_in_user=None
    def password_standard(self,password):
        count_u,count_l=0,0
        
            
        for i in password:
            if i.isupper():
                count_u+=1
            if i.islower():
                count_l+=1
        if count_u>=2 and count_l>=2 and len(password)>=6:
            return True
        else:
            return False
    def encrypt(self,password):
        encrypted=""
        for i in password:
            if i.isalpha():
                encrypted+=chr(ord(i)+1)
            elif i.isdigit():
                encrypted += str((int(i) + 1) % 10)
        return encrypted
            
    def add_new_customers(self,name,new_password,conform_password):
        
        
        
        if not self.password_standard(new_password):
            return("Password is violating the standard: must have at least 2 uppercase letters, "
                  "2 lowercase letters, and be at least 6 characters long.")
        elif new_password!=conform_password:
            return("password does not match")
        else:
            new_password=self.encrypt(new_password)
            
            cust_id=10000+len(self.customers)
                
            cust_details={
            'cust_id': cust_id,'name':name,'balance':self.balance,'password':new_password
        }
        
            self.customers.append(cust_details)
            return("kindly note your account number for future use: ",cust_id)
    def login(self,cust_id,password):
        encrypted=self.encrypt(password)
        for customer in self.customers:
            if customer['cust_id']==cust_id and customer['password']==encrypted:
                self.logged_in_user=cust_id
                return("logged in successfully")
            
        return("password or cust_id is incorrect")
        
    def withdraw(self,amt):
        if  self.logged_in_user:
            for customer in self.customers:
                if customer['cust_id']==self.logged_in_user:
                    if (customer['balance']-1000)<amt:
                        return("low balance")
                    customer['balance']-=amt
                    
                    transactions_details={
                'cust_id':self.logged_in_user,
                'operation_type':'withdraw',
                'amount':amt
            }
                    self.transactions.append(transactions_details)
                    return(amt,"debited from your account. current balance:",customer['balance'])
    def deposit(self,amt):
        if  self.logged_in_user:
            for customer in self.customers:
                if customer['cust_id']==self.logged_in_user:
                    customer['balance']+=amt
                    
                    transactions_details={
                'cust_id':self.logged_in_user,
                'operation_type':'deposit',
                'amount':amt
            }
                    self.transactions.append(transactions_details)
                    return(amt,"credited from your account. current balance:",customer['balance'])
    def acc_tranfer(self,to_acc,amt):
        if self.logged_in_user:
            from_acc=None
            to_cust=None


            for customer in self.customers:
                if customer['cust_id']==self.logged_in_user:
                    from_acc=customer
                if customer['cust_id']==to_acc:
                    to_cust=customer
            
            if not to_cust:
                return("user not found")
            
            if(from_acc['balance']-1000)<amt:
                return("low balance")
            from_acc['balance']-=amt
            to_cust['balance']+=amt
            
            
            
            transactions_details=[{
                'cust_id':self.logged_in_user,
                'operation_type':'account transfer',
                'amount':amt
            },{'cust_id':to_acc,
                'operation_type':'credited',
                'amount':amt}]
            
            self.transactions.extend(transactions_details)
            return("transaction successful")

    def top_n(self,n):
        top_customers=[]
        for i in range(n):
            max_bal=0
            for customer in self.customers:
                if customer not in top_customers and customer['balance']>max_bal:
                    max_bal=customer['balance']
                    top_customers.append(customer)
        return top_customers


            
c=Customers()
while True:
    user=input("register or login or admin : ")
    if user=="register":
        name=input("enter name: ")
        set_password=input("set a password: ")
        conform_password=input("conform password: ")
        res=c.add_new_customers(name,set_password,conform_password)
        print(res)
    if user=="login":
        cust_id=int(input("enter customer id: "))
        password=input("enter password")
        log_res=c.login(cust_id,password)
        print(log_res)
        while True:
            operation=input("1) withdraw 2)deposit 3) account transfer 4) logout: ")
            if operation=="withdraw":
                amt=int(input("enter amount to withdraw: "))
                print(c.withdraw(amt))
            if operation=="deposit":
                amt=int(input("enter amount to desposit: "))
                print(c.deposit(amt))
            if operation=="account transfer":
                amt=int(input("enter amount to transfer: "))
                to_acc=int(input("enter account number of receiver: "))
                print(c.acc_tranfer(to_acc,amt))
            if operation=="logout":
                c.logged_in_user=None
                print("logged out successfully")
                break
       
    if user=="admin":
        id=input("enter id: ")
        admin_password=input("enter password: ")
        if id=="admin123" and admin_password=="Welcomeadmin":
            print("admin logged in successfully!")
            operation=input("1) customers, 2) top n customers, 3) transactions: ")
            if operation=='customers':
                print(c.customers)
            if operation=='top n customers':
                n=int(input("top (1/2/3/...) customers:"))
                top_res=c.top_n(n)
                print(top_res)
            if operation=="transactions":
                print(c.transactions)
        else:
            print("wrong Id or password")
    
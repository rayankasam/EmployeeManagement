email= "hi2gmail.com"
password="1234s"
employeeID="00011"
line = "\n"+email +"\t"+ password +"\t" +employeeID
with open('password.txt', 'a') as fh:
    fh.writelines(line)  
with open('password.txt', 'a') as fh:
    fh.writelines(line)  

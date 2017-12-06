#!/usr/bin/env python3


from utils import db_connect

from bson.objectid import ObjectId
from datetime import datetime
import utils 
import cgi
import cgitb
cgitb.enable()


#db = utils.db_connect()
db = db_connect()





print("Content-Type: text/html\n")
print("""!<DOCTYPE html>
<html lang ="en">
<head>
<meta charset"utf-8">
<title>Hello My Cat</title>
</head>
<body>
<h1>Welcome to Catman</h1>""")

form = cgi.FieldStorage()

result = db.images.aggregate(
	[{'$sample': { 'size' : 1} } ]
)

if result:
	
	for img in result:
		img_src = img['url']
		img_alt = img['alt']
		img_id = img['_id']


	num_flucks = db.flucks.find( {"image_id": ObjectId(img_id), "is_flucked": 1} ).count()
	image = db.images.find_one({})


#print(image['url'], image['alt'])
	print("""<p>You are viewing a random image of a Cat.</p>
	<img src="{}" alt="{}" width=500>
	<p>This poor cat has been flucked {} times already.</p>
	<a href="/cgi-bin/serve_cat.py" title="serve cat">Skip this cat</a>
	""".format( img_src, img_alt,str(num_flucks) ))
else:
	print("<p> Oops. Something went wrong!</p>")

print("""<form method = "POST" action="/cgi-bin/serve_cat.py"
	<input type = "hidden" value="{}" name = "img_id">
	<input type = "submit" name= "btn_skip" value="Skip">
	<input type = "submit" name = "btn_fluck" value="Fluck">
	</form> """.format(img_id) )

if 'btn_fluck' in form:
	result = db.flucks.insert({
#		"image_id":ObjectId(form['img_id'].value),
		"is_flucked":1,
		"timestamp":datetime.now().timestamp()
	})
elif 'btn_skip' in form:
	result = db.flucks.insert({
#		"image_id":ObjectId(form['img_id'].value),
		"is_flucked":0,
		"timestamp":datetime.now().timestamp()

})



print("</body></html>")

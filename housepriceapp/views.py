from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,redirect
from django.db import connection
# Create your views here.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mpl_toolkits
from sklearn.preprocessing import scale
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import ensemble



def predict(request):
	data = pd.read_csv("housedata.csv")
	data.head()
	data.describe()

	data['bedrooms'].value_counts().plot(kind='bar')
	plt.title('number of Bedroom')
	plt.xlabel('Bedrooms')
	plt.ylabel('Count')
	sns.despine

	plt.figure(figsize=(10,10))
	sns.jointplot(x=data.lat.values, y=data.long.values, height=10)
	plt.ylabel('Longitude', fontsize=12)
	plt.xlabel('Latitude', fontsize=12)
	plt.show()
    
	sns.despine

	plt.scatter(data.price,data.sqft_living)
	plt.title("Price vs Square Feet")
	plt.scatter(data.price,data.long)
	plt.title("Price vs Location of the area")
	plt.scatter(data.price,data.lat)
	plt.xlabel("Price")
	plt.ylabel('Latitude')
	plt.title("Latitude vs Price")
	
	plt.scatter(data.bedrooms,data.price)
	plt.title("Bedroom and Price ")
	plt.xlabel("Bedrooms")
	
	plt.ylabel("Price")
	plt.show()
	sns.despine
	
	plt.scatter((data['sqft_living']+data['sqft_basement']),data['price'])
	
	plt.scatter(data.waterfront,data.price)
	plt.title("Waterfront vs Price ( 0= no waterfront)")
	plt.show()
	train1 = data.drop(['id', 'price'],axis=1)
	
	print(train1.head())
	data.floors.value_counts().plot(kind='bar')
	plt.show()
	plt.scatter(data.floors,data.price)
	plt.show()
	
	plt.scatter(data.condition,data.price)
	plt.show()
	plt.scatter(data.zipcode,data.price)
	plt.title("Which is the pricey location by zipcode?")

	reg = LinearRegression()
	labels = data['price']
	conv_dates = [1 if values == 2014 else 0 for values in data.date ]
	data['date'] = conv_dates
	train1 = data.drop(['id', 'price'],axis=1)
	
	x_train , x_test , y_train , y_test = train_test_split(train1 , labels , test_size = 0.10,random_state =2)
	reg.fit(x_train,y_train)
	
	print(reg.score(x_test,y_test))
	
	clf = ensemble.GradientBoostingRegressor(n_estimators = 400, max_depth = 5, min_samples_split = 2,
          learning_rate = 0.1, loss = 'ls')
	
	clf.fit(x_train, y_train)
	
	print(clf.score(x_test,y_test))
	
	t_sc = np.zeros((400),dtype=np.float64)
	y_pred = reg.predict(x_test)
	for i,y_pred in enumerate(clf.staged_predict(x_test)):
		t_sc[i]=clf.loss_(y_test,y_pred)
	testsc = np.arange((400))+1
	plt.figure(figsize=(12, 6))
	plt.subplot(1, 2, 1)
	plt.plot(testsc,clf.train_score_,'b-',label= 'Set dev train')
	plt.plot(testsc,t_sc,'r-',label = 'set dev test')
	plt.show()
	
	pca = PCA()
	pca.fit_transform(scale(train1))
	return render(request,'index.html')

def index(request):
	return render(request,'index.html')

def user_registration(request):
	return render(request,'user_registration.html')
	
def builder_registration(request):
	return render(request,'builder_registration.html')

def login(request):
	return render(request,'login.html')
	
def projectdetails(request):
	return render(request,'projectdetails.html')
	
def userhome(request):
	return render(request,'userhome.html')
	
def builderhome(request):
	return render(request,'builderhome.html')
	
def aquery(request):
	n=request.GET['id']
	return render(request,'aquery.html',{'pid':n})
	
def vbuilder(request):
	cur=connection.cursor()
	s="select * from builder"
	cur.execute(s)
	rs=cur.fetchall()
	blist=[]
	for row in rs:
		w={'bid':row[0],'name':row[1],'phnno':row[2],'email':row[3],'address':row[4],'regno':row[5]}
		blist.append(w)
	return render(request,'vbuilder.html',{'blist':blist})
	
def vbuilder1(request):
	cur=connection.cursor()
	s="select * from builder"
	cur.execute(s)
	rs=cur.fetchall()
	blist=[]
	for row in rs:
		w={'bid':row[0],'name':row[1],'phnno':row[2],'email':row[3],'address':row[4],'regno':row[5]}
		blist.append(w)
	return render(request,'vbuilder1.html',{'blist':blist})
	
def vflat(request):
	cur=connection.cursor()
	i=request.GET['id']
	s="select * from flat where pid='%s'"%(i)
	cur.execute(s)
	rs=cur.fetchall()
	flist=[]
	for row in rs:
		w={'fid':row[0],'cat':row[1],'bed':row[2],'bath':row[3],'fn':row[4],'tsq':row[5],'lsq':row[6],'rsq':row[7],'pid':row[8]}
		flist.append(w)
	return render(request,'vflat.html',{'flist':flist})

def adminhome(request):
	return render(request,'adminhome.html')

def vuser(request):
	cur=connection.cursor()
	s="select * from user"
	cur.execute(s)
	rs=cur.fetchall()
	ulist=[]
	for row in rs:
		w={'uid':row[0],'name':row[1],'phnno':row[2],'email':row[3]}
		ulist.append(w)
	return render(request,'vuser.html',{'ulist':ulist})

def flat_details(request):
	n=request.GET['id']
	return render(request,'flat_details.html',{'id':n})

def vproject(request):
	cursor=connection.cursor()
	id=request.session['id']
	sql="select * from project where bid='%s'"%(id)
	cursor.execute(sql)
	rs=cursor.fetchall()
	plist=[]
	for row in rs:
		x={'pid':row[0],'name':row[1],'loc':row[2],'nf':row[3],'sqft':row[4],'rate':row[5],'regno':row[6]}
		plist.append(x)
	return render(request,'vproject.html',{'plist':plist})

def vqueries(request):
	cursor=connection.cursor()
	i=request.GET['id']
	sql="select * from query where pid='%s'"%(i)
	cursor.execute(sql)
	rs=cursor.fetchall()
	qlist=[]
	for row in rs:
		x={'name':row[3],'que':row[1],'pid':row[2]}
		qlist.append(x)
	return render(request,'vqueries.html',{'qlist':qlist})	
	
def vproject1(request):
	cursor=connection.cursor()
	i=request.GET['id']
	sql="select * from project where bid='%s'"%(i)
	cursor.execute(sql)
	rs=cursor.fetchall()
	plist=[]
	for row in rs:
		x={'pid':row[0],'name':row[1],'loc':row[2],'nf':row[3],'sqft':row[4],'rate':row[5],'regno':row[6]}
		plist.append(x)
	return render(request,'vproject1.html',{'plist':plist})	

def user(request):
	cursor=connection.cursor()
	n=request.GET['name']
	ph=request.GET['phn']
	m=request.GET['mail']
	p=request.GET['pass']
	cp=request.GET['cpass']
	
	if p == cp:
		sql="insert into user (name,phnno,email) values('%s','%s','%s')" %(n,ph,m)
		cursor.execute(sql)
	
		sql1="select max(uid) as uid from user"
		cursor.execute(sql1)
		rs=cursor.fetchall()
	
		for row in rs:
			sql3="insert into login(id,email,password,type) values('%s','%s','%s','user')" %(row[0],m,p)
			cursor.execute(sql3)
	
		msg="<script>alert('success');window.location='/index/';</script>"
		
	else:
		msg="<script>alert('Passwords doesn't match!');window.location='/user_registration/';</script>"
	return HttpResponse(msg)
	
def builder(request):
	cursor=connection.cursor()
	n=request.GET['name']
	ph=request.GET['phn']
	m=request.GET['mail']
	a=request.GET['add']
	l=request.GET['lno']
	p=request.GET['pass']
	cp=request.GET['cpass']
	
	if p==cp:
		sql="insert into builder (name,phnno,email,address,regno) values('%s','%s','%s','%s','%s')" %(n,ph,m,a,l)
		cursor.execute(sql)
	
		sql1="select max(bid) as bid from builder"
		cursor.execute(sql1)
		rs=cursor.fetchall()
	
		for row in rs:
			sql3="insert into login(id,email,password,type) values('%s','%s','%s','builder')" %(row[0],m,p)
			cursor.execute(sql3)
	
	
		msg="<script>alert('success');window.location='/index/';</script>"
	else:
		msg="<script>alert('Passwords doesn't match!');window.location='/builder_registration/';</script>"
	return HttpResponse(msg)
	
def loginac(request):
	cursor=connection.cursor()
	un=request.GET['un']
	up=request.GET['up']
	sql="select * from login where email='%s' and password='%s'"%(un,up)
	cursor.execute(sql)
	if(cursor.rowcount)>0:
		rs=cursor.fetchall()
		for row in rs:
			request.session['id']=row[0]
			request.session['type']=row[3]
		if(request.session['type']=="user"):
			return render(request,'userhome.html')
		if(request.session['type']=="builder"):
			return render(request,'builderhome.html',{'id':request.session['id']})
		if(request.session['type']=="admin"):
			return render(request,'adminhome.html')
	else:
		msg="<script>alert('Login Failed');window.location='/login/';</script>"
		return HttpResponse(msg)

def projectac(request):
	cursor=connection.cursor()
	id=request.session['id']
	n=request.GET['name']
	l=request.GET['loc']
	b=request.GET['bed']
	s=request.GET['sq']
	r=request.GET['rsq']
	rn=request.GET['rno']
	
	sql="insert into project(name,loc,nf,sqft,rate,regno,bid) values('%s','%s','%s','%s','%s','%s','%s')" %(n,l,b,s,r,rn,id)
	cursor.execute(sql)
	
	msg="<script>alert('success');window.location='/projectdetails/';</script>"
	return HttpResponse(msg)
	
def flat(request):
	cursor=connection.cursor()
	i=request.GET['pid']
	n=request.GET['cat']
	ph=request.GET['bed']
	m=request.GET['bath']
	f=request.GET['fn']
	a=request.GET['sq']
	l=request.GET['lsq']
	p=request.GET['rate']
	tt=int(l)*int(p)
	
	sql="insert into flat (cat,bed,bath,fn,tsq,lsq,rsq,pid,price) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(n,ph,m,f,a,l,p,i,tt)
	cursor.execute(sql)
	
	
	msg="<script>alert('success');window.location='/vproject/';</script>"
	return HttpResponse(msg)
	
def delp(request):
	cursor=connection.cursor()
	n=request.GET['id']
	
	sql="delete from project where pid='%s'" %(n)
	cursor.execute(sql)
	
	
	msg="<script>alert('Deleted');window.location='/vproject/';</script>"
	return HttpResponse(msg)
	
def que(request):
	cursor=connection.cursor()
	i=request.GET['pid']
	n=request.GET['q']
	u=id=request.session['id']
	sql1="select name from user where uid='%s'"%(u)
	cursor.execute(sql1)
	un=cursor.fetchall()
	for r in un:
		sql="insert into query(que,pid,un) values('%s','%s','%s')" %(n,i,r[0])
		cursor.execute(sql)
	
	
	msg="<script>alert('success');window.location='/aquery/';</script>"
	return HttpResponse(msg)

def hpredict(request):
	cur=connection.cursor()
	flist=[]
	cur.execute("truncate table temp")
	s1="select distinct(loc) as loc from project"
	cur.execute(s1)
	rs1=cur.fetchall()
	for r1 in rs1:
		s="select builder.name,project.name,phnno,email,bed,bath,tsq,lsq,rsq,price from flat inner join project on project.pid=flat.pid inner join builder on builder.bid=project.bid where price=(select max(price) from flat inner join project on project.pid=flat.pid where project.loc='%s')"%(r1[0])
		cur.execute(s)
		rs=cur.fetchall()
		print(s)
		for r in rs:
			s3="insert into temp values('%s','%s','%s','%s','%s','%s','%s','high','%s')"%(r[0],r[1],r[4],r[5],r[6],r[8],r[9],r1[0])
			cur.execute(s3)
			print(s3)
		
		s="select builder.name,project.name,phnno,email,bed,bath,tsq,lsq,rsq,price from flat inner join project on project.pid=flat.pid inner join builder on builder.bid=project.bid where price=(select min(price) from flat inner join project on project.pid=flat.pid where project.loc='%s')"%(r1[0])
		cur.execute(s)
		rs=cur.fetchall()
		print(s)
		for r in rs:
			s3="insert into temp values('%s','%s','%s','%s','%s','%s','%s','low','%s')"%(r[0],r[1],r[4],r[5],r[6],r[8],r[9],r1[0])
			cur.execute(s3)
			print(s3)

	ss="select * from temp"
	cur.execute(ss)
	rss=cur.fetchall()
	for i in rss:
		w={'bname':i[0],'pname':i[1],'bed':i[2],'bath':i[3],'tsq':i[4],'rsq':i[5],'price':i[6],'stat':i[7],'loc':i[8]}
		flist.append(w)

	hlist=[]
	ss="select * from temp where stat='high'"
	cur.execute(ss)
	rss=cur.fetchall()
	for i in rss:
		w={'bname':i[0],'pname':i[1],'bed':i[2],'bath':i[3],'tsq':i[4],'rsq':i[5],'price':i[6],'stat':i[7],'loc':i[8]}
		hlist.append(w)
	
	llist=[]
	ss="select * from temp where stat='low'"
	cur.execute(ss)
	rss=cur.fetchall()
	for i in rss:
		w={'bname':i[0],'pname':i[1],'bed':i[2],'bath':i[3],'tsq':i[4],'rsq':i[5],'price':i[6],'stat':i[7],'loc':i[8]}
		llist.append(w)

	lplist=[]
	ss="select loc from temp where price=(select min(price) from temp where stat='low')"
	cur.execute(ss)
	rss=cur.fetchall()
	for i in rss:
		w={'loc':i[0]}
		lplist.append(w)

	hplist=[]
	ss="select loc from temp where price=(select max(price) from temp where stat='high')"
	cur.execute(ss)
	rss=cur.fetchall()
	for i in rss:
		w={'loc':i[0]}
		hplist.append(w)
	

	return render(request,'hpredict.html',{'flist':flist,'hlist':hlist,'llist':llist,'hplist':hplist,'lplist':lplist})


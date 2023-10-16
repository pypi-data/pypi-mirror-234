import pandas as pd
import numpy as np
from enum import Enum
import datetime as dt
from threading import Semaphore
from threading import Lock
from dhanhq import *
import yfinance as yf 
import time
#import gfdlws as gw
#import sys
# pip install wsgfdl-py==1.3.1
# con = gw.ws.connect(<EndPoint>, <API Key>)
# {"Complete":true,"Message":"Welcome!","MessageType":"AuthenticateResult"}"
"""
# Use InstrumentIdenfier value "NIFTY 50", "NIFTY BANK", "NIFTY 100", etc.
# Use NSE_IDX as Exchange
# Please note that Indices Symbols have white space. 
# For example, between NIFTY & 50, NIFTY & BANK above
"""
# -----  Realtime data ----
# con = gw.ws.connect(<EndPoint>, <API Key>)
# while True:
#     time.sleep(1)
#    response = gw.realtime.get(con, 'NFO', 'NIFTY-I')
#    print(str(response))
"""
# {	
    "Exchange":"NFO",
    "InstrumentIdentifier":"NIFTY-I",
    "LastTradeTime":1669262572,
    "ServerTime":1669262572,
    "AverageTradedPrice":18309.69,
    "BuyPrice":18323.9,
    "BuyQty":50,
    "Close":18286.75,
    "High":18329.35,
    "Low":18297.15,
    "LastTradePrice":18325.0,
    "LastTradeQty":750,
    "Open":18310.0,
    "OpenInterest":5657350,
    "QuotationLot":50.0,
    "SellPrice":18325.1,
    "SellQty":100,
    "TotalQtyTraded":681250,
    "Value":12473476312.5,
    "PreOpen":false,"PriceChange":38.25,"PriceChangePercentage":0.21,
    "OpenInterestChange":-98200,
    "MessageType":"RealtimeResult"
    }
"""
#  -----  History data ----
# response = gw.history.getbyperiod(con,<Exchange>,<InstrumentIdentifier>,<Periodicity>, <Period>,<Max>,<UserTag>,<isShortIdentifier Optional [true]/[false][default=false]>)
# response = gw.history.getbyperiod(con,'NFO','NIFTY-I','MINUTE','1','1658115000','1658138400','dhananjay','false')
# print(str(response))
"""
{
    "LastTradeTime":1658138400,
    "QuotationLot":50,
    "TradedQty":800,
    "OpenInterest":11179850,
    "Open":16312.95,
    "High":16312.95,
    "Low":16312.95,
    "Close":16312.95
},
{
    "LastTradeTime":1658138340,
    "QuotationLot":50,
    "TradedQty":89800,
    "OpenInterest":11179850,
    "Open":16305.0,
    "High":16312.0,
    "Low":16304.45,
    "Close":16310.0
}
...
"""
# (18-07-2022 15:30:00)
# response = gw.history.getcaldle(con,'NFO','NIFTY-I','MINUTE','1','10','dhananjay','false')
# print(str(response))
"""
[{
    "LastTradeTime":1594186301,
    "LastTradePrice":10775.0,
    "QuotationLot":75,
    "TradedQty":225,
    "OpenInterest":12176625,
    "BuyPrice":10774.3,
    "BuyQty":75,
    "SellPrice":10775.0,
    "SellQty":3150},
{
    "LastTradeTime":1594186300,
    "LastTradePrice":10774.0,
    "QuotationLot":75,
    "TradedQty":0,
    "OpenInterest":12176625,
    "BuyPrice":10774.3,
    "BuyQty":75,
    "SellPrice":10775.0,
    "SellQty":3375}*
"""
# class bars
class bars:
	# class ticks
	class ticks:
		def __init__(self,f,p):
			ohlc = {'Open':'first',
				'High':'max',
				'Low':'min',
				'Close':'last'}
			self.f = f.resample(p,offset='15min').apply(ohlc)
			self.f.dropna()
			self.f = self.f[self.f.Open.notnull() & 
				self.f.High.notnull() & 
				self.f.Low.notnull() & 
				self.f.Close.notnull()]
			self.f['a']=(f.Open+f.High+f.Low+f.Close)/4
			self.f['c'] = self.f.a.ewm(alpha=0.5,adjust=False).mean()
			self.f['o'] = (
					(
						self.f.Open.shift(1) + self.f.c.shift(1)
					)/2
				).ewm(alpha=0.5,adjust=False).mean()

			#t = np.maximum(self.f.High,self.f.o)
			self.f['h'] = (np.maximum(
						np.maximum(
							self.f.High,
							self.f.o
							),
							self.f.c
						)
					).ewm(alpha=0.5,adjust=False).mean()

			#t = np.minimum(self.f.Low,self.f.o)
			self.f['l'] = (np.minimum(
						np.minimum(
							self.f.Low,
							self.f.o
							),
							self.f.c
						)
					).ewm(alpha=0.5,adjust=False).mean()				
			self.f['fasttm'] = self.gettma(self.f.a,12)
			self.f['slowtm'] = self.gettma(self.f.a,24)
			def vals():
				if(list(self.f.o) > list(self.f.c)):
					return True
				else:
					return False			
			
			self.f['up']=vals()
			#print(self.f.shape)
		pass

	def trend(self):
		return self.f.up
		pass
	
	def fastm(self):
		return self.f.fasttm
		pass
	
	def slotm(self):
		return self.f.slowtm
		pass
	
	
	def getsma(self,N):
	    	return (self.f.avg.rolling(N).mean()).fillna(0)
	    	pass
	
	def getema(self,s,N):
	    	k=2/(1+N)
	    	return s.ewm(alpha=k,adjust=False).mean()
	    	pass
	
	def gettma(self,s,N):
	    	k=2/(1+N)
	    	e1 = self.getema(s,N)
	    	e2 = self.getema(e1,N)
	    	e3 = self.getema(e2,N)
	    	return (3*e1) - (3*e2) + e3
	    	pass	
	    
	def getdf(self):
	    	return self.f
	    	pass	
	    
	def getindex(self):
	    	return self.f.index
	    	pass	
	    
	def getopen(self):
	    	return self.f.o
	    	pass	
	    
	def gethigh(self):
	    	return self.f.h
	    	pass	
	    
	def getlow(self):
	    	return self.f.l
	    	pass	
	    
	def getclose(self):
	    	return self.f.c
	    	pass	
	    
	def getavg(self):
	    	return self.f.a
	    	pass
	pass

	
	# class utils
	class utils:
		def __init__(self):
			self.i='log.txt'
		pass
		
		###
		### epoh conversions
		###
		
		def toepoch(self,yr,mo,da,ho,mi,se):
		    	return dt.datetime(yr,mo,da,ho,mi,se).timestamp()
		    	pass
		    
		def fromepoch(self,ep):
		    	return dt.datetime.fromtimestamp(ep)
		    	pass		
		
		###
		### event log
		### file read write
		###
		
		def logevent(self,msg):
		    	try:
		        	with open(self.i,'a') as f:
		            		f.write(
		                	str(self.timenow())+" "+msg+'\n'
		            		)
		    	except:
		        	print('Error: logevent file open-close')
		    	pass
		    
		def readevents(self):
		    	try:
		        	with open(self.i,'r') as f:
		        		print(f.read())
		    	except:
		        		print('Error: readevent file open-close')
		    	pass
		    
		def printline(self,s):
		    	l=''
		    	for i in range(0,25):
		        	l+=s
		    	try:
		        	with open(self.i, 'a') as f:
		            		f.write(l+'\n') #msg='Error: File open-close@ {0}'.format(dt.datetime.now()) #print(msg)
		    	except:
		            	msg='Error: printline file open-close'
		            	print(msg)
		    	pass
		
		###
		### time now and preset date today
		###
		
		def timenow(self):
		    	return dt.datetime.now()
		    	pass
		    
		
		def todey(self):
		    	return (dt.datetime.now()).date()
		    	pass
		    		
		###
		### dhn operations
		###
		
		def enter(self,i,k):
		    	try:
		        	d = dhanhq(i,k)
		    	except:
		        	logeevent('Error: broker connection ')
		    	finally:
		        	return d
		    	pass
		    
		def funds(self,d):
		    	return (
		        	(
		                	d.get_fund_limits()
		                ).get('data')).get('availabelBalance')
		    	pass
				
		def getorderid(self,d,pos):
		    	return (
		        	(
		                	d.get_order_list()
		            	).get('data')[pos]).get('orderId')
		    	pass
		    
		def getsecurityid(self,d,pos):
		    	return (
		        	(
		                	d.get_order_list()).get('data')[pos]).get('securityId')
		    	pass
		
		def getorderstatus(self,d,pos):
		    	return (
		        	(
		                	d.get_order_list()
				).get('data')[pos]).get('orderStatus')
		
		def cancelorder(self,d,oid):
		    	return d.cancel_order(oid)
		    	pass
	
		
		def cancelall(self,d):
			k=d.get_order_list()
			for i in range(0, len(k.get('data'))):
				d.cancel_order(self.getorderid(d,i))
			pass

		def sail(self,d,secid,q,p):
		    	try:
		        	soi = d.place_order(
		                            security_id=secid,   
		                            exchange_segment=d.FNO,
		                            transaction_type=d.SELL,
		                            quantity=q,
		                            order_type=d.MARKET,
		                            product_type=d.INTRA,
		                            price=p
		                            )
		    	except:
		        	self.logevent('Error: sell order')
		    	finally:
		        	self.logevent('buy order id'+str(soi))
		    	return soi
		    	pass

		def bye(self,d,secid,q,p):
			try:
		        	boi = d.place_order(
		                            security_id=secid,
		                            exchange_segment=d.FNO,
		                            transaction_type=d.BUY,
		                            quantity=q,
		                            order_type=d.MARKET,
		                            product_type=d.INTRA,
		                            price=p
		                            )
			except:
				self.logevent('Error: buy order')
			finally:
				self.logevent('buy order id'+str(boi))
				return boi
			pass
		###
		### gdfl operations 
		###
		
		def gdflindex(self):
		    	return 'NIFTY&50.NSE_IDX' # 'NIFTY&BANK.NSE_IDX'
		    	pass
		    
		# 	NIFTY06JAN2217200CE - 
		#	BASE+EXPDATE(2DIGIT)-MON(3CHAR)-EXPYR(2-DIGIT)-STRIKE-CE/PE	
		def gdflcall(self,d,m,y,s):
			return 'NIFTY'+d+m+y+str(s)+'CE'
			pass
		    
		def gdflput(self,d,m,y,s):
		    	return 'NIFTY'+d+m+y+str(s)+'PE'
		    	pass
		    
		def gdflniftyfut(self,d,m,y):
		    	return 'NIFTY'+d+m+y+'FUT'
		    	pass
		    
		def gdflbankniftyfut(self,d,m,y):
		    	return 'BANKNIFTY'+d+m+y+'FUT'
		    	pass
			
		pass
	
	# scrips
	class scrips:
		def __init__(self, path, ltp, day, month, year):
			self.u=utils()
			self.ltp=ltp
			above=float(ltp+100)
			below=float(ltp-100)
			df=pd.read_csv(path)
			# NIFTY 27 JUN 72000 CALL OR, NIFTY 26 OCT
			targetday='NIFTY'+' '+day+' '+month
			# get exchange
			#exdf=df.loc[f.SEM_EXM_EXCH_ID.str.contains('NSE'),:]
			# get options
			oidf=df.loc[df.SEM_INSTRUMENT_NAME.str.contains('OPTI\w+'),:]
			# get options for given strike
			tddf=oidf.loc[oidf.SEM_CUSTOM_SYMBOL.str.startswith(targetday),:]
			# get withn strikes
			oit=tddf.query('SEM_STRIKE_PRICE < @above & SEM_STRIKE_PRICE > @below')
			# get all calls
			self.ces=oit.loc[oit.SEM_OPTION_TYPE.str.contains('CE'),:]
			# get all puts
			self.pes=oit.loc[oit.SEM_OPTION_TYPE.str.contains('PE'),:]
			# get all futs        
			self.fidf=df.loc[df.SEM_INSTRUMENT_NAME.str.contains('FUTI\w+'),:]
			#print(self.fidf)
			
			# validate in expiry is today 
			if(str(self.u.todey()) in str(list(self.pes.SEM_EXPIRY_DATE)[0])):
				self.isexpiryday=True
			else:
			    	self.isexpiryday=False
			    	
			if(self.isexpiryday): #ltp=19667.4
				self.strike_below 	= (int((self.ltp+50)/50)*50)-50
				self.strikece 		= str(self.strike_below)+"-CE"
				self.strike_above 	= int((self.ltp+50)/50)*50
				self.strikepe 		= str(self.strike_above)+"-PE"
				self.gdfce		= self.u.gdflcall(day,month,year,self.strike_below)
				self.gdfpe		= self.u.gdflcall(day,month,year,self.strike_above)
				self.pes		= self.pes.loc[self.pes.SEM_TRADING_SYMBOL.str.endswith(self.strikepe),:]
				self.ces		= self.ces.loc[self.ces.SEM_TRADING_SYMBOL.str.endswith(self.strikece),:]
			else:
		    		self.strike_above 	= int((self.ltp+50)/50)*50
		    		self.strikece 		= str(self.strike_above)+"-CE"
		    		self.strike_below 	= (int((self.ltp+50)/50)*50)-50
		    		self.strikepe		= str(self.strike_below)+"-PE"
		    		self.gdfce		= self.u.gdflcall(day,month,year,self.strike_above)
		    		self.gdfpe		= self.u.gdflcall(day,month,year,self.strike_below)
		    		self.pes		= self.pes.loc[self.pes.SEM_TRADING_SYMBOL.str.endswith(self.strikepe),:]
		    		self.ces		= self.ces.loc[self.ces.SEM_TRADING_SYMBOL.str.endswith(self.strikece),:]
			pass
		
		def peid(self): 
			return (self.pes.iloc[0,2:3]).to_numpy()[0]
			pass

		def ceid(self): 
			return (self.ces.iloc[0,2:3]).to_numpy()[0]
			pass

		def futid(symbol): 
			t=self.df.loc[self.df.SEM_TRADING_SYMBOL.str.startswith(self.symbol),:]
			return (t.iloc[0,2:3]).to_numpy()[0]
			pass
		
		def isexpiry(self): 
			return self.isexpiryday
			pass
		
		def gdflce(self):
			return self.gdfce
			pass
			
		def gdflpe(self):
			return self.gdfpe
			pass
			
		pass

	# enum type fix
	class fix(Enum):
		me_ 		= '1101194979'
		one 		= '1Min'
		fiv 		= '5Min'
		ten 		= '10Min'
		pass

    	# enum type month
	class month(Enum):
		JAN = 1
		FEB = 2
		MAR = 3
		APR = 4
		MAY = 5
		JUN = 6
		JUY = 7
		AUG = 8
		SEP = 9
		OCT = 10
		NOV = 11
		DEC = 12
		pass 
	
		    
	def preset(self,path,spotprice,expiryday,month,year):
		# initial scrips
		try:
			self.s=self.scrips(path,spotprice,expiryday,month,year)
			self.cetoken=self.s.gdflce()
			self.petoken=self.s.gdflpe()
			self.cesecid=self.s.ceid()
			self.pesecid=self.s.peid()
		except:
			self.u.logevent('error: scrips preset')
		# initial data 
		d=[{
			"Exchange":"NFO",
			"InstrumentIdentifier":"NIFTY-I",
			"LastTradeTime":1669262572,
			"ServerTime":1669262572,
			"AverageTradedPrice":18309.69,
			"BuyPrice":18323.9,
			"BuyQty":50,
			"Close":18286.75,
			"High":18329.35,
			"Low":18297.15,
			"LastTradePrice":18325.0,
			"LastTradeQty":750,
			"Open":18310.0,
			"OpenInterest":5657350,
			"QuotationLot":50.0,
			"SellPrice":18325.1,
			"SellQty":100,
			"TotalQtyTraded":681250,
			"Value":12473476312.5,
			"PreOpen":False,
			"PriceChange":38.25,
			"PriceChangePercentage":0.21,
			"OpenInterestChange":-98200,
			"MessageType":"RealtimeResult"
		}]
		# create structure 
		self.f=pd.DataFrame(d)
		# delte or dro the row
		self.f=[f.PreOpen!=False]
		# call/put structure
		self.cef=self.f
		self.pef=self.f
		pass
	
	def resize(self,f,p):# process sec data 
		#a=pd.read_csv('nsdata.csv')
		#f.index=pd.to_datetime(a['LastTradeTime'])
		f.index=pd.to_datetime(a['Datetime'])
		"""
		a.drop(a.columns[
			[0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
			],
			axis=1,
			inplace=True
			)
		"""	
		return ticks(self.f,p)
		pass
		
	def run(self):
		d=yf.download(tickers='^NSEI',period='2d',interval='1m')
		# Test Two
		self.startce=False
		self.lockcebuy=Lock()
		self.lockcesel=Lock()
		"""
		# pes
		self.startpe=False
		self.lockpebuy=Lock()
		self.lockpesel=Lock()
		"""
		while True: # With realtime data 
			self.cef=d
			"""
			# ces
		     	self.cef.loc[len(self.cef)]=gw.realtime.get(self.con,'NFO',self.cetoken)
		     	self.cebuyrice=(list(self.cef.BuyPrice))[-1]
		     	self.ceselrice=(list(self.cef.SellPrice))[-1]
		     	# pes
		     	self.pef.loc[len(self.pef)]=gw.realtime.get(self.con,'NFO',self.petoken)
		     	self.pebuyrice=(list(self.pef.BuyPrice))[-1]
		     	self.peselrice=(list(self.pef.SellPrice))[-1]
		     	"""
		     	# wait one sectime.
			time.sleep(1)
			while (dt.datetime.now().time() < dt.time(15,30,00)):
		     		# calls
		     		if(list(self.resize(self.cef,fix.one.value).trend())[-1] == True and list(self.resize(self.cef,fix.fiv.value).trend())[-1] == True):
		     			if(self.lockcebuy.locked()==False):
		     				self.lockcebuy.acquire()
		     				if(self.startce==True):
		     					self.u.logevent('buy ce')
		     				else:
		     					self.startce=True
		     				if(self.lockcesel.locked==True):
		     					self.lockcesel.release()
		     		if(list(self.resize(self.cef,fix.one.value).trend())[-1] == False and list(self.resize(self.cef,fix.fiv.value).trend())[-1] == False):
		     			if(self.lockcesel.locked()==False):
		     				self.lockcesel.acquire()
		     				if(self.startce==True):
		     					self.u.logevent('sell ce')
		     				if(self.lockcebuy.locked()==True):
		     					self.lockcebuy.release()
		     		"""			
		     		# puts
		     		if(list(self.resize(self.pef,fix.one.value).trend())[-1] == list(self.resize(self.pef,fix.fiv.value).trend())[-1] == True):
		     			if(self.lockpebuy.locked()==False):
		     				self.lockpebuy.acquire()
		     				if(self.startpe==True):
		     					self.u.logevent('buy pe')
		     				else:
		     					self.startpe=True
		     				if(self.lockpesel.locked==True):
		     					self.lockpesel.release()
		     		if(list(self.resize(self.pefelf.pef,fix.one.value).trend())[-1] == False):
		     			if(self.lockpesel.locked()==False):
		     				self.lockpesel.acquire()
		     				if(self.startpe==True):
		     					self.u.logevent('sell pe')
		     				if(self.lockpebuy.locked()==True):
		     					self.lockpebuy.release()
		     		"""			

	def __init__(self,bkey):
		self.u=self.utils()
		try: # dhn connection
			self.dhn=self.u.enter(self.fix.me_.value,bkey)
		except:
			self.u.logevent('Error: dhn-connection-null')
		finally:
			self.u.logevent('brokey-success')
		"""	
		try: # gdf connection
			self.con = gw.ws.connect(ep,dkey)
		except:
			self.u.logevent('Error: gdf-connection-null')
		finally:
			self.u.logevent('datkey-success')
		"""
		pass
	pass	

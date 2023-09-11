import os,aiohttp,socket,dotenv,orjson
from .classes import *
from discord.ext import commands

class LastFMException(commands.CommandError):
	def __init__(self,code,message):
		super().__init__()
		self.code=code
		self.message=message

	def __str__(self):
		return f"LastFM Error {self.code}"

	def __display__(self):
		return f"LastFM Error {self.code} : {self.message}"



class LastFM(object):
	def __init__(self,api_key):
		self.key=api_key

	async def request(self,params,ignore_exceptions=True):
		attempts=0
		retries=2
		url="http://ws.audioscrobbler.com/2.0/"
		params['api_key']=self.key
		params['format']='json'
		while True:
			attempts+=1
			async with aiohttp.ClientSession(json_serialize=orjson.dumps,connector=aiohttp.TCPConnector(family=socket.AF_INET)) as session:
				async with session.get(url,params=params,verify_ssl=False) as response:
					try:
						return await response.json(loads=orjson.loads)
					except Exception as e:
						if ignore_exceptions == True:
							if attempts != retries:
								pass
							else:
								raise LastFMException(code=response.status,message=await response.text())
						else:
							raise LastFMException(code=response.status,message=await response.text())

	async def get_track_playcount(self,track:str,artist:str,username:str):
		data=await self.request({'method':'track.getinfo','user':username,'track':track,'artist':artist,'autocorrect':1},ignore_exceptions=True)
		try: return int(data['track']['userplaycount'])
		except: return 0

	async def get_album_playcount(self,artist:str,album:str,username:str):
		data=await self.request({'method':'album.getinfo','artist':artist,'album':album,'user':username,'autocorrect':1})
		try: return int(data['album']['userplaycount'])
		except: return 0

	async def get_artist_playcount(self,username:str,artist:str):
		data=await self.request({'method':'artist.getinfo','artist':artist,'user':username,'autocorrect':1})
		try: return int(data['artist']['stats']['userplaycount'])
		except: return 0

	def normalize(self,value:str):
		return value.replace("+"," ")

	async def get_np(self,username:str):
		req=await self.request({'method':'user.getrecenttracks','user':username,'limit':1})
		tracks=req['recenttracks']['track']
		if tracks:
			if '@attr' in tracks[0] and 'nowplaying' in tracks[0]['@attr']:
				current=True
			else:
				current=False
			tags=[]
			trackurl=tracks[0]['url'] or None
			artisturl=f"https://last.fm/music/{tracks[0]['artist']['#text'].replace(' ','+')}"
			albumurl=tracks[0]['url'] or None
			image=tracks[0]['image'][-1]['#text']
			trackdata=await self.request({'method':'track.getInfo','user':username,'artist':tracks[0]['artist']['#text'],'track':tracks[0]['name']})
			for tag in trackdata['track']['toptags']['tag']:
				tags.append(tag['name'])
			track={'name':tracks[0]['name'],'url':tracks[0]['url'],'playcount':trackdata['track']['userplaycount'],'tags':tags,'image':image,'current':current}
			artist={'name':self.normalize(tracks[0]['artist']['#text']),'url':artisturl,'playcount':await self.get_artist_playcount(username,tracks[0]['artist']['#text'])}
			album={'name':tracks[0]['album']['#text'],'url':albumurl,'playcount':await self.get_album_playcount(tracks[0]['artist']['#text'],tracks[0]['album']['#text'],username),'image':image}
			data={'track':track,'album':album,'artist':artist}
			return NowPlaying(data=data)
		else:
			return None
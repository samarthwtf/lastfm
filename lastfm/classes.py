class User(object):
	def __init__(self,data):
		self.data=data

	@property
	def name(self):
		return self.data['name']

	@property
	def scrobbles(self):
		return int(self.data['playcount'])

class Artist(object):
	def __init__(self,data):
		self.data=data

	@property
	def name(self):
		return self.data['name']

	@property
	def url(self):
		return self.data['url']

	@property
	def playcount(self):
		return int(self.data['playcount'])

class Album(object):
	def __init__(self,data):
		self.data=data

	@property
	def name(self):
		return self.data['name']

	@property
	def image(self):
		return self.data['image']

	@property
	def url(self):
		return self.data['url']

	@property
	def playcount(self):
		return int(self.data['playcount'])

class Track(object):
	def __init__(self,data):
		self.data=data

	@property
	def name(self):
		return self.data['name']

	@property
	def playcount(self):
		return int(self.data['playcount'])

	@property
	def url(self):
		return self.data['url']

	@property
	def image(self):
		return self.data['image']

	@property
	def tags(self):
		return self.data['tags']

	@property
	def current(self):
		return self.data['current']

class NowPlaying(object):
	def __init__(self,data):
		self.data=data

	@property
	def track(self):
		return Track(data=self.data['track'])

	@property
	def artist(self):
		return Artist(data=self.data['artist'])

	@property
	def album(self):
		return Album(data=self.data['album'])
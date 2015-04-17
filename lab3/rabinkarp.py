class Hash:
	def __init__(self, string, size):
		self.str  = string
		self.hash = 0

		for i in xrange(0, size):
			self.hash += ord(self.str[i])

		self.init = 0
		self.end  = size

	def update(self):
		if self.end <= len(self.str) -1:
			self.hash -= ord(self.str[self.init])
			self.hash += ord(self.str[self.end])
			self.init += 1
			self.end  += 1

	def digest(self):
		return self.hash

	def text(self):
		return self.str[self.init:self.end]



def rabin_karp(pattern, text):
	if pattern == None or text == None:
		return -1
	if pattern == "" or text == "":
		return -1

	if len(pattern) > len(text):
		return -1

	hs 	 = Hash(text, len(pattern))
	hsub = Hash(pattern, len(pattern))
	hsub.update()

	for i in range(len(text)-len(pattern)+1):
		if hs.digest() == hsub.digest():
			if hs.text() == pattern:
				return i
		hs.update()

	return -1


def main():
	hay = "aaabaa"
	needle = "ab"
	print(rabin_karp(needle,hay))
#
main()
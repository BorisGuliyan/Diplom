class TextSplitter:

	@staticmethod
	def split(text, separators):
		result = []
		str = ""
		lines = text.splitlines()
		for line in lines:
			for symbol in line:
				if symbol in separators:
					result.append(str)
					str = ""
				else:
					str += symbol
		return result

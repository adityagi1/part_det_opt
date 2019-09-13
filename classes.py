class Detector:
	def __init__(self, detID, version, det_type, profile_size, size_label):
		self.det_id = detID
		self.prof_size = profile_size
		self.version = version
		self.det_type = det_type
		self.size_label = size_label

	def __eq__(self, other):
		if self.det_id == other.det_id:
			return True
		else:
			return False

	def __ne__(self, other):
		assert(type(other) == Detector)
		if self.det_id != other.det_id:
			return True
		else:
			return False
	def __repr__(self):
		return self.det_id
	def __str__(self):
		return self.det_id




class Partition:
	def __init__(self, partID, version, part_type):
		self.part_id = partID
		self.part_type = part_type
		self.version = version

	def __eq__(self, other):
		assert (type(self) == Partition)
		if self.part_id == other.part_id:
			return True
		else:
			return False

	def __ne__(self, other):
		assert (type(self) == Partition)
		if self.part_id != other.part_id:
			return True
		else:
			return False
	def __repr__(self):
		return self.part_id
	def __str__(self):
		return self.part_id






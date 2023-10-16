class RepositoryException(Exception):
	def __init__(self, status_code: int, message: str = 'Repository error'):
		self.message = message
		self.status_code = status_code
		super().__init__(self.message)


class DataException(Exception):
	def __init__(self, message: str = 'Database error'):
		self.message = message
		super().__init__(self.message)

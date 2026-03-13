import threading


class ReadWriteLock:
	"""
	A reentrant read-write lock. 

	Allows multiple readers to access a resource simultaneously, but only one writer at a time. 
	Writers are given priority over readers, meaning that if a writer is waiting to acquire the 
	lock, no new readers will be allowed to acquire the lock until the writer has acquired and 
	released it.

	Note: we have considered replacing it with `RWMutex` from [pygolang](https://lab.nexedi.com/kirr/pygolang),
	however, this project we're not sure how much this project is still maintained, and when adding
	it to our dependencies, it generates an error like "No module named 'imp'", which means it's stuck
	on Python 3.4.
	"""

	def __init__(self):
		self._read_ready = threading.Condition(threading.RLock())
		self._readers = 0
		self._writer = None
		self._write_recursion = 0

	def acquire_read(self):
		with self._read_ready:
			while self._writer is not None and self._writer != threading.get_ident():
				self._read_ready.wait()
			self._readers += 1

	def release_read(self):
		with self._read_ready:
			self._readers -= 1
			if self._readers == 0:
				self._read_ready.notify_all()

	def acquire_write(self):
		with self._read_ready:
			tid = threading.get_ident()
			if self._writer == tid:
				self._write_recursion += 1
				return
			while self._readers > 0 or self._writer is not None:
				self._read_ready.wait()
			self._writer = tid
			self._write_recursion = 1

	def release_write(self):
		with self._read_ready:
			if self._writer != threading.get_ident():
				raise RuntimeError("Cannot release write lock not owned by current thread")
			self._write_recursion -= 1
			if self._write_recursion == 0:
				self._writer = None
				self._read_ready.notify_all ()


class FakeReadWriteLock ( ReadWriteLock ):
	"""
	A fake read-write lock that does nothing.

	This can be used in code that can run in both single-thread and multi-thread mode. When 
	in single-thread, a fake lock can be used anywhere where a regular R/W lock acquires and 
	release locks, without any change to the consuming code. This makes the latter cleaner.

	For an example, see our :class:`brandizpyes.logging.ProgressLogger` class.
	"""

	def __init__ ( self ):
		pass

	def acquire_read ( self ):
		pass

	def release_read ( self ):
		pass

	def acquire_write ( self ):
		pass

	def release_write ( self ):
		pass

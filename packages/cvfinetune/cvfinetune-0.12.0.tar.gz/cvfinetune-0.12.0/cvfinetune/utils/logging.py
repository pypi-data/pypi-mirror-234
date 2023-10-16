import logging

def log_messages(*msg_list, n_chars=10, char="=", logger=None, level=logging.INFO):
	"""
		Adds <chars> and a space at each end of every message.
		Adjusts the length of each message to the maximum length
		of the messages in the list.
	"""

	max_len = max(map(len, msg_list))
	fmt_len = max_len + 2*(n_chars+1)
	fmt = "{:" + char + "^" + str(fmt_len) + "s}"

	logger = logger or logging.getLogger()

	for msg in msg_list:
		logger.log(level, fmt.format(f" {msg} "))

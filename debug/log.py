# log file

class Log(object):
    def __init__(self, name):
        self.name = name
        
    def open_debug_log(self):
        # log file
        log_file_name = self.name + '.log'
        self.file = open(log_file_name, 'w')
        
    def close_debug_log(self):
        self.file.close()

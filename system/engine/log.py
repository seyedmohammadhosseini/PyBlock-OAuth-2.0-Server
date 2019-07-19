import sys
import datetime


class handler:

    def __init__(self, config):
        self.runtime_error_path = config.log.runtime_error_path
        self.type_ = "file"
        pass

    def error(self, output_type, text, location, sys_exit):
        t = datetime.time(1, 2, 3)
        d = datetime.date.today()
        localtime = datetime.datetime.combine(d, t)
        if output_type == "file":
            with open(self.runtime_error_path, "a") as error_log:
                error_log.write("File  : " + location + "\nError : " + text + "\nTime  : " + str(localtime) )
                error_log.write("\n----------------------------------------- \n")
            if sys_exit:
                sys.exit()
        pass
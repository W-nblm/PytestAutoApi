from datetime import datetime, timedelta



class TimeControl:
    @staticmethod
    def get_current_time():
        return datetime.now()
    





if __name__ == '__main__':
    print(TimeControl.get_current_time())
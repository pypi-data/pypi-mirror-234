import sys, time

def slowprint(text:str="Type a string in", delay_time:int=.05):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(delay_time)
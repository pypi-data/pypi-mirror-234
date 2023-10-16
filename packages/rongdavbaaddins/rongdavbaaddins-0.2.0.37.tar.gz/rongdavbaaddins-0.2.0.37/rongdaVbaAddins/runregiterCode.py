import sys
if __name__ == '__main__':
    try:
        c= sys.argv[1]
        from registerCode import run
        run()
    except:
        pass
#count.py
def count_to(n):
    '''Counts up to "n"'''
    for x in range(1,n+1):
        print "%i Elephant" % x

def main():
    count_to(5)

if __name__ == "__main__":
    main()

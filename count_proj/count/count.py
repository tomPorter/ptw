#count.py
def count_to(n):
    '''Counts up to "n"'''
    results = []
    for x in range(1,n+1):
        results.append("%i Elephant" % x)
    return results

def main():
    for x in count_to(5):
        print x

if __name__ == "__main__":
    main()

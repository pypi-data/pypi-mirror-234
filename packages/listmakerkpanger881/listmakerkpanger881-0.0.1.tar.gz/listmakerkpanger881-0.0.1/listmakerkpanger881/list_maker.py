def make_list(*args):
    mylist = [item for item in args]
    # The following line of code added in version 2, absent in version 1,
    # Meaning the new version is incompatible with the old version.
    #mylist.sort()
    return mylist
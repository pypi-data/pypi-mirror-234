import multiprocessing

from echoloader.watcher import main

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()

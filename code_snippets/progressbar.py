import sys


class progressbar(object):
    def __init__(self, finalcount, block_char='.'):
        self.finalcount = finalcount
        self.blockcount = 0
        self.block = block_char
        self.f = sys.stdout
        if not self.finalcount: return
        self.f.write('\n------------------ % Progress -------------------1\n')

    def progress(self, count):
        count = min(count, self.finalcount)
        if self.finalcount:
            percentcomplete = int(round(100.0 * count / self.finalcount))
            if percentcomplete < 1: percentcomplete = 1
        else:
            percentcomplete = 100
        blockcount = int(percentcomplete // 2)
        if blockcount <= self.blockcount:
            return
        for i in range(self.blockcount, blockcount):
            self.f.write(self.block)
        self.f.flush()
        self.blockcount = blockcount
        if percentcomplete == 100:
            self.f.write("\n")


if __name__ == "__main__":
    from time import sleep

    pb = progressbar(100, '#')

    for i in range(0, 101):
        pb.progress(i)
        sleep(0.1)

from listmakerkpanger882 import make_list

def get_top_n(n, *args):
    sorted_list = make_list(item for item in args)
    return sorted_list[:n]

if __name__ == '__main__':
    make_list(1,3,5)

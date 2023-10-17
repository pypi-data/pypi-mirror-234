from listmakerkpanger882 import make_list


class Data:
    def __init__(self, *args):
        self.data = make_list(args)

    def find_item(self, search_item):
        index_list = []
        for index, item in enumerate(self.data):
            if item == search_item:
                index_list.append(item)
        return index_list


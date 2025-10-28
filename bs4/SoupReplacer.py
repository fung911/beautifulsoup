class SoupReplacer:
    def __init__(self, old_tag, new_tag):
        self.old_tag = old_tag
        self.new_tag = new_tag

    def replace(self, tag_name):
        return self.new_tag if tag_name == self.old_tag else tag_name
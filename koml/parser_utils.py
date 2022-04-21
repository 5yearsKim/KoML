
class TagStack:
    def __init__(self):
        self.tag_dict = {}
        self.stack = []
        self.tag_history = [] # for assertion

    def __len__(self):
        return len(self.stack)

    def is_resolved(self):
        return self.stack != [] and self.tag_history == []

    def refresh(self):
        self.tag_dict.clear()
        self.stack.clear()
        self.tag_history.clear()
    
    def push_tag(self, tag, attributes):
        item = (len(self.stack), tag, attributes)
        if tag in self.tag_dict:
            self.tag_dict[tag].append(item)
        else:
            self.tag_dict[tag] = [item]
        self.stack.append(None)
        self.tag_history.append(tag)

    def push_content(self, content):
        if self.tag_history == []: 
            return
        self.stack.append(content)

    def get_node(self, tag):
        tag_idx, _, attribute = self.tag_dict[tag][-1]
        item = self.stack[tag_idx:]
        if item[0] == None:
            item.pop(0)
        return item, attribute

    def resolve(self, tag, resolved):
        assert tag == self.tag_history[-1], f'tag {tag} is not the last node!'
        tag_idx, _, _ = self.tag_dict[tag][-1]
        self.stack = self.stack[:tag_idx] + [*resolved]
        self.tag_dict[tag].pop()
        self.tag_history.pop()
    
    def get_closing_tag(self):
        if self.tag_history == []:
            return None
        return self.tag_history[-1]


class SoupReplacer:
    def __init__(self, old_tag=None, new_tag=None, name_xformer=None, attrs_xformer=None, xformer=None):
        self.old_tag = old_tag
        self.new_tag = new_tag
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer

    def replace(self, tag_name):
        return self.new_tag if tag_name == self.old_tag else tag_name

    def transform(self, tag):
        # name replace from milestone2
        # if self.og_tag and tag.name == self.og_tag:
        #     tag.name = self.alt_tag

        # new Milestone3 transforms
        # ---  name_xformer ---
        if self.name_xformer is not None:
            try:
                original_tag_name = tag.name
                new_name = self.name_xformer(tag)
                if new_name is not None:
                    if not isinstance(new_name, str):
                        raise TypeError(f"name_xformer must return a string or None, got {type(new_name)}")
                    tag.name = new_name
                    self.old_tag = original_tag_name
                    self.new_tag = new_name
            except Exception as e:
                # print error
                print(f"[SoupReplacer Warning] name_xformer failed for <{tag.name}>: {e}")

        # ---  attrs_xformer ---
        if self.attrs_xformer is not None:
            try:
                new_attrs = self.attrs_xformer(tag)
                if new_attrs is not None:
                    if not isinstance(new_attrs, dict):
                        raise TypeError(f"attrs_xformer must return a dict or None, got {type(new_attrs)}")
                    tag.attrs = new_attrs
            except Exception as e:
                print(f"[SoupReplacer Warning] attrs_xformer failed for <{tag.name}>: {e}")

        # ---  xformer ---
        if self.xformer is not None:
            try:
                result = self.xformer(tag)
            except Exception as e:
                print(f"[SoupReplacer Warning] xformer failed for <{tag.name}>: {e}")

        # --- return final result ---
        return tag

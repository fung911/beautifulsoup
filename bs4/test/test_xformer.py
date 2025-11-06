import pytest
from bs4 import BeautifulSoup, SoupReplacer


class TestSoupReplacerMilestone3:
    """Test Milestone 3 functionality of SoupReplacer: name_xformer, attrs_xformer, xformer"""

    html_doc = """
    <html>
        <body>
            <b class="highlight">bold text</b>
            <i style="italic">italic text</i>
            <div class="container">
                <b>nested bold</b>
                <span class="remove-me">text</span>
            </div>
            <p>regular paragraph</p>
        </body>
    </html>
    """

    def test_name_xformer_changes_tag_name(self):
        """Test that name_xformer can rename tags dynamically"""
        replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # check that <b> tags are now <blockquote>
        blockquotes = soup.find_all("blockquote")
        assert len(blockquotes) == 2
        assert blockquotes[0].text.strip() == "bold text"
        assert blockquotes[1].text.strip() == "nested bold"

    def test_attrs_xformer_modifies_attributes(self):
        """Test that attrs_xformer can modify tag attributes"""

        def change_attrs(tag):
            if "class" in tag.attrs:
                tag.attrs["class"] = ["modified"]
            return tag.attrs

        replacer = SoupReplacer(attrs_xformer=change_attrs)
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # check that all class attributes have been replaced
        for tag in soup.find_all(True):
            if "class" in tag.attrs:
                assert tag.attrs["class"] == ["modified"]

    def test_xformer_can_delete_attributes(self):
        """Test that xformer can have side effects like deleting attributes"""

        def remove_class_attr(tag):
            if "class" in tag.attrs:
                del tag.attrs["class"]

        replacer = SoupReplacer(xformer=remove_class_attr)
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # check that no tag has class attribute
        for tag in soup.find_all(True):
            assert "class" not in tag.attrs

    def test_combined_name_and_attrs_xformer(self):
        """Test combined use of name_xformer and attrs_xformer"""
        replacer = SoupReplacer(
            name_xformer=lambda tag: "em" if tag.name == "i" else tag.name,
            attrs_xformer=lambda tag: {"style": "changed"} if "style" in tag.attrs else tag.attrs
        )
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # check <i> changed to <em>
        em_tags = soup.find_all("em")
        assert len(em_tags) == 1
        assert em_tags[0].text.strip() == "italic text"
        # check that style attribute changed
        assert em_tags[0].attrs["style"] == "changed"

    def test_xformer_with_side_effects_on_text(self):
        """Test xformer that modifies text content of tags"""

        def uppercase_text(tag):
            tag.string = tag.get_text().upper()

        replacer = SoupReplacer(xformer=uppercase_text)
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # check that all text is uppercased
        for tag in soup.find_all(["b", "i", "span", "p"]):
            text = tag.get_text()
            assert tag.get_text() == tag.get_text().upper()

    def test_name_xformer_returns_none_keeps_original(self):
        """Test that name_xformer returning None keeps original tag name"""
        replacer = SoupReplacer(name_xformer=lambda tag: None)
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # check that original tags remain unchanged
        assert soup.find_all("b")
        assert soup.find_all("i")
        assert soup.find_all("div")
        assert soup.find_all("p")

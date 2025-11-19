import pytest
from bs4 import BeautifulSoup, SoupReplacer


class TestSoupReplacerMilestone2:
    """Test Milestone 2 functionality of SoupReplacer: simple old_tag -> new_tag replacement"""

    html_doc = """
    <html>
        <body>
            <b>bold text</b>
            <i>italic text</i>
            <b>another bold</b>
        </body>
    </html>
    """

    def test_old_tag_replacement_changes_tag_name(self):
        """Test that old_tag 'b' is replaced by new_tag 'strong'"""

        replacer = SoupReplacer(old_tag="b", new_tag="strong")
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # manually transform each <b> tag
        for tag in soup.find_all("b"):
            replacer.transform(tag)

        # check that <b> tags are replaced by <strong>
        assert soup.find_all("b") == []  # no <b> tags should remain
        strong_tags = soup.find_all("strong")
        assert len(strong_tags) == 2
        assert strong_tags[0].text == "bold text"
        assert strong_tags[1].text == "another bold"

    def test_tags_not_matching_old_tag_remain_unchanged(self):
        """Test that tags not matching old_tag are not changed"""
        replacer = SoupReplacer(old_tag="b", new_tag="strong")
        soup = BeautifulSoup(self.html_doc, "html.parser", replacer=replacer)

        # transform only <b> tags
        for tag in soup.find_all(True):
            replacer.transform(tag)

        # <i> should remain unchanged
        i_tag = soup.find("i")
        assert i_tag is not None
        assert i_tag.name == "i"
        assert i_tag.text == "italic text"

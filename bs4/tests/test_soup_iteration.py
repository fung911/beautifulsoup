from bs4 import Tag, NavigableString, Comment
from . import SoupTest


class TestSoupIteration(SoupTest):
    """Test the new iteration API on the BeautifulSoup object."""

    def test_basic_iteration_order(self):
        """Test that iterating over soup yields tags in document order."""
        markup = "<html><body><div><p>1</p><p>2</p></div></body></html>"
        soup = self.soup(markup)

        tags = list(soup)
        tag_names = [t.name for t in tags]

        expected_names = ['html', 'body', 'div', 'p', 'p']
        assert expected_names == tag_names
        assert all(isinstance(t, Tag) for t in tags)

    def test_filtering_non_tags(self):
        """Test that NavigableStrings and Comments are filtered out."""
        markup = "<div>Text<!--Comment--></div>"
        soup = self.soup(markup)

        items = list(soup)

        # Should only contain the div
        assert 1 == len(items)
        assert 'div' == items[0].name

        # Verify that text and comments are NOT in the iteration result
        assert not any(isinstance(x, NavigableString) for x in items)
        assert not any(isinstance(x, Comment) for x in items)

    def test_nested_structure_traversal(self):
        """Test traversal of a deeply nested structure."""
        markup = """
        <root>
            <level1>
                <level2>
                    <level3>Target</level3>
                </level2>
            </level1>
            <sibling>Sibling</sibling>
        </root>
        """
        soup = self.soup(markup)

        tags = list(soup)
        names = [t.name for t in tags]

        # Should be depth-first
        expected = ['root', 'level1', 'level2', 'level3', 'sibling']
        assert expected == names

    def test_empty_soup_iteration(self):
        """Test iteration over an empty or minimal soup."""
        soup = self.soup("")
        assert [] == list(soup)

        soup_minimal = self.soup("Just text")
        assert [] == list(soup_minimal)

    def test_mixed_content_skipping(self):
        """Test that iteration skips mixed content correctly."""
        markup = "<a>A</a>Text<b>B</b><!--Comment--><c>C</c>"
        soup = self.soup(markup)

        tags = list(soup)
        names = [t.name for t in tags]

        assert ['a', 'b', 'c'] == names

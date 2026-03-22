import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_full(self):
        print(HTMLNode("<Test>", "Test Value", [], {"Test1.11":"Test1.12", "Test1.21":"Test1.22"}))
    def test_direct(self):
        print(HTMLNode(props={"Test2.11":"Test2.12", "Test2.21":"Test2.22"}))
    def test_empty(self):
        print(HTMLNode())
    def test_children(self):
        child=HTMLNode("<Test>", "Test Value", [], {"Test4.11":"Test4.12", "Test4.21":"Test4.22"})
        print(HTMLNode("<Test>", "Test Value", [child], {"Test4.31":"Test4.32", "Test4.31":"Test4.32"}))

if __name__ == "__main__":
    unittest.main()

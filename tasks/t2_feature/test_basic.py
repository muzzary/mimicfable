from slugify import slugify


def test_simple():
    assert slugify("Hello, World!") == "hello-world"


if __name__ == "__main__":
    test_simple()
    print("basic test passed")

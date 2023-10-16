"""Unit tests for the j_classify package."""

import json
import unittest
import tempfile

import j_classify


class TestJObject(unittest.TestCase):
    """Test the j_object package."""

    def setUp(self) -> None:
        """Set up the test case."""
        # Create a temp folder to store the test files
        self.temp_folder = tempfile.TemporaryDirectory()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test case."""
        # Delete the temp folder
        self.temp_folder.cleanup()
        return super().tearDown()

    def test_load_j_object(self) -> None:
        """Test the load_j_object function."""
        class test_class_1(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_1"
                self.number = 1
                self.boolean = True
                self.children: list = []

        class test_class_2(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_2"
                self.number = 2
                self.boolean = False
                self.children: list = []

        class test_class_3(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_3"
                self.number = 3
                self.boolean = True

        obj_1 = test_class_1()
        obj_1.name = "obj_1"
        obj_1.number = 2
        obj_1.boolean = False
        obj_2 = test_class_2()
        obj_2.name = "obj_2"
        obj_2.number = 3
        obj_2.boolean = True
        obj_1.children.append(obj_2)
        obj_3 = test_class_3()
        obj_3.name = "obj_3"
        obj_3.number = 4
        obj_3.boolean = False
        obj_2.children.append(obj_3)

        # Save the object to a file
        file_path = self.temp_folder.name + "/test_load_j_object.json"
        with open(file_path, "w") as file:
            json.dump(obj_1, file, cls=j_classify.j_object_encoder)

        # Load the object from the file
        with open(file_path, "r") as file:
            # Load a json dictionary of the file contents
            json_data = json.loads(file.read())
            loaded_obj_1 = json.loads(json.dumps(json_data), object_hook=j_classify.load_j_object)

        # Check the loaded object
        self.assertTrue(isinstance(loaded_obj_1, test_class_1), f"loaded_obj_1 is not a test_class_1, it is a {loaded_obj_1.__class__.__name__}")
        self.assertEqual(loaded_obj_1.name, "obj_1", "loaded_obj_1.name is not 'obj_1'")
        self.assertEqual(loaded_obj_1.number, 2, "loaded_obj_1.number is not 2")
        self.assertEqual(loaded_obj_1.boolean, False, "loaded_obj_1.boolean is not False")
        self.assertEqual(len(loaded_obj_1.children), 1, "loaded_obj_1.children does not have 1 item")
        self.assertTrue(isinstance(loaded_obj_1.children[0], test_class_2),
                        f"loaded_obj_1.children[0] is not a test_class_2, it is a {loaded_obj_1.children[0].__class__.__name__}")
        self.assertEqual(loaded_obj_1.children[0].name, "obj_2", "loaded_obj_1.children[0].name is not 'obj_2'")
        self.assertEqual(loaded_obj_1.children[0].number, 3, "loaded_obj_1.children[0].number is not 3")
        self.assertEqual(loaded_obj_1.children[0].boolean, True, "loaded_obj_1.children[0].boolean is not True")
        self.assertEqual(len(loaded_obj_1.children[0].children), 1,
                         "loaded_obj_1.children[0].children does not have 1 item")
        self.assertTrue(isinstance(loaded_obj_1.children[0].children[0], test_class_3),
                        "loaded_obj_1.children[0].children[0] is not a test_class_3")
        self.assertEqual(loaded_obj_1.children[0].children[0].name, "obj_3",
                         "loaded_obj_1.children[0].children[0].name is not 'obj_3'")
        self.assertEqual(loaded_obj_1.children[0].children[0].number, 4,
                         "loaded_obj_1.children[0].children[0].number is not 4")
        self.assertEqual(loaded_obj_1.children[0].children[0].boolean, False,
                         "loaded_obj_1.children[0].children[0].boolean is not False")

    def test_list_all_j_objects(self) -> None:
        """Test the list_all_j_objects function."""
        class test_class_1(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_1"
                self.number = 1
                self.boolean = True
                self.children: list = []

        class test_class_2(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_2"
                self.number = 2
                self.boolean = False
                self.children: list = []

        class test_class_3(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_3"
                self.number = 3
                self.boolean = True

        j_objects = j_classify.list_all_j_objects()
        self.assertTrue(isinstance(j_objects, dict), "j_objects is not a dict")
        self.assertEqual(len(j_objects), 3, "j_objects does not have 3 items")
        self.assertTrue("test_class_1" in j_objects, "test_class_1 is not in j_objects")
        self.assertTrue("test_class_2" in j_objects, "test_class_2 is not in j_objects")
        self.assertTrue("test_class_3" in j_objects, "test_class_3 is not in j_objects")

    def test_j_object(self) -> None:
        """Test the j_object class."""
        class test_class_1(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_1"
                self.number = 1
                self.boolean = True
                self.children: list = []

        class test_class_2(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_2"
                self.number = 2
                self.boolean = False
                self.children: list = []

        class test_class_3(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_3"
                self.number = 3
                self.boolean = True

        obj_1 = test_class_1()
        obj_2 = test_class_2()
        obj_3 = test_class_3()

        self.assertTrue(isinstance(obj_1, j_classify.j_object), "obj_1 is not a j_object")
        self.assertTrue(isinstance(obj_2, j_classify.j_object), "obj_2 is not a j_object")
        self.assertTrue(isinstance(obj_3, j_classify.j_object), "obj_3 is not a j_object")

    def test_j_object_encoder(self) -> None:
        """Test the j_object_encoder class."""
        class test_class_1(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_1"
                self.number = 1
                self.boolean = True
                self.children: list = []

        class test_class_2(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_2"
                self.number = 2
                self.boolean = False
                self.children: list = []

        class test_class_3(j_classify.j_object):
            def __init__(self) -> None:
                super().__init__()
                self.name = "test_class_3"
                self.number = 3
                self.boolean = True

        obj_1 = test_class_1()
        obj_2 = test_class_2()
        obj_3 = test_class_3()

        self.assertTrue(isinstance(obj_1, j_classify.j_object), "obj_1 is not a j_object")
        self.assertTrue(isinstance(obj_2, j_classify.j_object), "obj_2 is not a j_object")
        self.assertTrue(isinstance(obj_3, j_classify.j_object), "obj_3 is not a j_object")

        obj_1.children.append(obj_2)
        obj_2.children.append(obj_3)

        obj_data = json.dumps(obj_1, cls=j_classify.j_object_encoder, indent=4)
        self.assertTrue(isinstance(obj_data, str), "obj_data is not a string")
        print(obj_data)

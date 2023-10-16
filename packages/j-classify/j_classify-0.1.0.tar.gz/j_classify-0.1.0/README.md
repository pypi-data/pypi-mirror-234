# j_classify

Improved JSON deserializer for Python that allows for remapping to custom object types and nested objects. This allows for saving/loading complex Python objects, like using `pickle` while still preserving them in a human-readable format.

Example Usage:

``` python
import json

import j_classify


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


if __name__ == "__main__":
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

    # Dump the object to JSON - use the j_object_encoder class for the cls argument
    obj_data = json.dumps(obj_1, cls=j_classify.j_object_encoder, indent=4)

    # Load the object from JSON - use the load_j_object function for the object_hook
    loaded_obj_1 = json.loads(obj_data, object_hook=j_classify.load_j_object)

```

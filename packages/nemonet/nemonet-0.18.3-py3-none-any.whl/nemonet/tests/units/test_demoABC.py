import unittest
from abc import ABC, abstractmethod

""" - - - classes for demonstration purposes - - -"""


class _Demo_AbstractClass(ABC):
    """
        an ABC for demonstration purposes with abstract properties,
        abstract methods, and more
    """

    def __init__(self, foo=1):
        self.foo = foo

    @abstractmethod
    def time_wait(self):
        return "Abstract"

    @abstractmethod
    def execute_action(self):
        return "Abstract"

    @abstractmethod
    def screenshot(self):
        return "Abstract"

    def execute_command(self):
        res = ""
        res += self.time_wait()
        res += self.screenshot()
        res += self.execute_action()
        res += self.time_wait()
        res += self.screenshot()
        res += self.time_wait()
        return res


class _Demo_CompletelyInvalid_Subclass(_Demo_AbstractClass):
    """ a completely invalid subclass for demonstration purposes """

    pass  # implements none of the required abstract methods


class _Demo_Invalid_Subclass(_Demo_AbstractClass):
    """ an invalid but almost ok subclass for demonstration purposes """

    def time_wait(self):
        pass

    def execute_action(self):
        pass

    # not all abstract methods are implemented


class _Demo_Valid_NotConcreteSubclass(_Demo_AbstractClass):
    """ a valid subclass that doesn't do anything concrete """

    def time_wait(self):
        return super(_Demo_Valid_NotConcreteSubclass, self).time_wait()

    def execute_action(self):
        return super(_Demo_Valid_NotConcreteSubclass, self).execute_action()

    def screenshot(self):
        return super(_Demo_Valid_NotConcreteSubclass, self).screenshot()


class _Demo_Valid_ConcreteSubclass(_Demo_AbstractClass):
    """ a valid subclass that doesn't do anything concrete """

    def time_wait(self):
        return 'Concrete'

    def execute_action(self):
        return 'Concrete'

    def screenshot(self):
        return 'Concrete'


class _Demo_Valid_SemiConcreteCommand(_Demo_AbstractClass):
    """ a valid subclass that does some things concrete """

    def time_wait(self):
        return 'Concrete'

    def execute_action(self):
        return super(_Demo_Valid_SemiConcreteCommand, self).execute_action()

    def screenshot(self):
        return 'Concrete'


class _Demo_Valid_HyperConcreteSubclass(_Demo_AbstractClass):
    """ a valid subclass that doesn't do anything concrete """

    def time_wait(self):
        return 'Concrete'

    def execute_action(self):
        return 'Concrete'

    def screenshot(self):
        return 'Concrete'

    def execute_command(self):
        return "I have overwritten my superclass's implementation of non-abstract methods"


class _Demo_INIT(_Demo_AbstractClass):

    def __init__(self, foo):
        super().__init__(foo)

    def time_wait(self):
        return 'Concrete'

    def execute_action(self):
        return 'Concrete'

    def screenshot(self):
        return 'Concrete'


class _DemoPropertyAbstract(ABC):
    def __init__(self, name):
        self._name = name

    @property
    @abstractmethod
    def name(self):
        return self._name


class _DemoProperties(_DemoPropertyAbstract):

    @property
    def name(self):
        return self._name

""" - - - Demonstration tests - - - """


class TestDemoABC(unittest.TestCase):
    """ Unittest to illustrate functionality of python's abc.ABC class """

    def test_demo_abc_do_not_instantiate(self):
        with self.assertRaises(TypeError):
            _Demo_AbstractClass()

    def test_demo_abstract_methods_have_to_be_implemented(self):
        with self.assertRaises(TypeError, msg="ABC subclasses should implement abstract methods"):
            _Demo_CompletelyInvalid_Subclass()

        with self.assertRaises(TypeError, msg="ABC subclasses should implement all abstract methods"):
            _Demo_Invalid_Subclass()

        _Demo_Valid_ConcreteSubclass()

    def test_demo_concreteness_of_subclasses(self):
        expect = "ConcreteConcreteConcreteConcreteConcreteConcrete"
        actual = _Demo_Valid_ConcreteSubclass().execute_command()

        self.assertEqual(expect, actual, msg="ABC subclasses can have their own implementations")

        expect = "ConcreteConcreteAbstractConcreteConcreteConcrete"
        actual = _Demo_Valid_SemiConcreteCommand().execute_command()

        self.assertEqual(expect, actual, msg="ABC subclasses can use the abstract implementations")

        expect = "AbstractAbstractAbstractAbstractAbstractAbstract"
        actual = _Demo_Valid_NotConcreteSubclass().execute_command()

        self.assertEqual(expect, actual, msg="ABC subclasses can use all the abstract implementations")

        expect = "I have overwritten my superclass's implementation of non-abstract methods"
        actual = _Demo_Valid_HyperConcreteSubclass().execute_command()

        self.assertEqual(expect, actual, msg="ABC subclasses can overwrite non-abstract implementations")

    def test_demo_abstract_possibilities(self):
        # init
        foo = 2
        demo = _Demo_INIT(foo)
        self.assertEqual(demo.foo, 2)

    def testNameProperty(self):
        #property
        demo = _DemoProperties('Jan')
        self.assertEqual(demo.name, 'Jan')


if __name__ == '__main__':
    unittest.main()

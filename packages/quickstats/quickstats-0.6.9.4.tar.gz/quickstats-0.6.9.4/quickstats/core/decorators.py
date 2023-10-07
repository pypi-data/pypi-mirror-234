from functools import partial
import time

class semistaticmethod(object):
    """
    Descriptor to allow a staticmethod inside a class to use 'self' when called from an instance.

    This custom descriptor class `semistaticmethod` enables a static method defined inside a class 
    to access the instance (`self`) when called from an instance, similar to how regular instance 
    methods can access the instance attributes. By default, static methods do not have access to 
    the instance and can only access the class-level attributes.

    Note:
        When defining a static method using this descriptor, it should be used like a regular method 
        within the class definition. It will work as a normal static method when called from the class, 
        and when called from an instance, it will receive the instance as the first argument.

    Args:
        callable (function): The original static method defined within the class.

    Returns:
        callable: A callable object that behaves like a static method but can also access the instance.
    """
    def __init__(self, callable):
        self.f = callable

    def __get__(self, obj, type=None):
        if (obj is None) and (type is not None):
            return partial(self.f, type)
        if (obj is not None):
            return partial(self.f, obj)
        return self.f

    @property
    def __func__(self):
        return self.f

def cls_method_timer(func):
    """
    Decorator function to measure the execution time of a class method.

    The `cls_method_timer` decorator function can be applied to any class method to automatically measure 
    the execution time of the method. When the decorated method is called, it records the start and end 
    times, calculates the time interval, and prints a message with the method name and the execution time.

    Args:
        func (callable): The class method to be decorated.

    Returns:
        callable: The wrapped function with timing functionality.

    Example:
        class MyClass:
            @cls_method_timer
            def my_method(self, n):
                # Some time-consuming computation here
                result = sum(range(n))
                return result

        obj = MyClass()
        obj.my_method(1000000)  # The decorated method will print the execution time
        # Output: "Task MyClass::my_method executed in 0.006 s"

    Note:
        The `cls_method_timer` function should be used as a decorator when defining a class method. 
        When the decorated method is called, it will print the execution time to the console.
    """
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to measure the execution time of the class method.

        This wrapper function records the start time before calling the original method, then calls 
        the original method, and finally calculates and prints the execution time.

        Args:
            self: The instance of the class.
            *args: Variable-length argument list.
            **kwargs: Keyword arguments.

        Returns:
            The result returned by the original method.
        """
        t1 = time.time()
        result = func(self, *args, **kwargs)
        t2 = time.time()
        method_name = f"{type(self).__name__}::{func.__name__}"
        self.stdout.info(f'Task {method_name!r} executed in {(t2 - t1):.3f} s')
        return result

    return wrapper

class Timer:    
    """
    Context manager class for measuring the execution time of a code block.

    Example:
        with Timer() as t:
            # Perform some time-consuming task here
            time.sleep(2)

        print("Elapsed time:", t.interval)  # outputs: "Elapsed time: 2.0 seconds"

    """
    def __enter__(self):
        """
        Records the start time when entering the context.

        Returns:
            Timer: The Timer instance itself.
        """
        self.start = time.time()
        return self

    def __exit__(self, *args):
        """
        Calculates the time interval when exiting the context.

        Args:
            *args: Variable-length argument list.

        Returns:
            None
        """
        self.end = time.time()
        self.interval = self.end - self.start
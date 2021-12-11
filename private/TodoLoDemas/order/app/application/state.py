class State(object):
    """
    We define a state object which provides some utility functions for the
    individual states within the state machine.
    """

    def __init__(self, order):
        self.order = order
        print('Processing current state:', str(self))

    def on_event(self, event):
        """
        Handle events that are delegated to this State.
        """
        pass
    """
    def __repr__(self):

        return self.__str__()

    def __str__(self):

        return self.__class__.__name__
        """
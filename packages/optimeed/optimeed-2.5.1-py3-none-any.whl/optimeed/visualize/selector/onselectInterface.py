from abc import ABCMeta, abstractmethod


class OnselectInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_name(self):
        """Get the name of the action

        :return: string
        """
        pass

    @abstractmethod
    def selector_updated(self, selection_name, the_collection, selected_indices, not_selected_indices):
        """
        Action to perform once the data have been selected
        :param selection_name: name of the selection (deprecated ?)
        :param the_collection: the collection
        :param selected_indices: indices of selected data
        :param not_selected_indices: indices of data NOT selected
        :return: identifier that can later be used with cancel_selector
        """
        pass

    @abstractmethod
    def cancel_selector(self, selection_identifier):
        """
        Action to perform when data stopped being selected
        :param selection_identifier: identifier that was returned by selector_updated
        :return:
        """
        pass

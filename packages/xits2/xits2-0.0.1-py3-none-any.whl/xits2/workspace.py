from stix2 import Environment, Filter, MemoryStore
from stix2.datastore.filters import FilterSet


class Workspace(Environment):
    """
    Workspace is an extension of stix2.Environment, providing additional
    functionality such as querying unique STIX objects and removing STIX
    objects along with all their versions from the store.
    """

    def __init__(self, *args, store=None, **kwargs):
        if store is None:
            # Create a new MemoryStore instance if no store is provided.
            store = MemoryStore()

        super().__init__(*args, store=store, **kwargs)

    def stats(self, *args, **kwargs):
        stats = dict()
        for obj in self.query(*args, **kwargs):
            if obj.type in stats:
                stats[obj.type] += 1
            else:
                stats[obj.type] = 1
        return stats

    def query(self, *args, **kwargs):
        """
        Query STIX objects with an option to get the most recent version
        of unique objects.

        :param args: Positional arguments to be passed to the super's query method.
        :param unique: A boolean flag to decide whether to return the most recent
                       versions of unique objects. If True, it returns the most
                       recent versions of unique objects, otherwise all objects.
        :param kwargs: Keyword arguments to be passed to the super's query method.
        :return: A list of STIX objects from the query result. If unique is True,
                 the list will contain the most recent versions of unique objects,
                 in the reverse order they were added.
        """
        unique = kwargs.pop("unique", True)

        all_objects = super().query(*args, **kwargs)
        if not unique or not all_objects:
            return all_objects

        def get_most_recent_unique_objects():
            """
            A generator that yields the most recent versions of unique objects,
            processing them in the reverse order they were added to handle
            newer versions being appended to the environment.
            """
            seen = set()
            for obj in reversed(all_objects):
                if obj.id in seen:
                    continue
                seen.add(obj.id)
                yield obj

        return list(get_most_recent_unique_objects())

    def remove(self, object_id):
        """
        Removes an object along with all its versions from the store.

        :param object_id: The ID of the STIX object to be removed.
        """
        try:
            for source in self.source.data_sources:
                del source._data[object_id]
        except KeyError:
            raise ValueError(f"No object found with ID: {object_id}")

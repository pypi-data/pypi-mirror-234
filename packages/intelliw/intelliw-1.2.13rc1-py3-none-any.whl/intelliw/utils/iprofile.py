import io
import os
import sys
import tempfile
from functools import wraps

from intelliw.utils.storage_service import StorageService


def performance_profile(filepath=None):
    import cProfile
    import pstats

    def wrapper(function):
        @wraps(function)
        def inner(*args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()

            result = function(*args, **kwargs)

            pr.disable()
            s = io.StringIO()
            sort_by = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
            ps.print_stats()
            sys.stderr.write("{}\n".format(s.getvalue()))

            if filepath:
                curkey = os.path.join(filepath, "pipeline.prof")
                with tempfile.NamedTemporaryFile() as temp:
                    filename = temp.name + '.prof'
                    pr.dump_stats(filename)
                    StorageService(curkey, "upload").upload(filename)
            return result

        return inner

    return wrapper

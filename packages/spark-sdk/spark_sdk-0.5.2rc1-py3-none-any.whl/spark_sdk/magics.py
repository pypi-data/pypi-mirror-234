import json
import re
import traceback


from IPython.core.magic import (
    Magics,
    cell_magic,
    line_magic,
    magics_class,
    needs_local_scope,
)
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring


try:
    from traitlets.config.configurable import Configurable
    from traitlets import Bool, Int, Unicode
except ImportError:
    from IPython.config.configurable import Configurable
    from IPython.utils.traitlets import Bool, Int, Unicode

@magics_class
class SqlMagic(Magics, Configurable):
    """Runs SQL statement on a database, specified by SQLAlchemy connect string.
    Provides the %%sql magic."""

    def __init__(self, shell):
        Configurable.__init__(self, config=shell.config)
        Magics.__init__(self, shell=shell)

        # Add ourselves to the list of module configurable via %config
        self.shell.configurables.append(self)

    @needs_local_scope
    @line_magic("sql")
    @cell_magic("sql")
    @magic_arguments()
    @argument("line", default="", nargs="*", type=str, help="sql")
    @argument(
        "--append",
        action="store_true",
        help="create, or append to, a table name in the database from the named DataFrame",
    )
    @argument(
        "-a",
        "--connection_arguments",
        type=str,
        help="specify dictionary of connection arguments to pass to SQL driver",
    )
    def execute(self, line="", cell="", local_ns=None):
        """Runs SQL on DWH
        %%sql df
        select *
        from database.table_name
        """
        
        cell = self.shell.var_expand(cell)
        user_ns = self.shell.user_ns.copy()
        user_ns.update(local_ns)
        
        
        from spark_sdk.pyspark_add_on import sql
        result = sql(cell)
        if line:
            self.shell.user_ns.update({line: result})
            return None
        return result
        

            
def load_ipython_extension(ip):
    """Load the extension in IPython."""

    # this fails in both Firefox and Chrome for OS X.
    # I get the error: TypeError: IPython.CodeCell.config_defaults is undefined

    # js = "IPython.CodeCell.config_defaults.highlight_modes['magic_sql'] = {'reg':[/^%%sql/]};"
    # display_javascript(js, raw=True)
    ip.register_magics(SqlMagic)
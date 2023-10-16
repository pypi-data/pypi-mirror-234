from rich.console import Console
from rich.table import Table


def print_xyz(x,y,z,title,type="xyz"):
    '''
    Print an array 3x1 using rich

    Args:
    -----
        * x : element to print x
        * y : element to print y
        * z : element to print z
    '''
    # DO NOT MODIFY THIS CELL
    table = Table(title=title)
    if (type=="xyz"):
        table.add_column("X")
        table.add_column("Y")
        table.add_column("Z")
    elif (type=="ll"):
        table.add_column("Latitude")
        table.add_column("Longitude")
        table.add_column("Height")
    elif (type=="en"):
        table.add_column("Easting")
        table.add_column("Northing")
        table.add_column("Height")
    elif (type=="ba"):
        table.add_column("Delta Easting")
        table.add_column("Delta Northing")
        table.add_column("Delta Height")
    elif (type=="tr"):
        table.add_column("Tx")
        table.add_column("Ty")
        table.add_column("Tz")
    elif (type=="dif"):
        table.add_column("Diff. Easting")
        table.add_column("Diff. Northing")
        table.add_column("Diff. height")

    table.add_row(str(x),str(y),str(z))
    console = Console()
    console.print(table)

    return


import pyarrow as pa
import pyarrow.compute as pc
import quivr as qv


class Pair(qv.Table):
    """
    Pair o' values
    """

    x = qv.Float64Column()
    y = qv.Float64Column()

    label = qv.StringAttribute()

    def pairwise_sum(self) -> pa.DoubleArray:
        """
        Add the pairwise x and y values
        """
        return pc.add(self.x, self.y)


class MyTable(qv.Table):
    x = qv.Float64Column()

    #: Example of a documented y field
    y = qv.Int64Column()

    #: this one is documented
    #: on multiple lines
    #: and has an admonition
    #:
    #: .. warning::
    #:    Do not use
    z = qv.ListColumn(pa.int32())
    pairs = Pair.as_column()

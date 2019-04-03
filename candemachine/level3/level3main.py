from dataclasses import dataclass, field, InitVar

from ..exceptions import CandeDeserializationError
from ..read.readable import CandeReadableMixin


@dataclass(eq=False)
class Level3Main(CandeReadableMixin):
    title: str = ""
    n_steps_: int = 0
    mesh_output: InitVar[int] = field(init=False, repr=False, default=3)
    data_check: InitVar[int] = field(init=False, repr=False, default=0)
    plot_file_control: InitVar[int] = field(init=False, repr=False, default=3)
    response_data_ouput: InitVar[int] = field(init=False, repr=False, default=0)
    n_nodes_: int = 0
    n_elements_: int = 0
    n_boundaries_: int = 0
    n_soil_materials_: int = 0
    n_interface_materials_: int = 0
    bandwidth_minimization: int = field(init=False, repr=False, default=1)
    continuous_load_scaling: int = field(init=False, repr=False, default=2)

    @classmethod
    def from_cid(cls, lines):
        ilines = iter(lines)
        line = next(ilines)
        if line[:4]=="PREP":
            title = line[5:73]
            line = next(ilines)
        else:
            title = cls.__dataclass_fields__["title"].default
        try:
            obj = cls(
                title=title,
                n_steps_=int(line[:5]),
                n_nodes_=int(line[25:30]),
                n_elements_=int(line[30:35]),
                n_boundaries_=int(line[35:40]),
                n_soil_materials_=int(line[40:45]),
                n_interface_materials_=int(line[45:50])
            )
            if line[5:10].strip():
                obj.mesh_output= int(line[5:10])
            if line[10:15].strip():
                obj.data_check= int(line[10:15])
            if line[15:20].strip():
                obj.plot_file_control= int(line[15:20])
            if line[20:25].strip():
                obj.response_data_ouput= int(line[20:25])
            if line[5:10].strip():
                obj.mesh_output= int(line[5:10])
            if line[50:55].strip():
                obj.bandwidth_minimization = int(line[50:55])
            if line[55:60].strip():
                obj.continuous_load_scaling= int(line[55:60])
        except Exception as e:
            raise CandeDeserializationError(f"Failed to read line:\b{line!r}") from e
        else:
            return obj

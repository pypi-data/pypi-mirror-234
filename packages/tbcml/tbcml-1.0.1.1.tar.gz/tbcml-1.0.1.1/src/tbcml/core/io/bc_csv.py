import enum
import inspect
import uuid
from typing import Any, Optional, Union

from tbcml import core

"""
shopID	gatyaItemID	ItemValue	ItemPrice	drawItemValue	CategoryName	imgcut
0	0	9	2	1	shop_category1	0
1	1	2	2	1	shop_category1	1
2	2	7	100	1	shop_category1	2
3	3	20	20	1	shop_category1	3
4	4	5	2	1	shop_category1	4
5	5	3	3	1	shop_category1	5
6	80	1	25	0	shop_category2	6
7	81	1	50	0	shop_category2	7
8	82	1	150	0	shop_category2	8
9	83	1	300	0	shop_category2	9
10	84	1	500	0	shop_category2	10
11	55	3	6	1	shop_category3	11
12	56	3	10	1	shop_category3	12
13	57	3	15	1	shop_category3	13
14	105	5	30	1	shop_category1	14
15	123	1	1	0	shop_category1	15

class Item:
    def __init__(self, shop_id: int, gatya_item_id: int, item_value: int, item_price: int, draw_item_value: bool, category_name: str, imgcut: int):
        self.shop_id = shop_id
        self.gatya_item_id = gatya_item_id
        self.item_value = item_value
        self.item_price = item_price
        self.draw_item_value = draw_item_value
        self.category_name = category_name
        self.imgcut = imgcut


type_structure = {0: Item}

csv_structure = [
    Row(ignore=True, type_structure=str),
    Row(count=-1, type_structure=type_structure),
]

[modelanim:model2]
4
2
-1,0,0,0,0,0,0,0,1000,1000,0,1000,0,DM
0,0,1,1,0,0,29,58,1200,1200,0,1000,0,ネコ
1000,3600,1000,1
0

class MamodelRow:
    def __init__(self, ...):
        ...

class UnitLine:
    ...

type_structure = {0: ModelRow}
type_structure2 = UnitLine
        
csv_structure = [
    Row(ignore=True, count=2)
    Row(id="total_parts", length=1)
    Row(type_structure=type_structure, count="total_parts")
    Row(type_structure=type_structure2)
]


[modelanim:animation]
1
15
1,12,1,0,0,
7
0,0,0,0
10,2550,2,2
60,0,0,0
61,2550,0,0
136,2550,2,2
168,1200,2,-2
190,0,0,0
1,11,1,0,0,
3
0,0,0,0
152,0,2,2
190,-800,0,0

class KeyFrameSet:
    def __init__(self, part_id: int, modification_type: AnimModificationType, loop: int, min: int, max: int, name: str, keyframes: list[KeyFrame]):
        ...

type_structure = {0: KeyFrameSet}
        
csv_structure = [
    Row(ignore=True, count=2),
    Row(id="total_keyframe_sets", length=1, ignore=True),
    Row(type_structure=type_structure, count="total_keyframe_sets", rows = [
        Row(vars=[0, 1, 2, 3, 4, 5]),
        Row(id="total_keyframes", length=1, ignore=True),
        Row(vars=[6], type_structure=[KeyFrame], count="total_keyframes")
    ]),
]

GatyaType	利用形態(0:チケット、1:単発、2:連続、3:プラチナ、4:ステップアップ)	イベントトークン1(UU)	イベントトークン2(total)
0	0	jbx0ar	p91apx	レアガチャ
0	1	jbx0ar	p91apx	レアガチャ
0	2	gwt8uj	cxwqzk	レアガチャ
0	3	hcz9ku		プラチナガチャ
1	0	gru8b9	d22pak	ノーマルガチャ
1	1	gru8b9	d22pak	ノーマルガチャ
1	2	qbjzs4	zglouf	ノーマルガチャ
2	0			イベントガチャ
2	1			イベントガチャ
2	2			イベントガチャ

class GatyaEvent:
    def __init__(self, gatya_type: int, roll_type: int, ...)

type_structure = {0: {1: GatyaEvent}}

csv_structure = [
    Row(ignore=True),
    Row(type_structure=type_structure, count=-1)
]

"""


class Row:
    def __init__(
        self,
        ignore: bool = False,
        type_structure: Any = 0,
        count: Union[int, str] = 1,
        vars: Optional[list[int]] = None,
        id: Optional[str] = None,
        length: Optional[int] = None,
        rows: Optional[list["Row"]] = None,
        values: Optional[Any] = None,
        cls_vars: Optional[list[int]] = None,
    ):
        self.ignore = ignore
        self.type_structure = type_structure
        self.count = count
        self.to_read = vars
        self.id = id
        self.length = length
        self.rows = rows
        self.values = values
        self.cls_vars = cls_vars
        self.ref_id = str(uuid.uuid4())
        self.parent_row: Optional[Row] = None

        for row in self.rows or []:
            row.parent_row = self

        if (
            cls_vars is not None
            and len(cls_vars) > 1
            and isinstance(type_structure, (int, str))
        ):
            self.type_structure: Any = []


class CSV2:
    def __init__(self, csv_data: list[list[str]], structure: list[Row]):
        self.csv_data = csv_data
        self.structure = structure

        self.data = self.read()

    def get_total_ignored_rows(self) -> int:
        total = 0
        for row in self.structure:
            if not row.ignore:
                total += 1
        return total

    def read(self) -> Any:
        self.row_index = 0
        self.global_buffer: dict[str, Row] = {}
        final_data: Any = None
        total_ignored = self.get_total_ignored_rows()
        for row in self.structure:
            data = self.read_row(row, {})
            if not row.ignore:
                if total_ignored == 1:
                    final_data = data
                else:
                    if final_data is None:
                        final_data = []
                    final_data.append(data)
        return final_data

    def read_row(self, row: Row, local_buffer: dict[str, Row]) -> Any:
        if row.count == -1:
            count = len(self.csv_data) - self.row_index
        else:
            if isinstance(row.count, int):
                count = row.count
            else:
                cnt = local_buffer.get(row.count)
                if cnt is None:
                    cnt = self.global_buffer.get(row.count)
                if cnt is not None:
                    if cnt.values is not None:
                        count = int(cnt.values)
                    else:
                        raise ValueError("Row value must not be None!")
                else:
                    raise ValueError("ID not found!")

        data = None
        for i in range(count):
            try:
                line = self.csv_data[self.row_index]
            except IndexError:
                if row.count == -1:
                    break
                line = []
            if row.length is not None:
                values_to_read = list(range(row.length))
            else:
                values_to_read = list(range(len(line)))
                if row.to_read is not None:
                    values_to_read = row.to_read

            if row.rows is not None:
                local_data: Any = {}
                for extra_row in row.rows:
                    dt = self.read_row(extra_row, local_buffer)
                    values = dt

                    if not extra_row.ignore:
                        for i, cls_var in enumerate(extra_row.cls_vars or []):
                            if not isinstance(dt, list):
                                local_data[cls_var] = dt
                                break
                            if i >= len(dt):
                                dt.append("")
                            if len(extra_row.cls_vars or []) == 1:
                                local_data[cls_var] = dt
                            else:
                                local_data[cls_var] = dt[i]
                new_data: list[Any] = []
                keys: list[Any] = sorted(list(local_data.keys()))
                for key in keys:
                    new_data.append(local_data[key])
                if data is None:
                    data = []
                if isinstance(row.type_structure, list):
                    data.append(row.type_structure[0](*new_data))
                else:
                    data.append(row.type_structure(*new_data))
                if count == 1:
                    data = data[0]

            else:
                values: list[str] = []
                for index in values_to_read:
                    try:
                        value = line[index]
                    except IndexError:
                        value = ""

                    values.append(value)

                if isinstance(row.type_structure, int):
                    data = int(values[0])
                elif isinstance(row.type_structure, str):
                    data = values[0]
                elif isinstance(row.type_structure, list):
                    if not row.type_structure:
                        type_structure = [0]
                    else:
                        type_structure: Any = row.type_structure
                    if data is None:
                        data: Any = []
                    if isinstance(type_structure[0], list):
                        ls: list[Any] = []
                        for value in values:
                            ls.append(self.get_object(data, type_structure[0], [value]))
                        data.append(ls)
                    elif isinstance(type_structure[0], (int, str)):
                        for value in values:
                            data.append(
                                self.get_object(data, type_structure[0], [value])
                            )
                    else:
                        data.append(self.get_object(data, type_structure[0], values))
                elif isinstance(row.type_structure, dict):
                    if data is None:
                        data: Any = {}
                    key_index = int(list(row.type_structure.keys())[0])
                    key_value = values[key_index]
                    if key_value not in data:
                        data[key_value] = {}
                    data[key_value] = self.get_object(
                        data[key_value], row.type_structure[key_index], values
                    )
                else:
                    if data is None:
                        data = []
                    args = inspect.getfullargspec(row.type_structure).args[1:]
                    annotations = inspect.getfullargspec(row.type_structure).annotations
                    vals: list[Any] = []
                    for i, arg in enumerate(args):
                        if i >= len(values):
                            values.append("")
                        if row.cls_vars is not None and i not in row.cls_vars:
                            continue
                        type = annotations[arg]
                        value = self.get_object(data, type(), [values[i]])
                        vals.append(value)
                    try:
                        object = row.type_structure(*vals)
                        data.append(object)
                    except TypeError:
                        data.append(vals)
            row.values = data
            if row.id is not None:
                local_buffer[row.id] = row
                self.global_buffer[row.id] = row

            if not row.rows:
                self.row_index += 1
        return data

    def get_object(
        self, current_object: Any, type_structure: Any, values: list[str]
    ) -> Any:
        if isinstance(type_structure, int):
            return int(values[0])
        if isinstance(type_structure, str):
            return values[0]

        if isinstance(type_structure, list):
            if isinstance(type_structure[0], list):
                ls: list[Any] = []
                for value in values:
                    ls.append(
                        self.get_object(current_object, type_structure[0], [value])
                    )
                return ls
            return self.get_object(current_object, type_structure[0], [values[0]])

        if isinstance(type_structure, dict):
            key_index = int(list(type_structure.keys())[0])
            key_value = values[key_index]
            if key_value not in current_object:
                current_object[key_value] = {}
            current_object[key_value] = self.get_object(
                current_object[key_value], type_structure[key_index], values
            )
            return current_object

        args = inspect.getfullargspec(type_structure).args[1:]
        annotations = inspect.getfullargspec(type_structure).annotations
        vals: list[Any] = []
        for i, arg in enumerate(args):
            type = annotations[arg]
            value = self.get_object(current_object, type(), [values[i]])
            vals.append(value)

        object = type_structure(*vals)
        return object

    def get_row_by_id(self, row_id: str, local_row: Row) -> Optional[Row]:
        if local_row.id == row_id:
            return local_row
        parent = local_row.parent_row
        if parent is None:
            rows = self.structure
        else:
            if parent.id == row_id:
                return parent
            rows = parent.rows
        if rows is None:
            return None
        for row in rows:
            if row.id == row_id:
                return row
        return None

    def dict_insert(self, dict: dict[int, Any], item: Any, pos: int):
        keys = sorted(list(dict.keys()))
        try:
            to_move = keys[keys.index(pos) :]
        except ValueError:
            dict[pos] = item
            return dict
        to_move.reverse()
        for key in to_move:
            dict[key + 1] = dict[key]
        dict[pos] = item
        return dict

    def write(self, data: Any):
        self.csv_data: list[list[str]] = []
        self.row_index = 0
        self.write_buffer: dict[int, Row] = {}
        self.csv_buffer: dict[int, dict[int, str]] = {}
        for i, row in enumerate(self.structure):
            previous_rows = self.structure[: i + 1]
            total_ignores = 0
            for prev_row in previous_rows:
                if prev_row.ignore:
                    total_ignores += 1
            if row.id is not None:
                self.write_buffer[self.row_index] = row
                self.row_index += 1
                continue

            if i - total_ignores < 0:
                continue
            dt = data[i - total_ignores]

            if isinstance(row.type_structure, int):
                self.row_index += 1
            elif isinstance(row.type_structure, str):
                pass
            elif isinstance(row.type_structure, list):
                for i, item in enumerate(dt):
                    self.write_line(i, row.type_structure[0], item)
                if isinstance(row.count, str):
                    row_to_set = self.get_row_by_id(row.count, row)
                    if row_to_set is None:
                        raise ValueError(f"Cannot find row with id: {row.count}")
                    row_to_set.values = {0: str(len(dt))}
            elif isinstance(row.type_structure, dict):
                pass
            else:
                args = inspect.getfullargspec(row.type_structure).args[1:]
                annotations = inspect.getfullargspec(row.type_structure).annotations
        for index, row_buffer in self.write_buffer.items():
            self.csv_buffer = self.dict_insert(
                self.csv_buffer, row_buffer.values or {}, index
            )
        for row_index, row_val in self.csv_buffer.items():
            if row_index >= len(self.csv_data):
                for i in range(((row_index - len(self.csv_data)) + 1)):
                    self.csv_data.append([])

            for col_index, col in row_val.items():
                if col_index >= len(self.csv_data[row_index]):
                    self.csv_data[row_index].append(
                        "" * ((col_index - len(self.csv_data[row_index])) + 1)
                    )
                self.csv_data[row_index][col_index] = col

    def write_line(self, line_index: int, type_structure: Any, data: Any):
        if isinstance(type_structure, (int, str)):
            if self.row_index not in self.csv_buffer:
                self.csv_buffer[self.row_index] = {}
            self.csv_buffer[self.row_index][line_index] = str(data)
        elif isinstance(type_structure, list):
            for i, item in enumerate(data):
                self.write_line(i, type_structure[0], item)
            self.row_index += 1


class KeyFrame:
    def __init__(
        self,
        frame: int,
        change: int,
        ease_mode: int,
        ease_power: int,
    ):
        self.frame = frame
        self.change = change
        self.ease_mode = ease_mode
        self.ease_power = ease_power

    def __str__(self) -> str:
        return f"KeyFrame({self.frame}, {self.change}, {self.ease_mode}, {self.ease_power})"

    def __repr__(self) -> str:
        return str(self)


class KeyFrameSet:
    def __init__(
        self,
        part_id: int,
        modification_type: int,
        loop: int,
        min: int,
        max: int,
        name: str,
        keyframes: list[KeyFrame],
    ):
        self.part_id = part_id
        self.modification_type = modification_type
        self.loop = loop
        self.min = min
        self.max = max
        self.name = name
        self.keyframes = keyframes

    def __str__(self) -> str:
        return f"KeyFrameSet({self.part_id}, {self.modification_type}, {self.loop}, {self.min}, {self.max}, {self.name}, {self.keyframes})"

    def __repr__(self) -> str:
        return str(self)


# c1 i0 1
# c7 i1 6
# c12 i2 11


class Maanim:
    def __init__(self, keyframes: list[KeyFrameSet]):
        self.keyframes = keyframes

    def __str__(self) -> str:
        return f"Maanim({self.keyframes})"

    def __repr__(self) -> str:
        return str(self)


if __name__ == "__main__":
    csv_data: list[list[str]] = [
        ["3"],
        ["1", "12", "1", "0", "0"],
        ["3"],
        ["0", "0", "0", "0"],
        ["10", "2550", "2", "2"],
        ["60", "0", "0", "0"],
        ["1", "11", "1", "0", "0"],
        ["3"],
        ["0", "0", "0", "0"],
        ["152", "0", "2", "2"],
        ["190", "-800", "0", "0"],
        ["1", "11", "1", "0", "0"],
        ["3"],
        ["1", "0", "0", "0"],
        ["156", "0", "2", "2"],
        ["190", "-800", "0", "0"],
    ]
    # structure = [
    #    Row(
    #        type_structure=Maanim,
    #        rows=[
    #            Row(id="total_keyframe_sets"),
    #            Row(
    #                type_structure=[KeyFrameSet],
    #                count="total_keyframe_sets",
    #                cls_vars=[0],
    #                rows=[
    #                    Row(cls_vars=[0, 1, 2, 3, 4, 5]),
    #                    Row(id="total_keyframes"),
    #                    Row(
    #                        cls_vars=[6],
    #                        type_structure=[KeyFrame],
    #                        count="total_keyframes",
    #                    ),
    #                ],
    #            ),
    #        ],
    #    )
    # ]
    print(csv_data)
    print("\n\n\n\n")
    structure = [
        Row(id="total_lines", ignore=True),
        Row(type_structure=[[0]], count="total_lines"),
        Row(type_structure=[[0]], count="total_lines"),
    ]
    csv2 = CSV2(csv_data, structure)
    maanim = csv2.data
    print(maanim)
    print("\n\n\n")
    csv2.write(maanim)
    print("\n\n\n\n")
    print(csv2.csv_data)


def to_str(
    item: Optional[Union[str, int, enum.Enum, bool]], is_int: bool = True
) -> str:
    if item is None:
        if is_int:
            return "0"
        return ""
    if isinstance(item, enum.Enum):
        item = item.value
    if isinstance(item, bool):
        item = int(item)
    return str(item)


class DelimeterType(enum.Enum):
    COMMA = ","
    TAB = "\t"
    PIPE = "|"


class Delimeter:
    def __init__(self, de: Union[DelimeterType, str]):
        if isinstance(de, str):
            self.delimeter = DelimeterType(de)
        else:
            self.delimeter = de

    @staticmethod
    def from_country_code_res(cc: "core.CountryCode") -> "Delimeter":
        if cc == core.CountryCode.JP:
            return Delimeter(DelimeterType.COMMA)
        else:
            return Delimeter(DelimeterType.PIPE)

    def __str__(self) -> str:
        return self.delimeter.value


class CSV:
    def __init__(
        self,
        file_data: Optional["core.Data"] = None,
        delimeter: Union[Delimeter, str] = Delimeter(DelimeterType.COMMA),
        remove_padding: bool = True,
        remove_comments: bool = True,
        remove_empty: bool = True,
    ):
        if file_data is None:
            file_data = core.Data()
        self.file_data = file_data
        if remove_padding:
            try:
                self.file_data = self.file_data.unpad_pkcs7()
            except ValueError:
                pass
        self.delimeter = str(delimeter)
        self.remove_comments = remove_comments
        self.remove_empty = remove_empty
        self.index = 0
        self.str_index = 0
        self.line_length = 0
        self.is_int = True
        self.ignore_none = True
        self.parse()

    def parse(self):
        lines: list[list[str]] = []
        for line in self.file_data.to_str().splitlines():
            if self.remove_comments:
                line = line.split("//")[0]
            line = line.strip()
            line = line.split(self.delimeter)
            if self.remove_empty:
                line = [x for x in line if x]
                if not line:
                    continue
            lines.append(line)
        self.lines = lines

    @staticmethod
    def from_file(
        path: "core.Path", delimeter: Delimeter = Delimeter(DelimeterType.COMMA)
    ) -> "CSV":
        return CSV(path.read(), delimeter)

    def reset_index(self):
        self.index = 0
        self.str_index = 0

    def __iter__(self):
        return self

    def __next__(self) -> list[str]:
        line = self.read_line()
        if line is None:
            raise StopIteration
        return line

    def read_line(self) -> Optional[list[str]]:
        if self.index >= len(self.lines):
            return None
        line = self.lines[self.index]
        self.index += 1
        return line

    def get_current_line(self) -> Optional[list[str]]:
        if self.index >= len(self.lines):
            return None
        line = self.lines[self.index]
        return line

    def to_data(self) -> "core.Data":
        return core.Data(
            "\n".join([self.delimeter.join(line) for line in self.lines if line])
        )

    def extend(
        self,
        length: int,
        sub_length: int = 0,
        item: str = "",
    ):
        for _ in range(length):
            if sub_length == 0:
                self.lines.append([])
            else:
                self.lines.append([item] * sub_length)

    def extend_to(self, length: int, sub_length: int = 0, item: str = ""):
        if length > len(self.lines):
            self.extend(length - len(self.lines) + 1, sub_length, item)

    def set_line(self, line: list[str], index: int):
        if index >= len(self.lines):
            self.extend(index - len(self.lines) + 1)
        self.lines[index] = line

    def init_setter(
        self,
        index: Optional[int] = None,
        line_length: int = 0,
        is_int: bool = True,
        ignore_none: bool = True,
        index_line_index: Optional[int] = None,
    ):
        if index_line_index is not None:
            for i, line in enumerate(self.lines):
                if int(line[index_line_index]) == index:
                    self.index = i
                    break
            else:
                self.index = len(self.lines)
        self.str_index = 0
        if index is not None:
            self.index = index
        else:
            self.index += 1
        self.extend_to(self.index, line_length, "0" if is_int else "")
        self.is_int = is_int
        self.ignore_none = ignore_none

    def init_getter(
        self, index: Optional[Union[int, str]] = None, line_length: int = 0
    ):
        if isinstance(index, str):
            try:
                index = int(index)
            except ValueError:
                index = None
        self.str_index = 0
        if index is not None:
            self.index = index
        else:
            self.index += 1
        self.line_length = line_length

    def set_str(
        self,
        item: Optional[Union[str, int, enum.Enum, bool]],
    ):
        line = self.get_current_line()
        if line is None:
            raise ValueError("No line to set")
        if self.ignore_none and item is None:
            return line
        if isinstance(item, enum.Enum):
            item = item.value
        try:
            line[self.str_index] = to_str(item, self.is_int)
        except IndexError:
            if self.is_int:
                line.extend(["0"] * (self.str_index - len(line)))
            else:
                line.extend([""] * (self.str_index - len(line)))
            line.append(to_str(item, self.is_int))
        self.str_index += 1

        return line

    def get_str(self):
        line = self.get_current_line()
        if line is None:
            return ""
        if self.str_index >= len(line):
            return ""
        item = line[self.str_index]
        self.str_index += 1
        return item

    def get_int(self):
        try:
            return int(self.get_str())
        except ValueError:
            return 0

    def get_bool(self):
        return bool(self.get_int())

    def get_str_list(self) -> list[str]:
        line = self.get_current_line()
        if line is None:
            return []
        if self.str_index >= len(line):
            return []
        item = line[self.str_index :]
        self.str_index += len(item)
        return item

    def get_int_list(self) -> list[int]:
        line = self.get_current_line()
        if line is None:
            return []
        if self.str_index >= len(line):
            return []
        item = line[self.str_index :]
        self.str_index += len(item)
        lst: list[int] = []
        for i in item:
            try:
                lst.append(int(i))
            except ValueError:
                lst.append(0)
        return lst

    def set_list(self, item: Optional[list[Any]]):
        if item is None:
            return
        for i in item:
            self.set_str(i)

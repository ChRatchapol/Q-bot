# utils
# | IMPORT SECTION
import os
import sys
from typing import Any, Dict, List, Union
from dotenv import load_dotenv

# | GLOBAL EXECUTION

load_dotenv()
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
COMMAND_LIST = eval(os.getenv("COMMAND_LIST"))

# | CLASSES


class Queue:
    """
    Queue datatype
    """

    def __init__(
        self, size: Union[int, float] = float("inf"), content: Dict = {}
    ) -> None:
        self.max_size = int(size) if size != float("inf") else size
        self.content = content.copy()

    def __len__(self) -> int:
        return len(self.content)

    def __getitem__(self, index: int) -> Any:
        if len(self) - 1 >= abs(index):
            if index < 0:
                index = len(self) + index
            return self.content[index]
        else:
            raise IndexError("index out of range")

    def __setitem__(self, index: int, item: Any) -> None:
        if len(self) - 1 >= abs(index):
            if index < 0:
                index = len(self) + index
            self.content[index] = item
        else:
            raise IndexError("index out of range")

    def __contain__(self, item: Any) -> bool:
        return item in self.content.values()

    def __str__(self) -> str:
        return (
            "|" + ", ".join([f"{i}: {repr(c)}" for i, c in self.content.items()]) + "|"
        )

    def __repr__(self) -> str:
        tmp = "float('inf')"
        return f"Queue(size={repr(self.max_size) if self.max_size != float('inf') else tmp}, content={repr(self.content)})"

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        if self.__index <= len(self) - 1:
            res = self[self.__index]
            self.__index += 1
            return res
        else:
            raise StopIteration()

    def push(self, item: Any) -> None:
        """
        push item to the queue (at the end)

        Parameters
        ----------
        item : Any
            Item that will be pushed to the queue.

        Raises
        ------
        Queue.Full
            The queue is full. (limit by size)
        """

        if len(self) < self.max_size:
            self.content[len(self)] = item
        else:
            raise Queue.Full("queue is full")

    def pop(self) -> Any:
        """
        pop item out from the queue (at the top of the queue)

        Returns
        -------
        Any
            item in the queue

        Raises
        ------
        Queue.Empty
            The queue is empty.
        """

        if len(self) > 0:
            # index = list(self.content.keys())[0]
            # return self.content.pop(index)
            res = self.content.pop(0)
            tmp = {}
            for i, c in self.content.items():
                tmp[i - 1] = c
            self.content = tmp.copy()
            return res
        else:
            raise Queue.Empty("queue is empty")

    def show(self) -> str:
        """
        show contents inside the queue (line by line)

        Returns
        -------
        str
            string output
        """
        return "\n".join([f"{i+1}: {c}" for i, c in self.content.items()])

    def remove(self, index: int) -> None:
        """
        remove item from the queue by index

        Parameters
        ----------
        index : int
            index of item in the queue

        Raises
        ------
        IndexError
            Index is out of range.
        """

        if len(self) - 1 >= abs(index):
            if index < 0:
                index = len(self) + index
            self.content.pop(index)
            tmp = {}
            for i, c in self.content.items():
                if i < index:
                    tmp[i] = c
                else:
                    tmp[i - 1] = c
            self.content = tmp.copy()
        else:
            raise IndexError("index out of range")

    def remove_from_value(self, value: Any) -> None:
        """
        remove item from the queue by value

        Parameters
        ----------
        value : Any
            An item that will be removed.

        Raises
        ------
        ValueError
            An item is not in the queue.
        """

        for i, c in self.content.items():
            if c == value:
                self.remove(i)
                return
        raise ValueError(f"{value} not in this queue")

    class Full(Exception):
        """
        The queue is full.
        """
        pass

    class Empty(Exception):
        """
        The queue is empty.
        """
        pass


class QueueBotQ(Queue):
    """
    Queue datatype for Q Bot

    Overwrite
    ----------
    show :
        more beautiful
    """

    def show(self) -> str:
        if len(self) == 0:
            return ""
        bar = "─" * 40
        double_bar = "═" * 40
        tmp = []
        for i, c in self.content.items():
            c_str = ", ".join([f"{k}: {v}" for k, v in c.items()])
            tmp.append(f"{i+1}: {c_str}")
        return f"{double_bar}\n" + f"\n{bar}\n".join(tmp) + f"\n{double_bar}"

    def raw_show(self) -> str:
        if len(self) == 0:
            return ""
        tmp = []
        for _, c in self.content.items():
            c_str = ",".join([f"{v}" for _, v in c.items()])
            tmp.append(f"{c_str}")
        return f"\n".join(tmp)


# | FUNCTIONS


def chk_cmd(msg: str) -> bool:
    """
    check if received message is command or not

    Parameters
    ----------
    msg : str
        message that will be checked

    Returns
    -------
    bool
        True if msg is command otherwise False
    """

    global COMMAND_PREFIX
    global COMMAND_LIST

    msg = msg.strip().split(" ")
    cmd = msg[0]

    if cmd in [COMMAND_PREFIX + cmd for cmd in COMMAND_LIST]:
        return True
    else:
        return False


def parse_cmd(cmd: str) -> Dict[str, Union[str, List[str]]]:
    """
    parse received command from string to dictionary (For Inno. queue only)

    Parameters
    ----------
    cmd : str
        command that will be parsed

    Returns
    -------
    Dict[str, Union[str, List[str]]]
        A dictionary contain command in 'command' key as string and parameters in 'parameters' key as list of string
    """

    global COMMAND_PREFIX
    global COMMAND_LIST

    command = cmd.split(" ")[0]
    param = " ".join(cmd.split(" ")[1:])

    param_lst = []
    if command in ["$add", "$remove"]:
        found = False
        tmp = ""
        prev = ""
        for c in param:
            if c == '"':
                if found:
                    if prev == "\\":
                        tmp = tmp[:-1] + c
                        prev = c
                        continue
                    param_lst.append(tmp.strip())
                    tmp = ""
                    prev = ""
                    found = False
                else:
                    found = True
                    continue
            else:
                if found:
                    tmp += c
            prev = c

    return {"command": command, "parameters": param_lst}


def param_lst2param_dct(param_lst: List[str]) -> Dict[str, str]:
    """
    convert list of 2 parameters ([group, topic]) to parameters dict. ({"group": group, "topic": topic}) (For Inno. queue only)

    Parameters
    ----------
    param_lst : List[str]
        list of parameters (length must be 2 otherwise the other items will be ignored)

    Returns
    -------
    Dict[str, str]
       dictionary of parameters
    """

    return {"group": param_lst[0], "topic": param_lst[1]}


def write(q: QueueBotQ, filename: str) -> None:
    """
    write data from QueueBotQ to a file (For Inno. queue only)

    Parameters
    ----------
    q : QueueBotQ
        QueueBotQ that will be write to a file
    filename : str
        filename or filepath
    """

    filename = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], filename)
    with open(filename, "wt", encoding="utf-8") as f:
        f.write(q.raw_show())


def load(filename: str) -> QueueBotQ:
    """
    load content from a file and create QueueBotQ (For Inno. queue only)

    Parameters
    ----------
    filename : str
        filename or filepath

    Returns
    -------
    QueueBotQ
        QueueBotQ that contain data from a file
    """

    q = QueueBotQ()
    filename = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], filename)
    if not os.path.isfile(filename):
        with open(filename, "wt", encoding="utf-8") as f:
            pass

    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()
        data = [line.strip() for line in lines]
        data = [tuple(line.split(",")) for line in data]

        for g, t in data:
            q.push({"group": g, "topic": t})
    return q


def test() -> None:
    """
    for testing queue reading/writing from/to a file
    """
    q = QueueBotQ()
    q.push({"group": "1", "topic": "2"})
    q.push({"group": "2", "topic": "5"})
    q.push({"group": "3", "topic": "9"})
    write(q, "test_queue.q")
    t = load("test_queue.q")
    print(t)

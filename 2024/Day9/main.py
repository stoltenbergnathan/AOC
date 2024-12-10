from dataclasses import dataclass
from itertools import repeat


@dataclass
class File:
    id: int

    def copy(self) -> "File":
        return File(self.id)


class DiskMap:
    def __init__(self, disk_map: str) -> None:
        self.disk_map = disk_map
        self.num_files = 0
        self.files: list[File] = []

    def print_files(self) -> None:
        for file in self.files:
            if file.id != -1:
                print(file.id, end="")
            else:
                print(".", end="")
        print()

    def parse_disk_map(self) -> None:
        current_file_id = 0
        parsing_file = True

        for char in self.disk_map:
            if parsing_file:
                self.files.extend(repeat(File(current_file_id), int(char)))
                current_file_id += 1
            else:
                self.files.extend(repeat(File(-1), int(char)))

            parsing_file = not parsing_file

        self.num_files = current_file_id - 1

    def condense_files(self) -> None:
        left_index = 0
        right_index = len(self.files) - 1
        while left_index < right_index:
            if self.files[left_index].id != -1:
                left_index += 1
                continue

            if self.files[right_index].id == -1:
                right_index -= 1
                continue

            temp = self.files[left_index]
            self.files[left_index] = self.files[right_index]
            self.files[right_index] = temp
            right_index -= 1

    def condese_files_pt2(self) -> None:
        @dataclass
        class FreeSpan:
            start: int
            end: int
            length: int

        @dataclass
        class FileSpan:
            start: int
            end: int
            id: int
            length: int

        def get_spans() -> tuple[list[FreeSpan], list[FileSpan]]:
            free_spans: list[FreeSpan] = []
            file_spans: list[FileSpan] = []

            index: int = 0
            while len(file_spans) < (self.num_files + 1):
                file: File = self.files[index]
                if file.id == -1:
                    free_index: int = index
                    while free_index < len(self.files):
                        value: File = self.files[free_index]
                        if value.id != -1:
                            free_spans.append(
                                FreeSpan(index, free_index - 1, free_index - index)
                            )
                            index = free_index
                            break
                        free_index += 1
                else:
                    file_id: int = file.id
                    file_index: int = index
                    while file_index < len(self.files):
                        value: File = self.files[file_index]
                        if value.id != file_id:
                            file_spans.append(
                                FileSpan(
                                    index,
                                    file_index - 1,
                                    file.id,
                                    file_index - index,
                                )
                            )
                            index = file_index
                            break
                        file_index += 1
                    if file_index == len(self.files):
                        file_spans.append(
                            FileSpan(
                                index,
                                len(self.files) - 1,
                                file.id,
                                len(self.files) - index,
                            )
                        )

            return free_spans, file_spans

        free_spans, file_spans = get_spans()

        file_spans.sort(key=lambda x: x.id, reverse=True)

        for file_span in file_spans:
            for free_span in free_spans:
                if (
                    free_span.length >= file_span.length
                    and free_span.start < file_span.start
                ):  # There is enough space
                    start: int = free_span.start
                    end: int = free_span.start + file_span.length
                    self.files[start:end] = repeat(File(file_span.id), file_span.length)
                    self.files[file_span.start : file_span.end + 1] = repeat(
                        File(-1), file_span.length
                    )
                    free_span.start = end
                    free_span.length -= file_span.length
                    break

    def calculate_checksum(self) -> int:
        checksum = 0
        for index, file in enumerate(self.files):
            if file.id == -1:
                continue
            checksum += index * file.id
        return checksum


def read_file(file_name: str) -> str:
    with open(file_name) as f:
        return f.read()


def main() -> None:
    disk_map: DiskMap = DiskMap(read_file("input.txt"))
    disk_map.parse_disk_map()
    disk_map.print_files()
    disk_map.condese_files_pt2()
    disk_map.print_files()
    print(disk_map.calculate_checksum())


if __name__ == "__main__":
    # too high
    # 8564936405055
    # 6362722604045
    main()

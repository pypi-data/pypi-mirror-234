from biolib.typing_utils import List, Optional


class SeqUtilRecord:
    def __init__(self, sequence: str, sequence_id: str, description: Optional['str']):
        self.sequence = sequence
        self.id = sequence_id  # pylint: disable=invalid-name
        self.description = description

    def __repr__(self) -> str:
        return f'{self.__class__.__name__} ({self.id})'


class SeqUtil:
    @staticmethod
    def parse_fasta(file_name: str, default_header: Optional[str] = None) -> List[SeqUtilRecord]:
        with open(file_name, 'r') as file_handle:
            data = file_handle.read().strip()

        if not data:
            return []

        if '>' not in data:
            if default_header:
                lines_with_header = []
                for index, line in enumerate(data.split('\n')):
                    index_string = str(index + 1) if index > 0 else ''
                    lines_with_header.append(f'>{default_header}{index_string}\n{line}')

                data = '\n'.join(lines_with_header)
            else:
                raise Exception(f'No header line found in FASTA file "{file_name}"')

        splitted = []
        tmp_data = ""
        for line in data.splitlines():
            if line.startswith(">"):
                if tmp_data:
                    splitted.append(tmp_data)
                tmp_data = line[1:].strip() + '\n'
            else:
                if line.strip():
                    tmp_data += line.strip() + '\n'

        if tmp_data:
            splitted.append(tmp_data)

        parsed_sequences = []
        for sequence_data in splitted:
            sequence_data_splitted = sequence_data.strip().split('\n')
            header_line = sequence_data_splitted[0].split()
            sequence_id = header_line[0]
            description = sequence_data_splitted[0][len(sequence_id):].strip()
            sequence = "".join([seq.strip() for seq in sequence_data_splitted[1:]])
            parsed_sequences.append(
                SeqUtilRecord(sequence=sequence, sequence_id=sequence_id, description=description)
            )
        return parsed_sequences

    @staticmethod
    def write_records_to_fasta(file_name: str, records: List[SeqUtilRecord]) -> None:
        with open(file_name, mode='w') as file_handle:
            for record in records:
                optional_description = f' {record.description}' if record.description else ''
                sequence = '\n'.join(record.sequence[i:i + 80] for i in range(0, len(record.sequence), 80))
                file_handle.write(f'>{record.id}{optional_description}\n{sequence}\n')

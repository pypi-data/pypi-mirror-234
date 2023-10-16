class MergeCobertura:
    def __init__(self, files, output) -> None:
        self.files = files
        self.output = output

    def merge(self):
        print(f"merging {self.files} to {self.output}")

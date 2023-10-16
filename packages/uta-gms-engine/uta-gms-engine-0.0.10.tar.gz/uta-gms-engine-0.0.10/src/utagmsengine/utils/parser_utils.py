from xmcda.XMCDA import XMCDA

import os


class ParserUtils:

    @staticmethod
    def load_file(path: str) -> XMCDA:
        """
        Private method responsible for loading XMCDA files from tests/files location.
        To be refined later when we will read files from different location

        :param path: Path to XMCDA file

        :return: XMCDA
        """
        xmcda: XMCDA = XMCDA()
        current_script_path: str = os.path.dirname(os.path.abspath(__file__))
        directory_path: str = os.path.dirname(os.path.dirname(current_script_path))
        refined_path: str = os.path.normpath(os.path.join(directory_path, f"../tests/files/{path}"))

        xmcda: XMCDA = xmcda.load(refined_path)

        return xmcda



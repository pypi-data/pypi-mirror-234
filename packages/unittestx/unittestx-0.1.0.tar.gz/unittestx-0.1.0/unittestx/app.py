import unittest
import argparse
from typing import Literal, LiteralString, TextIO

from termcolor import colored


class UnitTestXTestResult(unittest.TestResult):
    def __init__(self, stream, descriptions, verbosity) -> None:
        super().__init__()
        self.stream: TextIO | None = stream
        self.descriptions: bool | None = descriptions
        self.verbosity: int | None = verbosity
        self.custom_output: list = []
        self.test_statuses: dict[str, int] = {
            'PASSED': 0,
            'FAILED': 0,
            'ERROR': 0,
            'SKIPPED': 0,
        }

    def addSuccess(self, test) -> None:
        STATUS: Literal['PASSED'] = self._format_message(
            "PASSED", '✓ ', "light_green", test)
        self.test_statuses[STATUS] += 1

    def addError(self, test, err) -> None:
        STATUS: Literal['ERROR'] = self._format_message(
            "ERROR", 'X ', "red", test)
        self.stream.write(str(err[1]) + "\n")
        self.test_statuses[STATUS] += 1

    def addFailure(self, test, err) -> None:
        STATUS: Literal['FAILED'] = self._format_message(
            "FAILED", '⨯ ', "light_red", test)
        self.stream.write(f"    Reason: {str(err[1])}\n")
        self.test_statuses[STATUS] += 1

    def addSkip(self, test, reason) -> None:
        STATUS: Literal['SKIPPED'] = self._format_message(
            "SKIPPED", 's ', "light_blue", test)
        self.stream.write(f"    Reason: {str(reason)}\n")
        self.test_statuses[STATUS] += 1

    def _format_message(self, arg0, arg1, arg2, test) -> str:
        result: str = arg0
        text: LiteralString = f"{arg1}{result}: "
        self.stream.write(f"  {colored(text, arg2)}{test}\n")
        return result

    def _get_divider(self, test) -> str:
        return f"{70 * '-'}\n{test}\n{70 * '-'}"

    def get_summary(self) -> str:
        return f"SUMMARY: " \
            f"  PASSED({self.test_statuses['PASSED']})" \
            f"  FAILED({self.test_statuses['FAILED']})" \
            f"  ERROR({self.test_statuses['ERROR']})" \
            f"  SKIPPED({self.test_statuses['SKIPPED']})"


class UnitTestXTestRunner(unittest.TextTestRunner):

    def _makeResult(self) -> UnitTestXTestResult:
        return UnitTestXTestResult(
            self.stream, self.descriptions, self.verbosity
        )


def load_tests(start_dir, pattern) -> unittest.TestSuite:
    test_loader = unittest.TestLoader()
    test_suite: unittest.TestSuite = test_loader.discover(
        start_dir=start_dir, pattern=pattern)
    return test_suite


def main() -> None:
    parser = argparse.ArgumentParser(description='Custom unittest runner')
    parser.add_argument(
        '-s', '--start-dir',
        type=str,
        default='tests',
        help='Starting directory for test discovery'
    )
    parser.add_argument(
        '-p', '--pattern',
        type=str,
        default='test_*.py',
        help='Pattern for test file discovery'
    )
    parser.add_argument(
        '-v', '--verbosity',
        type=int,
        default=2,
        help='Verbosity level (0, 1, 2)'
    )

    args: argparse.Namespace = parser.parse_args()

    test_suite: unittest.TestSuite = load_tests(args.start_dir, args.pattern)
    runner = UnitTestXTestRunner(verbosity=args.verbosity)
    result: unittest.TestResult = runner.run(test_suite)
    summary: str = result.get_summary()
    print("=" * 55)
    print(summary)
    print("=" * 55)


if __name__ == "__main__":
    main()

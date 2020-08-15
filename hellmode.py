from fakir import fixed, normal, repeat
from random import Random
import sys

from typing import List

guy = normal(100, 25)
dude = guy.bind(
  lambda g: repeat(normal(g, 5), 3).bind(lambda d: fixed((g, d))))

def main(argv: List[str]) -> int:
    r = Random(12345)
    for _ in range(25):
        print(dude.generate(r))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

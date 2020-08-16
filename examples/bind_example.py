from fakir import fixed, normal, repeat
from random import Random
import sys

from typing import List

guy = normal(100, 25)
dude = guy.bind(
  lambda g: repeat(normal(g, 2), 3).bind(lambda d: normal(d[0], 0.05).bind(lambda x: fixed((g, d, x)))))
dude2 = dude.iid()

def main(argv: List[str]) -> int:
    r = Random(12345)
    for _ in range(13):
        print(dude.generate(r))
        print(dude2.generate(r))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

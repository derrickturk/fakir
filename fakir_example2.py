from fakir import fixed, rng_fn, uniform, normal, choice, tupled, ifelse
from random import Random
import sys

from typing import List

def main(argv: List[str]) -> int:
    animal = choice(['Wolf', 'Eagle', 'Cheetah'])
    geo = choice(['Outcrop', 'Karst', 'Tundra'])

    formation = animal + fixed(' ') + geo

    area = normal(40, 10)
    height = uniform(10, 100)
    a_h_v = area.bind(lambda a: height.bind(lambda h: fixed((a, h, a * h))))

    phase = choice(['Oil', 'Gas'])
    phase_price = phase.bind(
            lambda p: (
                uniform(30, 60) if p == 'Oil' else uniform(1.5, 4.5)
            ).fmap(lambda pr: (p, pr)))

    row = tupled(formation, a_h_v, phase_price, area)

    r = Random(12345)
    for i in range(100):
        print(row.generate(r))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

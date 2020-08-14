from fakir import fixed, rng_fn, uniform, normal, choice, tupled, ifelse
from random import Random
import sys

from typing import List

def main(argv: List[str]) -> int:
    animal = choice(['Wolf', 'Eagle', 'Cheetah'])
    geo = choice(['Outcrop', 'Karst', 'Tundra'])

    formation = animal + fixed(' ') + geo

    area = normal(40, 10)
    some_other_area = area
    area = area.lock()
    height = uniform(10, 100).lock()
    volume = area * height

    phase = choice(['Oil', 'Gas']).lock()
    price = ifelse(phase == fixed('Oil'),
        uniform(30, 60),
        uniform(1.5, 4.5)
    )

    row = tupled(formation, area, height, volume, phase, price, some_other_area)

    r = Random(12345)
    for i in range(100):
        print(row.generate(r))
        area.clear()
        height.clear()
        phase.clear()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

from fakir2 import fixed, rng_fn, uniform, normal, choice, tupled, ifelse
from random import Random
import sys

from typing import List

def main(argv: List[str]) -> int:
    animal = choice(['Wolf', 'Eagle', 'Cheetah'])
    geo = choice(['Outcrop', 'Karst', 'Tundra'])

    formation = animal + fixed(' ') + geo

    area = normal(40, 10)
    some_other_area = area.clone() # another independent variable
    height = uniform(10, 100)
    volume = area * height

    phase = choice(['Oil', 'Gas'])
    price = ifelse(phase == fixed('Oil'),
        uniform(30, 60),
        uniform(1.5, 4.5)
    )

    price2 = price.clone()

    row = tupled(formation, area, height, volume, phase, price, some_other_area, price2)

    r = Random(12345)
    for i in range(100):
        print(row.generate(r))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

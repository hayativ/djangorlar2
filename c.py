"""
File C — prime checker + CLI arguments
"""

import argparse
import math


def is_prime(n: int) -> bool:
    """Check if number is prime."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    limit = int(math.sqrt(n))
    for i in range(3, limit + 1, 2):
        if n % i == 0:
            return False
    return True


def primes_up_to(n: int):
    """Generate a list of prime numbers up to n."""
    primes = []
    for x in range(2, n + 1):
        if is_prime(x):
            primes.append(x)
    return primes


def parse_cli():
    parser = argparse.ArgumentParser(
        description="Prime number generator"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=50,
        help="Help: message: Generate primes up to this number"
    )
    return parser.parse_args()


def main():
    args = parse_cli()
    print(f"Primes up to {args.n}:")
    print(primes_up_to(args.n))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
from pathlib import Path

from .metrics import AlertCriteria, is_alert
from .providers import PublicApiProvider, SampleProvider, SearchQuery


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Award availability alerting for public, authorized APIs."
    )
    parser.add_argument("--origin", required=True)
    parser.add_argument("--destination", required=True)
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument(
        "--provider",
        choices=["sample", "public"],
        default="sample",
        help="Data provider to use",
    )
    parser.add_argument(
        "--endpoint",
        default="",
        help="Public API endpoint when using provider=public",
    )
    parser.add_argument("--api-key", default="", help="Bearer token for API")
    parser.add_argument(
        "--min-cpp",
        type=float,
        default=None,
        help="Minimum cents per point to trigger alert",
    )
    parser.add_argument(
        "--max-points",
        type=int,
        default=None,
        help="Maximum points to trigger alert",
    )
    return parser


def select_provider(args: argparse.Namespace):
    if args.provider == "public":
        if not args.endpoint:
            raise ValueError("--endpoint is required when using provider=public")
        return PublicApiProvider(args.endpoint, api_key=args.api_key or None)
    data_path = Path(__file__).with_name("sample_data.json")
    return SampleProvider(data_path)


def run() -> int:
    parser = build_parser()
    args = parser.parse_args()

    provider = select_provider(args)
    query = SearchQuery(args.origin, args.destination, args.date)
    criteria = AlertCriteria(
        min_cents_per_point=args.min_cpp, max_points=args.max_points
    )

    results = list(provider.search(query))
    if not results:
        print("No award data found.")
        return 0

    for quote in results:
        cpp = quote.cents_per_point
        cpp_display = f"{cpp:.2f}" if cpp is not None else "N/A"
        alert_flag = "ALERT" if is_alert(quote, criteria) else "-"
        print(
            f"{alert_flag} {quote.carrier} {quote.origin}-{quote.destination} "
            f"{quote.date}: {quote.points} pts, ${quote.cash_usd:.2f}, "
            f"{cpp_display} cpp"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

"""Render GitHub's daily contribution levels as an isometric SVG."""
import json
import sys
from datetime import date
from pathlib import Path

calendar = json.load(sys.stdin)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"]
levels = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
colors = ["#233c55", "#367cb0", "#369fce", "#4bc8de", "#a3f4f6"]
days = [day for week in weeks for day in week["contributionDays"]]
if not 360 <= len(days) <= 371:
    raise ValueError("Incomplete contribution calendar")
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 420" role="img" aria-labelledby="t d">',
       '<title id="t">GitHub contribution landscape</title>',
       '<desc id="d">Each tile represents a day. Height and color follow GitHub activity levels.</desc>',
       '<rect width="1140" height="420" rx="18" fill="#0c192c"/>',
       '<g font-family="Arial,sans-serif"><text x="36" y="48" font-size="22" fill="#e1eefb">Contribution landscape</text>',
       f'<text x="36" y="75" font-size="16" fill="#9fb9d4">{days[0]["date"]} — {days[-1]["date"]}</text></g>']
svg.append('<defs>')
for level, height in enumerate([2, 11, 24, 38, 55]):
    svg.extend([f'<g id="tile{level}" fill="{colors[level]}">',
                f'<path d="M-16 2l16 4 16 -8v{height}l-16 8 -16 -4z"/>',
                f'<path d="M-16 2l16 4v{height}l-16 -4z" fill="#051832" opacity=".47"/>',
                f'<path d="M0 6l16 -8v{height}l-16 8z" fill="#00162a" opacity=".27"/>',
                '<path d="M0 -6l16 4 -16 8 -16 -4z"/></g>'])
svg.append('</defs>')
for week_index, week in enumerate(weeks):
    for day in week["contributionDays"]:
        weekday = (date.fromisoformat(day["date"]).weekday() + 1) % 7
        level = levels.index(day["contributionLevel"])
        x = 153 + 18 * week_index - 18 * weekday
        y = 110 + 4 * week_index + 9 * weekday - [2, 11, 24, 38, 55][level]
        svg.append(f'<use href="#tile{level}" x="{x}" y="{y}"/>')
svg.append('</svg>')
Path("assets/contributions.svg").write_text("\n".join(svg) + "\n")

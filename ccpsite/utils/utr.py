__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


def rating_and_status_to_display(rating, status):
    """Convert a rating and status to display format"""

    if rating is None:
        rating = 0.0
    else:
        rating = round(rating, 2)

    if status is None or status == "Unrated":
        status = "U"
    elif status == "Projected":
        status = "P"
    elif status == "Rated":
        status = "R"
    else:
        status = "U"

    return f"{rating} ({status})"


def get_display_rating(rating, status, reliability):
    """Convert rating, status and reliability to displayed rating"""

    ...

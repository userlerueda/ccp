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


def get_display_rating(player):
    """Convert rating, status and reliability to displayed rating"""

    rating = "0.00"
    rating_progress_singles = player.rating_progress_singles
    if rating_progress_singles is None:
        rating_progress_singles = 0.0
    my_utr_progress_singles = player.my_utr_progress_singles
    if my_utr_progress_singles is None:
        if player.my_utr_singles_reliability is not None:
            my_utr_progress_singles = round(
                player.my_utr_singles_reliability * 10, 0
            )
        else:
            my_utr_progress_singles = 0.0
    singles_utr = player.singles_utr
    my_utr_singles = player.my_utr_singles

    if singles_utr == 0.0 and my_utr_singles == 0.0:
        return f"{rating}"

    if rating_progress_singles == my_utr_progress_singles:
        rating_value = round(singles_utr, 2)
        rating = f"{rating_value} ✅ {rating_progress_singles}%"
    elif rating_progress_singles > my_utr_progress_singles:
        rating_value = round(singles_utr, 2)
        rating = f"{rating_value} ✅ {rating_progress_singles}%"
    else:
        rating_value = round(my_utr_singles, 2)
        rating = f"{rating_value} {my_utr_progress_singles}%"

    return f"{rating}"


def get_displayed_rating(players):
    """Get the displayed rating for a player"""
    if len(players) > 1:
        return get_displayed_doubles_rating(players)
    else:
        return get_displayed_singles_rating(players)


def get_displayed_singles_rating(player):
    """Get the displayed singles rating for a player"""
    ...


def get_displayed_doubles_rating(players):
    """Get the displayed doubles rating for a player"""
    team_rating = calculate_team_rating(players)
    team_names = []

    for player in players:
        display_name = player.display_name
        rating = "0.00"
        rating_progress_doubles = player.rating_progress_doubles
        if rating_progress_doubles is None:
            rating_progress_doubles = 0.0
        my_utr_progress_doubles = player.my_utr_progress_doubles
        if my_utr_progress_doubles is None:
            my_utr_progress_doubles = round(
                player.my_utr_doubles_reliability * 10, 0
            )
        doubles_utr = player.doubles_utr
        my_utr_doubles = player.my_utr_doubles

        if rating_progress_doubles == my_utr_progress_doubles:
            rating_value = round(doubles_utr, 2)
            rating = f"{rating_value} ✅ {rating_progress_doubles}%"
        elif rating_progress_doubles > my_utr_progress_doubles:
            rating_value = round(doubles_utr, 2)
            rating = f"{rating_value} ✅ {rating_progress_doubles}%"
        else:
            rating_value = round(my_utr_doubles, 2)
            rating = f"{rating_value} {my_utr_progress_doubles}%"
        team_names.append(f"{display_name} ({rating})")

    team_name = "/".join(team_names)

    return f"{team_rating} - {team_name}"


def calculate_team_rating(players):
    """Get the displayed doubles rating for a team"""
    team_rating = 0.0
    team_count = 0

    for player in players:
        rating_value = 0.0

        rating_progress_doubles = player.rating_progress_doubles
        if rating_progress_doubles is None:
            rating_progress_doubles = 0.0
        my_utr_progress_doubles = player.my_utr_progress_doubles
        if my_utr_progress_doubles is None:
            my_utr_progress_doubles = round(
                player.my_utr_doubles_reliability * 10, 0
            )
        doubles_utr = player.doubles_utr
        my_utr_doubles = player.my_utr_doubles

        if rating_progress_doubles == my_utr_progress_doubles:
            rating_value = round(doubles_utr, 2)
        elif rating_progress_doubles > my_utr_progress_doubles:
            rating_value = round(doubles_utr, 2)
        else:
            rating_value = round(my_utr_doubles, 2)
        if rating_value > 0:
            team_count += 1
            team_rating = team_rating + float(rating_value)

            team_rating = round(team_rating / team_count, 2)

    return team_rating

"""Holds the team class which performs calculations about the team"""
import pymongo
from typing import Union


class Team:
    """Retrieves, calculates, and stores data about the team"""

    def __init__(self, team_num: int):
        """Constructor Function

        db is the database to pull from"""
        self.team_num = team_num
        self.db = pymongo.MongoClient("localhost", 27017).scouting_system

    def _avg(self, numbers: list) -> float:
        """Calculate the average of a list of numbers

        numbers is a list of numbers
        Returns a float representing the average"""
        if len(numbers) != 0:  # Check if the list is empty
            avg = 0
            for number in numbers:
                avg += number
            return avg / len(numbers)
        return 0

    def _avg_balls(self) -> float:
        """Calculate the average balls scored"""
        balls = []  # Gather the balls scored per match
        for match in self.db.matches.find({"team_num": self.team_num}):
            balls.append(match["num_balls"])
        return self._avg(balls)

    def _climb_success(self) -> float:
        """Calculate the climb success percentage"""
        climb = []  # Gather the climb status of matches played
        for match in self.db.matches.find({"team_num": self.team_num}):
            if match["climbed"]:
                climb.append(1)
            else:
                climb.append(0)
        return self._avg(climb)

    def _matches_played(self) -> int:
        """Return the number of matches played"""
        matches = self.db.matches.find({"team_num": self.team_num})
        if matches:  # Check if the team has played any matches
            return len(list(matches))
        return 0

    def _least_balls(self) -> Union[int, None]:
        """Return the least number of balls scored out of all matches"""
        least_balls = None  # Return None if the team hasn't played matches
        for match in self.db.matches.find({"team_num": self.team_num}):
            if least_balls is None:
                least_balls = match["num_balls"]
            elif match["num_balls"] < least_balls:
                least_balls = match["num_balls"]
        return least_balls

    def _most_balls(self) -> Union[int, None]:
        """Return the highest number of balls stored in a match out of all matches"""
        most_balls = None  # Return None if the team hasn't played matches
        for match in self.db.matches.find({"team_num": self.team_num}):
            if most_balls is None:
                most_balls = match["num_balls"]
            elif match["num_balls"] > most_balls:
                most_balls = match["num_balls"]
        return most_balls

    def run_calcs(self) -> None:
        """Runs methods to perform the calcs of the team"""
        # Remove the existing team document
        self.db.teams.delete_many({"team_num": self.team_num})
        # Run the calcs and add them to the database
        self.db.teams.insert_one(
            {
                "team_num": self.team_num,
                "avg_balls": self._avg_balls(),
                "climb_success": self._climb_success(),
                "least_balls": self._least_balls(),
                "most_balls": self._most_balls(),
                "matches_played": self._matches_played(),
            }
        )

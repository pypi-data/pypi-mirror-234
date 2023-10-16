import os
import time

import bs4
from collections import defaultdict
import requests
import pandas as pd
import re

LEAGUE_MAPPING = {
    "Bundesliga": "buli",
    "Premier League": "epl",
    "La Liga": "laliga",
    "Ligue 1": "ligue1",
    "Serie A": "seriea",
}
DATA_DIR_PATH = "data/"


class FBRefScraper:
    """
    Class to scrape game stats, lineups and general info from FBRef website and output it as Dataframes
    """

    def __init__(self, season_start_year: int, season_end_year: int, league_name: str):
        """

        Parameters
        ----------
        season_start_year
            Year when the season started
        season_end_year
            Year when the season ended
        league_name
            Name of the league - must be the same as on the FBRef website
        """
        self.season_start_year: int = season_start_year
        self.season_end_year: int = season_end_year
        self.league_name: str = league_name

    def generate_fixtures_url(self):
        """
        Generates a url from the specified season and league
        Returns
        -------
        str
            Url to Fbref fixtures sites that contains the meta info to all games from that season
        """
        url = (
            f"https://fbref.com/en/comps/20/{self.season_start_year}-{self.season_end_year}/"
            f"schedule/{self.season_start_year}-{self.season_end_year}-{self.league_name}-Scores-and-Fixtures"
        )
        return url

    def retrieve_bs4_html(self, url: str):
        """
        Obtains the html of a given url as an Beautiful soup object

        Parameters
        ----------
        url: str
            link to desired website

        Returns
        -------
        bs4.BeautifulSoup
            BeautifulSoup representation of the url's html content
        """
        page = requests.get(url)
        soup = bs4.BeautifulSoup(page.text, features="html.parser")
        return soup

    def scrape_fixtures_to_df(self, save_as_csv: bool = True) -> pd.DataFrame:
        """
        Scrapes the meta info for all games in the season & specified and puts it into a df

        Returns
        -------
        pd.Dateframe
        """
        fixtures_url = self.generate_fixtures_url()
        soup = self.retrieve_bs4_html(fixtures_url)
        tables = soup.find_all("tbody")
        if len(tables) > 1:
            fixtures_table = tables[1]
        elif len(tables) == 0:
            ValueError("No fixtures table found")
        else:
            fixtures_table = tables[0]
        table_rows = fixtures_table.find_all("tr")
        all_fixtures_dict = defaultdict(list)
        for fixture in table_rows:
            if fixture.get("class") == ["spacer", "partial_table", "result_all"]:
                continue
            data_cells = fixture.find_all("td")
            game_week = fixture.find("th").text
            fixture_meta_infos = {
                game_stat["data-stat"]: game_stat.text.strip()
                if game_stat.text.strip()
                else pd.NA
                for game_stat in data_cells
            }
            fixture_meta_infos["match_report"] = (
                "https://fbref.com/"
                + fixture.find("td", attrs={"data-stat": "match_report"}).find("a")[
                    "href"
                ]
            )
            fixture_meta_infos["gameweek"] = game_week
            for stat_name, stat in fixture_meta_infos.items():
                all_fixtures_dict[stat_name].append(stat)
        df_fixtures = pd.DataFrame.from_dict(all_fixtures_dict, orient="columns")
        df_fixtures = df_fixtures.drop(columns=["notes"])
        df_fixtures.loc[
            :, "season"
        ] = f"{self.season_start_year}-{self.season_end_year}"
        df_fixtures = df_fixtures.rename(columns={"match_report": "match_report_url"})
        if save_as_csv:
            file_path = os.path.join(
                DATA_DIR_PATH,
                f"{LEAGUE_MAPPING[self.league_name]}/fbref/fixtures_{self.season_start_year}_{self.season_end_year}.csv",
            )
            df_fixtures.to_csv(file_path, index=False)
        return df_fixtures

    def match_report_to_stats_df(
        self,
        match_report_html: bs4.BeautifulSoup,
        meta_info_dict: dict[
            str,
        ],
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """

        Parameters
        ----------
        match_report_html
            Beautifulsoup object with html of the entire match report page
        meta_info_dict
            meta infos about the game such as teams, date
        Returns
        -------
        pd.DataFrame
        """
        df_keeper_stats = self.keeper_stats_to_df(match_report_html, meta_info_dict)
        df_player_stats = self.player_stats_to_df(match_report_html, meta_info_dict)
        return df_player_stats, df_keeper_stats

    def read_all_table_sheets_into_one_df(
        self,
        table_sheets: bs4.element.ResultSet,
        table_headers: bs4.element.ResultSet,
        team_name: str,
    ) -> pd.DataFrame:
        """
        Reads the stats from all table sheets (i.e. Passing, Pass Types,...) into a single df

        Parameters
        ----------
        table_sheets: bs4.element.ResultSet
            list of bs4 representations of the html code for sheets
        table_headers: bs4.element.ResultSet
            list of bs4 representations of the html code for the sheet headers
        team_name: str
            name of the team, for which the player stats are read

        Returns
        -------
        pd.DataFrame
            containing all the player stats from the table
        """
        if len(table_headers) != len(table_sheets):
            raise ValueError("Number of headers and tables are not equal")
        df_all = pd.DataFrame()
        for sheet_idx in range(len(table_sheets)):
            table_soup = table_sheets[sheet_idx]
            df_stats = self.df_from_single_fbref_table_sheet(table_soup=table_soup)
            if df_all.empty:
                df_all = df_stats
            else:
                df_all = df_all.merge(
                    df_stats,
                    on=[
                        "player",
                        "shirtnumber",
                        "nationality",
                        "position",
                        "age",
                        "minutes",
                    ],
                    suffixes=("", "_remove"),
                )
                df_all = df_all.drop(
                    [i for i in df_all.columns if "remove" in i], axis=1
                )
        df_all.loc[:, "team"] = team_name
        return df_all

    def df_from_single_fbref_table_sheet(
        self, table_soup: bs4.element.Tag
    ) -> pd.DataFrame:
        """
        Reads all stats from a single table sheet. A table sheet refers to one of the headers in the player
        stats table - i.e. Passing, Pass Types,...

        Parameters
        ----------
        table_soup: bs4.element.Tag
            bs4 representation of the html code for the table

        Returns
        -------
        pd.DataFrame
            Df containing all the stats from the given table sheet
        """
        table_rows = table_soup.find_all("tr")
        all_player_stats_dict = defaultdict(list)
        for player in table_rows:
            data_cells = player.find_all("td")
            player_stats = {
                player_stat["data-stat"]: player_stat.text.strip()
                if player_stat.text.strip()
                else pd.NA
                for player_stat in data_cells
            }
            if data_cells:
                player_stats["player"] = (
                    player.find("th", attrs={"data-stat": "player"})
                    .text.strip()
                    .lower()
                )
            for stat_name, stat in player_stats.items():
                all_player_stats_dict[stat_name].append(stat)
        df_stats = pd.DataFrame.from_dict(all_player_stats_dict, orient="columns")
        return df_stats

    def team_name_from_table_header(self, player_stats_soup: bs4.element.Tag):
        """
        Reads the team name from the stats table, to double check against the team name from the fixtures df
        Parameters
        ----------
        player_stats_soup: bs4.element.Tag
            bs4 representation of the player stats table

        Returns
        -------
        str
        """
        team_name = player_stats_soup.find("h2").text.split("Player")[0].strip()
        return team_name

    def add_meta_info_to_stats_df(self, df_stats: pd.DataFrame, meta_info_dict: dict):
        """
        Adds the meta info from the fixtures df to the player stats, so they can be identified by season,
        gameday etc.

        Parameters
        ----------
        df_stats: pd.DataFrame
        meta_info_dict: dict

        Returns
        -------
        pd.DataFrame
            Df with the added info
        """
        for col, value in meta_info_dict.items():
            df_stats.loc[:, col] = value
        return df_stats

    def stats_tables_from_report(
        self, match_report_html: bs4.BeautifulSoup, player_or_keeper: str
    ):
        """
        Splits the match report into the home/away stats and headers
        Parameters
        ----------
        match_report_html: bs4.BeautifulSoup
        player_or_keeper: str
            indication if the player or keeper stats should be read

        Returns
        -------
        """
        stats_tables = match_report_html.find_all(
            "div", attrs={"id": re.compile(f"all_{player_or_keeper}_stats_[a-z0-9]")}
        )
        if len(stats_tables) < 1:
            raise ValueError(
                match_report_html.find("div", attrs={"id": "content", "class": "box"})
                .find("h1")
                .text
            )
        stats_tables_home = stats_tables[0]
        stats_tables_away = stats_tables[1]
        stats_headers = stats_tables_home.find_all("thead")
        return stats_tables_home, stats_tables_away, stats_headers

    def check_team_names_equal_report_and_meta_info_dict(
        self,
        meta_info_dict: dict,
        player_stats_table_home: bs4.element.Tag,
        player_stats_table_away: bs4.element.Tag,
    ):
        """
        Raises ValueError if team names from the match report page and the passed names from the fixture df are not equal

        Parameters
        ----------
        meta_info_dict: dict
        player_stats_table_home: bs4.element.Tag
            bs4 representation of the home team's players stats
        player_stats_table_away: bs4.element.Tag
            bs4 representation of the home team's players stats

        Returns
        -------
        None
        """
        team_name_home = self.team_name_from_table_header(player_stats_table_home)
        team_name_away = self.team_name_from_table_header(player_stats_table_away)
        if (
            team_name_home != meta_info_dict["home_team"]
            or team_name_away != meta_info_dict["away_team"]
        ):
            raise ValueError(
                "Team names in match report and meta info dict are not equal"
            )

    def keeper_stats_to_df(
        self, match_report_html: bs4.BeautifulSoup, meta_info_dict: dict
    ):
        """
        Reads the stats for the keeper(s) into a df

        Parameters
        ----------
        match_report_html
        meta_info_dict

        Returns
        -------

        """
        (
            keeper_stats_table_home,
            keeper_stats_table_away,
            keeper_headers,
        ) = self.stats_tables_from_report(match_report_html, player_or_keeper="keeper")
        df_keeper_home = self.df_from_single_fbref_table_sheet(keeper_stats_table_home)
        df_keeper_away = self.df_from_single_fbref_table_sheet(keeper_stats_table_away)
        df_keeper_stats = pd.concat([df_keeper_home, df_keeper_away])
        df_keeper_stats = self.add_meta_info_to_stats_df(
            df_keeper_stats, meta_info_dict
        )
        return df_keeper_stats

    def player_stats_to_df(
        self, match_report_html: bs4.BeautifulSoup, meta_info_dict: dict
    ):
        """
        Reads all the player stats from a single match report into a df

        Parameters
        ----------
        match_report_html
        meta_info_dict

        Returns
        -------

        """
        (
            player_stats_table_home,
            player_stats_table_away,
            player_stats_headers,
        ) = self.stats_tables_from_report(match_report_html, player_or_keeper="player")
        self.check_team_names_equal_report_and_meta_info_dict(
            meta_info_dict, player_stats_table_home, player_stats_table_away
        )
        player_stats_sheets_home = player_stats_table_home.find_all("tbody")
        player_stats_sheets_away = player_stats_table_away.find_all("tbody")
        df_home = self.read_all_table_sheets_into_one_df(
            player_stats_sheets_home, player_stats_headers, meta_info_dict["home_team"]
        )
        df_away = self.read_all_table_sheets_into_one_df(
            player_stats_sheets_away, player_stats_headers, meta_info_dict["away_team"]
        )
        df_all_players = pd.concat([df_home, df_away])
        df_player_stats = self.add_meta_info_to_stats_df(df_all_players, meta_info_dict)
        return df_player_stats

    def scrape_lineups_to_df(self, match_report_html, meta_info_dict):
        """
        Reads the team lineups into a df from a match report

        Parameters
        ----------
        match_report_html
        meta_info_dict

        Returns
        -------

        """
        player_table_rows_home = match_report_html.find(
            "div", attrs={"class": "lineup", "id": "a"}
        ).find_all("tr")
        player_table_rows_away = match_report_html.find(
            "div", attrs={"class": "lineup", "id": "b"}
        ).find_all("tr")
        starting_lineup_home, bench_lineup_home = self.read_lineup_table_to_lists(
            player_table_rows_home
        )
        starting_lineup_away, bench_lineup_away = self.read_lineup_table_to_lists(
            player_table_rows_away
        )
        lineup_dict = {
            "starting_lineup_home": [starting_lineup_home],
            "starting_lineup_away": [starting_lineup_away],
            "bench_lineup_home": [bench_lineup_home],
            "bench_lineup_away": [bench_lineup_away],
        }
        lineup_dict = lineup_dict | meta_info_dict  # | is dict merge operator
        df_lineups = pd.DataFrame.from_dict(lineup_dict, orient="columns")
        return df_lineups

    def read_lineup_table_to_lists(
        self, player_table_rows: bs4.element.Tag
    ) -> (list[str], list[str]):
        """
        Puts all players in list depending if they started or are subs

        Parameters
        ----------
        player_table_rows

        Returns
        -------

        """
        starting_lineup, bench_lineup = [], []
        for idx in range(len(player_table_rows)):
            if idx == 0 or idx == 12:
                continue
            elif 0 < idx <= 11:
                player_info = player_table_rows[idx].find_all("td")
                jersey_nr, player_name = (
                    player_info[0].text,
                    player_info[1].text.strip().lower(),
                )
                starting_lineup.append((jersey_nr, player_name))
            else:
                player_info = player_table_rows[idx].find_all("td")
                jersey_nr, player_name = (
                    player_info[0].text,
                    player_info[1].text.strip().lower(),
                )
                bench_lineup.append((jersey_nr, player_name))
        return starting_lineup, bench_lineup

    def match_reports_to_dfs(self, path_to_fixtures_csv: str):
        """
        Reads all
        Parameters
        ----------
        path_to_fixtures_csv

        Returns
        -------

        """
        df_matches = pd.read_csv(path_to_fixtures_csv)
        df_player_stats_all = pd.DataFrame()
        df_keeper_stats_all = pd.DataFrame()
        df_lineups = pd.DataFrame()
        website_accesses_without_pause = 0
        for idx, row in df_matches.iterrows():
            if "Historical" in row["match_report_url"]:
                break
            match_report_html = self.retrieve_bs4_html(row["match_report_url"])
            website_accesses_without_pause += 1
            meta_info_dict = row[
                [
                    "gameweek",
                    "dayofweek",
                    "date",
                    "start_time",
                    "season",
                    "home_team",
                    "away_team",
                ]
            ].to_dict()
            df_player_stats, df_keeper_stats = self.match_report_to_stats_df(
                match_report_html, meta_info_dict
            )
            df_player_stats_all = pd.concat([df_player_stats_all, df_player_stats])
            df_keeper_stats_all = pd.concat([df_keeper_stats_all, df_keeper_stats])
            df_lineup = self.scrape_lineups_to_df(match_report_html, meta_info_dict)
            df_lineups = pd.concat([df_lineups, df_lineup])
            if website_accesses_without_pause > 20:
                time.sleep(60)
                website_accesses_without_pause = 0
            if int(idx) % 50 == 0:
                print(f"scraped {idx}/{len(df_matches)}")
        return df_player_stats_all, df_keeper_stats_all, df_lineups

    def match_reports_to_csv(
        self,
    ):
        """
        Reads all match reports from the fixtures df and saves them in seperate files for player stats, keeper stats,
        and lineups

        Returns
        -------

        """
        path_to_fixtures_csv = os.path.join(
            DATA_DIR_PATH,
            f"{LEAGUE_MAPPING[self.league_name]}/fbref/fixtures_{self.season_start_year}_{self.season_end_year}.csv",
        )
        df_player_stats, df_keeper_stats, df_lineups = self.match_reports_to_dfs(
            path_to_fixtures_csv
        )
        df_player_stats.to_csv(
            os.path.join(
                DATA_DIR_PATH,
                f"{LEAGUE_MAPPING[self.league_name]}/fbref/player_stats_{self.season_start_year}_{self.season_end_year}.csv",
            ),
            index=False,
        )
        df_keeper_stats.to_csv(
            os.path.join(
                DATA_DIR_PATH,
                f"{LEAGUE_MAPPING[self.league_name]}/fbref/keeper_stats_{self.season_start_year}_{self.season_end_year}.csv",
            ),
            index=False,
        )
        df_lineups.to_csv(
            os.path.join(
                DATA_DIR_PATH,
                f"{LEAGUE_MAPPING[self.league_name]}/fbref/lineups_{self.season_start_year}_{self.season_end_year}.csv",
            ),
            index=False,
        )

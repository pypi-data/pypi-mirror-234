import pandas as pd
from fbref_scraper.FBRef_scraper import FBRefScraper
import bs4
from website_texts import (
    keeper_stats,
    fixtures_21_22_buli,
    match_report_sge_fcb_22_23,
)


def test_scrape_fixtures_to_df(mocker):
    fb = FBRefScraper(2021, 2022, "Bundesliga")
    return_value = bs4.BeautifulSoup(fixtures_21_22_buli, features="html.parser")
    mocker.patch.object(fb, "retrieve_bs4_html", return_value=return_value)
    df_fixtures = fb.scrape_fixtures_to_df(save_as_csv=False)
    assert len(df_fixtures) == 306
    assert df_fixtures[df_fixtures.date == "2022-03-18"].values.tolist() == [
        [
            "Fri",
            "2022-03-18",
            "20:30",
            "Bochum",
            pd.NA,
            "0–2",
            pd.NA,
            "M'Gladbach",
            pd.NA,
            "Vonovia Ruhrstadion",
            "Benjamin Cortus",
            "https://fbref.com//en/matches/c34bbc21/Bochum-Monchengladbach-March-18-2022-Bundesliga",
            "27",
            "2021-2022",
        ]
    ]


def test_read_lineup_from_match_report(mocker):
    fb = FBRefScraper(2022, 2022, "Bundesliga")
    match_report_html = bs4.BeautifulSoup(
        match_report_sge_fcb_22_23, features="html.parser"
    )
    df_lineups = fb.scrape_lineups_to_df(match_report_html, {})
    df_exp = pd.DataFrame.from_dict(
        {
            "starting_lineup_home": [
                [
                    ("1", "kevin trapp"),
                    ("2", "obite n'dicka"),
                    ("8", "djibril sow"),
                    ("10", "filip kostić"),
                    ("17", "sebastian rode"),
                    ("18", "almamy touré"),
                    ("19", "rafael borré"),
                    ("27", "mario götze"),
                    ("29", "jesper lindstrøm"),
                    ("35", "tuta"),
                    ("36", "ansgar knauff"),
                ]
            ],
            "starting_lineup_away": [
                [
                    ("1", "manuel neuer"),
                    ("2", "dayot upamecano"),
                    ("5", "benjamin pavard"),
                    ("6", "joshua kimmich"),
                    ("7", "serge gnabry"),
                    ("17", "sadio mané"),
                    ("18", "marcel sabitzer"),
                    ("19", "alphonso davies"),
                    ("21", "lucas hernández"),
                    ("25", "thomas müller"),
                    ("42", "jamal musiala"),
                ]
            ],
            "bench_lineup_home": [
                [
                    ("40", "diant ramaj"),
                    ("6", "kristijan jakić"),
                    ("9", "randal kolo muani"),
                    ("11", "faride alidou"),
                    ("15", "daichi kamada"),
                    ("20", "makoto hasebe"),
                    ("21", "lucas alario"),
                    ("22", "timothy chandler"),
                    ("25", "christopher lenz"),
                ]
            ],
            "bench_lineup_away": [
                [
                    ("26", "sven ulreich"),
                    ("4", "matthijs de ligt"),
                    ("10", "leroy sané"),
                    ("23", "tanguy nianzou"),
                    ("32", "joshua zirkzee"),
                    ("38", "ryan gravenberch"),
                    ("39", "mathys tel"),
                    ("40", "noussair mazraoui"),
                    ("44", "josip stanišić"),
                ]
            ],
        },
        orient="columns",
    )
    assert df_lineups.equals(df_exp)


def test_empty_stat_cell_read_as_na():
    keeper_stats_table_away = bs4.BeautifulSoup(keeper_stats, "html.parser")
    fb = FBRefScraper(2022, 2023, "Bundesliga")
    df = fb.df_from_single_fbref_table_sheet(keeper_stats_table_away)
    assert pd.isna(df.loc[0, "gk_avg_distance_def_actions"])

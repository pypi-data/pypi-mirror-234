# SPDX-FileCopyrightText: 2023-present Tim Cuddeback <cuddebtj@gmail.com>
#
# SPDX-License-Identifier: MIT
import datetime
import logging
from collections import ChainMap
from copy import deepcopy
from pathlib import Path

import polars as pl
from polars import DataFrame

logger = logging.NullHandler()

data_type = dict | ChainMap | list


def mkdir_not_exists(dir_name: str | Path) -> None:
    cwd_path = Path.cwd()
    check_dir = cwd_path / dir_name
    check_dir.mkdir(parents=True, exist_ok=True)


def write_parquet_file(df: DataFrame, file_path: str | Path) -> None:
    file_path = Path(file_path) if isinstance(file_path, str) else file_path
    mkdir_not_exists(file_path.parent)
    df.write_parquet(file_path, use_pyarrow=True, compression="snappy")


class YahooParseBase:
    def __init__(self, response: dict, data_key_list: list[str], season: int) -> None:
        self.response = response.get("fantasy_content", response)
        self.query_data = self._parse_data(response.get("fantasy_content", response), data_key_list)
        self.data_cache_path = str((Path.cwd() / "data_cache").as_posix())
        self.season = season

    def _unnest(self, parse_obj: data_type) -> data_type:
        if parse_obj == 0 or parse_obj:
            if isinstance(parse_obj, list):
                parse_obj = [obj for obj in parse_obj if (obj == 0 or obj)]

                if len(parse_obj) == 1:
                    return self._unnest(parse_obj[0])

                elif any(isinstance(obj, dict) for obj in parse_obj):
                    return self._flatten(parse_obj)

                else:
                    return [self._unnest(obj) for obj in parse_obj if (obj == 0 or obj)]

            elif isinstance(parse_obj, dict):
                if "0" in parse_obj.keys() and "1" not in parse_obj.keys() and len(parse_obj.keys()) == 1:
                    return self._unnest(parse_obj.get("0"))

                elif isinstance(parse_obj.get("0"), dict):
                    parse_obj.update(parse_obj.pop("0"))

                if "count" in parse_obj.keys() and "position" in parse_obj.keys():
                    temp_dict = {}
                    for k, v in parse_obj.items():
                        if k != "count":
                            temp_dict.update({k: self._unnest(v)})
                    return temp_dict

                else:
                    parse_obj = {k: self._unnest(v) for k, v in parse_obj.items() if k != "count"}

                    if "0" in parse_obj.keys() and "1" in parse_obj.keys():
                        parse_obj = self._to_list(parse_obj)

                    return parse_obj
            else:
                return parse_obj

    def _flatten(self, parse_obj: data_type) -> data_type:
        parse_obj = [obj for obj in parse_obj if (obj == 0 or obj)]
        item_keys = []
        ndx = 0
        for item in parse_obj:
            if isinstance(item, list):
                flattened_item = self._flatten(item)
                parse_obj[ndx] = flattened_item
                item_keys.extend(list(flattened_item.keys()))
            else:
                item_keys.extend(list(item.keys()))
            ndx += 1

        if len(item_keys) == len(set(item_keys)):
            agg_dict = {}
            for dict_item in parse_obj:
                agg_dict.update(dict_item)

            return self._unnest(agg_dict)
        else:
            return [self._unnest(obj) for obj in parse_obj if (obj == 0 or obj)]

    def _to_list(self, parse_obj):
        if isinstance(parse_obj, dict):
            out = []
            for v in parse_obj.values():
                out.append(v)
            return out
        else:
            return parse_obj

    def _format_list(self, parse_obj: data_type) -> data_type:
        if isinstance(parse_obj[0], list):
            if len(parse_obj) > 1:
                temp_list = [self._format_list(item) if isinstance(item, list) else item for item in parse_obj]
                return self._format_list(temp_list)
            else:
                temp_list = parse_obj[0]
                return self._format_list(temp_list)
        else:
            temp_chainmap = ChainMap(*[value for value in parse_obj if (value == 0 or value)])
            return temp_chainmap

    def _json_handler(self, parse_obj: data_type) -> str:
        if hasattr(parse_obj, "serialized"):
            return parse_obj.serialized()
        else:
            return str(parse_obj, "utf-8")

    def _parse_data(self, response, data_key_list):
        for i in range(len(data_key_list)):
            if isinstance(response, list):
                if isinstance(data_key_list[i], list):
                    reformatted = self._format_list(response)
                    response = [
                        {data_key_list[i][0]: reformatted[data_key_list[i][0]]},
                        {data_key_list[i][1]: reformatted[data_key_list[i][1]]},
                    ]
                else:
                    response = self._format_list(response)[data_key_list[i]]

            elif isinstance(data_key_list[i], list):
                response = [
                    {data_key_list[i][0]: response[data_key_list[i][0]]},
                    {data_key_list[i][1]: response[data_key_list[i][1]]},
                ]
            else:
                response = response.get(data_key_list[i])

        query_data = self._unnest(response)

        return query_data


class GameParser(YahooParseBase):
    def __init__(
        self,
        response: data_type,
        query_timestamp: str | datetime.datetime,
        season: int,
        game_key: str | None = None,
        data_key_list: list[str] | None = None,
    ) -> None:
        """Parse the Yahoo Fantasy API game data from get_all_game_keys and get_game.

        Args:
            response (data_type): _description_
            query_timestamp (str | datetime.datetime): _description_
            season (int): Current NFL season or season of game_key.
            game_key (str | None, optional): Used for get_game. Defaults to None.
            data_key_list (list[str] | None, optional): ["games"] for get_all_game_keys and ["game"] for get_game. Defaults to None.
        """  # noqa: E501
        super().__init__(response, ["game"] if not data_key_list else data_key_list, season=season)
        self.query_timestamp = query_timestamp
        self.game_key_file = game_key if game_key else None

        if data_key_list == ["games"]:
            resp = [val.get("game", val) for key, val in self.query_data.items() if key != "count"]
            resp = sorted(resp, key=lambda x: len(x.values()), reverse=True)

        else:
            resp = deepcopy(self.query_data)

        self.game_resp_data = resp[0] if len(resp) == 1 else resp

    def game_key_df(self) -> pl.DataFrame:
        """Used for get_all_game_keys returns parsed out table of game_keys.

        Endpoints:
        - get_all_game_keys

        Returns:
            pl.DataFrame: Polars dataframe of game_keys and metadata.
        """
        data = sorted(self.game_resp_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in data)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(self.data_cache_path + "/parq/" + f"all_keys_{self.query_timestamp}.parquet")
        write_parquet_file(df, parq_file)

        return df

    def game_df(self) -> pl.DataFrame:
        """Metadata from get_game endpoint.

        Endpoints:
        - get_game

        Returns:
            pl.DataFrame: _description_
        """
        data = {
            key: val
            for key, val in self.game_resp_data.items()
            if key not in ["game_weeks", "stat_categories", "position_types", "roster_positions"]
        }

        self.game_key = pl.lit(data.get("game_key")).alias("game_key")

        df = pl.from_dict(data)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/game_{self.game_key_file}_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def game_week_df(self) -> pl.DataFrame:
        """NFL weeks data from get_game endpoint.

        Endpoints:
        - get_game

        Returns:
            pl.DataFrame: _description_
        """
        data = [val.get("game_week", val) for key, val in self.game_resp_data.get("game_weeks").items()]
        data = sorted(data, key=lambda x: len(x.values()), reverse=True)

        df = pl.from_dicts(d for d in data).with_columns(self.game_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/game_{self.game_key_file}_game_weeks_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def game_stat_categories_df(self) -> pl.DataFrame:
        """NFL stat categories data from get_game endpoint.

        Endpoints:
        - get_game

        Returns:
            pl.DataFrame: _description_
        """
        data = [d.get("stat", d) for d in self.game_resp_data.get("stat_categories").get("stats")]

        sub_data = []
        for d in data:
            sd = (
                [d.get("position_types").get("position_type")]
                if isinstance(d.get("position_types"), dict)
                else [z.get("position_type") for z in d.get("position_types")]
            )
            d["position_types"] = sd

            sub_data.append(d)

        sub_data = sorted(sub_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in sub_data).with_columns(self.game_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/game_{self.game_key_file}_stat_categories_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def game_position_type_df(self) -> pl.DataFrame:
        """NFL position types data from get_game endpoint.

        Endpoints:
        - get_game

        Returns:
            pl.DataFrame: _description_
        """
        data = [d.get("position_type", d) for d in self.game_resp_data.get("position_types")]
        data = sorted(data, key=lambda x: len(x.values()), reverse=True)

        df = pl.from_dicts(d for d in data).with_columns(self.game_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/game_{self.game_key_file}_position_types_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def game_roster_positions_df(self) -> pl.DataFrame:
        """NFL roster positions data from get_game endpoint.

        Endpoints:
        - get_game

        Returns:
            pl.DataFrame: _description_
        """
        data = [d.get("roster_position", d) for d in self.game_resp_data.get("roster_positions")]
        data = sorted(data, key=lambda x: len(x.values()), reverse=True)

        df = pl.from_dicts(d for d in data).with_columns(self.game_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/game_{self.game_key_file}_roster_positions_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df


class LeagueParser(YahooParseBase):
    def __init__(
        self,
        response: str,
        query_timestamp: str | datetime.datetime,
        season: int,
        league_key: str,
        end_point: str,
        week: str = "",
    ) -> None:
        """Parse league data from Yahoo Fantasy API.

        Args:
            response (str): _description_
            query_timestamp (str | datetime.datetime): _description_
            league_key (str): _description_
        """
        super().__init__(response, ["league"], season=season)

        self.league_key_file = league_key
        self.week = week
        self.query_timestamp = query_timestamp
        self.end_point = end_point

        # resp = [val.get("league", val) for key, val in self.query_data.items() if key != "count"]
        # data = sorted(resp, key=lambda x: len(x.values()), reverse=True)
        data = deepcopy(self.query_data)

        self.league_resp_data = data[0] if len(data) == 1 else data

    def league_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_draft_result
        - get_league_matchup
        - get_league_transaction
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        data = {
            key: val
            for key, val in self.league_resp_data.items()
            if key not in ["draft_results", "teams", "scoreboard", "transactions", "settings"]
        }

        self.league_key = pl.lit(data.get("league_key")).alias("league_key")

        df = pl.from_dict(data)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def draft_results_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_draft_result
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        data = [val.get("draft_result", val) for val in self.league_resp_data.get("draft_results").values()]
        data = sorted(data, key=lambda x: len(x.values()), reverse=True)

        df = pl.from_dicts(data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_draft_results_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def team_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_draft_result
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        data = [val.get("team", val) for val in self.league_resp_data.get("teams").values()]

        sub_data = []
        for d in data:
            t = (
                [d.get("team_logos").get("team_logo")]
                if isinstance(d.get("team_logos"), dict)
                else [logo.get("team_logo") for logo in d.get("team_logos")]
            )
            d["team_logo_url"] = t[0].get("url")

            z = d.get("roster_adds").get("value")
            d["roster_adds"] = z

            y = (
                [d.get("managers").get("manager")]
                if isinstance(d.get("managers"), dict)
                else [mngr.get("manager") for mngr in d.get("managers")]
            )

            d["manager_1_id"] = y[0].get("manager_id")
            d["manager_1_guid"] = y[0].get("guid")
            d["manager_1_name"] = y[0].get("nickname")
            d["manager_1_felo_score"] = y[0].get("felo_score")
            d["manager_1_felo_tier"] = y[0].get("felo_tier")

            if len(y) >= 2:  # noqa: PLR2004
                d["manager_2_id"] = y[1].get("manager_id")
                d["manager_2_guid"] = y[1].get("guid")
                d["manager_2_name"] = y[1].get("nickname")
                d["manager_2_felo_score"] = y[1].get("felo_score")
                d["manager_2_felo_tier"] = y[1].get("felo_tier")

            del d["managers"], d["team_logos"]

            sub_data.append(d)

        sub_data = sorted(sub_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in sub_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_teams_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def matchup_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_matchup

        Returns:
            pl.DataFrame: _description_
        """
        data = [d.get("matchup", d) for d in self.league_resp_data.get("scoreboard").get("matchups").values()]

        sub_data = []
        for d in data:
            t = [tm.get("team", tm) for tm in d.get("teams").values()]
            mu_grade = (
                [mug.get("matchup_grade", mug) for mug in d.get("matchup_grades")]
                if d.get("matchup_grades")
                else [{}, {}]
            )

            matchup = {
                "week": d.get("week"),
                "week_start": d.get("week_start"),
                "week_end": d.get("week_end"),
                "status": d.get("status"),
                "is_playoffs": d.get("is_playoffs"),
                "is_consolation": d.get("is_consolation"),
                "is_matchup_recap_available": d.get("is_matchup_recap_available"),
                "matchup_recap_url": d.get("matchup_recap_url"),
                "matchup_recap_title": d.get("matchup_recap_title"),
                "is_tied": d.get("is_tied"),
                "winner_team_key": d.get("winner_team_key"),
                "team_1_key": t[0].get("team_key"),
                "team_1_win_probability": t[0].get("win_probability"),
                "team_1_projected_points": t[0].get("team_projected_points").get("total"),
                "team_1_points": t[0].get("team_points").get("total"),
                "team_2_key": t[1].get("team_key"),
                "team_2_win_probability": t[1].get("win_probability"),
                "team_2_projected_points": t[1].get("team_projected_points").get("total"),
                "team_2_points": t[1].get("team_points").get("total"),
                "matchup_grade_1_team_key": mu_grade[0].get("team_key", None),
                "matchup_grade_1_grade": mu_grade[0].get("grade", None),
                "matchup_grade_2_team_key": mu_grade[1].get("team_key", None),
                "matchup_grade_2_grade": mu_grade[1].get("grade", None),
            }

            sub_data.append(matchup)

        sub_data = sorted(sub_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in sub_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_matchups_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def transaction_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_transaction
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        data = [d.get("transaction", d) for d in self.league_resp_data.get("transactions").values()]

        sub_data = []
        for d in data:
            if d.get("players"):
                z = [p.get("player", p) for p in d.get("players").values() if isinstance(d.get("players"), dict)]

                for idx, player in enumerate(z):
                    d[f"player_key_{idx+1}"] = player.get("player_key")
                    d[f"player_type_{idx+1}"] = player.get("transaction_data").get("type")
                    d[f"player_source_type_{idx+1}"] = player.get("transaction_data").get("source_type")
                    d[f"player_destination_type_{idx+1}"] = player.get("transaction_data").get("destination_type")
                    d[f"player_destination_team_key_{idx+1}"] = player.get("transaction_data").get(
                        "destination_team_key"
                    )

                del d["players"]

                sub_data.append(d)

            else:
                continue

        sub_data = sorted(sub_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in sub_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_transactions_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def setting_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        setting_data = self.league_resp_data.get("settings")
        setting_data = {
            key: val
            for key, val in setting_data.items()
            if key not in ["stat_modifiers", "roster_positions", "stat_categories"]
        }

        df = pl.from_dict(setting_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_settings_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def roster_position_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        roster_position_data = self.league_resp_data.get("settings").get("roster_positions")
        roster_position_data = [d.get("roster_position", d) for d in roster_position_data]

        df = pl.from_dicts(rp for rp in roster_position_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_roster_positions_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def stat_category_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        stat_category_data = self.league_resp_data.get("settings").get("stat_categories").get("stats")
        stat_category_data = [d.get("stat", d) for d in stat_category_data]
        for stat in stat_category_data:
            try:
                del stat["stat_position_types"]
            except KeyError as key_err:
                logger.debug(key_err)
                continue

        df = pl.from_dicts(ss for ss in stat_category_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_stat_categories_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def stat_group_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        stat_group_data = self.league_resp_data.get("settings").get("stat_categories").get("groups")
        stat_group_data = [d.get("group", d) for d in stat_group_data]

        df = pl.from_dicts(sg for sg in stat_group_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_stat_groups_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def stat_modifier_df(self) -> pl.DataFrame:
        """NFL league data.

        Endpoints:
        - get_league_preseason
        - get_league_offseason

        Returns:
            pl.DataFrame: _description_
        """
        stat_modifier_data = self.league_resp_data.get("settings").get("stat_modifiers").get("stats")
        stat_modifier_data = [d.get("stat", d) for d in stat_modifier_data]

        df = pl.from_dicts(sm for sm in stat_modifier_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/league/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/league_{self.league_key_file}_stat_modifiers_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df


class TeamParser(YahooParseBase):
    def __init__(
        self,
        response: str,
        query_timestamp: str | datetime.datetime,
        season: int,
        week: str = "",
    ) -> None:
        """Parse team data from Yahoo Fantasy API.

        Args:
            response (str): _description_
            query_timestamp (str | datetime.datetime): _description_
            season (int): _description_
        """
        super().__init__(response, ["teams"], season=season)

        self.week = week
        self.query_timestamp = query_timestamp

        self.team_resp_data = [val.get("team", val) for key, val in self.query_data.items() if key != "count"]

    def team_df(self) -> pl.DataFrame:
        """Yahoo manager data.

        Endpoints:
        - get_roster

        Returns:
            pl.DataFrame: _description_
        """
        sub_data = []

        for d in deepcopy(self.team_resp_data):
            t = (
                [d.get("team_logos").get("team_logo")]
                if isinstance(d.get("team_logos"), dict)
                else [logo.get("team_logo") for logo in d.get("team_logos")]
            )
            d["team_logo_url"] = t[0].get("url")

            z = d.get("roster_adds").get("value")
            d["roster_adds"] = z

            y = (
                [d.get("managers").get("manager")]
                if isinstance(d.get("managers"), dict)
                else [mngr.get("manager") for mngr in d.get("managers")]
            )

            d["manager_1_id"] = y[0].get("manager_id")
            d["manager_1_guid"] = y[0].get("guid")
            d["manager_1_name"] = y[0].get("nickname")
            d["manager_1_felo_score"] = y[0].get("felo_score")
            d["manager_1_felo_tier"] = y[0].get("felo_tier")
            d["manager_2_id"] = None
            d["manager_2_guid"] = None
            d["manager_2_name"] = None
            d["manager_2_felo_score"] = None
            d["manager_2_felo_tier"] = None

            if len(y) >= 2:  # noqa: PLR2004
                d["manager_2_id"] = y[1].get("manager_id")
                d["manager_2_guid"] = y[1].get("guid")
                d["manager_2_name"] = y[1].get("nickname")
                d["manager_2_felo_score"] = y[1].get("felo_score")
                d["manager_2_felo_tier"] = y[1].get("felo_tier")

            d["week"] = d.get("roster").get("week")

            del d["managers"], d["team_logos"], d["roster"]

            sub_data.append(d)

        sub_data = sorted(sub_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in sub_data)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/team_rosters"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/teams_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def roster_df(self) -> pl.DataFrame:
        """Yahoo manager data.

        Endpoints:
        - get_roster

        Returns:
            pl.DataFrame: _description_
        """
        sub_data = []

        for r in deepcopy(self.team_resp_data):
            m = (
                [r.get("managers").get("manager")]
                if isinstance(r.get("managers"), dict)
                else [mngr.get("manager") for mngr in r.get("managers")]
            )

            r["manager_1_id"] = m[0].get("manager_id")
            r["manager_1_guid"] = m[0].get("guid")
            r["manager_1_name"] = m[0].get("nickname")
            r["manager_1_felo_score"] = m[0].get("felo_score")
            r["manager_1_felo_tier"] = m[0].get("felo_tier")

            if len(m) >= 2:  # noqa: PLR2004
                r["manager_2_id"] = m[1].get("manager_id")
                r["manager_2_guid"] = m[1].get("guid")
                r["manager_2_name"] = m[1].get("nickname")
                r["manager_2_felo_score"] = m[1].get("felo_score")
                r["manager_2_felo_tier"] = m[1].get("felo_tier")

            else:
                r["manager_2_id"] = None
                r["manager_2_guid"] = None
                r["manager_2_name"] = None
                r["manager_2_felo_score"] = None
                r["manager_2_felo_tier"] = None

            r["week"] = r.get("roster").get("week")

            players = [p.get("player", p) for p in r.get("roster").get("players").values()]

            for p in players:
                player_data = {
                    "team_key": r.get("team_key"),
                    "player_key": p.get("player_key"),
                    "week": r.get("week"),
                    "injury_note": p.get("injury_note", "None"),
                    "has_recent_player_notes": p.get("has_recent_player_notes", 0),
                    "has_player_notes": p.get("has_player_notes", 0),
                    "player_notes_last_timestamp": p.get("player_notes_last_timestamp", 0),
                    "uniform_number": p.get("uniform_number") if p.get("uniform_number") else "-1",
                    "editorial_team_key": p.get("editorial_team_key"),
                    "editorial_team_full_name": p.get("editorial_team_full_name"),
                    "editorial_team_abr": p.get("editorial_team_abr"),
                    "editorial_team_url": p.get("editorial_team_url"),
                    "bye_weeks": p.get("bye_weeks").get("week"),
                    "is_undroppable": p.get("is_undroppable"),
                    "position_type": p.get("position_type"),
                    "primary_position": p.get("primary_position"),
                    "selected_position_is_flex": p.get("selected_position").get("is_flex"),
                    "selected_position": p.get("selected_position").get("position"),
                    "eligible_positions": (
                        [p.get("eligible_positions").get("position")]
                        if isinstance(p.get("eligible_positions"), dict)
                        else [
                            z.get("position")
                            for z in p.get("eligible_positions")
                            if isinstance(p.get("eligible_positions"), list)
                        ]
                    ),
                }

                sub_data.append(player_data)

        sub_data = sorted(sub_data, key=lambda x: len(x.values()), reverse=True)
        df = pl.from_dicts(d for d in sub_data)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}/team_rosters"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/rosters_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df


class PlayerParser(YahooParseBase):
    def __init__(
        self,
        response: str,
        query_timestamp: str | datetime.datetime,
        league_key: str,
        season: int,
        start: str,
        end: str,
        end_point: str,
        week: str = "",
    ) -> None:
        """Parse player data from Yahoo Fantasy API.

        Args:
            response (str): _description_
            query_timestamp (str | datetime.datetime): _description_
            league_key (str): _description_
            season (int): _description_
            start (str): _description_
            end (str): _description_
            end_point (str): _description_
        """
        league_key = response.get("fantasy_content", response).get("league")[0].get("league_key")
        self.league_key = pl.lit(league_key).alias("league_key")
        response = response.get("fantasy_content", response).get("league")[1]
        super().__init__(response, ["players"], season=season)

        self.query_timestamp = query_timestamp
        self.league_key_file = league_key
        self.start = start
        self.end = end
        self.end_point = end_point
        self.week = week

        try:
            self.player_resp_data = [val.get("player", val) for key, val in self.query_data.items() if key != "count"]
        except AttributeError as e:
            logger.exception(f"AttributeError: {e}", backtrace=True, diagnose=True)
            self.player_resp_data = [
                {
                    "player_key": "",
                    "player_id": "",
                    "name": {"full": "", "first": "", "last": "", "ascii_first": "", "ascii_last": ""},
                    "url": "",
                    "editorial_player_key": "",
                    "editorial_team_key": "",
                    "editorial_team_full_name": "",
                    "editorial_team_abbr": "",
                    "editorial_team_url": "",
                    "bye_weeks": {"week": ""},
                    "is_keeper": {"status": None, "cost": None, "kept": None},
                    "uniform_number": "",
                    "display_position": "",
                    "headshot": {"url": "", "size": ""},
                    "image_url": "",
                    "is_undroppable": "",
                    "position_type": "",
                    "primary_position": "",
                    "eligible_positions": {"position": ""},
                }
            ]

    def player_df(self) -> pl.DataFrame:
        """Yahoo player data.

        Endpoints:
        - get_player
        - get_player_draft_analysis
        - get_player_stat
        - get_player_pct_owned

        Returns:
            pl.DataFrame: _description_
        """
        sub_data = []

        for p in deepcopy(self.player_resp_data):
            player_data = {
                "full_name": p.get("name").get("full"),
                "first_name": p.get("name").get("first"),
                "last_name": p.get("name").get("last") if p.get("name").get("last") else "DST",
                "first_ascii_name": p.get("name").get("ascii_first"),
                "last_ascii_name": p.get("name").get("ascii_last") if p.get("name").get("ascii_last") else "DST",
                "is_keeper_status": p.get("is_keeper").get("status"),
                "is_keeper_cost": p.get("is_keeper").get("cost"),
                "is_keeper_kept": p.get("is_keeper").get("kept"),
                "headshot_url": p.get("headshot").get("url"),
                "player_url": p.get("url"),
                "player_key": p.get("player_key"),
                "player_id": p.get("player_id"),
                "editorial_player_key": p.get("editorial_player_key"),
            }

            sub_data.append(player_data)

        df = pl.from_dicts(player for player in sub_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/players_{self.league_key_file}/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/players_{self.start}_{self.end}_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def draft_analysis_df(self) -> pl.DataFrame:
        """Yahoo player data.

        Endpoints:
        - get_player_draft_analysis

        Returns:
            pl.DataFrame: _description_
        """
        sub_data = []

        for p in deepcopy(self.player_resp_data):
            draft_analysis = {
                "player_key": p.get("player_key"),
                "average_pick": p.get("draft_analysis").get("average_pick"),
                "average_round": p.get("draft_analysis").get("average_pick"),
                "average_cost": p.get("draft_analysis").get("average_pick"),
                "percent_drafted": p.get("draft_analysis").get("average_pick"),
                "preseason_average_pick": p.get("draft_analysis").get("preseason_average_pick"),
                "preseason_average_round": p.get("draft_analysis").get("preseason_average_round"),
                "preseason_average_cost": p.get("draft_analysis").get("preseason_average_cost"),
                "preseason_percent_drafted": p.get("draft_analysis").get("preseason_percent_drafted"),
            }
            sub_data.append(draft_analysis)

        df = pl.from_dicts(da for da in sub_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/players_{self.league_key_file}/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/players_{self.start}_{self.end}_draft_analysis_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def stats_df(self) -> pl.DataFrame:
        """Yahoo player data.

        Endpoints:
        - get_player_stat

        Returns:
            pl.DataFrame: _description_
        """
        sub_data = []

        for p in deepcopy(self.player_resp_data):
            for s in p.get("player_stats").get("stats"):
                player_stat = {
                    "player_key": p.get("player_key"),
                    "stat_id": s.get("stat").get("stat_id"),
                    "stat_value": s.get("stat").get("value"),
                    "total_points": p.get("player_points").get("total"),
                    "week": p.get("player_stats").get("week"),
                }
                sub_data.append(player_stat)

        df = pl.from_dicts((da for da in sub_data), infer_schema_length=500).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/players_{self.league_key_file}/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/players_{self.start}_{self.end}_stats_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

    def pct_owned_meta_df(self) -> pl.DataFrame:
        """Yahoo player data.

        Endpoints:
        - get_player_pct_owned

        Returns:
            pl.DataFrame: _description_
        """
        sub_data = []

        for p in deepcopy(self.player_resp_data):
            pct_owned = {
                "player_key": p.get("player_key"),
                "full_name": p.get("name").get("full"),
                "first_name": p.get("name").get("first"),
                "last_name": p.get("name").get("last") if p.get("name").get("last") else "DST",
                "first_ascii_name": p.get("name").get("ascii_first"),
                "last_ascii_name": p.get("name").get("ascii_last") if p.get("name").get("ascii_last") else "DST",
                "is_keeper_status": p.get("is_keeper").get("status"),
                "is_keeper_cost": p.get("is_keeper").get("cost"),
                "is_keeper_kept": p.get("is_keeper").get("kept"),
                "headshot_url": p.get("headshot").get("url"),
                "player_url": p.get("url"),
                "player_id": p.get("player_id"),
                "editorial_player_key": p.get("editorial_player_key"),
                "week": p.get("percent_owned").get("week"),
                "percent_owned_value": p.get("percent_owned").get("value"),
                "percent_owned_delta": p.get("percent_owned").get("delta"),
                "injury_note": p.get("injury_note", "None"),
                "has_recent_player_notes": p.get("has_recent_player_notes", 0),
                "has_player_notes": p.get("has_player_notes", 0),
                "player_notes_last_timestamp": p.get("player_notes_last_timestamp", 0),
                "uniform_number": p.get("uniform_number") if p.get("uniform_number") else "-1",
                "editorial_team_key": p.get("editorial_team_key"),
                "editorial_team_full_name": p.get("editorial_team_full_name"),
                "editorial_team_abr": p.get("editorial_team_abr"),
                "editorial_team_url": p.get("editorial_team_url"),
                "bye_weeks": p.get("bye_weeks").get("week"),
                "is_undroppable": p.get("is_undroppable"),
                "position_type": p.get("position_type"),
                "primary_position": p.get("primary_position"),
                "eligible_positions": (
                    [p.get("eligible_positions").get("position")]
                    if isinstance(p.get("eligible_positions"), dict)
                    else [
                        z.get("position")
                        for z in p.get("eligible_positions")
                        if isinstance(p.get("eligible_positions"), list)
                    ]
                ),
            }
            sub_data.append(pct_owned)

        df = pl.from_dicts(da for da in sub_data).with_columns(self.league_key)
        cols = sorted(df.columns)
        df = df.select(cols)
        parq_file = Path(
            self.data_cache_path
            + "/parq/"
            + f"{self.season!s}"
            + f"/players_{self.league_key_file}/{self.end_point}"
            + f"{'/week_' + self.week if self.week != '' else ''}"
            + f"/players_{self.start}_{self.end}_pct_owned_{self.query_timestamp}.parquet"
        )
        write_parquet_file(df, parq_file)

        return df

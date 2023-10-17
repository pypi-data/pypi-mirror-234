import json
from typing import Optional, List, Any
import requests
from datetime import date, timedelta, datetime
from dateutil import parser
import re
import os
import time

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def upsert_dataset_dates(
        schema_name,
        table_name,
        last_update,
        start_period,
        end_period,
        **kwargs: Any,
):
    dt_last_update = parser.parse(last_update)
    last_update_date_format = '%Y-%m-%dT%H:%M:%S'

    # Some tables, like dictionaries, don't have start and end periods.
    if {start_period, end_period} == {""}:
        dt_start_period, dt_end_period = start_period, end_period
    else:
        # Parse into date
        dt_start_period = parser.parse(start_period)
        dt_end_period = parser.parse(end_period)

        # Reformat the date into the Directus accepted format
        period_date_format = '%d-%m-%Y'
        dt_start_period = dt_start_period.strftime(period_date_format)
        dt_end_period = dt_end_period.strftime(period_date_format)

    data = f"""{{ 
                last_update: "{dt_last_update.strftime(last_update_date_format)}",
                start_period: "{dt_start_period}",
                end_period: "{dt_end_period}",
                table_owner: "{os.getenv('REDSHIFT_USER')}"
            }}"""

    do = DirectusOperator()
    json_dataset = do.get_dataset_items_id(lst_tables=[table_name])

    if len(json_dataset["data"]["Dataset"]) > 0:
        print("Table already exists in Directus. Updating last_update, start_period and end_period...")
        dataset_id = json_dataset["data"]["Dataset"][0]["id"]
        do.update_dataset_items(ids=[dataset_id], data=data)
        print("✅ Dataset updated successfully!")
    else:
        print("Table doesn't exist yet in Directus. Creating table in Directus and setting "
              "last_update, start_period and end_period...")
        status = kwargs.get("status", "draft")
        nickname = kwargs.get("nickname", "")
        do.create_dataset(
            status=status,
            nickname=nickname,
            schema_name=schema_name,
            table_name=table_name,
            last_update=dt_last_update.strftime(last_update_date_format),
            start_period=dt_start_period,
            end_period=dt_end_period,
            table_owner=os.getenv('REDSHIFT_USER'))
        print("✅ Dataset created successfully!")


class DirectusOperator:
    def __init__(self) -> None:
        self.directus_token = os.environ.get('DIRECTUS_TOKEN')
        self.directus_endpoint = os.environ.get('DIRECTUS_API_URL')
        self.headers = {'Content-Type': 'application/json', "Authorization": f"Bearer {self.directus_token}"}

    def post_request(self, query):
        resp = requests.post(f"{self.directus_endpoint}/graphql", json={'query': query}, headers=self.headers)
        if resp.status_code != 200 or '{"errors":[' in resp.text:
            raise SyntaxError(json.dumps(json.loads(resp.text), indent=4))

        return json.loads(resp.text)

    def update_dataset_items(self, ids: List, data: str):
        query_update_item = f"""mutation {{
                                    update_Dataset_items(ids: {json.dumps(ids)}, 
                                    data: {data}) {{
                                        id
                                    }}
                                }}
                                """
        self.post_request(query=query_update_item)

    def get_dataset_items_id(
            self,
            lst_status: Optional[List] = None,
            lst_tables: Optional[List] = None,
            updated_yesterday: bool = True
    ):
        if lst_status is None:
            lst_status = ['Verified']
        query_filter = self.define_filter(lst_status=lst_status, lst_tables=lst_tables,
                                          updated_yesterday=updated_yesterday)
        query = f"""query {{
                        Dataset (
                            limit: -1,
                            {query_filter}
                            ) {{
                            id
                            status
                            table_name
                            schema_name
                        }}
                    }}"""
        resp = self.post_request(query=query)
        return resp

    def get_dataset_items(
            self,
            lst_status: Optional[List] = None,
            lst_tables: Optional[List] = None,
            updated_yesterday: bool = True
    ):
        if lst_status is None:
            lst_status = ['Verified']
        query_filter = self.define_filter(lst_status=lst_status, lst_tables=lst_tables,
                                          updated_yesterday=updated_yesterday)
        query = f"""query {{
                        Dataset (
                            limit: -1,
                            {query_filter}
                            ) {{
                            id
                            status
                            user_created {{
                                email
                            }}
                            date_created
                            user_updated {{
                                email
                            }}
                            date_updated
                            nickname
                            detailed_description
                            table_name
                            schema_name
                            location
                            short_description
                            geographical_scope
                            table_type
                            data_coverage
                            geographical_granularity
                            time_granularity
                            update_frequency
                            last_update
                            last_update_func {{
                                day,
                                month,
                                weekday,
                                year,
                            }} 
                            start_period
                            end_period
                            caveats
                            additional_info
                            update_process
                            import_format
                            import_separator
                            data_cov_pctg
                            data_topics_and_metrics
                            table_owner
                            applications_list{{
                                Oip_Application_app_uuid {{
                                    app_uuid
                                    app_name
                                    app_description
                                    app_link
                                }}
                            }}
                            sources_list {{ 
                                Source_source_uuid {{
                                    source_uuid
                                    source_name
                                    source_description
                                    source_link
                                }}
                            }}
                            Columns {{
                                column_id
                                label
                                order
                            }}
                            business_keywords
                        }}
                    }}"""

        self.post_request(query=query)

    def define_filter(
            self,
            lst_status: Optional[List] = None,
            lst_tables: Optional[List] = None,
            updated_yesterday: bool = True
    ):
        date_yesterday = date.today() - timedelta(1)

        lst_tables_filter = ', '.join(
            [f"""{{table_name: {{_eq: "{table}"}}}}""" for table in lst_tables]) + ',' if lst_tables else ''

        date_filter = ""
        status_filter = ""
        if not lst_tables_filter:
            if lst_status is None:
                lst_status = ['Verified']
            status_filter = ', '.join([f"""{{status: {{_eq: "{st}"}}}}""" for st in lst_status]) + ','
            if updated_yesterday:
                date_filter = f"""{{
                                    date_created_func: {{
                                        day: {{_eq: "{date_yesterday.day}"}},
                                        month: {{_eq: "{date_yesterday.month}"}},
                                        year: {{_eq: "{date_yesterday.year}"}}
                                        }}
                                    }},
                                    {{
                                    date_updated_func: {{
                                        day: {{_eq: "{date_yesterday.day}"}},
                                        month: {{_eq: "{date_yesterday.month}"}},
                                        year: {{_eq: "{date_yesterday.year}"}}
                                        }}
                                    }}"""

        query_filter = f"""filter:{{
                                _and:[ 
                                    {{_or: [
                                        {status_filter}
                                    ]}}
                                    {{_or: [
                                        {lst_tables_filter}
                                        {date_filter}
                                    ]}}
                                ]
                            }}"""
        return query_filter

    def create_dataset(
            self,
            schema_name,
            table_name,
            last_update,
            start_period,
            end_period,
            table_owner,
            status,
            nickname: Optional[str] = None
    ):
        query = f"""mutation {{
        create_Dataset_items(
                data: {{ 
                    nickname: "{str(nickname or '')}"
                    status: "{status}",
                    table_name: "{table_name}",
                    schema_name: "{schema_name}",
                    last_update: "{last_update}",
                    start_period: "{start_period}",
                    end_period: "{end_period}",
                    table_owner: "{table_owner}"
                    }}) {{  
                id
                schema_name,
                table_name,
                status
                }}
        }}"""

        self.post_request(query=query)

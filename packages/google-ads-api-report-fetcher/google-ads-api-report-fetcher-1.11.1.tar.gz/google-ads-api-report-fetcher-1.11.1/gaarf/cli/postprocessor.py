# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse
from concurrent import futures
import logging
from rich.logging import RichHandler
import sqlalchemy

from gaarf.io import reader  # type: ignore
from .utils import (GaarfBqConfigBuilder, GaarfSqlConfigBuilder,
                    GaarfBqConfigException, GaarfSqlConfigException,
                    ConfigSaver, initialize_runtime_parameters)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="+")
    parser.add_argument("-c", "--config", dest="gaarf_config", default=None)
    parser.add_argument("--conn",
                        "--connection-string",
                        dest="connection_string",
                        default=None)
    parser.add_argument("--project", dest="project", default=None)
    parser.add_argument("--dataset-location",
                        dest="dataset_location",
                        default=None)
    parser.add_argument("--save-config",
                        dest="save_config",
                        action="store_true")
    parser.add_argument("--no-save-config",
                        dest="save_config",
                        action="store_false")
    parser.add_argument("--config-destination",
                        dest="save_config_dest",
                        default="config.yaml")
    parser.add_argument("--log", "--loglevel", dest="loglevel", default="info")
    parser.add_argument("--logger", dest="logger", default="local")
    parser.add_argument("--dry-run", dest="dry_run", action="store_true")
    parser.set_defaults(save_config=False)
    parser.set_defaults(dry_run=False)
    args = parser.parse_known_args()
    main_args = args[0]

    logger = init_logging(main_args.logger)
    try:
        config = GaarfBqConfigBuilder(args).build()
    except GaarfBqConfigException:
        try:
            config = GaarfSqlConfigBuilder(args).build()
        except GaarfSqlConfigException:
            raise ValueError("failed to build config")

    logger.debug("config: %s", config)
    if main_args.save_config and not main_args.gaarf_config:
        ConfigSaver(main_args.save_config_dest).save(config)
    if main_args.dry_run:
        exit()

    config = initialize_runtime_parameters(config)
    logger.debug("initialized config: %s", config)

    if config.project:
        from gaarf.bq_executor import BigQueryExecutor
        postprocessor = BigQueryExecutor(project_id=config.project,
                                         location=config.dataset_location)
        postprocessor.create_datasets(config.params.get("macro"))
    elif config.connection_string:
        from gaarf.sql_executor import SqlAlchemyQueryExecutor
        engine = sqlalchemy.create_engine(config.connection_string)
        postprocessor = SqlAlchemyQueryExecutor(engine)
    else:
        raise ValueError("Failed to instantiate query postprocessor")

    reader_client = reader.FileReader()

    with futures.ThreadPoolExecutor() as executor:
        future_to_query = {
            executor.submit(postprocessor.execute, query,
                            reader_client.read(query), config.params):
            query
            for query in main_args.query
        }
        for future in futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                logger.debug("starting query %s", query)
                future.result()
                logger.info("%s executed successfully", query)
            except Exception as e:
                logger.error("%s generated an exception: %s", query, str(e))


if __name__ == "__main__":
    main()

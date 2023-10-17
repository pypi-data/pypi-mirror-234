import datetime
import os

import honeycomb_io
import numpy as np
import pandas as pd
import postgres_client

from .log import logger

class HoneycombRDSClient(postgres_client.PostgresClient):
    def __init__(
        self,
        dbname=None,
        user=None,
        password=None,
        host=None,
        port=None
    ):
        super().__init__(
            dbname=os.getenv('HONEYCOMB_RDS_DATABASE') or dbname,
            user=os.getenv('HONEYCOMB_RDS_USER') or user,
            password=os.getenv('HONEYCOMB_RDS_PASSWORD') or password,
            host=os.getenv('HONEYCOMB_RDS_HOST') or host,
            port=os.getenv('HONEYCOMB_RDS_PORT') or port,
        )

    def fetch_position_data(
        self,
        start,
        end,
        device_ids=None,
        part_numbers=None,
        serial_numbers=None,
        tag_ids=None,
        names=None,
        environment_id=None,
        environment_name=None,
        include_device_info=False,
        include_entity_info=False,
        include_material_info=False,
        connection=None,
        honeycomb_chunk_size=100,
        honeycomb_client=None,
        honeycomb_uri=None,
        honeycomb_token_uri=None,
        honeycomb_audience=None,
        honeycomb_client_id=None,
        honeycomb_client_secret=None
    ):
        device_info = honeycomb_io.fetch_devices(
            device_types=['UWBTAG'],
            device_ids=device_ids,
            part_numbers=part_numbers,
            serial_numbers=serial_numbers,
            tag_ids=tag_ids,
            names=names,
            environment_id=environment_id,
            environment_name=environment_name,
            start=start,
            end=end,
            output_format='dataframe',
            chunk_size=honeycomb_chunk_size,
            client=honeycomb_client,
            uri=honeycomb_uri,
            token_uri=honeycomb_token_uri,
            audience=honeycomb_audience,
            client_id=honeycomb_client_id,
            client_secret=honeycomb_client_secret,
        )
        device_ids = device_info.index.unique().tolist()
        start_utc_naive = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        end_utc_naive = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        query_list = [
            {'fields': ['timestamp'], 'operator': 'gte', 'values': [start_utc_naive]},
            {'fields': ['timestamp'], 'operator': 'lt', 'values': [end_utc_naive]},
            {'fields': ['object'], 'operator': 'in', 'values': device_ids},
        ]
        position_data = self.select(
            table='positions',
            schema='honeycomb',
            fields=None,
            query_list=query_list,
            connection=connection,
            convert_to_dataframe=True
        )
        if len(position_data) == 0:
            logger.warning('No data returned')
            return pd.DataFrame([], columns = [
                'position_id',
                'timestamp',
                'device_id',
                'position',
                'quality',
                'anchor_count',
                'socket_read_time',
                'network_time',
                'coordinate_space_id',

            ]).set_index('position_id')
        position_data['timestamp'] = pd.to_datetime(position_data['timestamp']).dt.tz_localize('UTC')
        position_data['position'] = position_data['data.coordinates'].apply(np.asarray)
        position_data['anchor_count'] = pd.to_numeric(position_data['anchor_count']).astype('Int64')
        position_data['socket_read_time'] = pd.to_datetime(position_data['socket_read_time']).dt.tz_localize('UTC')
        position_data['network_time'] = pd.to_numeric(position_data['network_time']).astype('Int64')
        position_data = (
            position_data
            .rename(columns={
                'object': 'device_id',
                'coordinate_space': 'coordinate_space_id',
            })
            .reindex(columns=[
                'position_id',
                'timestamp',
                'device_id',
                'position',
                'quality',
                'anchor_count',
                'socket_read_time',
                'network_time',
                'coordinate_space_id',
            ])
            .set_index('position_id')
        )
        if include_device_info:
            position_data = (
                position_data
                .join(
                    device_info,
                    how='left',
                    on='device_id'
                )
            )
        if include_entity_info or include_material_info:
            position_data = honeycomb_io.add_device_entity_assignment_info(
                dataframe=position_data,
                timestamp_column_name='timestamp',
                device_id_column_name='device_id',
                chunk_size=honeycomb_chunk_size,
                client=honeycomb_client,
                uri=honeycomb_uri,
                token_uri=honeycomb_token_uri,
                audience=honeycomb_audience,
                client_id=honeycomb_client_id,
                client_secret=honeycomb_client_secret,
            )
        if include_material_info:
            position_data = honeycomb_io.add_tray_material_assignment_info(
                dataframe=position_data,
                timestamp_column_name='timestamp',
                tray_id_column_name='tray_id',
                chunk_size=honeycomb_chunk_size,
                client=honeycomb_client,
                uri=honeycomb_uri,
                token_uri=honeycomb_token_uri,
                audience=honeycomb_audience,
                client_id=honeycomb_client_id,
                client_secret=honeycomb_client_secret,
            )
        return position_data

    def fetch_accelerometer_data(
        self,
        start,
        end,
        device_ids=None,
        part_numbers=None,
        serial_numbers=None,
        tag_ids=None,
        names=None,
        environment_id=None,
        environment_name=None,
        include_device_info=False,
        include_entity_info=False,
        include_material_info=False,
        connection=None,
        honeycomb_chunk_size=100,
        honeycomb_client=None,
        honeycomb_uri=None,
        honeycomb_token_uri=None,
        honeycomb_audience=None,
        honeycomb_client_id=None,
        honeycomb_client_secret=None
    ):
        device_info = honeycomb_io.fetch_devices(
            device_types=['UWBTAG'],
            device_ids=device_ids,
            part_numbers=part_numbers,
            serial_numbers=serial_numbers,
            tag_ids=tag_ids,
            names=names,
            environment_id=environment_id,
            environment_name=environment_name,
            start=start,
            end=end,
            output_format='dataframe',
            chunk_size=honeycomb_chunk_size,
            client=honeycomb_client,
            uri=honeycomb_uri,
            token_uri=honeycomb_token_uri,
            audience=honeycomb_audience,
            client_id=honeycomb_client_id,
            client_secret=honeycomb_client_secret,
        )
        device_ids = device_info.index.unique().tolist()
        start_utc_naive = start.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        end_utc_naive = end.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        query_list = [
            {'fields': ['timestamp'], 'operator': 'gte', 'values': [start_utc_naive]},
            {'fields': ['timestamp'], 'operator': 'lt', 'values': [end_utc_naive]},
            {'fields': ['device'], 'operator': 'in', 'values': device_ids},
        ]
        accelerometer_data = self.select(
            table='accelerometer_data',
            schema='honeycomb',
            fields=None,
            query_list=query_list,
            connection=connection,
            convert_to_dataframe=True
        )
        if len(accelerometer_data) == 0:
            logger.warning('No data returned')
            return pd.DataFrame([], columns = [
                'accelerometer_data_id',
                'timestamp',
                'device_id',
                'acceleration',
                'socket_read_time',
                'network_time',

            ]).set_index('accelerometer_data_id')
        accelerometer_data['timestamp'] = pd.to_datetime(accelerometer_data['timestamp']).dt.tz_localize('UTC')
        accelerometer_data['acceleration'] = accelerometer_data['data.data'].apply(np.asarray)
        accelerometer_data['socket_read_time'] = pd.to_datetime(accelerometer_data['socket_read_time']).dt.tz_localize('UTC')
        accelerometer_data['network_time'] = pd.to_numeric(accelerometer_data['network_time']).astype('Int64')
        accelerometer_data = (
            accelerometer_data
            .rename(columns={
                'device': 'device_id',
            })
            .reindex(columns=[
                'accelerometer_data_id',
                'timestamp',
                'device_id',
                'acceleration',
                'socket_read_time',
                'network_time',
            ])
            .set_index('accelerometer_data_id')
        )
        if include_device_info:
            accelerometer_data = (
                accelerometer_data
                .join(
                    device_info,
                    how='left',
                    on='device_id'
                )
            )
        if include_entity_info or include_material_info:
            accelerometer_data = honeycomb_io.add_device_entity_assignment_info(
                dataframe=accelerometer_data,
                timestamp_column_name='timestamp',
                device_id_column_name='device_id',
                chunk_size=honeycomb_chunk_size,
                client=honeycomb_client,
                uri=honeycomb_uri,
                token_uri=honeycomb_token_uri,
                audience=honeycomb_audience,
                client_id=honeycomb_client_id,
                client_secret=honeycomb_client_secret,
            )
        if include_material_info:
            accelerometer_data = honeycomb_io.add_tray_material_assignment_info(
                dataframe=accelerometer_data,
                timestamp_column_name='timestamp',
                tray_id_column_name='tray_id',
                chunk_size=honeycomb_chunk_size,
                client=honeycomb_client,
                uri=honeycomb_uri,
                token_uri=honeycomb_token_uri,
                audience=honeycomb_audience,
                client_id=honeycomb_client_id,
                client_secret=honeycomb_client_secret,
            )
        return accelerometer_data


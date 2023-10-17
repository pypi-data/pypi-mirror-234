import logging
import time
from datetime import datetime
from typing import Dict, List

import pandas as pd
import wget
from google.protobuf.json_format import MessageToDict
from terrascope_api import TerrascopeAsyncClient
from terrascope_api.models.algorithm_computation_pb2 import AlgorithmComputationGetRequest, AlgorithmComputation
from terrascope_api.models.analysis_computation_pb2 import AnalysisComputationGetRequest
from terrascope_api.models.common_models_pb2 import Pagination
from terrascope_api.models.result_pb2 import ResultGetRequest, ResultGetResponse, ResultExportRequest


class APIResult:
    def __init__(self, client: TerrascopeAsyncClient, timeout):
        self.__timeout = timeout
        self.__client = client

    async def export(self, algorithm_computation_id: str, download: bool = False,
                     export_type: ResultExportRequest.ExportType = None,
                     file_type: ResultExportRequest.FileType = None) -> str:
        """
         algorithm_computation_id: [Required] str - Algorithm or Analysis computation ID
         export_type: [Optional] ResultExportRequest.ExportType
         file_type: [Optional] ResultExportRequest.FileType
        :return: str: file_name of exported results OR if download == True the Filename that was downloaded through wget
        """
        request = ResultExportRequest(
            algorithm_computation_id=algorithm_computation_id
        )
        if export_type:
            request.export_type = export_type
        if file_type:
            request.file_type = file_type
        response = await self.__client.api.result.export(request, timeout=self.__timeout)
        if download:
            filename = wget.download(response.download_url)
            return filename
        else:
            return response.download_url

    async def get(self, **kwargs) -> (pd.DataFrame, ResultGetResponse):
        """
         algorithm_computation_id: [Required] str - Algorithm Computation ID
         source_aoi_version: int
         dest_aoi_version: int
         algo_config_class: str
         algo_config_subclass: str
         created_on: TimeStamp
         observation_start_ts: Timestamp
         geom_wkt: str
         result_status: ResultStatus
         include_measurements: bool
         pagination: Pagination
        :return: Tuple(pd.DataFrame of flattened results, ResultGetResponse)
        """
        assert "algorithm_computation_id" in kwargs.keys()
        request = self.__generate_result_get_request(kwargs)
        response = await self.__client.api.result.get(request, timeout=self.__timeout)
        return await self.__process_result_response(request, response), response

    async def __process_result_response(self, request: ResultGetRequest, response: ResultGetResponse) -> pd.DataFrame:
        result_obj_list = await self.__fetch_all_result_responses(request, response)
        # TODO ... too many nested loops this is nasty.
        result_list = []
        for result_response in result_obj_list:
            for result in result_response.results:
                for observation in result.observations:
                    obs_dict = {
                        "result_id": result.id,
                        "created_on": datetime.fromtimestamp(result.created_on.seconds),
                        "source_aoi_version": result.source_aoi_version,
                        "dest_aoi_version": result.dest_aoi_version,
                        "algo_config_class": result.algo_config_class,
                        "algo_config_subclass": result.algo_config_subclass,
                        "observation_id": observation.id,
                        "data_view_id": observation.data_view_id,
                        "observation_created_on": datetime.fromtimestamp(observation.created_on.seconds),
                        "observation_start_ts": datetime.fromtimestamp(observation.start_ts.seconds),
                        "result_status": observation.result_status
                    }
                    # Flatten keys into dict and add to main
                    obs_value = MessageToDict(observation.value)
                    obs_dict.update(obs_value)

                    if len(observation.measurements) == 0:
                        result_list.append(obs_dict.copy())
                    else:
                        for measurement in observation.measurements:
                            obs_dict.update({
                                "measurement_id": measurement.id,
                                "measurement_value": measurement.value,
                                "geom": measurement.geom
                            })
                            result_list.append(obs_dict.copy())
        return pd.DataFrame(result_list)

    async def __fetch_all_result_responses(self, request: ResultGetRequest, response: ResultGetResponse) -> List:
        results_obj_list = []

        # Add first result page if exists
        if response and len(response.results) > 0:
            results_obj_list.append(response)

        # Add subsequent result pages if exist
        pagination: Pagination = response.pagination
        while pagination and pagination.next_page_token:
            pagination = Pagination(
                page_token=pagination.next_page_token, page_size=1000
            )
            request.pagination.MergeFrom(pagination)
            response = await self.__client.api.result.get(request, timeout=self.__timeout)
            if response and len(response.results) > 0:
                results_obj_list.append(response)
        return results_obj_list

    @staticmethod
    def __generate_result_get_request(kwargs: Dict) -> ResultGetRequest:
        request_fragments = []
        for key in kwargs.keys():
            if key == 'algorithm_computation_id':
                request_fragments.append(ResultGetRequest(algorithm_computation_id=kwargs[key]))
            if key == 'source_aoi_version':
                request_fragments.append(ResultGetRequest(source_aoi_version=kwargs[key]))
            if key == 'dest_aoi_version':
                request_fragments.append(ResultGetRequest(dest_aoi_version=kwargs[key]))
            if key == 'algo_config_class':
                request_fragments.append(ResultGetRequest(algo_config_class=kwargs[key]))
            if key == 'algo_config_subclass':
                request_fragments.append(ResultGetRequest(algo_config_subclass=kwargs[key]))
            if key == 'created_on':
                request_fragments.append(ResultGetRequest(created_on=kwargs[key]))
            if key == 'observation_start_ts':
                request_fragments.append(ResultGetRequest(observation_start_ts=kwargs[key]))
            if key == 'geom_wkt':
                request_fragments.append(ResultGetRequest(geom_wkt=kwargs[key]))
            if key == 'result_status':
                request_fragments.append(ResultGetRequest(result_status=kwargs[key]))
            if key == 'include_measurements':
                request_fragments.append(ResultGetRequest(include_measurements=kwargs[key]))
            if key == 'pagination':
                request_fragments.append(ResultGetRequest(pagination=kwargs[key]))

        request = ResultGetRequest()
        for request_fragment in request_fragments:
            request.MergeFrom(request_fragment)

        return request

    async def wait_and_download(self, algorithm_computation_ids: List[str],
                                output: str,
                                export_type: ResultExportRequest.ExportType = ResultExportRequest.ExportType.STANDARD,
                                file_type: ResultExportRequest.FileType = ResultExportRequest.FileType.CSV):
        """
        The method takes an algorithm computation id and an output filepath. It will watch a particular algorithm
        computation and wait until the computation has succeeded. Upon success, it will download the results to the
        specified output directory file name.

        There are two optional parameters export type which determine which result export type should be used, and
        file_type which determines the format of the results.

        :param algorithm_computation_ids:

        :param output: takes "file_path/file_name.zip"
        :param export_type:
        :param file_type:
        :return:
        """
        # TODO Upgrade to take multiple algorithm computation ids, or just an analysis id
        wait = True
        request = AlgorithmComputationGetRequest(
            ids=algorithm_computation_ids)
        while wait:
            logging.info(MessageToDict(request))
            response = await self.__client.api.algorithm_computation.get(request)
            size = len(response.algorithm_computations)
            for computation in response.algorithm_computations:
                size -= 1
                algorithm_computation_id = computation.id
                state = AlgorithmComputation.State.Name(
                    computation.state
                )
                if state == "NOT_STARTED" or state == "VALIDATING":
                    logging.info(
                        "algorithm_computation_id[{}] - {}, sleep[10s]".format(algorithm_computation_id, state))
                    if size == 0:
                        time.sleep(10)
                    continue

                if state == "COMPLETE":
                    wait = False
                    logging.info("\nalgorithm_computation_id[{}] - {}".format(algorithm_computation_id, state))
                    logging.info("\nProgress %s\n\t{}".format(computation.progress))
                    download_url = await self.export(algorithm_computation_id=algorithm_computation_id,
                                                     export_type=export_type,
                                                     file_type=file_type)
                    filename = wget.download(download_url, out=output)
                    logging.info("url: {}\nfile: {}".format(download_url, filename))

                elif state == "IN_PROGRESS" or state == "NEW":
                    logging.info("\n algorithm_computation_id[{}] - "
                                 ""
                                 "{} - Sleeping for 10 seconds".format(algorithm_computation_id, state))
                    logging.info("\nProgress %s\n\t{}".format(computation.progress))
                    if size == 0:
                        time.sleep(10)
                elif state == "FAILED":
                    wait = False
                    logging.info("\n algorithm_computation_id[{}] "
                                 "FAILED - exiting".format(algorithm_computation_id))
                    logging.info("\nProgress %s\n\t{}".format(computation.progress))
                else:
                    wait = False
                    logging.info(
                        "\n algorithm_computation_id[{}] - {}. Exiting".format(algorithm_computation_id, state))

    async def __monitor_computations_status(self, **kwargs):
        """
        STUBS -> Planned 0.4.9 Release
        :param kwargs:
            - ids: List[str]
        :return:
        """
        valid_fields = ['algorithm_computation_ids', 'ids', 'watch']
        assert valid_fields[0] or valid_fields[1] in kwargs.keys()
        for key in kwargs.keys():
            assert key in valid_fields

        analysis_computation_ids = kwargs['ids']

        analysis_stats = {}
        analysis_computations = await self.__client.api.analysis_computation.get(
            AnalysisComputationGetRequest(
                analysis_computation_ids=analysis_computation_ids
            )
        )
        for a_comp in analysis_computations:
            analysis_computation_id = a_comp.analysis_computation_id
            analysis_stats[analysis_computation_id] = {
                "created": a_comp.submitted_timestamp.ToDatetime(),
                "state": [{
                    "name": a_comp.state,
                    "recorded": datetime.now()
                }],
                "computation_node_count": len(a_comp.computation_nodes),
                "computation_nodes": {}
            }
            for node in a_comp.computation_nodes:
                analysis_stats[analysis_computation_id]["computation_nodes"][node.computation_id] = MessageToDict(node)
                analysis_stats[analysis_computation_id]["computation_nodes"][node.computation_id]['status_counts'] = {}

        wait = True
        while wait:
            analysis_computations = await self.__client.api.analysis_computation.get(
                AnalysisComputationGetRequest(
                    analysis_computation_ids=analysis_computation_ids
                )
            )
            in_progress = []
            done = []
            for a_comp in analysis_computations:
                analysis_computation_id = a_comp.analysis_computation_id
                state_entry_length = len(analysis_stats[a_comp.analysis_computation_id]["state"])
                if analysis_stats[analysis_computation_id]["state"][state_entry_length - 1]['name'] != a_comp.state:
                    analysis_stats[analysis_computation_id]["state"].append({
                        "name": a_comp.state,
                        "recorded": datetime.now()
                    })
                    if a_comp.state == "IN_PROGRESS":
                        in_progress.append(analysis_computation_id)
                    if a_comp.state == "DONE":
                        done.append(analysis_computation_id)

            # Get All the algorithm computation ids that could be in progress
            algorithm_computation_id_checks = []
            for analysis_computation_id in in_progress:
                for node_key in analysis_stats[analysis_computation_id]["computation_nodes"].keys():
                    algorithm_computation_id_checks.append(node_key)

            # Get all the algorithm computations
            algorithm_computations = await self.__client.api.algorithm_computation.get_computations(
                AlgorithmComputationGetRequest(
                    computation_ids=algorithm_computation_id_checks,
                    include_non_active_computation_exections=True
                )
            )
            for algorithm_computation in algorithm_computations:
                for analysis_computation_id in analysis_stats.keys():
                    if algorithm_computation.id in analysis_stats[analysis_computation_id]["computation_nodes"].keys():
                        analysis_stats[analysis_computation_id]["computation_nodes"][algorithm_computation.id][
                            "execution_count"] = len(algorithm_computation.computation_executions)
                        for execution in algorithm_computation.computation_executions:
                            if analysis_stats[analysis_computation_id]["computation_nodes"][algorithm_computation.id][
                                "status_counts"][execution.status] is None:
                                analysis_stats[analysis_computation_id]["computation_nodes"][algorithm_computation.id][
                                    "status_counts"][execution.status] = 1
                            else:
                                analysis_stats[analysis_computation_id]["computation_nodes"][algorithm_computation.id][
                                    "status_counts"][execution.status] += 1

    async def __get_algorithm_computation_status(self, algorithm_computation_ids: List[str]):
        # STUBS -> Planned 0.4.9 Release
        pass

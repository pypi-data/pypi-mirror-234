import binascii
import ntpath
import os
import posixpath
import queue
import signal as os_signal
import tempfile
import time
import zipfile
from threading import Thread
from typing import List, Callable, Sequence

import grpc
import remotivelabs.broker.generated.sync.traffic_api_pb2 as traffic_api
import remotivelabs.broker.sync as br
import remotivelabs.broker.sync.helper as br_helper
import typer

from cli import settings

from rich.console import Console

err_console = Console(stderr=True)


class Broker:

    def __init__(self, url: str, api_key):
        self.url = url
        self.api_key = api_key
        self.q = queue.Queue()
        """Main function, checking arguments passed to script, setting up stubs, configuration and starting Threads."""
        # Setting up stubs and configuration
        if api_key is None:
            if url.startswith("https"):
                self.intercept_channel = br.create_channel(url, None, settings.read_token())
                # TODO - Temporary solution to print proper error message, remove ENV once api-key is gone
                os.environ["ACCESS_TOKEN"] = "true"
            else:
                os.environ["ACCESS_TOKEN"] = "false"
                self.intercept_channel = br.create_channel(url, None, None)
        else:
            err_console.print("Option --api-key will is deprecated and will be removed. "
                              "Use access access tokens by logging in with cli.")
            os.environ["ACCESS_TOKEN"] = "false"
            self.intercept_channel = br.create_channel(url, api_key, None)

        self.network_stub = br.network_api_pb2_grpc.NetworkServiceStub(self.intercept_channel)
        self.system_stub = br.system_api_pb2_grpc.SystemServiceStub(self.intercept_channel)
        self.traffic_stub = br.traffic_api_pb2_grpc.TrafficServiceStub(self.intercept_channel)
        self.signal_creator = br.SignalCreator(self.system_stub)

    def seek(self, recording_and_namespace: List, offset: int):

        def to_playback(rec):
            return {
                "namespace": rec['namespace'],
                "path": rec['recording'],
                "mode": br.traffic_api_pb2.Mode.SEEK,
                "offsettime": offset
            }

        playback_list = map(to_playback, recording_and_namespace)

        infos = br.traffic_api_pb2.PlaybackInfos(
            playbackInfo=list(map(self.__create_playback_config, playback_list))
        )
        status = self.traffic_stub.PlayTraffic(
            infos
        )
        mode = status.playbackInfo[0].playbackMode
        print(mode)
        if mode.errorMessage:
            print(f'Error seeking in playback {mode.errorMessage}')
            raise typer.Exit(1)

    def play(self, recording_and_namespace: List):

        def to_playback(rec):
            return {
                "namespace": rec['namespace'],
                "path": rec['recording'],
                "mode": br.traffic_api_pb2.Mode.PLAY,
            }

        playback_list = map(to_playback, recording_and_namespace)

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )
        mode = status.playbackInfo[0].playbackMode
        if mode.errorMessage:
            print(f'Error playing playback {mode.errorMessage}')
            raise typer.Exit(1)

    def stop_play(self, recording_and_namespace: List):

        def to_playback(rec):
            return {
                "namespace": rec['namespace'],
                "path": rec['recording'],
                "mode": br.traffic_api_pb2.Mode.STOP,
            }

        playback_list = map(to_playback, recording_and_namespace)

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )
        mode = status.playbackInfo[0].playbackMode
        if mode.errorMessage:
            print(f'Error stopping playback{mode.errorMessage}')
            raise typer.Exit(1)

    def pause_play(self, recording_and_namespace: List):

        def to_playback(rec):
            return {
                "namespace": rec['namespace'],
                "path": rec['recording'],
                "mode": br.traffic_api_pb2.Mode.PAUSE,
            }

        playback_list = map(to_playback, recording_and_namespace)

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )

    def record_multiple(self, namespaces: List[str], path: str):

        def to_playback(namespace):
            return {
                "namespace": namespace,
                "path": path + "_" + namespace,
                "mode": br.traffic_api_pb2.Mode.RECORD,
            }

        playback_list = list(map(to_playback, namespaces))

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )

    def record(self, namespace: str, path: str):
        playback_list = [
            {
                "namespace": namespace,
                "path": path,
                "mode": br.traffic_api_pb2.Mode.RECORD,
            }]

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )
        # print(status)

    def stop(self, namespace: str, path: str):
        playback_list = [
            {
                "namespace": namespace,
                "path": path,
                "mode": br.traffic_api_pb2.Mode.STOP,
            }]

        status: traffic_api.PlaybackInfos = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )
        mode = status.playbackInfo[0].playbackMode
        if mode.errorMessage:
            print(f'Error stopping recording {mode.errorMessage}')
            raise typer.Exit(1)

    def pause(self, namespace: str, path: str):
        playback_list = [
            {
                "namespace": namespace,
                "path": path,
                "mode": br.traffic_api_pb2.Mode.PAUSE,
            }]

        status: traffic_api.PlaybackInfos = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )
        mode = status.playbackInfo[0].playbackMode
        if mode.errorMessage:
            print(f'Error pausing recording {mode.errorMessage}')
            raise typer.Exit(1)

    def stop_multiple(self, namespaces: List[str], path: str):
        def to_playback(namespace):
            return {
                "namespace": namespace,
                "path": path + "_" + namespace,
                "mode": br.traffic_api_pb2.Mode.STOP,
            }

        playback_list = list(map(to_playback, namespaces))

        status = self.traffic_stub.PlayTraffic(
            br.traffic_api_pb2.PlaybackInfos(
                playbackInfo=list(map(self.__create_playback_config, playback_list))
            )
        )
        mode = status.playbackInfo[0].playbackMode
        if mode.errorMessage:
            print(f'Error stopping recording {mode.errorMessage}')
            raise typer.Exit(1)

    def diagnose_stop(self, namespace: List[str]):
        recording_name = f"diagnose__"
        self.stop_multiple(namespace, recording_name)

    def diagnose(self, namespace: List[str], wait_for_traffic: bool = False):
        recording_name = f"diagnose__"

        keep_running = True
        keep_running_during_recording = True

        def exit_on_ctrlc(sig, frame):
            nonlocal keep_running
            keep_running = False
            nonlocal keep_running_during_recording
            keep_running_during_recording = False
            # progress.add_task(description=f"Cleaning up, please wait...", total=None)

        os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)

        while keep_running:
            keep_running = wait_for_traffic
            self.record_multiple(namespace, recording_name)
            for i in range(5):
                if keep_running_during_recording:
                    time.sleep(1)

            self.stop_multiple(namespace, recording_name)

            response = []
            with tempfile.TemporaryDirectory() as tmpdirname:
                for ns in namespace:
                    path = recording_name + "_" + ns
                    tmp_file = os.path.join(tmpdirname, path)
                    self.download(path, tmp_file)
                    self.delete_files([path], False)
                    with zipfile.ZipFile(tmp_file, 'r') as zip_ref:
                        zip_ref.extractall(tmpdirname)

                        file_stat = os.stat(os.path.join(tmpdirname, path + '.raw'))
                        response.append({'namespace': ns, 'data': file_stat.st_size > 0})

            for r in response:
                if r['data']:
                    print(f'Successfully received traffic on {r["namespace"]}')
                    keep_running = False
                else:
                    if not wait_for_traffic or (not keep_running and not keep_running_during_recording):
                        print(f'Namespace {r["namespace"]} did not receive any traffic')

    def upload(self, file: str, dest: str):
        try:
            br.helper.upload_file(system_stub=self.system_stub, path=file, dest_path=dest)
        except grpc.RpcError as rpc_error:
            print(f"Failed to upload file - {rpc_error.details()} ({rpc_error.code()})")
            raise typer.Exit(1)

    def delete_files(self,
                     path: List[str],
                     exitOnFaliure: bool
                     ) -> None:

        for file in path:
            try:
                self.system_stub.BatchDeleteFiles(
                    br.system_api_pb2.FileDescriptions(
                        fileDescriptions=[br.system_api_pb2.FileDescription(path=file.replace(ntpath.sep,
                                                                                              posixpath.sep))]
                    )
                )
            except grpc.RpcError as rpc_error:
                print(f"Failed to delete file - {rpc_error.details()} ({rpc_error.code()})")
                if exitOnFaliure:
                    raise typer.Exit(1)

    # rpc BatchDeleteFiles (FileDescriptions) returns (Empty) {}

    def upload_folder(self, folder: str):
        try:
            br.helper.upload_folder(system_stub=self.system_stub, folder=folder)
        except grpc.RpcError as rpc_error:
            print(f"Failed to upload file - {rpc_error.details()} ({rpc_error.code()})")
            raise typer.Exit(1)

    def download(self, file: str, dest: str):
        try:
            br_helper.download_file(system_stub=self.system_stub, path=file, dest_path=dest)
        except grpc.RpcError as rpc_error:
            print(f"Failed to download file - {rpc_error.details()} ({rpc_error.code()})")
            # There will be an empty file if the download fails so remove that one here
            os.remove(dest)
            raise typer.Exit(1)

    def reload_config(self):
        try:
            request = br.common_pb2.Empty()
            response = self.system_stub.ReloadConfiguration(request, timeout=60000)
            if response.errorMessage:
                print(f"Failed to reload config: {response.errorMessage}")
                raise typer.Exit(1)
            # br.helper.reload_configuration(system_stub=self.system_stub)
        except grpc.RpcError as rpc_error:
            print(f"Failed to reload configuration - {rpc_error.details()} ({rpc_error.code()})")
            raise typer.Exit(1)

    def list_namespaces(self):
        # Lists available signals
        configuration = self.system_stub.GetConfiguration(br.common_pb2.Empty())
        namespaces = []
        for networkInfo in configuration.networkInfo:
            namespaces.append(networkInfo.namespace.name)
        return namespaces

    def list_signal_names(self, namespace):
        # Lists available signals
        configuration = self.system_stub.GetConfiguration(br.common_pb2.Empty())

        signal_names = []
        for networkInfo in configuration.networkInfo:
            res = self.system_stub.ListSignals(networkInfo.namespace)
            for finfo in res.frame:
                for sinfo in finfo.childInfo:
                    signal_names.append({'signal': sinfo.id.name, 'namespace': networkInfo.namespace.name})
        return signal_names

    def list_signal_names(self):
        # Lists available signals
        configuration = self.system_stub.GetConfiguration(br.common_pb2.Empty())

        signal_names = []
        for networkInfo in configuration.networkInfo:
            res = self.system_stub.ListSignals(networkInfo.namespace)
            for finfo in res.frame:
                for sinfo in finfo.childInfo:
                    signal_names.append({'signal': sinfo.id.name, 'namespace': networkInfo.namespace.name})
        return signal_names

    def subscribe_on_script(
            self,
            script: bytes,
            on_frame: Callable[[Sequence[br.network_api_pb2.Signal]], None],
            changed_values_only: bool = False,
    ) -> grpc.RpcContext:

        client_id = br.common_pb2.ClientId(id="cli")
        # sync = queue.Queue()
        thread = Thread(
            target=br.act_on_scripted_signal,
            args=(
                client_id,
                self.network_stub,
                script,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self.__each_signal(frame, on_frame),
                lambda sub: (self.q.put(("cli", sub))),
            ),
        )
        thread.start()
        # wait for subscription to settle
        subscription = self.q.get()
        return subscription  # , thread

    def subscribe(self, signals: list, namespace, on_frame, changed_values_only: bool = True):
        client_id = br.common_pb2.ClientId(id="cli")

        signals_to_subscribe_on = \
            map(lambda signal: self.signal_creator.signal(signal, namespace), signals)

        Thread(
            target=br.act_on_signal,
            args=(
                client_id,
                self.network_stub,
                signals_to_subscribe_on,
                changed_values_only,  # True: only report when signal changes
                lambda frame: self.__each_signal(frame, on_frame),
                lambda sub: (self.q.put(("cloud_demo", sub))),
            ),
        ).start()
        # Wait for subscription
        ecu, subscription = self.q.get()
        return subscription

    def __each_signal(self, signals, callback):
        callback(map(lambda s: {
            'timestamp_us': s.timestamp,
            'name': s.id.name,
            'value': self.__get_value(s)
        }, signals))

    @staticmethod
    def __get_value(signal):
        if signal.raw != b"":
            return "0x" + binascii.hexlify(signal.raw).decode("ascii")
        elif signal.HasField("integer"):
            return signal.integer
        elif signal.HasField("double"):
            return signal.double
        elif signal.HasField("arbitration"):
            return signal.arbitration
        else:
            return "empty"

    @staticmethod
    def __create_playback_config(item):
        """Creating configuration for playback

        Parameters
        ----------
        item : dict
            Dictionary containing 'path', 'namespace' and 'mode'

        Returns
        -------
        PlaybackInfo
            Object instance of class

        """

        def get_offset_time():
            if 'offsettime' in item:
                return item["offsettime"]

        playbackConfig = br.traffic_api_pb2.PlaybackConfig(
            fileDescription=br.system_api_pb2.FileDescription(path=item["path"]),
            namespace=br.common_pb2.NameSpace(name=item["namespace"]),
        )
        return br.traffic_api_pb2.PlaybackInfo(
            playbackConfig=playbackConfig,
            playbackMode=br.traffic_api_pb2.PlaybackMode(mode=item["mode"], offsetTime=get_offset_time()),
        )

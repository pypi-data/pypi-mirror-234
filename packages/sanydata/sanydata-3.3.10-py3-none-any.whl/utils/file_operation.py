from utils.cos_handler import CosHandler
from utils.local_handler import LocalHandler
from sanydata import model_data_message_pb2
import json
from env_helper import get_int_from_env
import time

def GetDeployment(stub):
    data_input = model_data_message_pb2.GetDeploymentRequest()
    res = stub.GetDeployment(data_input, timeout=20000)

    return res.output


def GetCosToken(stub):
    data_input = model_data_message_pb2.GetCosTokenRequest()
    res = stub.GetCosToken(data_input, timeout=20000)
    return json.loads(res.output)


def GetTargetFile(filelist, cos_tocken):

    deployment = cos_tocken['deployment']
    max_attempts = get_int_from_env("MAX_ATTEMPTS", 3)
    file_handler = None
    if deployment == "cloud":
        file_handler = CosHandler(cos_tocken)
    elif deployment == "site":
        pass
    elif deployment == "local":
        file_handler = LocalHandler()

    for file in filelist:
        attempts = 0
        while attempts < max_attempts:
            try:
                file = file.replace('../', '')
                data = file_handler.download(file)
                if data is not None:
                    yield data
                    break  # 下载成功，跳出循环
                else:
                    time.sleep(1)
                    # 下载失败，增加尝试次数
                    attempts += 1
                    print(f"Download failed for {file}, retrying ({attempts}/{max_attempts})...")
            except Exception as e:
                time.sleep(1)
                print(f"Error while downloading {file}: {str(e)}")
                attempts += 1
                print(f"Retrying ({attempts}/{max_attempts})...")

        if attempts >= max_attempts:
            # raise IOError(f"Max download attempts reached for {file}")
            yield None  # 达到最大尝试次数仍然下载失败

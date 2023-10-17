#!/bin/bash
set -x

# 需要设置环境变量
# MODEL_YAML_URL: model.yaml文件地址
# REPORT_ADDR : 用来报告运行接口的回调地址， restful形式    给后台
# INPUT_ADDR : 用来获取输入数据， restful形式              数据湖地址
# OUTPUT_ADDR : 用来输出数据， restful形式                 数据湖地址2
# INPUT_MODEL_ID : 数据湖输入模型id
# OUTPUT_DATA_SOURCE_ID : 数据湖输出数据源id
# BATCH_FORMAT : 批处理任务调度格式， crontab格式
# INSTANCE_ID: 实例ID
# INFER_ID: 推理id
# TRAINER_ID: 训练id
# TOKEN: token
# TENANT_ID: 租户id
# PERODIC_INTERVAL: 状态信息定时上报间隔
# DATA_SOURCE_READ_SIZE: 一次性读取数据源数据大小
# DATA_SOURCE_READ_LIMIT: 最多读取数据源数据大小
# API_EXTRAINFO: api接口增加额外信息， 比如 API_EXTRAINFO=1 返回 {"extrainfo":{"status":500, "message":"er"}, "data":data} ,否则返回 {"data": data}
# ERR_MASSAGE: 错判信息， 由框架写入环境变量， 然后脚本上报

# 分布式(distributed)训练环境变量
# DISTRIBUTED_TYPE: 分布式框架 pytouch/tf/paddle
# DIST_IS_MASTER: 是否为分布式主机
# DIST_MASTER_ADDR: 分布式主机地址
# DIST_MASTER_PORT: 分布式主机端口

# pytouch https://pytorch.org/docs/stable/elastic/run.html
# DIST_TORCH_NNODE: 用于训练的主机总数
# DIST_TORCH_NODE_RANK: 当前的主机编号
# DIST_TORCH_NPROC_PER_NODE: 每个主机上启动的进程数

echo "[ Prepare Env Start ]:"$(TZ=UTC-8 date +%Y-%m-%d" "%H:%M:%S)

workdir="/root"
packages_path="$workdir/packages"
intelliw_path="$workdir/intelliw"
controller_path="$intelliw_path/interface/controller.py"

export PYTHONPATH=$workdir:$PYTHONPATH # PYTHONPATH is the default search path of Python
if [ -d "/usr/local/cuda" ]; then
  export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
fi

REPORT_CODE=$1
if [ "$REPORT_CODE" != "custom" ]; then
  export FRAMEWORK_MODE=$REPORT_CODE
fi

function get_report_type() {
  if [ "$REPORT_CODE" == "importmodel" ]; then
    echo "importmodel"
  elif [ "$REPORT_CODE" == "importalg" ]; then
    echo "importalg"
  elif [ "$REPORT_CODE" == "analysis" ]; then
    export FRAMEWORK_MODE="train"
    echo "train_fail"
  elif [ "$REPORT_CODE" == "train" ] || [ "$REPORT_CODE" == "distributedtrain" ]; then
    echo "train_fail"
  elif [ "$REPORT_CODE" == "batchservice" ] || [ "$REPORT_CODE" == "allserver" ]; then
    echo "batchjob-"$TASK
  elif [ "$REPORT_CODE" == "apiservice" ]; then
    echo "inferstatus"
  elif [ "$REPORT_CODE" == "custom" ]; then
    echo "custom_fail"
  else
    echo "unknow"
  fi
}
REPORT_TYPE=$(get_report_type)

if [[ "$PERODIC_INTERVAL" -eq "" ]]; then
  export PERODIC_INTERVAL=10
  echo '设置状态信息定时上报间隔' $PERODIC_INTERVAL
fi

function caught_error() {
  if [[ -n "$REPORT_ADDR" ]]; then
    message=$1
    if [[ -z "$message" ]]; then
      curl -s -o /dev/nul -H "Content-Type:application/json" -X POST --data "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}" $REPORT_ADDR
    else
      curl -s -o /dev/nul -H "Content-Type:application/json" -X POST --data $message $REPORT_ADDR
    fi
  fi
}

function report_error() {
  if [ "$1" != "0" ]; then
    # 报错分析
    if [ "$1" == "137" ]; then
      message="Process finished with exit code 137: Out Of Memory"
    else
      message="Process finished with Error: $1, function $2, occurred on $3"
    fi

    # 上报报错
    if [[ -n "$REPORT_ADDR" ]]; then
      curl -s -o /dev/nul -H "Content-Type:application/json" -X POST --data "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$message\",\"data\":\"\"}" "$REPORT_ADDR"
    else
      echo "$message"
    fi
  fi
}

function report_info() {
  # 上报
  T=$1
  M=$2
  D=$3
  curl -s -o /dev/nul -H "Content-Type:application/json" -X POST --data "{\"id\":\"$INSTANCE_ID\",\"code\":200,\"token\":\"$TOKEN\",\"type\":\"$T\",\"message\":\"$M\",\"data\":$D}" "$REPORT_ADDR"
}

trap 'report_error $? $FUNCNAME $LINENO' CHLD ILL

get_package() {
  if [[ -f "$packages_path/algorithm.yaml" ]]; then
    echo $packages_path
  else
    for subpath in $(ls -1 $packages_path); do
      if [[ -f "$packages_path/$subpath/algorithm.yaml" ]]; then
        echo $packages_path/$subpath
        break
      fi
    done
  fi
  echo ''
}

download_model_yaml() {
  if [[ -n "$1" ]]; then
    echo "model.yaml开始下载"
    if [[ -f "$2/model.yaml" ]]; then
      mv "$2/model.yaml" "$2/model.yaml.bak"
    fi

    wget -d -c -t 5 "$1" -O "$2/model.yaml" --no-check-certificate
    if [ $? != 0 ]; then
      echo "model.yaml更新失败"
      caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"model.yaml更新失败\",\"data\":\"\"}"
      exit 10
    fi
  else
    echo "model.yaml下载地址为空,跳过处理"
  fi
}

# 获取算法文件位置
algorithm_root_dir=$(get_package)
# 下载model.yaml
download_model_yaml "$MODEL_YAML_URL" "$algorithm_root_dir"

# ↓↓↓↓ 导入 ↓↓↓↓
# import 导入模型 导入算法
import() {
  cd "$algorithm_root_dir" || exit # python会读取项目启动时当前目录作为工作路径，如果不进到算法的包里，很容易导致算法的相对路径全部失效

  cmd="python $controller_path -m $1 -p $algorithm_root_dir "
  if [[ -n "$REPORT_ADDR" ]]; then
    cmd="$cmd -r $REPORT_ADDR"
  fi
  $cmd

  if [[ $? != 0 ]]; then
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

#  ↓↓↓↓ 训练 ↓↓↓↓
# train 训练
train() {
  cd "$algorithm_root_dir" || exit
  export TASK=train

  cmd="python $controller_path -m train -p $algorithm_root_dir  "
  if [[ -n "$REPORT_ADDR" ]]; then
    cmd="$cmd -r $REPORT_ADDR"
  fi
  $cmd

  errorCode=$?
  if [[ $errorCode != 0 ]]; then
    if [ "$ERR_MASSAGE" == "" ]; then
      ERR_MASSAGE="ErrorCode:$errorCode"
    fi
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

# distributedtrain 分布式训练
distributedtrain() {
  cd "$algorithm_root_dir" || exit
  export TASK=train
  final_getrow_address=$(getRowAddress)

  if [ "$DISTRIBUTED_TYPE" == "pytorch" ]; then
    cmd="torchrun --nnode=$DIST_TORCH_NNODE --node_rank=$DIST_TORCH_NODE_RANK --nproc_per_node=$DIST_TORCH_NPROC_PER_NODE \
                --master_addr=$DIST_MASTER_ADDR  --master_port=$DIST_MASTER_PORT \
                $controller_path -m train -p $algorithm_root_dir "
    if [[ -n "$REPORT_ADDR" ]]; then
      cmd="$cmd -r $REPORT_ADDR"
    fi
    $cmd
  else
    message="unknow distributes type: $DISTRIBUTED_TYPE"
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$message\",\"data\":\"\"}"
  fi

  errorCode=$?
  if [[ $errorCode != 0 ]]; then
    if [ "$ERR_MASSAGE" == "" ]; then
      ERR_MASSAGE="ErrorCode:$errorCode"
    elif [ "$errorCode" == "137" ]; then
      ERR_MASSAGE="Process finished with exit code 137: Out Of Memory"
    fi
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

# ↓↓↓↓ 推理 ↓↓↓↓
# apiservice推理
apiservice() {
  cd "$algorithm_root_dir" || exit

  cmd="python $controller_path -m apiservice -p $algorithm_root_dir "
  if [[ -n "$REPORT_ADDR" ]]; then
    cmd="$cmd -r $REPORT_ADDR"
  fi
  $cmd
}

# batchservice 主要针对批量推理
batchservice() {
  cd "$algorithm_root_dir" || exit

  if [[ -n "$REPORT_ADDR" ]]; then
    python $controller_path -m batchservice -p "$algorithm_root_dir" -t $TASK -o $OUTPUT_ADDR -r $REPORT_ADDR -f "$BATCH_FORMAT"
  else
    python $controller_path -m batchservice -p "$algorithm_root_dir" -t $TASK -o $OUTPUT_ADDR -f "$BATCH_FORMAT"
  fi

  if [[ $? != 0 ]]; then
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

# allservice 推理时即开启api又进行定时任务
allservice() {
  export IS_ALLSERVER=True
  export TASK=infer

  cd "$algorithm_root_dir" || exit

  echo "开始api服务"

  apicmd="python $controller_path -m apiservice -p $algorithm_root_dir"
  if [[ -n "$REPORT_ADDR" ]]; then
    apicmd="$apicmd -r $REPORT_ADDR &"
  else
    apicmd="$apicmd &"
  fi
  $apicmd

  echo "开始批处理服务"
  final_getrow_address=$(getRowAddress)
  if [[ -n "$REPORT_ADDR" ]]; then
    python $controller_path -m batchservice -p "$algorithm_root_dir" -t $TASK -r $REPORT_ADDR -f "$BATCH_FORMAT" &
  else
    python $controller_path -m batchservice -p "$algorithm_root_dir" -t $TASK -f "$BATCH_FORMAT" &
  fi

  wait # wait for all subshells to finish

  if [[ $? != 0 ]]; then
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

validateservice() {
  cd "$algorithm_root_dir" || exit

  cmd="python $controller_path -m validateservice -n validate -p $algorithm_root_dir"
  if [[ -n "$REPORT_ADDR" ]]; then
    cmd="$cmd  -r $REPORT_ADDR"
  fi
  $cmd

  if [[ $? != 0 ]]; then
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

customservice() {
  cd "$algorithm_root_dir" || exit

  cmd="python $controller_path -m custom -p $algorithm_root_dir"
  if [[ -n "$REPORT_ADDR" ]]; then
    cmd="$cmd  -r $REPORT_ADDR"
  fi
  $cmd

  if [[ $? != 0 ]]; then
    caught_error "{\"id\":\"$INSTANCE_ID\",\"code\":500,\"token\":\"$TOKEN\",\"type\":\"$REPORT_TYPE\",\"message\":\"$ERR_MASSAGE\",\"data\":\"\"}"
  fi
}

case $REPORT_CODE in
importmodel)
  import importmodel
  ;;
importalg)
  import importalg
  ;;
train)
  train
  ;;
analysis)
  train
  ;;
distributedtrain)
  distributedtrain
  ;;
apiservice)
  apiservice
  ;;
batchservice)
  batchservice
  ;;
allservice)
  allservice
  ;;
custom)
  customservice
  ;;
kill)
  terminate
  ;;
validateservice)
  validateservice
  ;;
*)
  echo -e "no parameter"
  ;;
esac
echo "[ Prepare Env Start ]:"$(TZ=UTC-8 date +%Y-%m-%d" "%H:%M:%S)
exit 0

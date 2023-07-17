#!/bin/bash

# 카운터를 초기화합니다.
count=0

# 'ps -ef | grep wazuh' 명령을 실행하고 결과를 파이프로 전달합니다.
ps -ef | grep $1 | while read -r line
do
  # 각 줄에서 파일 경로를 추출합니다.
  path=$(echo "$line" | grep -oP '/var/log/[^/]*/')
  if [[ $path == */ ]]
  then
          echo "${path%% -*}"
  fi

  path=$(echo "$line" | grep -oP '/var/lib/[^/]*/')
  if [[ $path == */ ]]
  then
          echo "${path%% -*}"
  fi

  path=$(echo "$line" | grep -oP '/var/[^/]*/')
  if [[ ! $path =~ /var/lib/ ]]; then
	  echo "${path%%/*/*/*/ -*}"
  fi	  

  path=$(echo "$line" | grep -oP '/usr/share/[^/]*/')
  if [[ $path == */ ]] 
  then
          echo "${path%% -*}"
  fi

  path=$(echo "$line" | grep -oP '/etc/[^/]*/')
  if [[ $path == */ ]]
  then
          echo "${path%% -*}"
  fi

done | sed 's/\/$//' | sort  | uniq | while read dir
do
  # 디렉토리 내의 각 파일에 대해 루프를 실행합니다.
  find "$dir" -type f -print | while read file
  do
    # 파일의 엔트로피를 계산합니다.
    entropy=$(ent "$file" | grep Entropy | awk '{print $3}')
    # 엔트로피가 7 이하인 경우에만 파일의 전체 경로를 출력합니다.
    if (( $(echo "$entropy <= 7" | bc -l) )); then
      echo "$file"
      # 카운터를 증가시킵니다.
      ((count++))
      echo $count
    fi
  done
done

# 전체 파일 경로의 개수를 출력합니다.
echo "Total file paths: $count"


#!/bin/bash

# 'ps -ef | grep wazuh' 명령을 실행하고 결과를 파이프로 전달합니다.
ps -ef | grep wazuh | while read -r line
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


#  path=$(echo "$line" | grep -oP '/var/[^/]*/.*wazuh.*')
#  echo "${path%%/*/*/*}"

#  path=$(echo "$line" | grep -oP '/var/ossec/bin/wazuh-monitord')
#  if [[ -n $path ]]; then
#    echo "/var/ossec/"
#  fi

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

done | sed 's/\/$//' | sort  | uniq

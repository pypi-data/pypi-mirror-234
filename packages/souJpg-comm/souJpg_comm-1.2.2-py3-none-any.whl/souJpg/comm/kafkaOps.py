import json
import time
from typing import Optional

from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from loguru import logger as logger1
from pydantic import BaseModel

from souJpg.comm.contextManagers import ExceptionCatcher
from souJpg.comm.utils import singleton


class ConsumerParams(BaseModel):
    topicName: str = None
    groupId: str = None
    max_partition_fetch_bytes: Optional[int] = 20485760
    auto_offset_reset: Optional[str] = "latest"
    updatedOffset: Optional[int] = None
    partitionNum: Optional[int] = None


class Message(BaseModel):
    topicName: str = None
    content: Optional[dict] = None


@singleton
class KafkaOps:
    def __init__(self):
        # self.bootstrap_servers = gcf.kafkaBrokerServerList.split(",")
        # self.producer = KafkaProducer(bootstrap_servers=self.bootstrap_servers)
        self.bootstrap_servers = None
        self.producer = None

    def sendMessage(self, message=None):
        """

        :param message: json from BaseModel
        :return:
        """
        logger1.info(message)
        topicName = message.topicName
        content = message.content
        content = json.dumps(content, indent=4)
        content = content.encode("utf8")
        self.producer.send(topicName, content)

    def createConsumer(self, consumerParams=None):
        topicName = consumerParams.topicName
        groupId = consumerParams.groupId
        max_partition_fetch_bytes = consumerParams.max_partition_fetch_bytes
        auto_offset_reset = consumerParams.auto_offset_reset
        bootstrap_servers = self.bootstrap_servers
        auto_offset_reset = consumerParams.auto_offset_reset
        partitionNum = consumerParams.partitionNum

        updatedOffset = consumerParams.updatedOffset
        partitionNum = consumerParams.partitionNum
        if updatedOffset is not None:
            consumer = KafkaConsumer(
                group_id=groupId,
                max_partition_fetch_bytes=max_partition_fetch_bytes,
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset=auto_offset_reset,
            )
            partition = TopicPartition(topicName, partitionNum)
            consumer.assign([partition])
            consumer.seek(partition, updatedOffset)
            logger1.info(
                "reset offset to {}, topicName:{}, groupId:{}",
                updatedOffset,
                topicName,
                groupId,
            )
        else:
            consumer = KafkaConsumer(
                topicName,
                group_id=groupId,
                max_partition_fetch_bytes=max_partition_fetch_bytes,
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset=auto_offset_reset,
            )

        return consumer

    def consume(self, consumer=None, batchMessageHandler=None):
        """

        :param consumer:
        :param batchMessageHandler:  do not throw exception
        :return:
        """

        while True:
            with ExceptionCatcher() as ec:
                partionResults = consumer.poll(timeout_ms=1000)
                time.sleep(1)
                values = []
                for partionResult in partionResults.values():
                    for record in partionResult:
                        value = record.value
                        s = value.decode("utf-8")
                        content = json.loads(s)
                        logger1.info("consume message:{}", content)
                        values.append(content)

                if batchMessageHandler is not None:
                    batchMessageHandler(values)

            consumer.commit_async()

        consumer.close(autocommit=True)

import logging
from datetime import datetime

LOGGING = logging.getLogger(__name__)

from airflow.models.variable import Variable
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook


ALERTS_CONFIG = Variable.get('airflow_alerts_config', deserialize_json=True)
      

class Notify:

    def __init__(
        self,
        aws_sns_topic_arn: str,
        airflow_url: str
    ):
        """
        params:
            aws_sns_topic_arn: AWS SNS topic ARN where airflow send error messages
            airflow_url: AWS load balancer DNS by airflow
        """

        self.aws_sns_topic_arn = aws_sns_topic_arn
        self.airflow_url = airflow_url


    def callback_failure_msg(self, context):
        """
            Airflow failure function callback to notify sns

            params:
                context:  Airflow task execution context
            return:
                Message error formated
        """
        url = context.get('task_instance').log_url
        msg = """
        *DAG*           {dag} 
        *Task*:         {task}
        *Exec. time*:   {exec_date}
        *URL log*:      {log_url}
        """.format(
            dag=context.get('task_instance').dag_id,
            task=context.get('task_instance').task_id,
            exec_date=context.get('execution_date'),
            log_url=url.replace("localhost:8080", self.airflow_url)
        )
        return msg


    def callback_success_msg(self, context):
        """
            Airflow success  function callback to notify sns

            params:
                context:  Airflow task execution context
            return:
                Message success formated
        """
        msg = "Airflow DAG {dag} successfully executed at {exec_date}.".format(
            dag=context.get('task_instance').dag_id,
            exec_date=context.get('execution_date')
        )
        return msg
    

    def callback_sla_msg(self, context):
        """
            Airflow SLA function callback to notify sns
            params:
                context:  Airflow task execution context
            return:
                Message success formated
        """

        url = context.get('task_instance').log_url
        msg = """
        *DAG*           {dag} 
        *Task*:         {task}
        *Exec. time*:   {exec_date}
        *URL log*:      {log_url}
        """.format(
            dag=context.get('task_instance').dag_id,
            task=context.get('task_instance').task_id,
            exec_date=context.get('execution_date'),
            log_url=url.replace("localhost:8080", self.airflow_url)
        )
        return msg
        

    def send(self, msg_subject, msg_content, context):
        """ 
            Publish Airflow Error Notification to a SNS Topic

            Parameters:
                context: Airflow task execution context
            
            Returns:
                boto3 sns_client.publish() response
        """

        sns_client = AwsBaseHook(client_type="sns", aws_conn_id='aws_default')

        # Sending message to topic
        LOGGING.info(f"Sending message to SNS Topic ARN [{self.aws_sns_topic_arn}]")
        try:
            response = sns_client.get_conn().publish(
                TopicArn=self.aws_sns_topic_arn,
                Subject=msg_subject,
                Message=msg_content
            )
            LOGGING.info("Message successfully sent do SNS Topic")
            return response
        except Exception as ex:
            LOGGING.error(f"Error sending message to SNS: [{ex}]")
            return None

        return None


def airflow_failure_notify(context, **kwargs):
    
    if not ALERTS_CONFIG:
        LOGGING.error("Variable [airflow_alerts_config] not found in Airflow")
        return

    notification = Notify(
        aws_sns_topic_arn = ALERTS_CONFIG.get('sns_topic_arn'),
        airflow_url = ALERTS_CONFIG.get('airflow_url')
    )
        
    notification.send(
        msg_subject=":disappointed: ERROR - Airflow task execution failed",
        msg_content=notification.callback_failure_msg(context),
        context=context
    )


def airflow_success_notify(context, **kwargs):
    
    if not ALERTS_CONFIG:
        LOGGING.error("Variable [airflow_alerts_config] not found in Airflow")
        return
    
    notification = Notify(
        aws_sns_topic_arn = ALERTS_CONFIG.get('sns_topic_arn'),
        airflow_url = ALERTS_CONFIG.get('airflow_url')
    )

    notification.send(
        msg_subject=" :rocket: SUCCESS - Airflow DAG execution",
        msg_content=notification.callback_success_msg(context),
        context=context
    )

def airflow_sla_notify(context, **kwargs):
    
    if not ALERTS_CONFIG:
        LOGGING.error("Variable [airflow_alerts_config] not found in Airflow")
        return
    
    notification = Notify(
        aws_sns_topic_arn = ALERTS_CONFIG.get('sns_topic_arn'),
        airflow_url = ALERTS_CONFIG.get('airflow_url')
    )

    notification.send(
        msg_subject=" :warning: WARNING - Airflow DAG SLA Exceeded",
        msg_content=notification.callback_sla_msg(context),
        context=context
    )
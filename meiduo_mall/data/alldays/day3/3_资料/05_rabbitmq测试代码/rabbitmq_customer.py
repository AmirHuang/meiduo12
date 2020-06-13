import pika


# 链接到rabbitmq服务器
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
# 创建频道，声明消息队列
channel = connection.channel()
channel.queue_declare(queue='zxc')
# 定义接受消息的回调函数
def callback(ch, method, properties, body):
        print(body)

# 告诉RabbitMQ使用callback来接收信息
channel.basic_consume(callback, queue='zxc', no_ack=True)
# 开始接收信息
channel.start_consuming()

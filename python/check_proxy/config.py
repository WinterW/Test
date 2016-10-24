#encoding: utf-8

## mysql
g_db = {}

g_db['host'] = '192.168.64.16'
g_db['port'] = 3306
#write
g_db['user'] = 'pub_proxy'
g_db['passwd'] = 'pubproxy8848!'
g_db['db'] = 'octopus_crawler'
#g_db['db'] = 'test'

CHECK_THREAD_NUM = 50  #建议配置为与一轮检测中不可用代理数量相当的值 
CHECK_TIMEOUT = 5
FIXED_PROXY_NUM = 1000
PROXY_SEED_URL_LIST = ["http://183.131.83.251:888/API?orderid=865319184290474&num=%d&gq=0&carrier=0&protocol=0&an_ha=2&sec=0&zf=0"
                       , "http://183.131.83.251:888/API?orderid=865319184290474&num=%d&gq=0&carrier=0&protocol=0&an_ha=3&sec=0&zf=0"]

## 测试代理是否可用并查看自身出口ip url
SHOW_IP_URL = 'http://diagtool.ganji.com/showip.php'
#SHOW_IP_URL = 'https://www.baidu.com/'
CHECK_HTTPS_URL = 'https://www.baidu.com/img/baidu_jgylogo3.gif'

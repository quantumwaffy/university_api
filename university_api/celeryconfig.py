from kombu import Exchange, Queue

task_default_queue = "university_api"

task_queues = (Queue("university_api", Exchange("university_api"), routing_key="university_api"),)

imports = "api.tasks"

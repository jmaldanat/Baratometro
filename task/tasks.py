from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_task(task_id, url, user_id):
    """
    Process a task asynchronously
    
    This function will be called via Celery when a new Task is created.
    It performs scraping/processing using the provided URL and user_id.
    """
    from task.models import Task
    
    try:
        # Get the task instance
        task = Task.objects.get(id=task_id)
        
        logger.info(f"Started processing task {task_id} for URL: {url} and User: {user_id}")
        
        # Update task status to "processing"
        task.status = 'processing'
        task.save(update_fields=['status'])
        
        # Perform the actual processing using the URL and user_id
        # For example: scrape_data(url, user_id)
        
        # Simulate some processing time (remove in production)
        import time
        time.sleep(5)
        
        # Update task to completed
        task.status = 'completed'
        task.save(update_fields=['status'])
        
        logger.info(f"Task {task_id} completed successfully for User: {user_id}")
        return f"Task {task_id} processed successfully for User: {user_id}"
        
    except Task.DoesNotExist:
        logger.error(f"Task {task_id} not found")
        return f"Task {task_id} not found"
    except Exception as e:
        logger.error(f"Error processing task {task_id}: {str(e)}")
        return f"Error processing task {task_id}: {str(e)}"
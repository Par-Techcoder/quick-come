from ..models import Worker

def worker_create(user, expertise, experience, worker_garage):
    return Worker.objects.create(
        worker = user,
        garage = worker_garage,
        experience = experience,
        expertise = expertise
    )


def worker_update(worker, expertise, experience, worker_garage, user):
    if worker:
        worker.experience = experience
        worker.expertise = expertise
        worker.garage = worker_garage
        worker.updated_by = user
        worker.save()
        return worker
    return None


def get_worker_details(worker_id):
    try:
        return Worker.objects.get(id=worker_id) 
    except Worker.DoesNotExist:
        return None


def is_user_a_garage_worker(user):
    return Worker.objects.filter(worker=user, is_active=True).exists()

def get_worker_of_garage(garage_id):
    return list(Worker.objects.filter(garage=garage_id, is_active=True))

def get_worker_object(worker_id):
    return Worker.objects.get(id=worker_id)

def get_all_workers():
    return Worker.objects.all()

def worker_toggle(worker_id):
    worker = get_worker_details(worker_id)

    if worker:
        worker.is_active = not worker.is_active
        worker.save()
        return worker
    
    return None
from django.db.models.signals import post_save

def handle(self, *args, **kwargs):
    # Disconnect signal so movies don't auto-generate seats
    post_save.disconnect(create_seats_for_movie, sender=Movie)
    
    call_command('loaddata', 'fixtures/movies.json')
    call_command('loaddata', 'fixtures/seats.json')
    call_command('loaddata', 'fixtures/bookings.json')
    
    # Reconnect signal for normal use
    post_save.connect(create_seats_for_movie, sender=Movie)
    
    self.stdout.write(self.style.SUCCESS('Done!'))
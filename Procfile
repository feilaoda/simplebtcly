#web: gunicorn btcly.wsgi
web: python manage.py collectstatic --noinput; gunicorn btcly.wsgi

#bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT btcly/settings/production.py 

#web:          bundle exec rails server -p $PORT
#worker:       bundle exec rake resque:work QUEUE=*
#urgentworker: bundle exec rake resque:work QUEUE=urgent
#clock:        bundle exec clockwork clock.rb


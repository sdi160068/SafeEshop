# Django σημειώσεις

## tutorial
- https://www.youtube.com/watch?v=rHux0gMZ3Eg (κάπου από το 20 λεπτό και μετά)

## Δημιουργία καινούργιου project
django-admin startproject "mysite"

## Δημιουργία app
- python manage.py startapp "app"
- Πρέπει μέσα στο settings.py του project, στο section INSTALLED_APPS να δηλώσουμε το app

## views.py
- Βασικά είναι request handler. Κάτι σαν controller αν καταλαβαίνω σωστά

## 1st view function
* Μέσα στην playground/views.py
<pre><code>
from django.shortcuts import render
from django.http import HttpResponse

def say_hello(request): 
    # Pull data from db
    # transform data
    # send email etc
    return HttpResponse("Hello World")
</code></pre>

## urls mapping
- Φτιάχνουμε ένα αρχείο urls.py μέσα στο root του app
- Δεν έχει σημασία αν το αρχείο λέγεται urls.py ή κάτι άλλο.
- Μέσα στο urls.py κάνουμε import το path από τα urls της django : <code>from django.urls import path</code>
- Επίσης, από τον current φάκελο, κάνουμε import το views : <code>from . import views</code>
- Δημιουργία variable urlpatterns.
<pre><code>
# URLConf
    urlpatterns = [
        path('playground/hello', views.say_hello)
    ]
</code></pre>
- Το προσθέτουμε και αυτό μέσα στην urls.py. Είναι απαραίτησο η urlpatterns μεταβλητή να μην αλλάζει όνομα, γιατί αυτή την μεταβλητή ψάχνει η django.
- Σε αυτή την μεταβλητή, ορίζουμε τα urls ενός app.
- Μέσω της path , ορίζουμε το url και το που δείχνει αυτό το url (στην προκειμένη περίπτωση στην function say_hello του "controller" view.py)
- στην συνέχεια, προσθέτουμε το urlpatterns στον φάκελο urls.py του project (ΠΡΟΣΟΧΗ! Του project, όχι του app).
- Οδηγίες υπάρχουν και μέσα στο αρχείο για την τοποθέτηση των urls.
<pre><code>from django.contrib import admin
from django.urls import include,path

urlpatterns = [
    path('playground/', include('playground.urls')),
    path("eshop/", include('eshop.urls')),
]
</code></pre>
- Σημείωση : από την στιγμή που περνάμε σε αυτό το path το "playground/" από το url, δεν χρειάζεται να το έχουμε και στο urls.py του playground.py. Αλλιώς θα πρέπει να χτυπάμε το url playground/playground/hello


## Templates
- template.py
|-> Το πραγματικό "view". Είναι το σημείο που φτιάχνεται το "φαίνεσθαι" των σελίδων.
- Φτιάχνουμε ένα template hello.html μέσα στον φάκελο templates (δεν υπάρχει στο app, πρέπει να το φτιάξουμε).
- Για να κατευθύνουμε το view στο template χρησιμοποιούμε την render.
- Τι επιστρέφουμε από την views.py
<pre><code>def say_hello(request): 
        return render(request,'hello.html')
</code></pre>
- όπου request είναι το request και το hello.html είναι το template μας.
- Σημαντκό! Αν έχουμε error από την python ότι δεν βρίσκει το template ή κάτι τέτοιο, καλό είναι να τσεκάρουμε πρώτα το settings.py για τον αν έχουμε προσθέσει το app στα INSTALLED_APPS



## migrations
python manage.py makemigrations
python manage.py migrate

## check shell for objects
from auth.models import User as Object
User.objects.all()
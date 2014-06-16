---
layout: post
title: How to set up nginx and uWSGI for Django using vagrant
published: true
feature_image: "feature_nginx-uwsgi-django.png"
disqus_comments: true
---

Setting up a web server is never an easy task. This tutorial will show you how to setup a fully functional Ubuntu Server 12.04 LTS 32-bit running [nginx](http://nginx.com/) as a HTTP Server and [uWSGI](http://uwsgi-docs.readthedocs.org/en/latest/) (Web Server Gateway Interface) to allow [Django](https://www.djangoproject.com/) application to communicate with nginx. Additionally we will also learn to use [virtualenv](http://www.virtualenv.org/en/latest/), which is a great tool for any Python application. All this will run inside a virtual machine on your desktop using [vagrant](http://www.vagrantup.com/). Awesome, right?

## 1. Before we start
There are some requirements and assumptions that are important for seamlessly following this tutorial.

Here are the little things you will need:

- A text editor you like (I personally use [Sublime Text](http://www.sublimetext.com/))
- To be very comfortable with the Linux terminal
- To already know the basics of Django

## 2. Let’s start with vagrant!
Basically, vagrant makes it really easy to create and configure virtual environments that are lightweight and portable and, most importantly, reproducible. We will use it to run an Ubuntu server inside a virtual machine. It’s a great tool to work with alone or with a team and it will change the way you setup development environments.

### 2.1 Installing vagrant
If you don't have it yet, don't worry, it’s very easy to install vagrant on your computer, just go on the official website, download the package and follow the instructions.

Here’s the link: [http://www.vagrantup.com/downloads.html](http://www.vagrantup.com/downloads.html)

### 2.2 Setup your virtual environment
Now that you have vagrant installed, we will create and configure your first virtual environment.

Open a terminal and navigate to a directory (for example `~/myproject/`) where you would like to put your project and type the following command:

{% highlight bash %}
vagrant init
{% endhighlight %}

This will create a file named `Vagrantfile`. This file defines your virtual environment. For the moment, it's pretty basic and only creates a "base" box. Let's improve this! Open it in your text editor and replace the content with the following:

{% highlight ruby %}
# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise32"
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  config.vm.network :forwarded_port, host: 1337, guest: 80

  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.define "web" do |web|
    web.vm.box = "precise32"
	web.vm.hostname = "web"
	web.vm.network "private_network", ip: "192.168.101.11"
  end
end
{% endhighlight %}

Now, let's quickly go through each parameter and see what we just defined. If you are familiar with vagrant, you can skip to the next chapter.

{% highlight ruby %}
config.vm.box = "precise32"
config.vm.box_url = "http://files.vagrantup.com/precise32.box"
{% endhighlight %}
	
First we defined a box named "precise32" and set the url of the virtual machine, which is an Ubuntu Server 12.04 LTS 32-bit. You can change the 32 to 64 if you prefer 64-bit.

{% highlight ruby %}
config.vm.network :forwarded_port, host: 1337, guest: 80
{% endhighlight %}

Next, we forward the port 1337 from the virtual machine (host) to our port 80.

{% highlight ruby %}
config.vm.provider "virtualbox" do |vb|
  vb.customize ["modifyvm", :id, "--memory", "512"]
end
{% endhighlight %}

Here, we just modify our virtual machine, which is running in virtual box for my case, such that it uses maximum 512 mb of memory. This parameter is useful to limit the resources given to the VM.

{% highlight ruby %}
config.vm.define "web" do |web|
  web.vm.box = "precise32"
  web.vm.hostname = "web"
  web.vm.network "private_network", ip: "192.168.101.11"
end
{% endhighlight %}

And finally, we define a virtual machine named "web", which uses our box previously defined, and we set the IP to `192.168.101.11` so that we can access it from our browser.

For this tutorial, the file could have been simplified a lot more, but it can be a great template for all your projects. You can easily just copy and paste the last code block and define multiple virtual machines. It's very useful when you want to simulate a network with 2 or 3 servers working together.

Now `vagrant up`  to start the box. Once done, type `vagrant ssh web`  to log into the server. Congratulations, your virtual environment is up and running! By the way, your username is vagrant.

## 3. Configuring our fresh Ubuntu
Like every fresh installation, we will need to first update some packages before continuing. So, in your virtual machine type the following commands:
	
{% highlight bash %}
sudo aptitude update
sudo aptitude safe-upgrade
{% endhighlight%}
	
The second command might take a while and the grub package installation might require some user interaction. When it's done, we need to install a bunch of other packages before we dive in the interesting stuff.

{% highlight bash %}
sudo apt-get install build-essential python-dev python-pip
{% endhighlight%}
	
## 4. Basic Virtualenv and Django setup
Let's make things clear. This part is a basic setup for a new Django project. We will create it from the command line for testing purposes, but for a production environment you might for example use [git](http://git-scm.com/) to pull the project from your remote repository or better, making use of a provisioning tool like [Ansible](http://www.ansible.com/home), [Puppet](http://puppetlabs.com) or [Chef](http://www.getchef.com/chef/).

Ok, let's continue by installing virtuelenv. For this, just type the following:

{% highlight bash %}	
sudo pip install virtualenv
{% endhighlight%}
	
Next, we will setup our Python virtual environment for our Django web application. Type `pwd` in the terminal, it should print `/home/vagrant`. This is the location where we will put our Django app along with other files.

{% highlight bash %}
virtualenv venv
{% endhighlight%}
	
This command creates a Python virtual environment called `venv` (You can name it differently if you wish). Let's use/activate it now.

{% highlight bash %}
source venv/bin/activate
{% endhighlight%}
	
You should now see `(venv)`  in front of your command line. To install Django, just type:

{% highlight bash %}
pip install Django
{% endhighlight%}
	
Now we will create our Django project named `mysite`.

{% highlight bash %}
django-admin.py startproject mysite
{% endhighlight%}
	
Go into the directory with `cd mysite/` and launch the server to test if it works:

{% highlight bash %}
python manage.py runserver 0.0.0.0:8080
{% endhighlight%}
	
Then visit the following url: [http://192.168.101.11:8080](http://192.168.101.11:8080)

<img class="img-responsive feature-img" title="How to set up nginx and uWSGI for Django using vagrant" alt="How to set up nginx and uWSGI for Django using vagrant" src="/img/blog/djangoWorked_1.png" width="588" height="167" />
Easy, right ?

Type `deactivate`  to quit the virtual environment.

## 5. Installing uWSGI + nginx
Before installing nginx, we need uWSGI in order for Django to communicate with nginx. WSGI is a Python standard, so it's perfect for our Django app. *Note that uWSGI is one possibility, there exists alternatives like [gunicorn](http://gunicorn.org).*

We have two choices, wether install uWSGI in the Python virtual environment we created for Django, or install it globally. Here we will install it globally, so it is not tight to any virtual environment and can be easily put into an upstart job for example.

{% highlight bash %}
sudo pip install uwsgi
{% endhighlight %}
	
If the installation fails, you probably did not install the python-dev package. Now, since we went for the global installation, we will also install nginx right away and make everything work together nicely in one shot.
	
{% highlight bash %}
sudo apt-get install nginx
{% endhighlight %}

Starting nginx is simple, just enter this:

{% highlight bash %}
sudo /etc/init.d/nginx start
{% endhighlight %}

*Note: Similarly to **start**, there is also **restart** and **stop**.*

Visit your virtual machine's IP address and you should see this:

<img class="img-responsive feature-img" title="How to set up nginx and uWSGI for Django using vagrant" alt="How to set up nginx and uWSGI for Django using vagrant" src="/img/blog/nginxWorked_1.png" width="460" height="149" />

## 6. Configuration files
All right, now that we have uWSGI and nginx installed, we will go ahead and connect everything together. I will show one quite clean way to achieve this, by creating 3 files:

- `uwsgi_mysite.ini`: Defines the uWSGI configuration, very easy to (re)use.
- `nginx_mysite.conf`: Defines the nginx server configuration, also very easy.
- `uwsgi_params`: Required for nginx and uWSGI to work together. Just copy/paste.

Let's start with the `uwsgi_mysite.ini` file (N°1), which we will put inside the Django project at `/home/vagrant/mysite`. You can put it elsewhere, but I find it conveniant to have those files inside the Django project, for the simple reason that, you can easily have it under version control (assuming you use version control) and make development and deployment much easier. You can also have multiple `.ini`  files for development, testing and production, each with, for example, different number of worker processes.

Anyway, put this inside `uwsgi_mysite.ini`

{% highlight nginx %}
# uwsgi_mysite.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /home/vagrant/mysite
# Django's wsgi file (path starting from chdir/)
module          = mysite.wsgi:application
# the virtualenv (full path)
home            = /home/vagrant/venv

# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 2
# the socket (use the full path to be safe)
socket          = /home/vagrant/mysite/mysite.sock
# ... with appropriate permissions - may be needed
chmod-socket    = 666
# clear environment on exit
vacuum          = true
{% endhighlight %}

Next (N°2 and N°3), let's first create the `uwsgi_params` file, which is copied from [https://github.com/nginx/nginx/blob/master/conf/uwsgi_params](https://github.com/nginx/nginx/blob/master/conf/uwsgi_params) and used by nginx.

For `nginx_mysite.conf` copy and paste the following:

{% highlight nginx %}
# nginx_mysite.conf

# the upstream component nginx needs to connect to
upstream django {
  server unix:///home/vagrant/mysite/mysite.sock; # for a file socket
  #server 127.0.0.1:8001; # for a web port socket
}

# configuration of the server
server {
  # the port your site will be served on
  listen      1337;
  # the domain name it will serve for
  server_name 192.168.101.11; # .example.com; # substitute your machine's IP address or FQDN
  charset     utf-8;

  # max upload size
  client_max_body_size 2M;   # adjust to taste

  # Django media
  location /media  {
    alias /home/vagrant/mysite/media;  # your Django project's media files - amend as required
  }

  location /static {
    alias /home/vagrant/mysite/static; # your Django project's static files - amend as required
  }
	
  # Finally, send all non-media requests to the Django server.
  location / {
    uwsgi_pass  django;
    include     /home/vagrant/mysite/uwsgi_params; # the uwsgi_params file you installed
  }
}
{% endhighlight %}

nginx will listen to port 1337, because we defined this port as being forwarded in our `Vagrantfile`, remember?

You should end up with a file structure inside you Django project like the following:

{% highlight bash %}
vagrant@web:~/mysite$ ls -l
total 20
-rwxrwxr-x 1 vagrant vagrant  249 Feb 23 14:26 manage.py
drwxrwxr-x 2 vagrant vagrant 4096 Feb 23 14:52 mysite
-rw-rw-r-- 1 vagrant vagrant 1062 Feb 26 13:33 nginx_mysite.conf
-rw-rw-r-- 1 vagrant vagrant  623 Feb 26 13:05 uwsgi_mysite.ini
-rw-rw-r-- 1 vagrant vagrant  622 Feb 26 13:34 uwsgi_params
{% endhighlight %}

Next very <span style="color: #ff0000;">**important**</span> step is to make a **Symlink** from `/etc/nginx/sites-enabled` to our nginx configuration file:

{% highlight bash %}
sudo ln -s /home/vagrant/mysite/nginx_mysite.conf /etc/nginx/sites-enabled/
{% endhighlight %}

And now, restart nginx! Command: `sudo /etc/init.d/nginx restart`

## Let's run it !!!

{% highlight bash %}
sudo wsgi --ini uwsgi_mysite.ini
{% endhighlight %}
	
Got to [192.168.101.11](http://192.168.101.11) and Tadaaaa!

<img class="img-responsive feature-img" title="How to set up nginx and uWSGI for Django using vagrant" alt="How to set up nginx and uWSGI for Django using vagrant" src="/img/blog/djangoWorked_2.png" width="705" height="201" />

## Conclusion
Ok, so let's summarise what we achieved:

- We created a virtual machine, running an Ubuntu server, using **vagrant**
- We installed a Python virtual environment with the help of **virtualenv**
- Then, we installed and configured **nginx** and **uWSGI** to serve a **Django** application

Basically, we learned how to set up a fully functional virtual machine for our Django application, nearly perfect for development purposes. Those installation steps can also be reused for a production server, but be careful, because some additional steps are required.

## What to do next?
As I said before, this is really a basic tutorial about how to set up nginx and uWSGI for Django using vagrant. If you plan to go into production or improve some steps, then I recommend, first of all to read the [official Django documentation to prepare your app for production](https://docs.djangoproject.com/en/dev/howto/deployment/checklist/). You should actually create the `media`  and `static` folders inside your Django project and run a `python manage.py collectstatic`. This will collect all your static files and put them into the static folder at the root of the project in order for nginx to be able to access them.

Then, when it comes to deployment, you might want to use (if not already) [git]( http://git-scm.com) or [svn]( http://subversion.apache.org). It will greatly improve your workflow and make updates on your live server much simpler.

For the most serious developers, who want to automate everything, from server provisioning to live updates of your web application, then look into one of the IT [orchestration](http://en.wikipedia.org/wiki/Orchestration_(computing)) and automation tools out there. My favourite one is [Ansible]( http://www.ansible.com/home), because it simply requires Python on the target machine and it does everything per SSH connection, no additional server-side client must be installed.

**Thank you** for reading. I hope you did not ran into trouble while following this tutorial. If it is the case, I'll be happy to help you out.

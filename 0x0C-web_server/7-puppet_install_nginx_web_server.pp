#!/usr/bin/env bash
# Using puppet for config management

class nginx {
  package { 'nginx':
    ensure => installed,
  }

  file { '/var/www/html/index.nginx-debian.html':
    ensure  => file,
    content => 'Hello World!',
    require => Package['nginx'],
  }

  file { '/etc/nginx/sites-available/redirection':
    ensure  => file,
    content => 'server {
      listen 80;
      server_name localhost;
      location / {
        try_files $uri $uri/ =404;
      }
      location /redirect_me {
        return 301 https://www.example.com;
      }
    }',
    require => Package['nginx'],
  }

  exec { 'enable_redirection':
    command => 'ln -s /etc/nginx/sites-available/redirection /etc/nginx/sites-enabled/',
    unless  => 'test -L /etc/nginx/sites-enabled/redirection',
    require => File['/etc/nginx/sites-available/redirection'],
  }

  service { 'nginx':
    ensure    => running,
    enable    => true,
    subscribe => [
      File['/var/www/html/index.nginx-debian.html'],
      File['/etc/nginx/sites-available/redirection'],
    ],
  }
}

include nginx

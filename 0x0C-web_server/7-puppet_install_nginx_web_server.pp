#!/usr/bin/env bash
# Using puppet for config management

package { 'nginx':
  ensure => installed,
}

file { 'install':
  ensure  => 'present',
  path 	  => '/etc/nginx/sites-available/default',
  after   => 'listen 80 default_server;',
  line    => 'rewrite ^/redirect_me https://www.github.com/chukwuka1488 permanent;',    
}

file { '/var/www/html/index.html':
  content => 'Hello World!',
}

service { 'nginx':
  ensure  => running,
  require => Package['nginx'],
}    
